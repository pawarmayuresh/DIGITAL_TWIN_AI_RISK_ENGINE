"""
Real-time Policy Engine with Human Behavior Under Uncertainty
Integrates real-time sensor data, human psychology, and adaptive policy recommendations
"""
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import math
from datetime import datetime


class UncertaintyLevel(Enum):
    """Levels of uncertainty in the situation"""
    LOW = "LOW"           # Clear information, predictable
    MEDIUM = "MEDIUM"     # Some ambiguity
    HIGH = "HIGH"         # Significant confusion
    EXTREME = "EXTREME"   # Chaos, panic


class HumanBehaviorState(Enum):
    """Human psychological states during disasters"""
    CALM = "CALM"                    # Rational decision-making
    ANXIOUS = "ANXIOUS"              # Heightened alertness
    PANICKED = "PANICKED"            # Irrational behavior
    DENIAL = "DENIAL"                # Refusing to believe danger
    COMPLIANT = "COMPLIANT"          # Following instructions
    RESISTANT = "RESISTANT"          # Refusing to evacuate
    HELPING = "HELPING"              # Assisting others
    SELF_PRESERVING = "SELF_PRESERVING"  # Only caring for self


@dataclass
class RealTimeSituation:
    """Current real-time situation snapshot"""
    timestamp: datetime
    
    # Environmental conditions
    rain_intensity: float  # mm/hr
    water_level: float     # meters
    wind_speed: float      # km/hr
    visibility: float      # meters
    
    # Infrastructure status
    power_availability: float      # 0.0 to 1.0
    communication_status: float    # 0.0 to 1.0
    road_accessibility: float      # 0.0 to 1.0
    
    # Population metrics
    population_at_risk: int
    population_evacuated: int
    casualties: int
    injured: int
    
    # Information quality
    uncertainty_level: UncertaintyLevel
    information_accuracy: float    # 0.0 to 1.0
    rumor_spread_rate: float       # 0.0 to 1.0
    
    # Resource availability
    emergency_vehicles: int
    medical_personnel: int
    shelter_capacity: int
    food_supplies: float  # days worth
    
    def get_crisis_severity(self) -> float:
        """Calculate overall crisis severity (0.0 to 1.0)"""
        env_severity = (
            min(1.0, self.rain_intensity / 100.0) * 0.3 +
            min(1.0, self.water_level / 3.0) * 0.4 +
            min(1.0, self.wind_speed / 100.0) * 0.3
        )
        
        infra_severity = 1.0 - (
            self.power_availability * 0.3 +
            self.communication_status * 0.4 +
            self.road_accessibility * 0.3
        )
        
        human_severity = 0.0
        if self.population_at_risk > 0:
            human_severity = (
                (self.casualties / max(1, self.population_at_risk)) * 0.5 +
                (self.injured / max(1, self.population_at_risk)) * 0.3 +
                (1.0 - self.population_evacuated / max(1, self.population_at_risk)) * 0.2
            )
        
        return (env_severity * 0.4 + infra_severity * 0.3 + human_severity * 0.3)



