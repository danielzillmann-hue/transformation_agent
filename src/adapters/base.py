"""
Base adapter class for source system configurations.
Provides a unified interface for accessing source-specific settings.
"""
import os
import re
import yaml
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class SourceAdapter:
    """
    Adapter for source database systems.
    Loads configuration from YAML and provides methods to access settings.
    """
    
    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict] = None):
        """
        Initialize adapter from config file or dictionary.
        
        Args:
            config_path: Path to YAML config file
            config_dict: Configuration dictionary (alternative to file)
        """
        if config_dict:
            self._config = config_dict
        elif config_path:
            self._config = self._load_config(config_path)
        else:
            raise ValueError("Either config_path or config_dict must be provided")
        
        self._validate_config()
        self._compile_patterns()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Loaded source system config: {config.get('name', 'Unknown')}")
        return config
    
    def _validate_config(self):
        """Validate required configuration fields."""
        required = ['name', 'type_mappings']
        missing = [f for f in required if f not in self._config]
        if missing:
            raise ValueError(f"Missing required config fields: {missing}")
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for performance."""
        self._incremental_patterns = []
        for pattern in self._config.get('incremental_patterns', []):
            try:
                self._incremental_patterns.append(re.compile(pattern, re.IGNORECASE))
            except re.error as e:
                logger.warning(f"Invalid incremental pattern '{pattern}': {e}")
    
    # =========================================================================
    # Basic Properties
    # =========================================================================
    
    @property
    def name(self) -> str:
        """Source system name."""
        return self._config.get('name', 'Unknown')
    
    @property
    def description(self) -> str:
        """Source system description."""
        return self._config.get('description', '')
    
    # =========================================================================
    # Type Mappings
    # =========================================================================
    
    def get_type_mappings(self) -> Dict[str, str]:
        """Get source to BigQuery type mappings."""
        return self._config.get('type_mappings', {})
    
    def map_type(self, source_type: str) -> str:
        """
        Map a source database type to BigQuery type.
        
        Args:
            source_type: Source database type (e.g., 'VARCHAR', 'NUMBER(10,2)')
        
        Returns:
            BigQuery type (e.g., 'STRING', 'NUMERIC')
        """
        mappings = self.get_type_mappings()
        
        # Normalize: uppercase, strip whitespace
        normalized = source_type.upper().strip()
        
        # Try exact match first
        if normalized in mappings:
            return mappings[normalized]
        
        # Try base type (without precision/scale)
        base_type = re.split(r'[\(\s]', normalized)[0]
        if base_type in mappings:
            return mappings[base_type]
        
        # Default fallback
        logger.warning(f"No mapping for type '{source_type}', defaulting to STRING")
        return 'STRING'
    
    # =========================================================================
    # File Detection
    # =========================================================================
    
    def get_file_patterns(self) -> Dict[str, Any]:
        """Get file detection patterns."""
        return self._config.get('file_patterns', {})
    
    def categorize_file(self, filename: str) -> str:
        """
        Categorize a file based on its name and extension.
        
        Args:
            filename: Name of the file
        
        Returns:
            Category: 'ddl', 'procedure', 'etl', or 'unknown'
        """
        lower_name = filename.lower()
        patterns = self.get_file_patterns()
        
        # Check DDL patterns
        ddl_config = patterns.get('ddl', {})
        if self._matches_file_pattern(lower_name, ddl_config):
            return 'sybase_ddl'  # Keep backward compatible name
        
        # Check procedure patterns
        proc_config = patterns.get('procedures', {})
        if self._matches_file_pattern(lower_name, proc_config):
            # Also check for indicators in filename
            indicators = proc_config.get('indicators', [])
            if indicators:
                # For procedures, we might need to check file content
                # For now, rely on extension and prefix
                pass
            return 'sql_transformation'
        
        # Check ETL patterns
        etl_config = patterns.get('etl_exports', {})
        if self._matches_file_pattern(lower_name, etl_config):
            return 'informatica_xml'  # Keep backward compatible name
        
        return 'unknown'
    
    def _matches_file_pattern(self, filename: str, config: Dict) -> bool:
        """Check if filename matches pattern configuration."""
        if not config:
            return False
        
        # Check extensions
        extensions = config.get('extensions', [])
        if extensions:
            if not any(filename.endswith(ext.lower()) for ext in extensions):
                return False
        
        # Check prefixes (if specified, at least one must match)
        prefixes = config.get('prefixes', [])
        if prefixes:
            base_name = os.path.basename(filename)
            if not any(base_name.lower().startswith(p.lower()) for p in prefixes):
                # Prefixes specified but none matched - still allow if extension matched
                # This makes prefixes optional filters rather than requirements
                pass
        
        return True
    
    def get_etl_tool(self) -> str:
        """Get the ETL tool name for this source system."""
        etl_config = self._config.get('file_patterns', {}).get('etl_exports', {})
        return etl_config.get('tool', 'informatica')
    
    # =========================================================================
    # Table Classification
    # =========================================================================
    
    def get_table_classification(self) -> Dict[str, List[str]]:
        """Get table classification prefixes."""
        return self._config.get('table_classification', {
            'dimension_prefixes': ['dim_', 'd_'],
            'fact_prefixes': ['fact_', 'f_'],
            'staging_prefixes': ['stg_', 'stage_', 'tmp_'],
            'bridge_prefixes': ['bridge_', 'b_']
        })
    
    def classify_table(self, table_name: str) -> str:
        """
        Classify a table based on its name.
        
        Returns: 'dimension', 'fact', 'staging', 'bridge', or 'unknown'
        """
        lower_name = table_name.lower()
        classification = self.get_table_classification()
        
        for prefix in classification.get('dimension_prefixes', []):
            if lower_name.startswith(prefix.lower()):
                return 'dimension'
        
        for prefix in classification.get('fact_prefixes', []):
            if lower_name.startswith(prefix.lower()):
                return 'fact'
        
        for prefix in classification.get('staging_prefixes', []):
            if lower_name.startswith(prefix.lower()):
                return 'staging'
        
        for prefix in classification.get('bridge_prefixes', []):
            if lower_name.startswith(prefix.lower()):
                return 'bridge'
        
        return 'unknown'
    
    # =========================================================================
    # SCD Detection
    # =========================================================================
    
    def get_scd_config(self) -> Dict[str, Any]:
        """Get SCD detection configuration."""
        return self._config.get('scd_detection', {})
    
    def get_type2_tables(self) -> set:
        """Get set of tables that should be SCD Type 2."""
        tables = self._config.get('scd_detection', {}).get('type2_tables', [])
        return {t.lower() for t in tables}
    
    def get_type1_tables(self) -> set:
        """Get set of tables that should be SCD Type 1."""
        tables = self._config.get('scd_detection', {}).get('type1_tables', [])
        return {t.lower() for t in tables}
    
    def get_type2_column_indicators(self) -> List[str]:
        """Get column names that indicate SCD Type 2."""
        return self._config.get('scd_detection', {}).get('type2_column_indicators', [
            'effective_date', 'expiry_date', 'valid_from', 'valid_to',
            'is_current', 'current_flag', 'version'
        ])
    
    def get_type1_column_indicators(self) -> List[str]:
        """Get column names that indicate SCD Type 1."""
        return self._config.get('scd_detection', {}).get('type1_column_indicators', [
            'code', 'description', 'name'
        ])
    
    def is_type2_table(self, table_name: str) -> bool:
        """Check if table should be SCD Type 2."""
        return table_name.lower() in self.get_type2_tables()
    
    def is_type1_table(self, table_name: str) -> bool:
        """Check if table should be SCD Type 1."""
        return table_name.lower() in self.get_type1_tables()
    
    # =========================================================================
    # Incremental Loading
    # =========================================================================
    
    def is_incremental_table(self, table_name: str) -> bool:
        """Check if table should use incremental loading."""
        lower_name = table_name.lower()
        for pattern in self._incremental_patterns:
            if pattern.search(lower_name):
                return True
        return False
    
    # =========================================================================
    # Domain Mapping
    # =========================================================================
    
    def get_domain_mapping(self) -> Dict[str, str]:
        """Get domain to dataset mapping."""
        return self._config.get('domain_mapping', {'default': 'bq_staging'})
    
    def map_domain_to_dataset(self, domain: str) -> str:
        """Map a business domain to a BigQuery dataset name."""
        mapping = self.get_domain_mapping()
        return mapping.get(domain, mapping.get('default', 'bq_staging'))
    
    # =========================================================================
    # Function Mappings
    # =========================================================================
    
    def get_function_mappings(self) -> Dict[str, str]:
        """Get source to BigQuery function mappings."""
        # Check for source-specific section first
        for key in self._config:
            if key.endswith('_specific'):
                specific = self._config[key]
                if 'function_mappings' in specific:
                    return specific['function_mappings']
        
        # Fall back to top-level function_mappings
        return self._config.get('function_mappings', {})
    
    # =========================================================================
    # Prompts
    # =========================================================================
    
    def get_prompts(self) -> Dict[str, str]:
        """Get LLM prompts for this source system."""
        return self._config.get('prompts', {})
    
    def get_schema_analysis_prompt(self) -> Optional[str]:
        """Get the schema analysis prompt."""
        return self.get_prompts().get('schema_analysis')
    
    def get_procedure_analysis_prompt(self) -> Optional[str]:
        """Get the procedure analysis prompt."""
        return self.get_prompts().get('procedure_analysis')
    
    def get_etl_analysis_prompt(self) -> Optional[str]:
        """Get the ETL analysis prompt."""
        return self.get_prompts().get('etl_analysis')
    
    # =========================================================================
    # Serialization
    # =========================================================================
    
    def to_dict(self) -> Dict:
        """Export configuration as dictionary."""
        return self._config.copy()
    
    def __repr__(self) -> str:
        return f"SourceAdapter(name='{self.name}')"
