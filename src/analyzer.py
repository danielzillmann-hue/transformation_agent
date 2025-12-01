import logging
import os

logger = logging.getLogger(__name__)

from src.llm_client import LLMClient
from src.prompts import SCHEMA_ANALYSIS_PROMPT, SP_ANALYSIS_PROMPT, INFORMATICA_ANALYSIS_PROMPT

class AnalysisEngine:
    def __init__(self, project_id="gcp-sandpit-intelia"):
        self.llm_client = LLMClient(project_id)

    def analyze(self, files):
        """Analyzes the provided files."""
        results = {}
        for blob in files:
            file_type = self._categorize_file(blob.name)
            logger.info(f"Analyzing {blob.name} as {file_type}")
            
            try:
                content = blob.download_as_text()
            except Exception as e:
                logger.error(f"Failed to read {blob.name}: {e}")
                content = None
                continue

            analysis_result = "Skipped"
            if content:
                if file_type == "sybase_ddl":
                    prompt = SCHEMA_ANALYSIS_PROMPT.format(content=content)
                    analysis_result = self.llm_client.generate_content(prompt)
                elif file_type == "sql_transformation": # Treating as SP for now or generic SQL
                    prompt = SP_ANALYSIS_PROMPT.format(content=content)
                    analysis_result = self.llm_client.generate_content(prompt)
                elif file_type == "informatica_xml":
                    # XML might be too large for full context, truncating for now or need smarter chunking
                    # For POC, taking first 30000 chars to avoid token limits if huge
                    prompt = INFORMATICA_ANALYSIS_PROMPT.format(content=content[:30000]) 
                    analysis_result = self.llm_client.generate_content(prompt)

            results[blob.name] = {
                "type": file_type,
                "analysis": analysis_result
            }
        return results

    def _categorize_file(self, filename):
        """Categorizes file based on extension and naming convention."""
        lower_name = filename.lower()
        if lower_name.endswith(".sql"):
            if lower_name.startswith("m_") or lower_name.startswith("wkf_"): # Potential Informatica generated SQL or similar
                return "sql_transformation" 
            return "sybase_ddl"
        elif lower_name.endswith(".xml"):
            return "informatica_xml"
        return "unknown"