@dataclass
class HumanBehaviorModel:
    """Models human behavior under uncertainty"""
    
    # Psychological factors
    panic_level: float = 0.0           # 0.0 to 1.0
    trust_in_authority: float = 0.7    # 0.0 to 1.0
    risk_perception: float = 0.5       # 0.0 to 1.0
    social_influence: float = 0.6      # 0.0 to 1.0
    
    # Behavioral tendencies
    compliance_rate: float = 0.7       # % following instructions
    evacuation_willingness: float = 0.6  # % willing to evacuate
    helping_behavior: float = 0.5      # % helping others
    
    # Uncertainty responses
    information_seeking: float = 0.8   # How much they seek info
    rumor_susceptibility: float = 0.4  # Likelihood to believe rumors
    decision_paralysis: float = 0.2    # Inability to decide
    
    # Demographics influence
    age_distribution: Dict[str, float] = field(default_factory=lambda: {
        "children": 0.25,
        "adults": 0.55,
        "elderly": 0.20
    })
    
    education_level: float = 0.6       # 0.0 to 1.0
    previous_disaster_experience: float = 0.3  # 0.0 to 1.0
    
    def update_from_situation(self, situation: RealTimeSituation):
        """Update behavior based on current situation"""
        
        # Panic increases with severity and uncertainty
        severity = situation.get_crisis_severity()
        uncertainty_factor = {
            UncertaintyLevel.LOW: 0.1,
            UncertaintyLevel.MEDIUM: 0.3,
            UncertaintyLevel.HIGH: 0.6,
            UncertaintyLevel.EXTREME: 0.9
        }[situation.uncertainty_level]
        
        self.panic_level = min(1.0, severity * 0.5 + uncertainty_factor * 0.5)
        
        # Trust decreases if communication fails
        self.trust_in_authority = max(0.2, situation.communication_status * 0.8)
        
        # Risk perception affected by casualties
        if situation.casualties > 0:
            casualty_impact = min(1.0, situation.casualties / 100.0)
            self.risk_perception = min(1.0, self.risk_perception + casualty_impact * 0.3)
        
        # Compliance decreases with panic
        self.compliance_rate = max(0.2, 0.8 - self.panic_level * 0.5)
        
        # Evacuation willingness increases with risk perception
        self.evacuation_willingness = min(1.0, 
            self.risk_perception * 0.6 + 
            (1.0 - self.panic_level) * 0.4  # Too much panic = paralysis
        )
        
        # Decision paralysis increases with uncertainty
        self.decision_paralysis = min(0.8, uncertainty_factor * 0.7)
        
        # Rumor susceptibility increases with poor communication
        self.rumor_susceptibility = min(0.9, 
            (1.0 - situation.communication_status) * 0.6 +
            (1.0 - situation.information_accuracy) * 0.4
        )
    
    def predict_behavior_distribution(self) -> Dict[str, float]:
        """Predict distribution of behavioral states in population"""
        
        # Base probabilities
        calm_prob = max(0.05, (1.0 - self.panic_level) * self.trust_in_authority)
        panic_prob = self.panic_level * (1.0 - self.trust_in_authority)
        denial_prob = (1.0 - self.risk_perception) * 0.3
        compliant_prob = self.compliance_rate * self.trust_in_authority
        resistant_prob = (1.0 - self.compliance_rate) * 0.5
        helping_prob = self.helping_behavior * (1.0 - self.panic_level)
        self_preserving_prob = self.panic_level * 0.7
        
        # Normalize to sum to 1.0
        total = (calm_prob + panic_prob + denial_prob + compliant_prob + 
                resistant_prob + helping_prob + self_preserving_prob)
        
        return {
            "CALM": calm_prob / total,
            "PANICKED": panic_prob / total,
            "DENIAL": denial_prob / total,
            "COMPLIANT": compliant_prob / total,
            "RESISTANT": resistant_prob / total,
            "HELPING": helping_prob / total,
            "SELF_PRESERVING": self_preserving_prob / total
        }
    
    def estimate_evacuation_compliance(self) -> float:
        """Estimate % of population that will comply with evacuation order"""
        
        # Factors affecting compliance
        base_compliance = self.compliance_rate
        
        # Trust factor
        trust_factor = self.trust_in_authority * 0.3
        
        # Risk perception factor
        risk_factor = self.risk_perception * 0.3
        
        # Panic penalty (too much panic = chaos)
        panic_penalty = -self.panic_level * 0.2 if self.panic_level > 0.6 else 0
        
        # Decision paralysis penalty
        paralysis_penalty = -self.decision_paralysis * 0.15
        
        # Experience bonus
        experience_bonus = self.previous_disaster_experience * 0.15
        
        compliance = (base_compliance + trust_factor + risk_factor + 
                     panic_penalty + paralysis_penalty + experience_bonus)
        
        return max(0.1, min(1.0, compliance))



