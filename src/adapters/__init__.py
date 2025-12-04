# Source system adapters for multi-database support
from src.adapters.base import SourceAdapter
from src.adapters.registry import AdapterRegistry

__all__ = ["SourceAdapter", "AdapterRegistry"]
