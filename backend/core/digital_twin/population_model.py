"""
Population Model - Demographics, movement, and behavior simulation
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class AgeGroup(Enum):
    """Age group categories"""
    CHILDREN = "children"  # 0-17 years
    ADULTS = "adults"      # 18-64 years
    ELDERLY = "elderly"    # 65+ years
    VULNERABLE = "vulnerable"  # Disabled, chronic illness


@dataclass
class Demographics:
    """Population demographics breakdown"""
    children: int = 0
    adults: int = 0
    elderly: int = 0
    vulnerable: int = 0
    
    @property
    def total(self) -> int:
        return self.children + self.adults + self.elderly + self.vulnerable
    
    def to_dict(self) -> Dict:
        return {
            "children": self.children,
            "adults": self.adults,
            "elderly": self.elderly,
            "vulnerable": self.vulnerable,
            "total": self.total
        }


class PopulationModel:
    """
    Manages population distribution, demographics, and behavior.
    Tracks population impacts from disasters and calculates evacuation needs.
    """
    
    def __init__(
        self,
        total_population: int,
        demographics: Optional[Demographics] = None
    ):
        self.total_population = total_population
        
        # Initialize demographics if not provided
        if demographics is None:
            self.demographics = self._generate_default_demographics()
        else:
            self.demographics = demographics
        
        # Population distribution by zone
        self.population_by_zone: Dict[str, int] = {}
        
        # Vulnerability factors (0.0 to 1.0)
        self.vulnerability_factors: Dict[str, float] = {
            "children": 0.6,
            "adults": 0.3,
            "elderly": 0.8,
            "vulnerable": 0.9
        }
        
        # Evacuation capacity (percentage of population that can evacuate quickly)
        self.evacuation_capacity: float = 0.7
        
        # Status tracking
        self.casualties: int = 0
        self.displaced: int = 0
        self.evacuated: int = 0
    
    def _generate_default_demographics(self) -> Demographics:
        """Generate default demographic distribution"""
        return Demographics(
            children=int(self.total_population * 0.20),  # 20%
            adults=int(self.total_population * 0.65),    # 65%
            elderly=int(self.total_population * 0.10),   # 10%
            vulnerable=int(self.total_population * 0.05) # 5%
        )
    
    def initialize_population(self, grid_manager) -> None:
        """Initialize population distribution across grid"""
        if not grid_manager:
            return
        
        self.distribute_population_to_cells(grid_manager)
    
    def distribute_population_to_cells(self, grid_manager) -> None:
        """Distribute population across grid cells based on zones"""
        if not grid_manager or not grid_manager.cells:
            return
        
        total_cells = len(grid_manager.cells)
        if total_cells == 0:
            return
        
        # Calculate base population per cell
        base_pop_per_cell = self.total_population / total_cells
        
        # Distribute with zone-based multipliers
        zone_multipliers = {
            "residential": 1.5,
            "commercial": 0.8,
            "industrial": 0.3,
            "rural": 0.5,
            "urban": 1.2
        }
        
        for cell in grid_manager.cells.values():
            zone_type = getattr(cell.metadata, 'zone_type', 'residential')
            multiplier = zone_multipliers.get(zone_type, 1.0)
            
            # Assign population
            cell_population = int(base_pop_per_cell * multiplier)
            cell.metadata.population_density = cell_population
            
            # Track by zone
            if zone_type not in self.population_by_zone:
                self.population_by_zone[zone_type] = 0
            self.population_by_zone[zone_type] += cell_population
    
    def calculate_evacuation_demand(self) -> Dict:
        """Calculate evacuation demand and capacity"""
        total_at_risk = self.displaced + self.casualties
        evacuation_needed = int(total_at_risk * 0.8)  # 80% need evacuation
        evacuation_possible = int(self.total_population * self.evacuation_capacity)
        
        return {
            "total_at_risk": total_at_risk,
            "evacuation_needed": evacuation_needed,
            "evacuation_capacity": evacuation_possible,
            "evacuation_gap": max(0, evacuation_needed - evacuation_possible),
            "can_evacuate_all": evacuation_needed <= evacuation_possible
        }
    
    def update_population_status(self, disaster_impacts: Dict) -> None:
        """Update population status based on disaster impacts"""
        if not disaster_impacts:
            return
        
        # Extract impact data
        cells_affected = disaster_impacts.get("total_cells_affected", 0)
        population_affected = disaster_impacts.get("population_affected", 0)
        
        # Calculate casualties based on severity
        severity_factor = disaster_impacts.get("average_severity", 0.5)
        
        # Casualties (higher for vulnerable populations)
        casualty_rate = severity_factor * 0.1  # 10% max casualty rate
        new_casualties = int(population_affected * casualty_rate)
        
        # Apply vulnerability factors
        vulnerable_casualties = int(
            new_casualties * self.vulnerability_factors["vulnerable"] * 0.3
        )
        elderly_casualties = int(
            new_casualties * self.vulnerability_factors["elderly"] * 0.2
        )
        
        self.casualties += new_casualties + vulnerable_casualties + elderly_casualties
        
        # Displaced population
        displacement_rate = severity_factor * 0.3  # 30% max displacement
        self.displaced += int(population_affected * displacement_rate)
        
        # Ensure we don't exceed total population
        self.casualties = min(self.casualties, self.total_population)
        self.displaced = min(self.displaced, self.total_population - self.casualties)
    
    def get_casualties_estimate(self) -> Dict:
        """Get detailed casualties breakdown"""
        return {
            "total_casualties": self.casualties,
            "casualty_rate": self.casualties / self.total_population if self.total_population > 0 else 0,
            "by_age_group": {
                "children": int(self.casualties * 0.15),
                "adults": int(self.casualties * 0.50),
                "elderly": int(self.casualties * 0.25),
                "vulnerable": int(self.casualties * 0.10)
            }
        }
    
    def get_displaced_population(self) -> Dict:
        """Get displaced population details"""
        return {
            "total_displaced": self.displaced,
            "displacement_rate": self.displaced / self.total_population if self.total_population > 0 else 0,
            "shelter_needed": int(self.displaced * 0.8),  # 80% need shelter
            "medical_attention_needed": int(self.displaced * 0.3)  # 30% need medical care
        }
    
    def get_population_vulnerability(self) -> Dict:
        """Calculate overall population vulnerability"""
        # Weighted vulnerability based on demographics
        total_vuln_score = (
            self.demographics.children * self.vulnerability_factors["children"] +
            self.demographics.adults * self.vulnerability_factors["adults"] +
            self.demographics.elderly * self.vulnerability_factors["elderly"] +
            self.demographics.vulnerable * self.vulnerability_factors["vulnerable"]
        )
        
        avg_vulnerability = total_vuln_score / self.demographics.total if self.demographics.total > 0 else 0
        
        return {
            "total_population": self.total_population,
            "at_risk_population": int(self.total_population * avg_vulnerability),
            "vulnerability_index": avg_vulnerability,
            "high_risk_groups": {
                "elderly": self.demographics.elderly,
                "vulnerable": self.demographics.vulnerable,
                "children": self.demographics.children
            }
        }
    
    def get_status_summary(self) -> Dict:
        """Get concise population status"""
        return {
            "total_population": self.total_population,
            "demographics": self.demographics.to_dict(),
            "casualties": self.casualties,
            "displaced": self.displaced,
            "evacuated": self.evacuated,
            "population_by_zone": self.population_by_zone,
            "evacuation_demand": self.calculate_evacuation_demand()
        }
    
    def reset(self) -> None:
        """Reset population status to baseline"""
        self.casualties = 0
        self.displaced = 0
        self.evacuated = 0