@dataclass
class AdaptivePolicy:
    """Policy that adapts to real-time conditions and human behavior"""
    policy_id: str
    name: str
    description: str
    
    # Policy parameters
    target_population: int
    required_resources: Dict[str, float]
    implementation_time: float  # hours
    cost: float
    
    # Effectiveness modifiers
    base_effectiveness: float  # 0.0 to 1.0
    uncertainty_sensitivity: float  # How much uncertainty affects it
    behavior_dependency: float  # How much it depends on compliance
    
    # Adaptive thresholds
    min_communication_required: float = 0.3
    min_trust_required: float = 0.2
    max_panic_tolerable: float = 0.8
    
    # Real-time adjustments
    current_effectiveness: float = 0.0
    adjustment_history: List[Dict] = field(default_factory=list)
    
    def calculate_effectiveness(
        self, 
        situation: RealTimeSituation,
        behavior: HumanBehaviorModel
    ) -> float:
        """Calculate policy effectiveness given current conditions"""
        
        # Start with base effectiveness
        effectiveness = self.base_effectiveness
        
        # Adjust for uncertainty
        uncertainty_penalty = {
            UncertaintyLevel.LOW: 0.0,
            UncertaintyLevel.MEDIUM: 0.1,
            UncertaintyLevel.HIGH: 0.25,
            UncertaintyLevel.EXTREME: 0.5
        }[situation.uncertainty_level]
        effectiveness -= uncertainty_penalty * self.uncertainty_sensitivity
        
        # Adjust for human behavior
        compliance = behavior.estimate_evacuation_compliance()
        effectiveness *= (0.5 + compliance * 0.5 * self.behavior_dependency)
        
        # Adjust for infrastructure
        if situation.communication_status < self.min_communication_required:
            effectiveness *= 0.5  # Severe penalty
        
        if behavior.trust_in_authority < self.min_trust_required:
            effectiveness *= 0.6
        
        if behavior.panic_level > self.max_panic_tolerable:
            effectiveness *= 0.4  # Panic undermines policy
        
        # Adjust for resource availability
        resource_factor = 1.0
        if situation.emergency_vehicles < self.required_resources.get("vehicles", 0):
            resource_factor *= 0.7
        if situation.shelter_capacity < self.target_population:
            resource_factor *= 0.8
        
        effectiveness *= resource_factor
        
        self.current_effectiveness = max(0.0, min(1.0, effectiveness))
        
        # Record adjustment
        self.adjustment_history.append({
            "timestamp": situation.timestamp,
            "effectiveness": self.current_effectiveness,
            "uncertainty_penalty": uncertainty_penalty,
            "compliance": compliance,
            "resource_factor": resource_factor
        })
        
        return self.current_effectiveness
    
    def get_implementation_barriers(
        self,
        situation: RealTimeSituation,
        behavior: HumanBehaviorModel
    ) -> List[Dict[str, Any]]:
        """Identify barriers to policy implementation"""
        barriers = []
        
        # Communication barriers
        if situation.communication_status < self.min_communication_required:
            barriers.append({
                "type": "COMMUNICATION",
                "severity": "HIGH",
                "description": f"Communication at {situation.communication_status:.0%}, need {self.min_communication_required:.0%}",
                "recommendation": "Deploy emergency broadcast systems, use sirens, door-to-door notification"
            })
        
        # Trust barriers
        if behavior.trust_in_authority < self.min_trust_required:
            barriers.append({
                "type": "TRUST",
                "severity": "MEDIUM",
                "description": f"Public trust at {behavior.trust_in_authority:.0%}",
                "recommendation": "Use community leaders, show visible authority presence, provide transparent information"
            })
        
        # Panic barriers
        if behavior.panic_level > self.max_panic_tolerable:
            barriers.append({
                "type": "PANIC",
                "severity": "HIGH",
                "description": f"Panic level at {behavior.panic_level:.0%}",
                "recommendation": "Deploy calming measures, provide clear instructions, show organized response"
            })
        
        # Resource barriers
        if situation.emergency_vehicles < self.required_resources.get("vehicles", 0):
            barriers.append({
                "type": "RESOURCES",
                "severity": "MEDIUM",
                "description": f"Insufficient vehicles: {situation.emergency_vehicles} available, {self.required_resources.get('vehicles', 0)} needed",
                "recommendation": "Request additional vehicles from neighboring areas, prioritize high-risk zones"
            })
        
        # Uncertainty barriers
        if situation.uncertainty_level in [UncertaintyLevel.HIGH, UncertaintyLevel.EXTREME]:
            barriers.append({
                "type": "UNCERTAINTY",
                "severity": "HIGH" if situation.uncertainty_level == UncertaintyLevel.EXTREME else "MEDIUM",
                "description": f"High uncertainty affecting decision-making",
                "recommendation": "Increase information gathering, provide frequent updates, establish clear protocols"
            })
        
        return barriers



