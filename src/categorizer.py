import json
import os
import logging
from src.llm_client import LLMClient

logger = logging.getLogger(__name__)

class DataCategorizer:
    def __init__(self, project_id="gcp-sandpit-intelia", output_dir="output"):
        self.output_dir = output_dir
        self.llm_client = LLMClient(project_id)

    def categorize(self, analysis_results):
        """Categorizes table fields by business domain."""
        logger.info("Starting data categorization...")
        
        # Step 1: Infer business domains from all tables
        domains = self._infer_domains(analysis_results)
        
        # Step 2: Categorize each field
        categorizations = self._categorize_fields(analysis_results, domains)
        
        # Step 3: Save results
        self._save_results(domains, categorizations)
        
        # Step 4: Generate report
        self._generate_report(domains, categorizations)
        
        logger.info("Data categorization complete.")

    def _infer_domains(self, analysis_results):
        """Infer business domains from table schemas."""
        logger.info("Inferring business domains...")
        
        # Collect all table names and sample columns
        table_summary = []
        for filename, data in analysis_results.items():
            analysis = data.get('analysis', '')
            if 'table_name' in analysis:
                try:
                    # Extract JSON
                    clean_analysis = analysis.replace("```json", "").replace("```", "").strip()
                    if "{" in clean_analysis:
                        start = clean_analysis.find("{")
                        end = clean_analysis.rfind("}") + 1
                        clean_analysis = clean_analysis[start:end]
                    
                    info = json.loads(clean_analysis)
                    table_name = info.get("table_name")
                    columns = [col.get("name") for col in info.get("columns", [])][:10]  # First 10 columns
                    
                    if table_name:
                        table_summary.append({
                            "table": table_name,
                            "sample_columns": columns
                        })
                except:
                    continue
        
        # Create prompt for domain inference
        prompt = f"""You are analyzing a Sybase database schema for a gaming/casino business.

Based on the following table names and their columns, identify 5-8 high-level business data domains that best categorize this data.

Tables:
{json.dumps(table_summary[:20], indent=2)}

Return ONLY a JSON array of domain objects with this structure:
[
  {{
    "domain_name": "Customer & Patron Management",
    "description": "Data related to casino patrons, memberships, and customer profiles"
  }},
  ...
]

Focus on domains that are:
1. Business-oriented (not technical)
2. Mutually exclusive where possible
3. Comprehensive enough to cover most tables
"""

        response = self.llm_client.generate_content(prompt)
        
        try:
            # Parse domains
            clean_response = response.replace("```json", "").replace("```", "").strip()
            if "[" in clean_response:
                start = clean_response.find("[")
                end = clean_response.rfind("]") + 1
                clean_response = clean_response[start:end]
            
            domains = json.loads(clean_response)
            logger.info(f"Identified {len(domains)} business domains")
            return domains
        except Exception as e:
            logger.error(f"Failed to parse domains: {e}")
            # Fallback domains
            return [
                {"domain_name": "Customer & Patron Management", "description": "Patron data, memberships, profiles"},
                {"domain_name": "Gaming Operations", "description": "Gaming machines, ratings, transactions"},
                {"domain_name": "Financial & Transactions", "description": "Payments, promotions, jackpots"},
                {"domain_name": "Location & Venue", "description": "Casino locations, departments, sites"},
                {"domain_name": "Reference Data", "description": "Lookup tables, codes, statuses"}
            ]

    def _categorize_fields(self, analysis_results, domains):
        """Categorize each field in each table."""
        logger.info("Categorizing fields...")
        
        categorizations = {}
        domain_list = "\n".join([f"- {d['domain_name']}: {d['description']}" for d in domains])
        
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
                columns = info.get("columns", [])
                
                if not table_name or not columns:
                    continue
                
                logger.info(f"Categorizing {table_name}...")
                
                # Create categorization prompt
                prompt = f"""Categorize each field in the following table to one of the business domains.

Table: {table_name}
Columns: {json.dumps(columns, indent=2)}

Business Domains:
{domain_list}

Return ONLY a JSON object mapping each column name to its domain:
{{
  "column_name": "Domain Name",
  ...
}}
"""

                response = self.llm_client.generate_content(prompt)
                
                # Parse response
                clean_response = response.replace("```json", "").replace("```", "").strip()
                if "{" in clean_response:
                    start = clean_response.find("{")
                    end = clean_response.rfind("}") + 1
                    clean_response = clean_response[start:end]
                
                field_domains = json.loads(clean_response)
                categorizations[table_name] = field_domains
                
            except Exception as e:
                logger.warning(f"Failed to categorize {filename}: {e}")
                continue
        
        return categorizations

    def _save_results(self, domains, categorizations):
        """Save categorization results to JSON."""
        output_path = os.path.join(self.output_dir, "data_categorization.json")
        
        results = {
            "domains": domains,
            "categorizations": categorizations
        }
        
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved categorization results to {output_path}")

    def _generate_report(self, domains, categorizations):
        """Generate categorization report."""
        report_path = os.path.join(self.output_dir, "categorization_report.txt")
        
        with open(report_path, "w") as f:
            f.write("Data Categorization Report\n\n")
            
            # Domains section
            f.write("Identified Business Domains\n\n")
            for domain in domains:
                f.write(f"{domain['domain_name']}\n")
                f.write(f"{domain['description']}\n\n")
            
            # Statistics
            f.write("## Categorization Statistics\n\n")
            f.write(f"- **Total Tables Categorized**: {len(categorizations)}\n")
            
            total_fields = sum(len(fields) for fields in categorizations.values())
            f.write(f"- **Total Fields Categorized**: {total_fields}\n\n")
            
            # Domain distribution
            domain_counts = {}
            for table_fields in categorizations.values():
                for domain in table_fields.values():
                    domain_counts[domain] = domain_counts.get(domain, 0) + 1
            
            f.write("### Fields per Domain\n\n")
            for domain_name, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
                f.write(f"- **{domain_name}**: {count} fields\n")
            f.write("\n")
            
            # Table-by-table categorization
            f.write("## Table Categorizations\n\n")
            for table_name in sorted(categorizations.keys()):
                f.write(f"### {table_name}\n\n")
                f.write("| Field | Domain |\n")
                f.write("|-------|--------|\n")
                
                for field, domain in sorted(categorizations[table_name].items()):
                    f.write(f"| {field} | {domain} |\n")
                
                f.write("\n")
        
        logger.info(f"Generated categorization report at {report_path}")
