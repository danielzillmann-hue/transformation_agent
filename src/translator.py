import json
import os
import re
import logging
from typing import Optional
from google.cloud import storage
from src.llm_client import LLMClient
from src.json_utils import safe_parse_json
from src.adapters.registry import get_adapter
from src.adapters.base import SourceAdapter

logger = logging.getLogger(__name__)

class SchemaTranslator:
    def __init__(self, project_id="dan-sandpit", output_dir="output", source_system: Optional[str] = None):
        self.output_dir = output_dir
        self.dataform_dir = os.path.join(output_dir, "dataform")
        self.llm_client = LLMClient(project_id)
        
        # Load source system adapter
        self.adapter = get_adapter(source_system)
        logger.info(f"SchemaTranslator initialized for source system: {self.adapter.name}")
        
        # Domain to dataset mapping - use adapter's mapping with fallback
        self.domain_to_dataset = self.adapter.get_domain_mapping()
        # Add legacy Crown mappings if not present (backward compatibility)
        legacy_mappings = {
            "Customer & Loyalty Management": "crown_customer_loyalty",
            "Casino Operations & Locations": "crown_casino_operations",
            "Gaming Products & Assets": "crown_gaming_products",
            "Gaming Activity & Performance": "crown_gaming_activity",
            "Promotions & Marketing": "crown_promotions",
            "Regulatory & Compliance": "crown_regulatory",
            "Reference & Time Data": "crown_reference"
        }
        for k, v in legacy_mappings.items():
            if k not in self.domain_to_dataset:
                self.domain_to_dataset[k] = v
        
        # SCD Type 2 tables from adapter
        self.scd_type2_tables = self.adapter.get_type2_tables()
        
        # SCD Type 1 tables from adapter
        self.scd_type1_tables = self.adapter.get_type1_tables()
        
        # Incremental patterns - adapter handles this via is_incremental_table()
        # Keep for backward compatibility
        self.incremental_table_patterns = []
        
        # Cache for LLM-detected SCD types to avoid repeated calls
        self._scd_type_cache = {}
        
        # Control whether to use LLM for SCD detection (can be disabled for performance)
        self._use_llm_for_scd = os.getenv("SCD_DETECTION_USE_LLM", "true").lower() != "false"
        
        # Type mappings from adapter
        self.type_mappings = self.adapter.get_type_mappings()

        # Track which types came from overrides and which were not mapped at all.
        self._override_types = set()
        self._unmapped_types = {}  # base_type -> chosen BQ type

        # Optionally load overrides from a simple text mapping file in GCS.
        # This allows users to add or change mappings without code changes.
        bucket = os.getenv("TYPE_MAPPING_BUCKET")
        path = os.getenv("TYPE_MAPPING_PATH", "config/type_mappings.txt")
        if bucket:
            overrides = self._load_type_overrides_from_gcs(bucket, path)
            if overrides:
                self.type_mappings.update(overrides)
                self._override_types.update(overrides.keys())
                logger.info(
                    "Loaded %d %s→BigQuery type overrides from gs://%s/%s",
                    len(overrides),
                    self.adapter.name,
                    bucket,
                    path,
                )
            else:
                logger.info(
                    "No %s type overrides loaded from gs://%s/%s (file missing or empty)",
                    self.adapter.name,
                    bucket,
                    path,
                )

    def translate(self, analysis_results, categorization_results, status_callback=None):
        """Translates source schemas to BigQuery Dataform project."""
        logger.info("Starting schema translation...")
        
        if status_callback:
            status_callback("translation", "Creating Dataform project structure...", 1, 4)
        
        # Create Dataform project structure
        self._create_dataform_structure()
        
        # Load categorization data
        domains = categorization_results.get("domains", [])
        categorizations = categorization_results.get("categorizations", {})
        
        # Count tables for progress
        table_files = [f for f, d in analysis_results.items() if 'table_name' in d.get('analysis', '')]
        total_tables = len(table_files)
        
        if status_callback:
            status_callback("translation", f"Translating {total_tables} tables to BigQuery...", 2, 4)
        
        # Translate source tables
        translated_count = 0
        for filename, data in analysis_results.items():
            analysis = data.get('analysis', '')
            if 'table_name' not in analysis:
                continue
            
            try:
                # Extract table info using safe JSON parsing with repair
                info = safe_parse_json(analysis)
                if not info:
                    logger.warning(f"Could not parse JSON for {filename}, skipping")
                    continue
                
                table_name = info.get("table_name")
                
                if not table_name:
                    continue
                
                translated_count += 1
                logger.info(f"Translating {table_name}...")
                
                if status_callback:
                    status_callback("translation", f"Translating table {translated_count}/{total_tables}: {table_name}", translated_count, total_tables)
                
                # Determine domain and dataset
                domain = self._get_table_domain(table_name, categorizations, domains)
                dataset = self.domain_to_dataset.get(domain, "crown_default")
                
                # Translate schema
                self._translate_table(table_name, info, dataset, domain)
                
            except Exception as e:
                logger.warning(f"Failed to translate {filename}: {e}")
                continue
        
        if status_callback:
            status_callback("translation", "Converting Informatica mappings...", 3, 4)
        
        # Convert Informatica transformations (pass source_system for function mappings)
        logger.info("Converting Informatica transformations...")
        from src.informatica_converter import InformaticaConverter
        # Get source_system name from adapter to pass to InformaticaConverter
        source_system_name = self.adapter.name.lower().replace(" ", "").replace("-", "")
        # Map adapter name back to config name (e.g., "Sybase ASE" -> "sybase")
        source_system_key = None
        for key in ["sybase", "oracle", "sqlserver", "mysql", "postgres", "teradata", "snowflake"]:
            if key in source_system_name:
                source_system_key = key
                break
        informatica_converter = InformaticaConverter(output_dir=self.output_dir, source_system=source_system_key)
        informatica_converter.convert_informatica_mappings(analysis_results, categorization_results)
        
        if status_callback:
            status_callback("translation", f"Translation complete: {translated_count} tables processed", 4, 4)
        
        logger.info("Schema translation complete.")

        # After translating all tables, write a small report listing any
        # source types that were not explicitly mapped and what BigQuery
        # type was used for them. This helps users decide which new
        # entries to add to the GCS mapping file.
        self._write_type_mapping_report()

    def _create_dataform_structure(self):
        """Creates Dataform project structure."""
        # Create directories
        os.makedirs(self.dataform_dir, exist_ok=True)
        os.makedirs(os.path.join(self.dataform_dir, "includes"), exist_ok=True)
        os.makedirs(os.path.join(self.dataform_dir, "definitions"), exist_ok=True)
        
        # Create domain subdirectories
        for domain, dataset in self.domain_to_dataset.items():
            domain_slug = self._slugify(domain)
            os.makedirs(os.path.join(self.dataform_dir, "definitions", domain_slug), exist_ok=True)
        
        # Create dataform.json
        dataform_config = {
            "defaultProject": "dan-sandpit",
            "defaultLocation": "australia-southeast2",
            "defaultDataset": "crown_default",
            "assertionSchema": "dataform_assertions",
            "warehouse": "bigquery",
            "defaultDatabase": "dan-sandpit"
        }
        
        with open(os.path.join(self.dataform_dir, "dataform.json"), "w") as f:
            json.dump(dataform_config, f, indent=2)
        
        # Create includes/type_mappings.js with source-specific mappings
        source_name = self.adapter.name.replace(" ", "")
        type_mappings_js = f"""// {self.adapter.name} to BigQuery type mappings
function mapSourceType(sourceType) {{
  const mappings = {json.dumps(self.type_mappings, indent=4)};
  
  return mappings[sourceType.toUpperCase()] || 'STRING';
}}

module.exports = {{ mapSourceType }};
"""
        
        with open(os.path.join(self.dataform_dir, "includes", "type_mappings.js"), "w") as f:
            f.write(type_mappings_js)
        
        logger.info(f"Created Dataform project structure at {self.dataform_dir}")

    def _translate_table(self, table_name, table_info, dataset, domain):
        """Translates a single table to Dataform .sqlx."""
        columns = table_info.get("columns", [])
        primary_keys = table_info.get("primary_keys", [])
        
        # Map columns to BigQuery types
        bq_columns = []
        for col in columns:
            col_name = col.get("name")
            source_type = col.get("type", "STRING")
            nullable = col.get("nullable", True)
            
            # Map type
            bq_type = self._map_type(source_type)
            
            # Build column definition
            null_constraint = "" if nullable else " NOT NULL"
            bq_columns.append(f"  {col_name} {bq_type}{null_constraint}")
        
        # Determine partitioning and clustering
        partition_field = self._suggest_partition_field(columns)
        cluster_fields = self._suggest_cluster_fields(columns, primary_keys)
        
        # Determine table type using LLM analysis with fallback to pattern matching
        table_type = self._get_table_type(table_name, columns, primary_keys, domain)
        logger.info(f"Table {table_name} detected as type: {table_type}")
        
        if table_type == "scd_type2":
            sqlx_content = self._generate_scd_type2_sqlx(
                table_name,
                dataset,
                bq_columns,
                primary_keys,
                partition_field,
                cluster_fields,
                domain
            )
        elif table_type == "incremental":
            sqlx_content = self._generate_incremental_sqlx(
                table_name,
                dataset,
                bq_columns,
                primary_keys,
                partition_field,
                cluster_fields,
                domain
            )
        else:
            # Standard table (SCD Type 1 - full replace)
            sqlx_content = self._generate_sqlx(
                table_name, 
                dataset, 
                bq_columns, 
                partition_field, 
                cluster_fields,
                domain
            )
        
        # Write to file
        domain_slug = self._slugify(domain)
        table_slug = table_name.lower().replace(".", "_")
        sqlx_path = os.path.join(
            self.dataform_dir, 
            "definitions", 
            domain_slug, 
            f"{table_slug}.sqlx"
        )
        
        # Ensure the domain-specific directory exists even if the domain
        # name wasn't part of the original domain_to_dataset mapping
        # (for example, if the LLM inferred a slightly different label).
        os.makedirs(os.path.dirname(sqlx_path), exist_ok=True)
        
        with open(sqlx_path, "w") as f:
            f.write(sqlx_content)
        
        logger.info(f"Created {sqlx_path}")

    def _map_type(self, source_type):
        """Maps source database type to BigQuery type."""
        # Extract base type (remove size/precision)
        base_type = re.split(r'[\(\[]', source_type.upper())[0].strip()
        
        if base_type in self.type_mappings:
            return self.type_mappings[base_type]

        # Fallback for unknown types: record them so we can report later.
        fallback = "STRING"
        if base_type not in self._unmapped_types:
            self._unmapped_types[base_type] = fallback
        return fallback

    def _write_type_mapping_report(self):
        """Write a report of unmapped source types encountered in this run."""
        if not self._unmapped_types:
            return

        report_path = os.path.join(self.output_dir, "type_mapping_report.txt")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"{self.adapter.name} Type Mapping Report\n\n")
                f.write(
                    f"The following {self.adapter.name} base types were encountered during translation "
                    "but did not have explicit mappings in the built-in table or the "
                    "GCS override file. The agent defaulted them as shown below.\n\n"
                )
                for base_type in sorted(self._unmapped_types.keys()):
                    bq_type = self._unmapped_types[base_type]
                    f.write(f"{base_type} -> {bq_type}\n")

            logger.info("Wrote type mapping report to %s", report_path)
        except Exception as e:
            logger.warning("Failed to write type mapping report: %s", e)

    def _load_type_overrides_from_gcs(self, bucket_name: str, blob_path: str):
        """Load source→BigQuery type overrides from a text file in GCS.

        File format (lines):
            SMALL_IDENTIFIER=INT64
            AGE_RANGE=STRING

        Lines starting with '#' or empty lines are ignored.
        """
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            if not blob.exists():
                logger.warning(
                    "Type mapping override file not found in GCS: gs://%s/%s",
                    bucket_name,
                    blob_path,
                )
                return {}

            text = blob.download_as_text()
            overrides = {}
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    logger.warning("Skipping invalid type mapping line: %s", line)
                    continue
                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()
                if not key or not value:
                    logger.warning("Skipping incomplete type mapping line: %s", line)
                    continue
                overrides[key] = value

            return overrides
        except Exception as e:
            logger.warning(
                "Failed to load type overrides from gs://%s/%s: %s",
                bucket_name,
                blob_path,
                e,
            )
            return {}

    def _suggest_partition_field(self, columns):
        """Suggests a partition field based on column types."""
        # Look for date/timestamp fields
        for col in columns:
            col_name = col.get("name", "").lower()
            col_type = col.get("type", "").upper()
            
            if "DATE" in col_type or "TIMESTAMP" in col_type or "DATETIME" in col_type:
                # Prefer fields with common date names
                if any(keyword in col_name for keyword in ["date", "dt", "time", "dttm"]):
                    return col.get("name")
        
        return None

    def _suggest_cluster_fields(self, columns, primary_keys):
        """Suggests clustering fields."""
        # Use primary keys if available
        if primary_keys:
            return primary_keys[:4]  # BigQuery supports up to 4 clustering columns
        
        # Otherwise, look for common filter columns
        cluster_candidates = []
        for col in columns:
            col_name = col.get("name", "").lower()
            if any(keyword in col_name for keyword in ["id", "code", "type", "status", "site"]):
                cluster_candidates.append(col.get("name"))
                if len(cluster_candidates) >= 4:
                    break
        
        return cluster_candidates

    def _generate_sqlx(self, table_name, dataset, columns, partition_field, cluster_fields, domain):
        """Generates Dataform .sqlx content for standard tables (SCD Type 1 - full replace).
        
        SCD Type 1 simply overwrites existing data with new values.
        This is the default for most dimension tables except Patron.
        """

        # Base properties (include commas on the lines themselves)
        config_lines = [
            '  type: "table",',
            f'  schema: "{dataset}",',
            f'  description: "Migrated from {self.adapter.name} - {domain}"'
        ]

        # Optional BigQuery-specific settings
        if partition_field or cluster_fields:
            config_lines.append('  bigquery: {')
            if partition_field:
                config_lines.append(f'    partitionBy: "{partition_field}",')
            if cluster_fields:
                cluster_str = ", ".join([f'"{f}"' for f in cluster_fields])
                config_lines.append(f'    clusterBy: [{cluster_str}]')
            config_lines.append('  }')

        config_block = "config {\n" + "\n".join(config_lines) + "\n}\n\n"
        
        # Generate SELECT statement
        select_statement = "SELECT\n" + ",\n".join(columns) + "\nFROM `${{ref('source_table')}}`"
        
        sqlx = f"""-- Dataform table definition for {table_name}
-- Source: {self.adapter.name}
-- Domain: {domain}
-- Dataset: {dataset}

{config_block}{select_statement}
"""
        
        return sqlx

    def _get_table_domain(self, table_name, categorizations, domains):
        """Gets the primary domain for a table based on categorization."""
        if table_name not in categorizations:
            return "Reference & Time Data"  # Default
        
        field_domains = categorizations[table_name]
        
        # Count domain occurrences
        domain_counts = {}
        for domain in field_domains.values():
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Return most common domain
        if domain_counts:
            return max(domain_counts.items(), key=lambda x: x[1])[0]
        
        return "Reference & Time Data"

    def _slugify(self, text):
        """Converts text to slug format."""
        return text.lower().replace(" & ", "_").replace(" ", "_").replace("-", "_")

    def _is_scd_type2_table(self, table_name):
        """Checks if a table is in the known SCD Type 2 list (fallback)."""
        table_lower = table_name.lower()
        return table_lower in self.scd_type2_tables

    def _is_scd_type1_table(self, table_name):
        """Checks if a table is in the known SCD Type 1 list (reference tables).
        
        These tables should NEVER be SCD Type 2, regardless of what the LLM says.
        """
        table_lower = table_name.lower()
        return table_lower in self.scd_type1_tables

    def _is_incremental_table(self, table_name):
        """Checks if a table matches incremental patterns (fallback)."""
        table_lower = table_name.lower()
        # Check against patterns
        for pattern in self.incremental_table_patterns:
            if re.search(pattern, table_lower):
                return True
        return False

    def _detect_scd_type_with_llm(self, table_name, columns, primary_keys, domain):
        """Uses LLM to intelligently detect the appropriate SCD type based on schema analysis."""
        from src.prompts import SCD_TYPE_DETECTION_PROMPT
        
        # Check cache first
        if table_name in self._scd_type_cache:
            cached = self._scd_type_cache[table_name]
            logger.info(f"Using cached SCD type for {table_name}: {cached['scd_type']}")
            return cached
        
        # Format columns for the prompt
        column_info = []
        for col in columns:
            if isinstance(col, dict):
                column_info.append(f"{col.get('name', 'unknown')}: {col.get('type', 'unknown')}")
            else:
                # Already formatted string
                column_info.append(str(col).strip())
        
        prompt = SCD_TYPE_DETECTION_PROMPT.format(
            table_name=table_name,
            domain=domain,
            columns=", ".join(column_info[:20]),  # Limit to 20 columns for prompt size
            primary_keys=", ".join(primary_keys) if primary_keys else "Not specified"
        )
        
        try:
            response = self.llm_client.generate_content(prompt)
            
            # Parse response
            clean_response = response.replace("```json", "").replace("```", "").strip()
            if "{" in clean_response:
                start = clean_response.find("{")
                end = clean_response.rfind("}") + 1
                clean_response = clean_response[start:end]
            
            result = json.loads(clean_response)
            
            # Normalize scd_type value
            scd_type = result.get("scd_type", "scd_type1").lower().replace("-", "_").replace(" ", "_")
            if scd_type not in ["scd_type2", "scd_type1", "incremental"]:
                scd_type = "scd_type1"  # Default fallback
            
            result["scd_type"] = scd_type
            
            # Cache the result
            self._scd_type_cache[table_name] = result
            
            logger.info(f"LLM detected SCD type for {table_name}: {scd_type} (confidence: {result.get('confidence', 'unknown')})")
            logger.info(f"  Reasoning: {result.get('reasoning', 'N/A')}")
            
            return result
            
        except Exception as e:
            logger.warning(f"LLM SCD detection failed for {table_name}: {e}. Using fallback detection.")
            return None

    def _detect_scd_type_heuristic(self, table_name, columns, domain):
        """Uses heuristics to detect SCD type without LLM (fast fallback).
        
        Looks for common patterns in column names that indicate SCD Type 2.
        """
        table_lower = table_name.lower()
        
        # Dimension table naming patterns that often need SCD Type 2
        scd2_table_patterns = [
            r"^d_",           # Dimension prefix
            r"^dim_",
            r"_dim$",
            r"employee",
            r"staff",
            r"vendor",
            r"supplier",
            r"product",
            r"account",
        ]
        
        # Column names that suggest mutable attributes (SCD Type 2 candidates)
        scd2_column_indicators = {
            "address", "addr", "street", "city", "state", "zip", "postal",
            "status", "tier", "level", "grade", "rank", "rating",
            "department", "dept", "division", "team", "group",
            "title", "position", "role", "job",
            "salary", "wage", "rate", "price",
            "email", "phone", "mobile", "contact",
            "manager", "supervisor", "reports_to",
            "category", "classification", "segment",
            "membership", "subscription", "plan"
        }
        
        # Check if table name matches SCD2 patterns
        is_dimension_table = any(re.search(p, table_lower) for p in scd2_table_patterns)
        
        # Count SCD2 indicator columns
        scd2_column_count = 0
        for col in columns:
            col_name = col.get("name", "").lower() if isinstance(col, dict) else str(col).lower()
            for indicator in scd2_column_indicators:
                if indicator in col_name:
                    scd2_column_count += 1
                    break
        
        # If it's a dimension table with 2+ mutable attribute columns, suggest SCD Type 2
        if is_dimension_table and scd2_column_count >= 2:
            logger.info(f"Heuristic: {table_name} detected as SCD Type 2 (dimension table with {scd2_column_count} mutable columns)")
            return "scd_type2"
        
        # Customer/patron domain tables with mutable columns
        if domain and "customer" in domain.lower() and scd2_column_count >= 2:
            logger.info(f"Heuristic: {table_name} detected as SCD Type 2 (customer domain with {scd2_column_count} mutable columns)")
            return "scd_type2"
        
        return None

    def _get_table_type(self, table_name, columns=None, primary_keys=None, domain=None):
        """Determines the table type using LLM analysis with pattern-based fallback.
        
        Priority:
        1. Known SCD Type 1 tables (reference tables - NEVER Type 2)
        2. Known SCD Type 2 tables (explicit override list for people entities)
        3. Pattern matching for incremental/fact tables
        4. LLM-based detection (if enabled, analyzes schema semantically)
        5. Default to SCD Type 1 (standard table)
        
        Note: SCD Type 1 check comes FIRST to prevent LLM from over-classifying
        reference tables as Type 2.
        """
        # Priority 1: Check explicit SCD Type 1 list (reference tables)
        # These should NEVER be Type 2, regardless of what LLM says
        if self._is_scd_type1_table(table_name):
            logger.info(f"Table {table_name} matched explicit SCD Type 1 list (reference table)")
            return "table"
        
        # Priority 2: Check explicit SCD Type 2 list (people entities)
        if self._is_scd_type2_table(table_name):
            logger.info(f"Table {table_name} matched explicit SCD Type 2 list")
            return "scd_type2"
        
        # Priority 3: Pattern matching for incremental/fact tables
        if self._is_incremental_table(table_name):
            logger.info(f"Table {table_name} matched incremental pattern")
            return "incremental"
        
        # Priority 4: Use LLM detection if enabled and we have column info
        if self._use_llm_for_scd and columns and domain:
            llm_result = self._detect_scd_type_with_llm(table_name, columns, primary_keys or [], domain)
            if llm_result:
                scd_type = llm_result.get("scd_type", "scd_type1")
                # Only accept SCD Type 2 from LLM if confidence is high
                # and it's not a table that looks like a reference table
                if scd_type == "scd_type2":
                    confidence = llm_result.get("confidence", "low")
                    if confidence == "high":
                        return "scd_type2"
                    else:
                        logger.info(f"LLM suggested Type 2 for {table_name} but confidence was {confidence}, defaulting to Type 1")
                        return "table"
                elif scd_type == "incremental":
                    return "incremental"
                else:
                    return "table"
        
        # Priority 5: Default to standard table (SCD Type 1)
        return "table"

    def _generate_scd_type2_sqlx(self, table_name, dataset, columns, primary_keys, partition_field, cluster_fields, domain):
        """Generates Dataform .sqlx content for SCD Type 2 dimension tables.
        
        SCD Type 2 maintains history by:
        - Adding effective_from, effective_to, and is_current columns
        - Closing off old records (setting effective_to and is_current=false)
        - Inserting new records with is_current=true
        """
        # Determine the business key (usually the primary key minus surrogate keys)
        business_keys = primary_keys if primary_keys else ["id"]
        business_key_str = ", ".join(business_keys)
        business_key_match = " AND ".join([f"target.{k} = source.{k}" for k in business_keys])
        
        # Build column list for comparison (exclude SCD metadata columns)
        scd_metadata_cols = {"effective_from", "effective_to", "is_current", "dw_insert_date", "dw_update_date"}
        compare_columns = []
        all_column_names = []
        for col_def in columns:
            # Extract column name from definition like "  col_name TYPE"
            col_name = col_def.strip().split()[0]
            all_column_names.append(col_name)
            if col_name.lower() not in scd_metadata_cols:
                compare_columns.append(col_name)
        
        # Generate change detection condition
        change_conditions = " OR ".join([f"target.{c} != source.{c}" for c in compare_columns[:10]])  # Limit to 10 for readability
        
        # Column list for INSERT
        source_columns = ", ".join([f"source.{c}" for c in all_column_names])
        
        unique_key_list = ", ".join([f'"{k}"' for k in business_keys])
        config_lines = [
            '  type: "incremental",',
            f'  schema: "{dataset}",',
            f'  description: "SCD Type 2 dimension - {table_name} (migrated from {self.adapter.name})",',
            f'  uniqueKey: [{unique_key_list}, "effective_from"],',
        ]
        
        # Add BigQuery-specific settings
        if partition_field or cluster_fields:
            config_lines.append('  bigquery: {')
            if partition_field:
                config_lines.append(f'    partitionBy: "{partition_field}",')
            if cluster_fields:
                cluster_str = ", ".join([f'"{f}"' for f in cluster_fields])
                config_lines.append(f'    clusterBy: [{cluster_str}]')
            config_lines.append('  }')
        
        config_block = "config {\n" + "\n".join(config_lines) + "\n}\n\n"
        
        sqlx = f"""-- Dataform SCD Type 2 dimension table for {table_name}
-- Source: {self.adapter.name}
-- Domain: {domain}
-- Dataset: {dataset}
-- 
-- SCD Type 2 Logic:
-- - Tracks historical changes by closing off old records and inserting new ones
-- - Uses effective_from/effective_to date range and is_current flag
-- - Business Key: {business_key_str}

{config_block}-- Step 1: Get incoming source data with change detection
WITH source_data AS (
  SELECT
{chr(10).join(['    ' + col + ',' for col in columns])}
    CURRENT_TIMESTAMP() AS effective_from,
    CAST(NULL AS TIMESTAMP) AS effective_to,
    TRUE AS is_current
  FROM ${{ref('stg_{table_name.lower()}')}}
),

-- Step 2: Identify changed records that need to be closed off
records_to_close AS (
  SELECT
    target.*
  FROM ${{self()}} AS target
  INNER JOIN source_data AS source
    ON {business_key_match}
  WHERE target.is_current = TRUE
    AND ({change_conditions})
),

-- Step 3: Close off changed records (set effective_to and is_current = false)
closed_records AS (
  SELECT
{chr(10).join(['    ' + c + ',' for c in all_column_names])}
    effective_from,
    CURRENT_TIMESTAMP() AS effective_to,
    FALSE AS is_current
  FROM records_to_close
),

-- Step 4: New and changed records to insert
new_records AS (
  SELECT source.*
  FROM source_data AS source
  LEFT JOIN ${{self()}} AS target
    ON {business_key_match}
    AND target.is_current = TRUE
  WHERE target.{business_keys[0]} IS NULL  -- New record
     OR ({change_conditions})              -- Changed record
)

-- Final output: closed records + new records
SELECT * FROM closed_records
UNION ALL
SELECT * FROM new_records
"""
        
        return sqlx

    def _generate_incremental_sqlx(self, table_name, dataset, columns, primary_keys, partition_field, cluster_fields, domain):
        """Generates Dataform .sqlx content for incremental tables (fact tables, etc.).
        
        Uses MERGE logic to handle inserts and updates efficiently.
        """
        # Determine merge keys
        merge_keys = primary_keys if primary_keys else ["id"]
        merge_key_match = " AND ".join([f"target.{k} = source.{k}" for k in merge_keys])
        
        # Extract column names
        all_column_names = []
        for col_def in columns:
            col_name = col_def.strip().split()[0]
            all_column_names.append(col_name)
        
        # Generate update set clause
        update_set = ", ".join([f"{c} = source.{c}" for c in all_column_names if c not in merge_keys])
        
        unique_key_list = ", ".join([f'"{k}"' for k in merge_keys])
        config_lines = [
            '  type: "incremental",',
            f'  schema: "{dataset}",',
            f'  description: "Incremental table - {table_name} (migrated from {self.adapter.name})",',
            f'  uniqueKey: [{unique_key_list}],',
        ]
        
        # Add BigQuery-specific settings
        if partition_field or cluster_fields:
            config_lines.append('  bigquery: {')
            if partition_field:
                config_lines.append(f'    partitionBy: "{partition_field}",')
            if cluster_fields:
                cluster_str = ", ".join([f'"{f}"' for f in cluster_fields])
                config_lines.append(f'    clusterBy: [{cluster_str}]')
            config_lines.append('  }')
        
        config_block = "config {\n" + "\n".join(config_lines) + "\n}\n\n"
        
        # For incremental, we select only new/changed records
        sqlx = f"""-- Dataform incremental table for {table_name}
-- Source: {self.adapter.name}
-- Domain: {domain}
-- Dataset: {dataset}
-- Merge Keys: {", ".join(merge_keys)}

{config_block}-- Incremental load: only process new or updated records
SELECT
{chr(10).join(['  ' + col + ',' for col in columns[:-1]])}
  {columns[-1] if columns else ''}
FROM ${{ref('stg_{table_name.lower()}')}} AS source

${{when(incremental(), `
WHERE NOT EXISTS (
  SELECT 1 FROM ${{self()}} AS target
  WHERE {merge_key_match}
)
OR EXISTS (
  SELECT 1 FROM ${{self()}} AS target
  WHERE {merge_key_match}
    AND source.dw_update_date > target.dw_update_date
)
`)}}
"""
        
        return sqlx
