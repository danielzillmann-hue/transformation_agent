import json
import os
import re
import logging
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
        
        # Sybase to BigQuery type mapping
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
        
        return self.type_mappings.get(base_type, "STRING")

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
        """Generates Dataform .sqlx content."""
        config_lines = [
            f'  type: "table"',
            f'  schema: "{dataset}"',
            f'  description: "Migrated from Sybase - {domain}"'
        ]
        
        if partition_field:
            config_lines.append(f'  bigquery: {{')
            config_lines.append(f'    partitionBy: "{partition_field}"')
            if cluster_fields:
                cluster_str = ", ".join([f'"{f}"' for f in cluster_fields])
                config_lines.append(f'    clusterBy: [{cluster_str}]')
            config_lines.append(f'  }}')
        elif cluster_fields:
            cluster_str = ", ".join([f'"{f}"' for f in cluster_fields])
            config_lines.append(f'  bigquery: {{')
            config_lines.append(f'    clusterBy: [{cluster_str}]')
            config_lines.append(f'  }}')
        
        config_block = "config {\n" + ",\n".join(config_lines) + "\n}\n\n"
        
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
