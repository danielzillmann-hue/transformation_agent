import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

from src.llm_client import LLMClient
from src.prompts import SCHEMA_ANALYSIS_PROMPT, SP_ANALYSIS_PROMPT, INFORMATICA_ANALYSIS_PROMPT

# Max parallel LLM calls - balance between speed and API rate limits
MAX_WORKERS = int(os.getenv("ANALYSIS_MAX_WORKERS", "5"))


class AnalysisEngine:
    def __init__(self, project_id="dan-sandpit"):
        self.llm_client = LLMClient(project_id)

    def _read_blob_content(self, blob):
        """Read blob content with encoding fallback."""
        try:
            return blob.download_as_text()
        except UnicodeDecodeError:
            try:
                return blob.download_as_bytes().decode('latin-1')
            except Exception as e:
                logger.error(f"Failed to read {blob.name} with fallback encoding: {e}")
                return None
        except Exception as e:
            logger.error(f"Failed to read {blob.name}: {e}")
            return None

    def _analyze_single_file(self, blob):
        """Analyze a single file - designed for parallel execution."""
        file_type = self._categorize_file(blob.name)
        logger.info(f"Analyzing {blob.name} as {file_type}")
        
        content = self._read_blob_content(blob)
        
        analysis_result = "Skipped"
        if content:
            if file_type == "sybase_ddl":
                prompt = SCHEMA_ANALYSIS_PROMPT.format(content=content)
                analysis_result = self.llm_client.generate_content(prompt)
            elif file_type == "sql_transformation":
                prompt = SP_ANALYSIS_PROMPT.format(content=content)
                analysis_result = self.llm_client.generate_content(prompt)
            elif file_type == "informatica_xml":
                # Truncate large XML to avoid token limits
                prompt = INFORMATICA_ANALYSIS_PROMPT.format(content=content[:30000])
                analysis_result = self.llm_client.generate_content(prompt)
        
        return blob.name, {
            "type": file_type,
            "analysis": analysis_result
        }

    def analyze(self, files, status_callback=None):
        """Analyzes the provided files in parallel."""
        results = {}
        total_files = len(files)
        completed = 0
        
        if status_callback:
            status_callback("analysis", f"Starting parallel analysis of {total_files} files...", 0, total_files)
        
        # Use ThreadPoolExecutor for parallel LLM calls
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all tasks
            future_to_blob = {
                executor.submit(self._analyze_single_file, blob): blob 
                for blob in files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_blob):
                blob = future_to_blob[future]
                try:
                    filename, result = future.result()
                    results[filename] = result
                    completed += 1
                    
                    if status_callback:
                        status_callback("analysis", f"Analyzed {completed}/{total_files}: {blob.name}", completed, total_files)
                        
                except Exception as e:
                    logger.error(f"Failed to analyze {blob.name}: {e}")
                    completed += 1
        
        if status_callback:
            status_callback("analysis", f"Analysis complete: {len(results)} files processed", total_files, total_files)
        
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
