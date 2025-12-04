import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

logger = logging.getLogger(__name__)

from src.llm_client import LLMClient
from src.prompts import SCHEMA_ANALYSIS_PROMPT, SP_ANALYSIS_PROMPT, INFORMATICA_ANALYSIS_PROMPT
from src.adapters.registry import get_adapter
from src.adapters.base import SourceAdapter

# Max parallel LLM calls - balance between speed and API rate limits
MAX_WORKERS = int(os.getenv("ANALYSIS_MAX_WORKERS", "5"))


class AnalysisEngine:
    def __init__(self, project_id="dan-sandpit", source_system: Optional[str] = None):
        self.llm_client = LLMClient(project_id)
        self.adapter = get_adapter(source_system)
        logger.info(f"AnalysisEngine initialized for source system: {self.adapter.name}")

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

    def _get_prompt(self, file_type: str, content: str) -> Optional[str]:
        """Get the appropriate prompt for the file type."""
        # Try adapter's custom prompts first
        if file_type == "sybase_ddl":
            custom_prompt = self.adapter.get_schema_analysis_prompt()
            if custom_prompt:
                return custom_prompt.format(content=content, name=self.adapter.name)
            return SCHEMA_ANALYSIS_PROMPT.format(content=content)
        
        elif file_type == "sql_transformation":
            custom_prompt = self.adapter.get_procedure_analysis_prompt()
            if custom_prompt:
                return custom_prompt.format(content=content, name=self.adapter.name)
            return SP_ANALYSIS_PROMPT.format(content=content)
        
        elif file_type == "informatica_xml":
            custom_prompt = self.adapter.get_etl_analysis_prompt()
            if custom_prompt:
                return custom_prompt.format(content=content[:30000], name=self.adapter.name)
            return INFORMATICA_ANALYSIS_PROMPT.format(content=content[:30000])
        
        return None

    def _analyze_single_file(self, blob):
        """Analyze a single file - designed for parallel execution."""
        # Use adapter for file categorization
        file_type = self.adapter.categorize_file(blob.name)
        logger.info(f"Analyzing {blob.name} as {file_type}")
        
        content = self._read_blob_content(blob)
        
        analysis_result = "Skipped"
        if content:
            prompt = self._get_prompt(file_type, content)
            if prompt:
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
        """Categorizes file based on extension and naming convention.
        
        DEPRECATED: Use self.adapter.categorize_file() instead.
        Kept for backward compatibility.
        """
        return self.adapter.categorize_file(filename)
