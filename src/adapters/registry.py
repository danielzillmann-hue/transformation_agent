"""
Adapter registry for managing source system configurations.
Auto-discovers available configs and provides factory methods.
"""
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional

from src.adapters.base import SourceAdapter

logger = logging.getLogger(__name__)

# Default config directory
DEFAULT_CONFIG_DIR = Path(__file__).parent.parent.parent / "config" / "source_systems"


class AdapterRegistry:
    """
    Registry for source system adapters.
    Discovers available configs and caches loaded adapters.
    """
    
    _instance = None
    _adapters: Dict[str, SourceAdapter] = {}
    _config_dir: Path = DEFAULT_CONFIG_DIR
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._adapters = {}
        self._discover_configs()
    
    def _discover_configs(self):
        """Discover available config files."""
        self._available_configs = {}
        
        if not self._config_dir.exists():
            logger.warning(f"Config directory not found: {self._config_dir}")
            return
        
        for config_file in self._config_dir.glob("*.yaml"):
            # Skip template
            if config_file.name.startswith("_"):
                continue
            
            name = config_file.stem.lower()
            self._available_configs[name] = config_file
            logger.debug(f"Discovered config: {name} -> {config_file}")
        
        logger.info(f"Discovered {len(self._available_configs)} source system configs")
    
    @classmethod
    def set_config_dir(cls, config_dir: str):
        """Set custom config directory."""
        cls._config_dir = Path(config_dir)
        # Reset instance to re-discover
        if cls._instance:
            cls._instance._initialized = False
            cls._instance._adapters = {}
            cls._instance._discover_configs()
    
    def list_available(self) -> List[str]:
        """List available source system names."""
        return sorted(self._available_configs.keys())
    
    def get(self, source_system: str) -> SourceAdapter:
        """
        Get adapter for a source system.
        
        Args:
            source_system: Name of source system (e.g., 'sybase', 'oracle')
        
        Returns:
            SourceAdapter instance
        
        Raises:
            ValueError: If source system not found
        """
        name = source_system.lower()
        
        # Return cached adapter if available
        if name in self._adapters:
            return self._adapters[name]
        
        # Load from config file
        if name not in self._available_configs:
            available = ", ".join(self.list_available())
            raise ValueError(
                f"Unknown source system: '{source_system}'. "
                f"Available: {available}"
            )
        
        config_path = self._available_configs[name]
        adapter = SourceAdapter(config_path=str(config_path))
        self._adapters[name] = adapter
        
        logger.info(f"Loaded adapter for: {adapter.name}")
        return adapter
    
    def get_or_default(self, source_system: Optional[str] = None) -> SourceAdapter:
        """
        Get adapter for source system, or default (sybase) if not specified.
        
        Args:
            source_system: Name of source system, or None for default
        
        Returns:
            SourceAdapter instance
        """
        if source_system:
            return self.get(source_system)
        
        # Default to sybase for backward compatibility
        return self.get("sybase")
    
    def register_custom(self, name: str, config_dict: Dict):
        """
        Register a custom adapter from a dictionary config.
        
        Args:
            name: Name for the adapter
            config_dict: Configuration dictionary
        """
        adapter = SourceAdapter(config_dict=config_dict)
        self._adapters[name.lower()] = adapter
        logger.info(f"Registered custom adapter: {name}")
    
    def get_config_info(self, source_system: str) -> Dict:
        """
        Get summary info about a source system config.
        
        Returns dict with: name, description, type_count, has_prompts, etc.
        """
        adapter = self.get(source_system)
        return {
            "name": adapter.name,
            "description": adapter.description,
            "type_mappings_count": len(adapter.get_type_mappings()),
            "type2_tables_count": len(adapter.get_type2_tables()),
            "type1_tables_count": len(adapter.get_type1_tables()),
            "has_custom_prompts": bool(adapter.get_prompts()),
            "etl_tool": adapter.get_etl_tool(),
            "function_mappings_count": len(adapter.get_function_mappings())
        }


# Convenience function for getting the registry
def get_registry() -> AdapterRegistry:
    """Get the adapter registry singleton."""
    return AdapterRegistry()


# Convenience function for getting an adapter
def get_adapter(source_system: Optional[str] = None) -> SourceAdapter:
    """
    Get adapter for a source system.
    
    Args:
        source_system: Name of source system, or None for default (sybase)
    
    Returns:
        SourceAdapter instance
    """
    return get_registry().get_or_default(source_system)
