"""Adapter abstractions and registry."""

from data_access_tool.adapters.base import AdapterCapabilities, DataAdapter
from data_access_tool.adapters.registry import AdapterRegistry

__all__ = ["AdapterCapabilities", "DataAdapter", "AdapterRegistry"]
