import json
import os
import re
import logging
from google.cloud import storage
from src.llm_client import LLMClient

logger = logging.getLogger(__name__)

class SchemaTranslator:
    def __init__(self, project_id="gcp-sandpit-intelia", output_dir="output"):
        self.output_dir = output_dir
        self.dataform_dir = os.path.join(output_dir, "dataform")
        self.llm_client = LLMClient(project_id)
        
        # Domain to dataset mapping
        self.domain_to_dataset = {
            "Customer & Loyalty Management": "crown_customer_loyalty",
            "Casino Operations & Locations": "crown_casino_operations",
            "Gaming Products & Assets": "crown_gaming_products",
            "Gaming Activity & Performance": "crown_gaming_activity",
            "Promotions & Marketing": "crown_promotions",
            "Regulatory & Compliance": "crown_regulatory",
            "Reference & Time Data": "crown_reference"
        }
        
        # Sybase to BigQuery type mapping (built-in defaults)
        self.type_mappings = {
            "INT": "INT64",
            "INTEGER": "INT64",
            "SMALLINT": "INT64",
            "TINYINT": "INT64",
            "BIGINT": "INT64",
            "DECIMAL": "NUMERIC",
            "NUMERIC": "NUMERIC",
            "MONEY": "NUMERIC(19,4)",
            "SMALLMONEY": "NUMERIC(10,4)",
            "FLOAT": "FLOAT64",
            "REAL": "FLOAT64",
            "CHAR": "STRING",
            "VARCHAR": "STRING",
            "TEXT": "STRING",
            "NCHAR": "STRING",
            "NVARCHAR": "STRING",
            "NTEXT": "STRING",
            "DATETIME": "TIMESTAMP",
            "SMALLDATETIME": "TIMESTAMP",
            "DATE": "DATE",
            "TIME": "TIME",
            "BIT": "BOOL",
            "BINARY": "BYTES",
            "VARBINARY": "BYTES",
            "IMAGE": "BYTES"
        }

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
                    "Loaded %d Sybase→BigQuery type overrides from gs://%s/%s",
                    len(overrides),
                    bucket,
                    path,
                )
            else:
                logger.info(
                    "No Sybase type overrides loaded from gs://%s/%s (file missing or empty)",
                    bucket,
                    path,
                )

    def translate(self, analysis_results, categorization_results):
        """Translates Sybase schemas to BigQuery Dataform project."""
        logger.info("Starting schema translation...")
        
        # Create Dataform project structure
        self._create_dataform_structure()
        
        # Load categorization data
        domains = categorization_results.get("domains", [])
        categorizations = categorization_results.get("categorizations", {})
        
        # Translate Sybase tables
        for filename, data in analysis_results.items():
            analysis = data.get('analysis', '')
            if 'table_name' not in analysis:
                continue
            
            try:
                # Extract table info
                clean_analysis = analysis.replace("```json", "").replace("```", "").strip()
                if "{" in clean_analysis:
                    start = clean_analysis.find("{")
                    end = clean_analysis.rfind("}") + 1
                    clean_analysis = clean_analysis[start:end]
                
                info = json.loads(clean_analysis)
                table_name = info.get("table_name")
                
                if not table_name:
                    continue
                
                logger.info(f"Translating {table_name}...")
                
                # Determine domain and dataset
                domain = self._get_table_domain(table_name, categorizations, domains)
                dataset = self.domain_to_dataset.get(domain, "crown_default")
                
                # Translate schema
                self._translate_table(table_name, info, dataset, domain)
                
            except Exception as e:
                logger.warning(f"Failed to translate {filename}: {e}")
                continue
        
        # Convert Informatica transformations
        logger.info("Converting Informatica transformations...")
        from src.informatica_converter import InformaticaConverter
        informatica_converter = InformaticaConverter(output_dir=self.output_dir)
        informatica_converter.convert_informatica_mappings(analysis_results, categorization_results)
        
        logger.info("Schema translation complete.")

        # After translating all tables, write a small report listing any
        # Sybase types that were not explicitly mapped and what BigQuery
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
            "defaultProject": "gcp-sandpit-intelia",
            "defaultLocation": "australia-southeast2",
            "defaultDataset": "crown_default",
            "assertionSchema": "dataform_assertions",
            "warehouse": "bigquery",
            "defaultDatabase": "gcp-sandpit-intelia"
        }
        
        with open(os.path.join(self.dataform_dir, "dataform.json"), "w") as f:
            json.dump(dataform_config, f, indent=2)
        
        # Create includes/type_mappings.js
        type_mappings_js = """// Sybase to BigQuery type mappings
function mapSybaseType(sybaseType) {
  const mappings = {
    'INT': 'INT64',
    'INTEGER': 'INT64',
    'SMALLINT': 'INT64',
    'TINYINT': 'INT64',
    'BIGINT': 'INT64',
    'DECIMAL': 'NUMERIC',
    'NUMERIC': 'NUMERIC',
    'MONEY': 'NUMERIC(19,4)',
    'SMALLMONEY': 'NUMERIC(10,4)',
    'FLOAT': 'FLOAT64',
    'REAL': 'FLOAT64',
    'CHAR': 'STRING',
    'VARCHAR': 'STRING',
    'TEXT': 'STRING',
    'NCHAR': 'STRING',
    'NVARCHAR': 'STRING',
    'NTEXT': 'STRING',
    'DATETIME': 'TIMESTAMP',
    'SMALLDATETIME': 'TIMESTAMP',
    'DATE': 'DATE',
    'TIME': 'TIME',
    'BIT': 'BOOL',
    'BINARY': 'BYTES',
    'VARBINARY': 'BYTES',
    'IMAGE': 'BYTES'
  };
  
  return mappings[sybaseType.toUpperCase()] || 'STRING';
}

module.exports = { mapSybaseType };
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
            sybase_type = col.get("type", "STRING")
            nullable = col.get("nullable", True)
            
            # Map type
            bq_type = self._map_type(sybase_type)
            
            # Build column definition
            null_constraint = "" if nullable else " NOT NULL"
            bq_columns.append(f"  {col_name} {bq_type}{null_constraint}")
        
        # Determine partitioning and clustering
        partition_field = self._suggest_partition_field(columns)
        cluster_fields = self._suggest_cluster_fields(columns, primary_keys)
        
        # Generate .sqlx content
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

    def _map_type(self, sybase_type):
        """Maps Sybase type to BigQuery type."""
        # Extract base type (remove size/precision)
        base_type = re.split(r'[\(\[]', sybase_type.upper())[0].strip()
        
        if base_type in self.type_mappings:
            return self.type_mappings[base_type]

        # Fallback for unknown types: record them so we can report later.
        fallback = "STRING"
        if base_type not in self._unmapped_types:
            self._unmapped_types[base_type] = fallback
        return fallback

    def _write_type_mapping_report(self):
        """Write a report of unmapped Sybase types encountered in this run."""
        if not self._unmapped_types:
            return

        report_path = os.path.join(self.output_dir, "type_mapping_report.txt")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("Type Mapping Report\n\n")
                f.write(
                    "The following Sybase base types were encountered during translation "
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
        """Load Sybase→BigQuery type overrides from a text file in GCS.

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
        """Generates Dataform .sqlx content with valid config syntax."""

        # Base properties (include commas on the lines themselves)
        config_lines = [
            '  type: "table",',
            f'  schema: "{dataset}",',
            f'  description: "Migrated from Sybase - {domain}"'
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
        select_statement = "SELECT\n" + ",\n".join(columns) + "\nFROM `${ref('sybase_source')}`"
        
        sqlx = f"""-- Dataform table definition for {table_name}
-- Source: Sybase
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