class RealTimePolicyEngine:
    """
    Enhanced policy engine with real-time situation awareness
    and human behavior modeling under uncertainty
    """
    
    def __init__(self):
        self.policies: Dict[str, AdaptivePolicy] = {}
        self.current_situation: Optional[RealTimeSituation] = None
        self.behavior_model: HumanBehaviorModel = HumanBehaviorModel()
        self.active_policies: List[str] = []
        self.policy_history: List[Dict] = []
        
        self._initialize_policies()
    
    def _initialize_policies(self):
        """Initialize standard adaptive policies"""
        
        # Immediate Evacuation Policy
        self.register_policy(AdaptivePolicy(
            policy_id="EVAC_IMMEDIATE",
            name="Immediate Mass Evacuation",
            description="Evacuate all at-risk population immediately",
            target_population=10000,
            required_resources={"vehicles": 50, "personnel": 200, "shelters": 5},
            implementation_time=2.0,
            cost=500000,
            base_effectiveness=0.85,
            uncertainty_sensitivity=0.6,
            behavior_dependency=0.8,
            min_communication_required=0.5,
            min_trust_required=0.4,
            max_panic_tolerable=0.7
        ))
        
        # Phased Evacuation Policy
        self.register_policy(AdaptivePolicy(
            policy_id="EVAC_PHASED",
            name="Phased Evacuation",
            description="Evacuate in priority zones first, then expand",
            target_population=10000,
            required_resources={"vehicles": 30, "personnel": 150, "shelters": 5},
            implementation_time=6.0,
            cost=350000,
            base_effectiveness=0.75,
            uncertainty_sensitivity=0.4,
            behavior_dependency=0.6,
            min_communication_required=0.6,
            min_trust_required=0.5,
            max_panic_tolerable=0.6
        ))
        
        # Shelter-in-Place Policy
        self.register_policy(AdaptivePolicy(
            policy_id="SHELTER_IN_PLACE",
            name="Shelter in Place",
            description="Instruct population to stay indoors in safe locations",
            target_population=10000,
            required_resources={"vehicles": 10, "personnel": 50, "shelters": 0},
            implementation_time=1.0,
            cost=50000,
            base_effectiveness=0.60,
            uncertainty_sensitivity=0.3,
            behavior_dependency=0.7,
            min_communication_required=0.7,
            min_trust_required=0.6,
            max_panic_tolerable=0.5
        ))
        
        # Communication Enhancement Policy
        self.register_policy(AdaptivePolicy(
            policy_id="COMM_ENHANCE",
            name="Enhanced Communication",
            description="Deploy multiple communication channels, reduce uncertainty",
            target_population=10000,
            required_resources={"vehicles": 5, "personnel": 30, "shelters": 0},
            implementation_time=0.5,
            cost=100000,
            base_effectiveness=0.70,
            uncertainty_sensitivity=0.8,  # Highly effective against uncertainty
            behavior_dependency=0.4,
            min_communication_required=0.2,
            min_trust_required=0.3,
            max_panic_tolerable=0.9
        ))
        
        # Panic Management Policy
        self.register_policy(AdaptivePolicy(
            policy_id="PANIC_MGMT",
            name="Panic Management",
            description="Deploy calming measures, visible authority, clear instructions",
            target_population=10000,
            required_resources={"vehicles": 15, "personnel": 100, "shelters": 0},
            implementation_time=1.0,
            cost=150000,
            base_effectiveness=0.65,
            uncertainty_sensitivity=0.5,
            behavior_dependency=0.9,  # Highly dependent on behavior
            min_communication_required=0.4,
            min_trust_required=0.3,
            max_panic_tolerable=1.0  # Designed for high panic
        ))
        
        # Resource Mobilization Policy
        self.register_policy(AdaptivePolicy(
            policy_id="RESOURCE_MOB",
            name="Emergency Resource Mobilization",
            description="Request and deploy additional resources from neighboring areas",
            target_population=10000,
            required_resources={"vehicles": 0, "personnel": 50, "shelters": 0},
            implementation_time=3.0,
            cost=300000,
            base_effectiveness=0.80,
            uncertainty_sensitivity=0.3,
            behavior_dependency=0.2,
            min_communication_required=0.5,
            min_trust_required=0.2,
            max_panic_tolerable=0.9
        ))
    
    def register_policy(self, policy: AdaptivePolicy):
        """Register a new adaptive policy"""
        self.policies[policy.policy_id] = policy
    
    def update_situation(self, situation: RealTimeSituation):
        """Update current situation and recalculate behavior"""
        self.current_situation = situation
        self.behavior_model.update_from_situation(situation)
        
        # Recalculate effectiveness of all policies
        for policy in self.policies.values():
            policy.calculate_effectiveness(situation, self.behavior_model)
    
    def recommend_policies(
        self,
        max_policies: int = 3,
        max_cost: float = 1000000
    ) -> List[Dict[str, Any]]:
        """Recommend best policies for current situation"""
        
        if not self.current_situation:
            return []
        
        # Score each policy
        policy_scores = []
        for policy_id, policy in self.policies.items():
            effectiveness = policy.calculate_effectiveness(
                self.current_situation,
                self.behavior_model
            )
            
            # Calculate urgency score
            severity = self.current_situation.get_crisis_severity()
            urgency = severity * (1.0 / max(0.1, policy.implementation_time))
            
            # Calculate cost-effectiveness
            cost_effectiveness = effectiveness / max(1, policy.cost / 100000)
            
            # Combined score
            score = effectiveness * 0.5 + urgency * 0.3 + cost_effectiveness * 0.2
            
            policy_scores.append({
                "policy_id": policy_id,
                "policy": policy,
                "effectiveness": effectiveness,
                "urgency": urgency,
                "cost_effectiveness": cost_effectiveness,
                "score": score,
                "barriers": policy.get_implementation_barriers(
                    self.current_situation,
                    self.behavior_model
                )
            })
        
        # Sort by score
        policy_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Select top policies within budget
        selected = []
        total_cost = 0
        for item in policy_scores:
            if len(selected) >= max_policies:
                break
            if total_cost + item["policy"].cost <= max_cost:
                selected.append(item)
                total_cost += item["policy"].cost
        
        return selected

    
    def simulate_policy_outcome(
        self,
        policy_id: str,
        time_horizon: int = 24  # hours
    ) -> Dict[str, Any]:
        """Simulate policy outcome considering human behavior uncertainty"""
        
        if policy_id not in self.policies:
            return {"error": "Policy not found"}
        
        policy = self.policies[policy_id]
        
        if not self.current_situation:
            return {"error": "No current situation data"}
        
        # Calculate expected compliance
        compliance = self.behavior_model.estimate_evacuation_compliance()
        
        # Calculate expected evacuees
        expected_evacuees = int(
            self.current_situation.population_at_risk * 
            compliance * 
            policy.current_effectiveness
        )
        
        # Calculate casualties with uncertainty
        base_casualty_rate = 0.02  # 2% base rate
        
        # Increase with panic
        panic_casualty_increase = self.behavior_model.panic_level * 0.03
        
        # Decrease with effectiveness
        effectiveness_reduction = policy.current_effectiveness * 0.015
        
        casualty_rate = max(0.001, base_casualty_rate + panic_casualty_increase - effectiveness_reduction)
        
        expected_casualties = int(
            (self.current_situation.population_at_risk - expected_evacuees) * 
            casualty_rate
        )
        
        # Calculate resource consumption
        resource_usage = {
            resource: amount * (expected_evacuees / max(1, policy.target_population))
            for resource, amount in policy.required_resources.items()
        }
        
        # Calculate time to complete
        time_to_complete = policy.implementation_time
        if self.behavior_model.panic_level > 0.6:
            time_to_complete *= 1.5  # Panic slows things down
        if self.behavior_model.compliance_rate < 0.5:
            time_to_complete *= 1.3  # Low compliance takes longer
        
        # Uncertainty range
        uncertainty_factor = {
            UncertaintyLevel.LOW: 0.1,
            UncertaintyLevel.MEDIUM: 0.2,
            UncertaintyLevel.HIGH: 0.4,
            UncertaintyLevel.EXTREME: 0.6
        }[self.current_situation.uncertainty_level]
        
        evacuees_range = (
            int(expected_evacuees * (1 - uncertainty_factor)),
            int(expected_evacuees * (1 + uncertainty_factor))
        )
        
        casualties_range = (
            int(expected_casualties * (1 - uncertainty_factor)),
            int(expected_casualties * (1 + uncertainty_factor))
        )
        
        return {
            "policy_id": policy_id,
            "policy_name": policy.name,
            "effectiveness": policy.current_effectiveness,
            "expected_outcomes": {
                "evacuees": expected_evacuees,
                "evacuees_range": evacuees_range,
                "casualties": expected_casualties,
                "casualties_range": casualties_range,
                "time_to_complete_hours": round(time_to_complete, 1),
                "compliance_rate": compliance,
                "success_probability": policy.current_effectiveness * compliance
            },
            "resource_usage": resource_usage,
            "human_factors": {
                "panic_level": self.behavior_model.panic_level,
                "trust_level": self.behavior_model.trust_in_authority,
                "compliance_rate": compliance,
                "behavior_distribution": self.behavior_model.predict_behavior_distribution()
            },
            "uncertainty": {
                "level": self.current_situation.uncertainty_level.value,
                "impact": uncertainty_factor,
                "information_accuracy": self.current_situation.information_accuracy
            },
            "barriers": policy.get_implementation_barriers(
                self.current_situation,
                self.behavior_model
            )
        }
    
    def compare_policies_realtime(
        self,
        policy_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare multiple policies under current conditions"""
        
        if not self.current_situation:
            return {"error": "No current situation data"}
        
        comparisons = []
        for policy_id in policy_ids:
            if policy_id in self.policies:
                outcome = self.simulate_policy_outcome(policy_id)
                comparisons.append(outcome)
        
        # Find best policy
        best_policy = max(
            comparisons,
            key=lambda x: x["expected_outcomes"]["success_probability"]
        )
        
        return {
            "timestamp": self.current_situation.timestamp,
            "situation_severity": self.current_situation.get_crisis_severity(),
            "uncertainty_level": self.current_situation.uncertainty_level.value,
            "policies_compared": len(comparisons),
            "comparisons": comparisons,
            "recommendation": {
                "policy_id": best_policy["policy_id"],
                "policy_name": best_policy["policy_name"],
                "reason": f"Highest success probability ({best_policy['expected_outcomes']['success_probability']:.1%}) under current conditions",
                "expected_evacuees": best_policy["expected_outcomes"]["evacuees"],
                "expected_casualties": best_policy["expected_outcomes"]["casualties"]
            },
            "human_behavior_summary": {
                "panic_level": self.behavior_model.panic_level,
                "compliance_rate": self.behavior_model.compliance_rate,
                "trust_level": self.behavior_model.trust_in_authority,
                "dominant_behavior": max(
                    self.behavior_model.predict_behavior_distribution().items(),
                    key=lambda x: x[1]
                )[0]
            }
        }

    
    def get_adaptive_recommendations(self) -> Dict[str, Any]:
        """Get comprehensive adaptive policy recommendations"""
        
        if not self.current_situation:
            return {"error": "No current situation data"}
        
        severity = self.current_situation.get_crisis_severity()
        
        # Get top policy recommendations
        recommended_policies = self.recommend_policies(max_policies=3)
        
        # Identify critical issues
        critical_issues = []
        
        if self.behavior_model.panic_level > 0.7:
            critical_issues.append({
                "issue": "HIGH_PANIC",
                "severity": "CRITICAL",
                "description": f"Panic level at {self.behavior_model.panic_level:.0%}",
                "immediate_action": "Deploy panic management policy, show visible authority presence"
            })
        
        if self.current_situation.communication_status < 0.4:
            critical_issues.append({
                "issue": "COMMUNICATION_FAILURE",
                "severity": "CRITICAL",
                "description": f"Communication at {self.current_situation.communication_status:.0%}",
                "immediate_action": "Deploy emergency broadcast, use sirens, door-to-door notification"
            })
        
        if self.behavior_model.trust_in_authority < 0.3:
            critical_issues.append({
                "issue": "LOW_TRUST",
                "severity": "HIGH",
                "description": f"Public trust at {self.behavior_model.trust_in_authority:.0%}",
                "immediate_action": "Use community leaders, provide transparent information"
            })
        
        if self.current_situation.uncertainty_level == UncertaintyLevel.EXTREME:
            critical_issues.append({
                "issue": "EXTREME_UNCERTAINTY",
                "severity": "HIGH",
                "description": "Extreme uncertainty affecting all decisions",
                "immediate_action": "Increase information gathering, provide frequent updates"
            })
        
        # Generate adaptive strategy
        strategy = self._generate_adaptive_strategy(severity, recommended_policies)
        
        return {
            "timestamp": self.current_situation.timestamp,
            "situation_assessment": {
                "severity": severity,
                "severity_level": "CRITICAL" if severity > 0.7 else "HIGH" if severity > 0.5 else "MEDIUM" if severity > 0.3 else "LOW",
                "uncertainty": self.current_situation.uncertainty_level.value,
                "population_at_risk": self.current_situation.population_at_risk,
                "population_evacuated": self.current_situation.population_evacuated,
                "evacuation_progress": (
                    self.current_situation.population_evacuated / 
                    max(1, self.current_situation.population_at_risk)
                )
            },
            "human_behavior_analysis": {
                "panic_level": self.behavior_model.panic_level,
                "trust_level": self.behavior_model.trust_in_authority,
                "compliance_rate": self.behavior_model.compliance_rate,
                "evacuation_willingness": self.behavior_model.evacuation_willingness,
                "behavior_distribution": self.behavior_model.predict_behavior_distribution(),
                "expected_compliance": self.behavior_model.estimate_evacuation_compliance()
            },
            "critical_issues": critical_issues,
            "recommended_policies": [
                {
                    "policy_id": item["policy_id"],
                    "policy_name": item["policy"].name,
                    "effectiveness": item["effectiveness"],
                    "score": item["score"],
                    "barriers": item["barriers"],
                    "cost": item["policy"].cost,
                    "implementation_time": item["policy"].implementation_time
                }
                for item in recommended_policies
            ],
            "adaptive_strategy": strategy,
            "next_review_time": "15 minutes"  # Review frequently in crisis
        }
    
    def _generate_adaptive_strategy(
        self,
        severity: float,
        recommended_policies: List[Dict]
    ) -> Dict[str, Any]:
        """Generate adaptive strategy based on conditions"""
        
        strategy = {
            "phase": "",
            "primary_actions": [],
            "secondary_actions": [],
            "monitoring_priorities": [],
            "adaptation_triggers": []
        }
        
        # Determine phase
        if severity > 0.7:
            strategy["phase"] = "CRISIS_RESPONSE"
            strategy["primary_actions"] = [
                "Immediate evacuation of high-risk zones",
                "Deploy all available emergency resources",
                "Establish emergency command center"
            ]
        elif severity > 0.5:
            strategy["phase"] = "ACTIVE_MITIGATION"
            strategy["primary_actions"] = [
                "Phased evacuation starting with priority zones",
                "Enhance communication channels",
                "Pre-position emergency resources"
            ]
        elif severity > 0.3:
            strategy["phase"] = "PREPARATION"
            strategy["primary_actions"] = [
                "Issue warnings and advisories",
                "Prepare evacuation routes",
                "Alert emergency services"
            ]
        else:
            strategy["phase"] = "MONITORING"
            strategy["primary_actions"] = [
                "Continue monitoring conditions",
                "Maintain readiness",
                "Update public information"
            ]
        
        # Add behavior-specific actions
        if self.behavior_model.panic_level > 0.6:
            strategy["secondary_actions"].append(
                "Deploy panic management: visible authority, clear instructions, calming measures"
            )
        
        if self.behavior_model.trust_in_authority < 0.4:
            strategy["secondary_actions"].append(
                "Build trust: use community leaders, transparent communication, show competence"
            )
        
        if self.current_situation.uncertainty_level in [UncertaintyLevel.HIGH, UncertaintyLevel.EXTREME]:
            strategy["secondary_actions"].append(
                "Reduce uncertainty: increase information gathering, frequent updates, clear protocols"
            )
        
        # Monitoring priorities
        strategy["monitoring_priorities"] = [
            "Population evacuation progress",
            "Human behavior indicators (panic, compliance)",
            "Infrastructure status (communication, roads, power)",
            "Resource availability and consumption",
            "Casualty and injury reports"
        ]
        
        # Adaptation triggers
        strategy["adaptation_triggers"] = [
            {
                "condition": "Panic level exceeds 0.8",
                "action": "Switch to panic management policy immediately"
            },
            {
                "condition": "Compliance rate drops below 0.3",
                "action": "Enhance communication and trust-building measures"
            },
            {
                "condition": "Casualties exceed 10",
                "action": "Escalate to crisis response, request external assistance"
            },
            {
                "condition": "Communication failure",
                "action": "Deploy alternative communication methods (sirens, door-to-door)"
            }
        ]
        
        return strategy


# Example usage and testing
if __name__ == "__main__":
    # Create engine
    engine = RealTimePolicyEngine()
    
    # Create a crisis situation
    situation = RealTimeSituation(
        timestamp=datetime.now(),
        rain_intensity=85.0,
        water_level=2.1,
        wind_speed=45.0,
        visibility=100.0,
        power_availability=0.4,
        communication_status=0.5,
        road_accessibility=0.3,
        population_at_risk=10000,
        population_evacuated=2000,
        casualties=5,
        injured=20,
        uncertainty_level=UncertaintyLevel.HIGH,
        information_accuracy=0.6,
        rumor_spread_rate=0.7,
        emergency_vehicles=30,
        medical_personnel=50,
        shelter_capacity=8000,
        food_supplies=3.0
    )
    
    # Update engine with situation
    engine.update_situation(situation)
    
    # Get recommendations
    recommendations = engine.get_adaptive_recommendations()
    
    print("=== REAL-TIME POLICY ENGINE ===")
    print(f"\nSituation Severity: {recommendations['situation_assessment']['severity']:.2f}")
    print(f"Uncertainty Level: {recommendations['situation_assessment']['uncertainty']}")
    print(f"\nHuman Behavior:")
    print(f"  Panic Level: {recommendations['human_behavior_analysis']['panic_level']:.2%}")
    print(f"  Trust Level: {recommendations['human_behavior_analysis']['trust_level']:.2%}")
    print(f"  Expected Compliance: {recommendations['human_behavior_analysis']['expected_compliance']:.2%}")
    
    print(f"\nRecommended Policies:")
    for policy in recommendations['recommended_policies']:
        print(f"  - {policy['policy_name']}: {policy['effectiveness']:.2%} effective")
    
    print(f"\nAdaptive Strategy Phase: {recommendations['adaptive_strategy']['phase']}")
