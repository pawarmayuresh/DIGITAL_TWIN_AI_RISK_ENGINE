"""
Policy Simulator - Simulates different disaster response policies
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class PolicyType(Enum):
    """Types of disaster response policies"""
    EVACUATION = "evacuation"
    SHELTER_IN_PLACE = "shelter_in_place"
    RESOURCE_DISTRIBUTION = "resource_distribution"
    INFRASTRUCTURE_REPAIR = "infrastructure_repair"
    MEDICAL_RESPONSE = "medical_response"
    ECONOMIC_STIMULUS = "economic_stimulus"
    COMMUNICATION = "communication"
    QUARANTINE = "quarantine"


@dataclass
class Policy:
    """Represents a disaster response policy"""
    policy_id: str
    policy_type: PolicyType
    name: str
    description: str
    cost: float  # Implementation cost
    duration_days: int  # How long policy is active
    effectiveness: float  # 0.0 to 1.0
    prerequisites: List[str] = field(default_factory=list)  # Required conditions
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "policy_id": self.policy_id,
            "policy_type": self.policy_type.value,
            "name": self.name,
            "description": self.description,
            "cost": self.cost,
            "duration_days": self.duration_days,
            "effectiveness": self.effectiveness,
            "prerequisites": self.prerequisites,
            "parameters": self.parameters
        }


class PolicySimulator:
    """
    Simulates the effects of different disaster response policies.
    Evaluates policy effectiveness and recommends optimal strategies.
    """
    
    def __init__(self):
        self.available_policies: Dict[str, Policy] = {}
        self.active_policies: Dict[str, Policy] = {}
        self.policy_history: List[Dict] = []
        self.simulation_results: Dict[str, Any] = {}
        
        # Initialize default policies
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize standard disaster response policies"""
        
        # Evacuation policy
        self.register_policy(Policy(
            policy_id="evac_001",
            policy_type=PolicyType.EVACUATION,
            name="Mass Evacuation",
            description="Evacuate population from high-risk areas",
            cost=1_000_000,
            duration_days=7,
            effectiveness=0.85,
            parameters={"evacuation_radius_km": 10, "transport_capacity": 10000}
        ))
        
        # Shelter in place
        self.register_policy(Policy(
            policy_id="shelter_001",
            policy_type=PolicyType.SHELTER_IN_PLACE,
            name="Shelter in Place",
            description="Instruct population to remain indoors",
            cost=100_000,
            duration_days=3,
            effectiveness=0.60,
            parameters={"communication_channels": ["tv", "radio", "mobile"]}
        ))
        
        # Resource distribution
        self.register_policy(Policy(
            policy_id="resource_001",
            policy_type=PolicyType.RESOURCE_DISTRIBUTION,
            name="Emergency Resource Distribution",
            description="Distribute food, water, and medical supplies",
            cost=500_000,
            duration_days=14,
            effectiveness=0.75,
            parameters={"distribution_points": 10, "supplies_per_person": 7}
        ))
        
        # Infrastructure repair
        self.register_policy(Policy(
            policy_id="repair_001",
            policy_type=PolicyType.INFRASTRUCTURE_REPAIR,
            name="Emergency Infrastructure Repair",
            description="Prioritize critical infrastructure restoration",
            cost=2_000_000,
            duration_days=30,
            effectiveness=0.80,
            prerequisites=["disaster_assessment_complete"],
            parameters={"repair_crews": 50, "priority": ["power", "water", "hospital"]}
        ))
        
        # Medical response
        self.register_policy(Policy(
            policy_id="medical_001",
            policy_type=PolicyType.MEDICAL_RESPONSE,
            name="Emergency Medical Response",
            description="Deploy medical teams and field hospitals",
            cost=1_500_000,
            duration_days=21,
            effectiveness=0.90,
            parameters={"medical_teams": 20, "field_hospitals": 5}
        ))
        
        # Economic stimulus
        self.register_policy(Policy(
            policy_id="econ_001",
            policy_type=PolicyType.ECONOMIC_STIMULUS,
            name="Economic Recovery Package",
            description="Financial aid for affected businesses and individuals",
            cost=10_000_000,
            duration_days=180,
            effectiveness=0.70,
            parameters={"business_grants": 5000, "individual_aid": 2000}
        ))
    
    def register_policy(self, policy: Policy) -> None:
        """Register a new policy"""
        self.available_policies[policy.policy_id] = policy
    
    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """Get policy by ID"""
        return self.available_policies.get(policy_id)
    
    def simulate_policy(
        self,
        policy_id: str,
        current_state: Dict,
        twin_manager=None
    ) -> Dict:
        """
        Simulate the effects of applying a policy.
        
        Args:
            policy_id: ID of policy to simulate
            current_state: Current system state
            twin_manager: TwinManager instance for state updates
        
        Returns:
            Simulation results with projected outcomes
        """
        policy = self.get_policy(policy_id)
        if not policy:
            return {"error": f"Policy {policy_id} not found"}
        
        # Check prerequisites
        if not self._check_prerequisites(policy, current_state):
            return {
                "error": "Prerequisites not met",
                "missing": policy.prerequisites
            }
        
        # Calculate policy effects
        results = {
            "policy_id": policy_id,
            "policy_name": policy.name,
            "cost": policy.cost,
            "duration_days": policy.duration_days,
            "effectiveness": policy.effectiveness,
            "projected_outcomes": self._calculate_outcomes(policy, current_state),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store results
        self.simulation_results[policy_id] = results
        
        return results
    
    def _check_prerequisites(self, policy: Policy, current_state: Dict) -> bool:
        """Check if policy prerequisites are met"""
        if not policy.prerequisites:
            return True
        
        # Simple prerequisite checking (can be enhanced)
        state_conditions = current_state.get("conditions", [])
        return all(prereq in state_conditions for prereq in policy.prerequisites)
    
    def _calculate_outcomes(self, policy: Policy, current_state: Dict) -> Dict:
        """Calculate projected outcomes of policy"""
        
        # Extract current metrics
        population = current_state.get("population", {})
        economy = current_state.get("economy", {})
        infrastructure = current_state.get("infrastructure", {})
        
        casualties = population.get("casualties", 0)
        displaced = population.get("displaced", 0)
        total_pop = population.get("total_population", 1)
        
        economic_loss = economy.get("total_economic_loss", 0)
        infra_health = infrastructure.get("average_health", 1.0)
        
        # Calculate policy-specific outcomes
        outcomes = {}
        
        if policy.policy_type == PolicyType.EVACUATION:
            # Evacuation reduces casualties
            prevented_casualties = int(displaced * policy.effectiveness * 0.5)
            outcomes["casualties_prevented"] = prevented_casualties
            outcomes["people_evacuated"] = int(displaced * policy.effectiveness)
            outcomes["evacuation_success_rate"] = policy.effectiveness
        
        elif policy.policy_type == PolicyType.MEDICAL_RESPONSE:
            # Medical response reduces casualties
            lives_saved = int(casualties * policy.effectiveness * 0.3)
            outcomes["lives_saved"] = lives_saved
            outcomes["medical_capacity_increase"] = policy.parameters.get("field_hospitals", 0) * 500
        
        elif policy.policy_type == PolicyType.INFRASTRUCTURE_REPAIR:
            # Repair improves infrastructure health
            health_improvement = (1.0 - infra_health) * policy.effectiveness
            outcomes["infrastructure_health_improvement"] = health_improvement
            outcomes["estimated_repair_time_days"] = policy.duration_days
        
        elif policy.policy_type == PolicyType.ECONOMIC_STIMULUS:
            # Stimulus reduces economic loss
            loss_reduction = economic_loss * policy.effectiveness * 0.4
            outcomes["economic_loss_reduction"] = loss_reduction
            outcomes["businesses_supported"] = policy.parameters.get("business_grants", 0)
        
        elif policy.policy_type == PolicyType.RESOURCE_DISTRIBUTION:
            # Resources support displaced population
            people_supported = min(displaced, policy.parameters.get("distribution_points", 10) * 1000)
            outcomes["people_supported"] = people_supported
            outcomes["support_coverage"] = people_supported / displaced if displaced > 0 else 1.0
        
        # Calculate cost-benefit ratio
        total_benefit = sum(v for v in outcomes.values() if isinstance(v, (int, float)))
        outcomes["cost_benefit_ratio"] = total_benefit / policy.cost if policy.cost > 0 else 0
        
        return outcomes
    
    def compare_policies(
        self,
        policy_ids: List[str],
        current_state: Dict
    ) -> Dict:
        """
        Compare multiple policies and rank them.
        
        Args:
            policy_ids: List of policy IDs to compare
            current_state: Current system state
        
        Returns:
            Comparison results with rankings
        """
        results = []
        
        for policy_id in policy_ids:
            sim_result = self.simulate_policy(policy_id, current_state)
            if "error" not in sim_result:
                results.append(sim_result)
        
        # Rank by cost-benefit ratio
        ranked = sorted(
            results,
            key=lambda x: x["projected_outcomes"].get("cost_benefit_ratio", 0),
            reverse=True
        )
        
        return {
            "comparison_count": len(ranked),
            "ranked_policies": ranked,
            "best_policy": ranked[0] if ranked else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def recommend_policy_bundle(
        self,
        current_state: Dict,
        budget: float,
        max_policies: int = 5
    ) -> Dict:
        """
        Recommend a bundle of complementary policies within budget.
        
        Args:
            current_state: Current system state
            budget: Available budget
            max_policies: Maximum number of policies in bundle
        
        Returns:
            Recommended policy bundle
        """
        # Simulate all available policies
        simulations = []
        for policy_id in self.available_policies:
            result = self.simulate_policy(policy_id, current_state)
            if "error" not in result:
                simulations.append(result)
        
        # Sort by effectiveness and cost-benefit
        sorted_policies = sorted(
            simulations,
            key=lambda x: (
                x["effectiveness"],
                x["projected_outcomes"].get("cost_benefit_ratio", 0)
            ),
            reverse=True
        )
        
        # Select policies within budget
        selected = []
        total_cost = 0.0
        
        for policy in sorted_policies:
            if len(selected) >= max_policies:
                break
            
            if total_cost + policy["cost"] <= budget:
                selected.append(policy)
                total_cost += policy["cost"]
        
        return {
            "recommended_policies": selected,
            "total_cost": total_cost,
            "budget_remaining": budget - total_cost,
            "policy_count": len(selected),
            "estimated_effectiveness": sum(p["effectiveness"] for p in selected) / len(selected) if selected else 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def activate_policy(self, policy_id: str) -> Dict:
        """Activate a policy"""
        policy = self.get_policy(policy_id)
        if not policy:
            return {"error": f"Policy {policy_id} not found"}
        
        self.active_policies[policy_id] = policy
        
        self.policy_history.append({
            "policy_id": policy_id,
            "action": "activated",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "status": "activated",
            "policy": policy.to_dict()
        }
    
    def deactivate_policy(self, policy_id: str) -> Dict:
        """Deactivate a policy"""
        if policy_id in self.active_policies:
            del self.active_policies[policy_id]
            
            self.policy_history.append({
                "policy_id": policy_id,
                "action": "deactivated",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return {"status": "deactivated"}
        
        return {"error": f"Policy {policy_id} not active"}
    
    def get_active_policies(self) -> List[Dict]:
        """Get all currently active policies"""
        return [p.to_dict() for p in self.active_policies.values()]
    
    def get_policy_history(self) -> List[Dict]:
        """Get policy activation history"""
        return self.policy_history
    
    def get_all_policies(self) -> List[Dict]:
        """Get all available policies"""
        return [p.to_dict() for p in self.available_policies.values()]
