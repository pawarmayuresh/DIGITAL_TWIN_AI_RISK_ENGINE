"""
Economic Model - Economic activity and impact calculation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class SectorType(Enum):
    """Economic sector types"""
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"
    TECHNOLOGY = "technology"
    TOURISM = "tourism"
    GOVERNMENT = "government"
    AGRICULTURE = "agriculture"


@dataclass
class EconomicSector:
    """Represents an economic sector"""
    name: str
    sector_type: SectorType
    gdp_contribution: float  # Annual GDP contribution in dollars
    employment: int  # Number of employees
    infrastructure_dependencies: List[str]  # Infrastructure node types needed
    disruption_tolerance: float  # 0.0 to 1.0, higher = more tolerant
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "sector_type": self.sector_type.value,
            "gdp_contribution": self.gdp_contribution,
            "employment": self.employment,
            "infrastructure_dependencies": self.infrastructure_dependencies,
            "disruption_tolerance": self.disruption_tolerance
        }


class EconomicModel:
    """
    Manages economic activity and calculates economic impacts from disasters.
    Tracks GDP, employment, and business continuity.
    """
    
    def __init__(self, gdp: float, total_employment: Optional[int] = None):
        self.gdp = gdp
        self.baseline_gdp = gdp
        self.total_employment = total_employment or 0
        
        # Economic sectors
        self.sectors: Dict[str, EconomicSector] = {}
        
        # Employment rate (0.0 to 1.0)
        self.employment_rate: float = 0.95
        
        # Business continuity index (0.0 to 1.0)
        self.business_continuity_index: float = 1.0
        
        # Economic loss tracking
        self.total_economic_loss: float = 0.0
        self.daily_loss_rate: float = 0.0
        
        # Initialize default sectors
        self._initialize_default_sectors()
    
    def _initialize_default_sectors(self) -> None:
        """Initialize default economic sectors"""
        # Distribute GDP across sectors
        retail_sector = EconomicSector(
            name="Retail & Commerce",
            sector_type=SectorType.RETAIL,
            gdp_contribution=self.gdp * 0.20,
            employment=int(self.total_employment * 0.25) if self.total_employment else 0,
            infrastructure_dependencies=["power", "telecom", "transport"],
            disruption_tolerance=0.4
        )
        
        manufacturing_sector = EconomicSector(
            name="Manufacturing",
            sector_type=SectorType.MANUFACTURING,
            gdp_contribution=self.gdp * 0.25,
            employment=int(self.total_employment * 0.20) if self.total_employment else 0,
            infrastructure_dependencies=["power", "water", "transport"],
            disruption_tolerance=0.3
        )
        
        services_sector = EconomicSector(
            name="Services",
            sector_type=SectorType.SERVICES,
            gdp_contribution=self.gdp * 0.30,
            employment=int(self.total_employment * 0.35) if self.total_employment else 0,
            infrastructure_dependencies=["power", "telecom"],
            disruption_tolerance=0.6
        )
        
        technology_sector = EconomicSector(
            name="Technology",
            sector_type=SectorType.TECHNOLOGY,
            gdp_contribution=self.gdp * 0.15,
            employment=int(self.total_employment * 0.10) if self.total_employment else 0,
            infrastructure_dependencies=["power", "telecom"],
            disruption_tolerance=0.7
        )
        
        tourism_sector = EconomicSector(
            name="Tourism",
            sector_type=SectorType.TOURISM,
            gdp_contribution=self.gdp * 0.05,
            employment=int(self.total_employment * 0.05) if self.total_employment else 0,
            infrastructure_dependencies=["power", "telecom", "transport"],
            disruption_tolerance=0.2
        )
        
        government_sector = EconomicSector(
            name="Government",
            sector_type=SectorType.GOVERNMENT,
            gdp_contribution=self.gdp * 0.05,
            employment=int(self.total_employment * 0.05) if self.total_employment else 0,
            infrastructure_dependencies=["power", "telecom"],
            disruption_tolerance=0.8
        )
        
        self.sectors = {
            "retail": retail_sector,
            "manufacturing": manufacturing_sector,
            "services": services_sector,
            "technology": technology_sector,
            "tourism": tourism_sector,
            "government": government_sector
        }
    
    def calculate_economic_loss(self, infrastructure_status: Dict[str, float]) -> float:
        """
        Calculate economic loss based on infrastructure status.
        
        Args:
            infrastructure_status: Dict mapping infrastructure type to health (0.0 to 1.0)
        
        Returns:
            Total economic loss in dollars
        """
        total_loss = 0.0
        sector_losses = {}
        
        for sector_id, sector in self.sectors.items():
            # Calculate sector disruption based on infrastructure dependencies
            disruption_level = 0.0
            
            for infra_type in sector.infrastructure_dependencies:
                infra_health = infrastructure_status.get(infra_type, 1.0)
                # Infrastructure damage contributes to disruption
                disruption_level += (1.0 - infra_health)
            
            # Average disruption across dependencies
            if sector.infrastructure_dependencies:
                disruption_level /= len(sector.infrastructure_dependencies)
            
            # Apply disruption tolerance
            effective_disruption = max(0.0, disruption_level - sector.disruption_tolerance)
            
            # Calculate sector loss (daily GDP loss)
            daily_gdp = sector.gdp_contribution / 365.0
            sector_loss = daily_gdp * effective_disruption
            
            sector_losses[sector_id] = sector_loss
            total_loss += sector_loss
        
        self.daily_loss_rate = total_loss
        self.total_economic_loss += total_loss
        
        return total_loss
    
    def estimate_recovery_time(self, infrastructure_status: Dict[str, float]) -> Dict:
        """Estimate economic recovery time based on infrastructure status"""
        # Calculate average infrastructure health
        avg_infra_health = sum(infrastructure_status.values()) / len(infrastructure_status) if infrastructure_status else 1.0
        
        # Recovery time in days (inverse relationship with infrastructure health)
        base_recovery_days = 365  # 1 year max
        recovery_days = int(base_recovery_days * (1.0 - avg_infra_health))
        
        # Calculate recovery phases
        return {
            "estimated_recovery_days": recovery_days,
            "emergency_phase_days": int(recovery_days * 0.1),  # 10%
            "restoration_phase_days": int(recovery_days * 0.4),  # 40%
            "reconstruction_phase_days": int(recovery_days * 0.5),  # 50%
            "full_recovery_date": f"{recovery_days} days from now"
        }
    
    def calculate_business_disruption(self, infrastructure_status: Dict[str, float]) -> Dict:
        """Calculate business disruption metrics"""
        # Calculate sector-wise disruption
        sector_disruptions = {}
        total_disruption = 0.0
        
        for sector_id, sector in self.sectors.items():
            disruption = 0.0
            for infra_type in sector.infrastructure_dependencies:
                infra_health = infrastructure_status.get(infra_type, 1.0)
                disruption += (1.0 - infra_health)
            
            if sector.infrastructure_dependencies:
                disruption /= len(sector.infrastructure_dependencies)
            
            # Apply tolerance
            effective_disruption = max(0.0, disruption - sector.disruption_tolerance)
            sector_disruptions[sector_id] = effective_disruption
            total_disruption += effective_disruption
        
        # Calculate business continuity index
        avg_disruption = total_disruption / len(self.sectors) if self.sectors else 0.0
        self.business_continuity_index = max(0.0, 1.0 - avg_disruption)
        
        # Calculate employment impact
        jobs_at_risk = int(self.total_employment * avg_disruption) if self.total_employment else 0
        
        return {
            "business_continuity_index": self.business_continuity_index,
            "average_disruption": avg_disruption,
            "sector_disruptions": sector_disruptions,
            "jobs_at_risk": jobs_at_risk,
            "businesses_operational": f"{self.business_continuity_index * 100:.1f}%"
        }
    
    def get_sector_status(self) -> Dict:
        """Get status of all economic sectors"""
        return {
            sector_id: {
                "name": sector.name,
                "gdp_contribution": sector.gdp_contribution,
                "employment": sector.employment,
                "health": "operational"  # Will be updated based on disruptions
            }
            for sector_id, sector in self.sectors.items()
        }
    
    def get_economic_summary(self) -> Dict:
        """Get comprehensive economic summary"""
        return {
            "baseline_gdp": self.baseline_gdp,
            "current_gdp": self.gdp,
            "total_economic_loss": self.total_economic_loss,
            "daily_loss_rate": self.daily_loss_rate,
            "business_continuity_index": self.business_continuity_index,
            "employment_rate": self.employment_rate,
            "total_employment": self.total_employment,
            "sectors": {k: v.to_dict() for k, v in self.sectors.items()}
        }
    
    def reset(self) -> None:
        """Reset economic model to baseline"""
        self.gdp = self.baseline_gdp
        self.total_economic_loss = 0.0
        self.daily_loss_rate = 0.0
        self.business_continuity_index = 1.0
        self.employment_rate = 0.95
