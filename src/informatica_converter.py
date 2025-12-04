import json
import os
import logging
from src.llm_client import LLMClient
from src.json_utils import safe_parse_json

logger = logging.getLogger(__name__)

class InformaticaConverter:
    def __init__(self, project_id="dan-sandpit", output_dir="output"):
        self.output_dir = output_dir
        self.dataform_dir = os.path.join(output_dir, "dataform")
        self.llm_client = LLMClient(project_id)

    def convert_informatica_mappings(self, analysis_results, categorization_results):
        """Converts Informatica mappings to Dataform transformation SQL."""
        logger.info("Starting Informatica transformation conversion...")
        
        # Create staging and intermediate directories
        staging_dir = os.path.join(self.dataform_dir, "definitions", "staging")
        intermediate_dir = os.path.join(self.dataform_dir, "definitions", "intermediate")
        os.makedirs(staging_dir, exist_ok=True)
        os.makedirs(intermediate_dir, exist_ok=True)
        
        # Track shared objects for documentation
        shared_objects = []
        converted_count = 0
        
        # Process each Informatica XML
        for filename, data in analysis_results.items():
            if data.get('type') != 'informatica_xml':
                continue
            
            analysis = data.get('analysis', '')
            if not analysis or 'mapping_name' not in analysis:
                continue
            
            try:
                # Use safe JSON parsing with repair
                mapping_info = safe_parse_json(analysis)
                if not mapping_info:
                    logger.warning(f"Could not parse JSON for {filename}, skipping")
                    continue
                
                mapping_name = mapping_info.get("mapping_name")
                
                # Check if this is a shared/reusable object (not a mapping)
                if self._is_shared_object(mapping_name, mapping_info):
                    shared_objects.append({
                        "filename": filename,
                        "description": mapping_name,
                        "transformations": mapping_info.get("transformations", []),
                        "logic_summary": mapping_info.get("logic_summary", "")
                    })
                    logger.info(f"Found shared object in {filename}: {mapping_name}")
                    continue
                
                if not mapping_name or mapping_name == "null":
                    logger.info(f"Skipping {filename} - no mapping name found")
                    continue
                
                logger.info(f"Converting Informatica mapping: {mapping_name}")
                
                # Generate transformation SQL using LLM
                self._generate_transformation_sql(filename, mapping_info, categorization_results)
                converted_count += 1
                
            except Exception as e:
                logger.warning(f"Failed to convert {filename}: {e}")
                continue
        
        # Generate shared objects reference document
        if shared_objects:
            self._generate_shared_objects_doc(shared_objects)
        
        logger.info(f"Informatica conversion complete: {converted_count} mappings converted, {len(shared_objects)} shared objects documented.")
    
    def _is_shared_object(self, mapping_name, mapping_info):
        """Detect if this is a shared/reusable object rather than a mapping."""
        if not mapping_name:
            return False
        
        # Common indicators of shared objects
        shared_indicators = [
            "not found",
            "shared object",
            "reusable",
            "folder",
            "n/a",
            "this xml"
        ]
        
        mapping_name_lower = mapping_name.lower()
        for indicator in shared_indicators:
            if indicator in mapping_name_lower:
                return True
        
        # Also check if sources and targets are both empty/null (typical for shared objects)
        sources = mapping_info.get("sources") or []
        targets = mapping_info.get("targets") or []
        if not sources and not targets:
            return True
        
        return False
    
    def _generate_shared_objects_doc(self, shared_objects):
        """Generate a reference document for shared/reusable Informatica objects."""
        doc_path = os.path.join(self.output_dir, "informatica_shared_objects.md")
        
        with open(doc_path, "w") as f:
            f.write("# Informatica Shared Objects Reference\n\n")
            f.write("This document lists reusable transformations and shared objects found in the Informatica exports.\n")
            f.write("These are not converted to Dataform SQLX as they are components used by mappings, not complete ETL flows.\n\n")
            f.write("---\n\n")
            
            for idx, obj in enumerate(shared_objects, 1):
                f.write(f"## {idx}. {obj['filename']}\n\n")
                
                if obj['description']:
                    f.write(f"**Description**: {obj['description']}\n\n")
                
                if obj['transformations']:
                    f.write("**Transformations**:\n")
                    for t in obj['transformations']:
                        if isinstance(t, dict):
                            t_name = t.get('name', t.get('type', str(t)))
                            t_type = t.get('type', '')
                            f.write(f"- {t_name}")
                            if t_type:
                                f.write(f" ({t_type})")
                            f.write("\n")
                        else:
                            f.write(f"- {t}\n")
                    f.write("\n")
                
                if obj['logic_summary']:
                    f.write(f"**Logic Summary**:\n{obj['logic_summary']}\n\n")
                
                f.write("---\n\n")
        
        logger.info(f"Generated shared objects reference: {doc_path}")

    def _generate_transformation_sql(self, filename, mapping_info, categorization_results):
        """Generates transformation SQL for an Informatica mapping using LLM."""
        mapping_name = mapping_info.get("mapping_name", filename.replace(".XML", ""))
        sources = mapping_info.get("sources", [])
        targets = mapping_info.get("targets", [])
        transformations = mapping_info.get("transformations", [])
        logic_summary = mapping_info.get("logic_summary", "")
        
        # Create prompt for LLM to generate BigQuery SQL
        prompt = f"""You are an ETL expert converting Informatica PowerCenter mappings to BigQuery SQL for Dataform.

**Informatica Mapping**: {mapping_name}

**Sources**: {json.dumps(sources, indent=2)}

**Targets**: {json.dumps(targets, indent=2)}

**Transformations**: {json.dumps(transformations, indent=2) if transformations else "Not explicitly defined"}

**Logic Summary**: {logic_summary}

**Task**: Generate a BigQuery SQL query that:
1. Reads from the source tables (use `${{ref('table_name')}}` for Dataform references)
2. Applies the transformation logic described
3. Outputs to the target table(s)

**Requirements**:
- Use CTEs for multi-step transformations
- Use standard BigQuery SQL syntax
- Include appropriate JOINs, WHERE clauses, GROUP BY, etc. based on the logic
- Add comments explaining the transformation steps
- If the logic is unclear, make reasonable assumptions for a typical ETL mapping

Return ONLY the SQL query, no explanation.
"""

        try:
            sql_response = self.llm_client.generate_content(prompt)
            
            # Clean up response
            sql = sql_response.replace("```sql", "").replace("```", "").strip()
            
            # Generate .sqlx file
            self._create_transformation_sqlx(mapping_name, sql, sources, targets, categorization_results)
            
        except Exception as e:
            logger.error(f"Failed to generate SQL for {mapping_name}: {e}")

    def _create_transformation_sqlx(self, mapping_name, sql, sources, targets, categorization_results):
        """Creates a Dataform .sqlx file for the transformation."""
        # Determine target dataset based on categorization
        target_dataset = "crown_default"
        if targets and categorization_results:
            categorizations = categorization_results.get("categorizations", {})
            # Try to find domain for first target
            for target in targets:
                if target in categorizations:
                    # Get most common domain for this table
                    field_domains = categorizations[target]
                    if field_domains:
                        domain_counts = {}
                        for domain in field_domains.values():
                            domain_counts[domain] = domain_counts.get(domain, 0) + 1
                        
                        if domain_counts:
                            primary_domain = max(domain_counts.items(), key=lambda x: x[1])[0]
                            target_dataset = self._domain_to_dataset(primary_domain)
                            break
        
        # Create config block
        config_lines = [
            f'  type: "view"',  # Use view for transformations
            f'  schema: "{target_dataset}"',
            f'  description: "Informatica mapping: {mapping_name}"'
        ]
        
        if sources:
            dependencies = ", ".join([f'"{s}"' for s in sources[:5]])  # Limit to 5
            config_lines.append(f'  dependencies: [{dependencies}]')
        
        config_block = "config {\n" + ",\n".join(config_lines) + "\n}\n\n"
        
        # Create full .sqlx content
        sqlx_content = f"""-- Dataform transformation from Informatica mapping
-- Mapping: {mapping_name}
-- Sources: {', '.join(sources) if sources else 'N/A'}
-- Targets: {', '.join(targets) if targets else 'N/A'}

{config_block}{sql}
"""
        
        # Write to intermediate directory
        mapping_slug = mapping_name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")
        sqlx_path = os.path.join(
            self.dataform_dir,
            "definitions",
            "intermediate",
            f"{mapping_slug}.sqlx"
        )
        
        with open(sqlx_path, "w") as f:
            f.write(sqlx_content)
        
        logger.info(f"Created transformation: {sqlx_path}")

    def _domain_to_dataset(self, domain):
        """Maps domain to dataset name."""
        domain_mapping = {
            "Customer & Loyalty Management": "crown_customer_loyalty",
            "Casino Operations & Locations": "crown_casino_operations",
            "Gaming Products & Assets": "crown_gaming_products",
            "Gaming Activity & Performance": "crown_gaming_activity",
            "Promotions & Marketing": "crown_promotions",
            "Regulatory & Compliance": "crown_regulatory",
            "Reference & Time Data": "crown_reference"
        }
        return domain_mapping.get(domain, "crown_default")
