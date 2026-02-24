"""
Economic Loss Estimator - Estimates economic losses from disasters.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class EconomicLossBreakdown:
    """Breakdown of economic losses."""
    infrastructure_damage: float
    business_interruption: float
    property_damage: float
    emergency_response_costs: float
    healthcare_costs: float
    lost_productivity: float
    total_loss: float


class EconomicLossEstimator:
    """Estimates economic losses from disaster scenarios."""
    
    def __init__(self):
        self.loss_history: List[EconomicLossBreakdown] = []
        
        # Cost factors (per unit)
        self.cost_factors = {
            'infrastructure_damage_per_unit': 100000,
            'business_interruption_per_day': 50000,
            'property_damage_per_unit': 200000,
            'emergency_response_per_person': 1000,
            'healthcare_per_casualty': 50000,
            'productivity_loss_per_person_day': 200
        }
    
    def estimate_losses(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> EconomicLossBreakdown:
        """Estimate total economic losses."""
        
        # Infrastructure damage
        infrastructure_damage = self._estimate_infrastructure_damage(
            disaster_data, city_data
        )
        
        # Business interruption
        business_interruption = self._estimate_business_interruption(
            disaster_data, city_data
        )
        
        # Property damage
        property_damage = self._estimate_property_damage(
            disaster_data, city_data
        )
        
        # Emergency response costs
        emergency_costs = self._estimate_emergency_response_costs(
            disaster_data, city_data
        )
        
        # Healthcare costs
        healthcare_costs = self._estimate_healthcare_costs(
            disaster_data, city_data
        )
        
        # Lost productivity
        lost_productivity = self._estimate_lost_productivity(
            disaster_data, city_data
        )
        
        # Total loss
        total_loss = (
            infrastructure_damage +
            business_interruption +
            property_damage +
            emergency_costs +
            healthcare_costs +
            lost_productivity
        )
        
        breakdown = EconomicLossBreakdown(
            infrastructure_damage=infrastructure_damage,
            business_interruption=business_interruption,
            property_damage=property_damage,
            emergency_response_costs=emergency_costs,
            healthcare_costs=healthcare_costs,
            lost_productivity=lost_productivity,
            total_loss=total_loss
        )
        
        self.loss_history.append(breakdown)
        return breakdown
    
    def _estimate_infrastructure_damage(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> float:
        """Estimate infrastructure damage costs."""
        severity = disaster_data.get('severity', 0)
        infrastructure_health = disaster_data.get('infrastructure_health', 100)
        
        # Damage percentage
        damage_pct = (100 - infrastructure_health) / 100.0
        
        # Infrastructure value
        infrastructure_value = city_data.get('infrastructure_value', 10000000)
        
        # Calculate damage
        damage = infrastructure_value * damage_pct * (severity / 10.0)
        
        return damage
    
    def _estimate_business_interruption(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> float:
        """Estimate business interruption costs."""
        duration_days = disaster_data.get('duration_days', 1)
        severity = disaster_data.get('severity', 0)
        
        # Business value per day
        daily_business_value = city_data.get('daily_business_value', 1000000)
        
        # Interruption percentage based on severity
        interruption_pct = min(severity / 10.0, 1.0)
        
        # Calculate loss
        loss = daily_business_value * duration_days * interruption_pct
        
        return loss
    
    def _estimate_property_damage(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> float:
        """Estimate property damage costs."""
        severity = disaster_data.get('severity', 0)
        affected_area = disaster_data.get('affected_area_km2', 1)
        
        # Property value per km2
        property_value_per_km2 = city_data.get('property_value_per_km2', 5000000)
        
        # Damage factor
        damage_factor = (severity / 10.0) ** 2
        
        # Calculate damage
        damage = property_value_per_km2 * affected_area * damage_factor
        
        return damage
    
    def _estimate_emergency_response_costs(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> float:
        """Estimate emergency response costs."""
        population_affected = disaster_data.get('population_affected', 0)
        severity = disaster_data.get('severity', 0)
        
        # Base cost per person
        cost_per_person = self.cost_factors['emergency_response_per_person']
        
        # Severity multiplier
        severity_multiplier = 1 + (severity / 10.0)
        
        # Calculate cost
        cost = population_affected * cost_per_person * severity_multiplier
        
        return cost
    
    def _estimate_healthcare_costs(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> float:
        """Estimate healthcare costs."""
        casualties = disaster_data.get('casualties', 0)
        injured = disaster_data.get('injured', casualties * 3)
        
        # Costs
        cost_per_casualty = self.cost_factors['healthcare_per_casualty']
        cost_per_injured = cost_per_casualty * 0.3
        
        # Calculate total
        total_cost = (casualties * cost_per_casualty) + (injured * cost_per_injured)
        
        return total_cost
    
    def _estimate_lost_productivity(
        self,
        disaster_data: Dict[str, Any],
        city_data: Dict[str, Any]
    ) -> float:
        """Estimate lost productivity costs."""
        population_affected = disaster_data.get('population_affected', 0)
        duration_days = disaster_data.get('duration_days', 1)
        
        # Workforce percentage
        workforce_pct = 0.6
        
        # Cost per person per day
        cost_per_person_day = self.cost_factors['productivity_loss_per_person_day']
        
        # Calculate loss
        loss = population_affected * workforce_pct * duration_days * cost_per_person_day
        
        return loss
    
    def estimate_loss_prevented(
        self,
        baseline_losses: EconomicLossBreakdown,
        actual_losses: EconomicLossBreakdown
    ) -> float:
        """Estimate economic loss prevented by interventions."""
        return max(0, baseline_losses.total_loss - actual_losses.total_loss)
    
    def calculate_roi(
        self,
        intervention_cost: float,
        loss_prevented: float
    ) -> float:
        """Calculate return on investment for interventions."""
        if intervention_cost == 0:
            return 0.0
        
        return (loss_prevented - intervention_cost) / intervention_cost
    
    def get_loss_breakdown_percentages(
        self,
        breakdown: EconomicLossBreakdown
    ) -> Dict[str, float]:
        """Get loss breakdown as percentages."""
        if breakdown.total_loss == 0:
            return {k: 0.0 for k in [
                'infrastructure_damage', 'business_interruption',
                'property_damage', 'emergency_response_costs',
                'healthcare_costs', 'lost_productivity'
            ]}
        
        return {
            'infrastructure_damage': (breakdown.infrastructure_damage / breakdown.total_loss) * 100,
            'business_interruption': (breakdown.business_interruption / breakdown.total_loss) * 100,
            'property_damage': (breakdown.property_damage / breakdown.total_loss) * 100,
            'emergency_response_costs': (breakdown.emergency_response_costs / breakdown.total_loss) * 100,
            'healthcare_costs': (breakdown.healthcare_costs / breakdown.total_loss) * 100,
            'lost_productivity': (breakdown.lost_productivity / breakdown.total_loss) * 100
        }
    
    def get_average_losses(self, last_n: Optional[int] = None) -> Dict[str, float]:
        """Get average losses over recent simulations."""
        history = self.loss_history[-last_n:] if last_n else self.loss_history
        
        if not history:
            return {}
        
        return {
            'avg_infrastructure_damage': sum(l.infrastructure_damage for l in history) / len(history),
            'avg_business_interruption': sum(l.business_interruption for l in history) / len(history),
            'avg_property_damage': sum(l.property_damage for l in history) / len(history),
            'avg_emergency_costs': sum(l.emergency_response_costs for l in history) / len(history),
            'avg_healthcare_costs': sum(l.healthcare_costs for l in history) / len(history),
            'avg_lost_productivity': sum(l.lost_productivity for l in history) / len(history),
            'avg_total_loss': sum(l.total_loss for l in history) / len(history)
        }
    
    def update_cost_factor(self, factor_name: str, value: float):
        """Update a cost factor."""
        if factor_name in self.cost_factors:
            self.cost_factors[factor_name] = value
