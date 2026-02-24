"""
Digital Twin Core Module

Provides realistic city modeling with population dynamics,
economic activity, and critical asset management.
"""

from .city_model import CityModel
from .population_model import PopulationModel, Demographics
from .economic_model import EconomicModel, EconomicSector
from .critical_asset_registry import (
    CriticalAssetRegistry,
    CriticalAsset,
    AssetType
)
from .baseline_state_manager import BaselineStateManager
from .twin_manager import TwinManager

__all__ = [
    "CityModel",
    "PopulationModel",
    "Demographics",
    "EconomicModel",
    "EconomicSector",
    "CriticalAssetRegistry",
    "CriticalAsset",
    "AssetType",
    "BaselineStateManager",
    "TwinManager",
]
