"""
Expert System Engine - Lightweight Production Rules
Forward chaining expert system without external dependencies
"""
from typing import Dict, List, Any, Callable
from dataclasses import dataclass


@dataclass
class Fact:
    """Represents a fact in the knowledge base"""
    name: str
    value: Any
    
    def __hash__(self):
        return hash((self.name, str(self.value)))
    
    def __eq__(self, other):
        return self.name == other.name and self.value == other.value


@dataclass
class Rule:
    """Represents a production rule"""
    name: str
    conditions: List[Callable[[Dict], bool]]
    action: Callable[[Dict], List[Fact]]
    priority: int = 0


class ExpertSystem:
    """
    Lightweight expert system with forward chaining
    """
    
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.decisions = []
        self.rules_fired = []
        self.risk_level = "LOW"
    
    def add_fact(self, name: str, value: Any):
        """Add a fact to the knowledge base"""
        self.facts.add(Fact(name, value))
    
    def add_rule(self, rule: Rule):
        """Add a rule to the rule base"""
        self.rules.append(rule)
    
    def get_fact_value(self, name: str) -> Any:
        """Get value of a fact by name"""
        for fact in self.facts:
            if fact.name == name:
                return fact.value
        return None
    
    def has_fact(self, name: str, value: Any = None) -> bool:
        """Check if a fact exists"""
        for fact in self.facts:
            if fact.name == name:
                if value is None or fact.value == value:
                    return True
        return False
    
    def run(self):
        """Run forward chaining"""
        changed = True
        iterations = 0
        max_iterations = 100
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            
            # Sort rules by priority
            sorted_rules = sorted(self.rules, key=lambda r: r.priority, reverse=True)
            
            for rule in sorted_rules:
                # Check if all conditions are met
                fact_dict = {f.name: f.value for f in self.facts}
                
                if all(cond(fact_dict) for cond in rule.conditions):
                    # Fire the rule
                    if rule.name not in self.rules_fired:
                        self.rules_fired.append(rule.name)
                        new_facts = rule.action(fact_dict)
                        
                        for fact in new_facts:
                            if fact not in self.facts:
                                self.facts.add(fact)
                                changed = True


class MumbaiEmergencySystem:
    """
    Expert system for Mumbai emergency management
    Supports multiple disaster types: flood, fire, contamination
    """
    
    def __init__(self, disaster_type: str = "flood"):
        self.engine = ExpertSystem()
        self.decisions = []
        self.rules_fired = []
        self.risk_level = "LOW"
        self.disaster_type = disaster_type.lower()
        self._setup_rules()
    
    def _setup_rules(self):
        """Setup production rules based on disaster type"""
        
        if self.disaster_type == "flood":
            self._setup_flood_rules()
        elif self.disaster_type == "fire":
            self._setup_fire_rules()
        elif self.disaster_type == "contamination":
            self._setup_contamination_rules()
        else:
            self._setup_flood_rules()  # Default
    
    def _setup_flood_rules(self):
        """Setup flood-specific rules"""
        
        # LEVEL 1: Environmental Detection Rules
        self.engine.add_rule(Rule(
            name="R1: Extreme Rainfall Detection",
            conditions=[lambda f: f.get('rainfall', 0) > 100],
            action=lambda f: [
                Fact('condition', 'extreme_rainfall'),
                Fact('decision', 'Alert: Extreme rainfall detected (>100mm)')
            ],
            priority=10
        ))
        
        self.engine.add_rule(Rule(
            name="R2: Heavy Rainfall Detection",
            conditions=[lambda f: 50 < f.get('rainfall', 0) <= 100],
            action=lambda f: [
                Fact('condition', 'heavy_rainfall'),
                Fact('decision', 'Warning: Heavy rainfall detected (50-100mm)')
            ],
            priority=9
        ))
        
        self.engine.add_rule(Rule(
            name="R3: Critical Water Level",
            conditions=[lambda f: f.get('water_level', 0) > 3.0],
            action=lambda f: [
                Fact('condition', 'critical_water'),
                Fact('decision', 'Alert: Critical water level (>3.0m)')
            ],
            priority=10
        ))
        
        self.engine.add_rule(Rule(
            name="R4: High Water Level",
            conditions=[lambda f: 2.0 < f.get('water_level', 0) <= 3.0],
            action=lambda f: [
                Fact('condition', 'high_water'),
                Fact('decision', 'Warning: High water level (2.0-3.0m)')
            ],
            priority=8
        ))
        
        # LEVEL 2: Infrastructure Rules
        self.engine.add_rule(Rule(
            name="R5: Critical Infrastructure Failure",
            conditions=[lambda f: f.get('failed_infrastructure', 0) > 5],
            action=lambda f: [
                Fact('infrastructure', 'critical_failure'),
                Fact('decision', 'Alert: Multiple infrastructure failures detected')
            ],
            priority=9
        ))
        
        self.engine.add_rule(Rule(
            name="R6: Severe Traffic Congestion",
            conditions=[lambda f: f.get('traffic_density', 0) > 0.8],
            action=lambda f: [
                Fact('traffic', 'severe_congestion'),
                Fact('decision', 'Alert: Severe traffic congestion (>80%)')
            ],
            priority=8
        ))
        
        # LEVEL 3: Compound Risk Rules
        self.engine.add_rule(Rule(
            name="R7: EXTREME FLOOD RISK",
            conditions=[
                lambda f: any(fact.name == 'condition' and fact.value == 'extreme_rainfall' for fact in self.engine.facts),
                lambda f: any(fact.name == 'condition' and fact.value == 'critical_water' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('risk', 'extreme_flood'),
                Fact('decision', '🚨 EXTREME FLOOD RISK: Immediate evacuation required'),
                Fact('risk_level', 'EXTREME')
            ],
            priority=15
        ))
        
        self.engine.add_rule(Rule(
            name="R8: HIGH FLOOD RISK",
            conditions=[
                lambda f: (
                    (any(fact.name == 'condition' and fact.value == 'heavy_rainfall' for fact in self.engine.facts) and
                     any(fact.name == 'condition' and fact.value == 'high_water' for fact in self.engine.facts)) or
                    (any(fact.name == 'condition' and fact.value == 'extreme_rainfall' for fact in self.engine.facts) and
                     any(fact.name == 'condition' and fact.value == 'high_water' for fact in self.engine.facts))
                )
            ],
            action=lambda f: [
                Fact('risk', 'high_flood'),
                Fact('decision', '⚠️ HIGH FLOOD RISK: Prepare for evacuation'),
                Fact('risk_level', 'HIGH')
            ],
            priority=12
        ))
        
        # LEVEL 4: Evacuation Rules
        self.engine.add_rule(Rule(
            name="R9: Emergency Evacuation Difficult",
            conditions=[
                lambda f: any(fact.name == 'risk' and fact.value == 'extreme_flood' for fact in self.engine.facts),
                lambda f: any(fact.name == 'traffic' and fact.value == 'severe_congestion' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'emergency_evacuation_difficult'),
                Fact('decision', '🚨 CRITICAL: Evacuation difficult due to traffic - Deploy boats/helicopters'),
                Fact('risk_level', 'CRITICAL')
            ],
            priority=20
        ))
        
        self.engine.add_rule(Rule(
            name="R10: Emergency Evacuation Order",
            conditions=[
                lambda f: any(fact.name == 'risk' and fact.value == 'extreme_flood' for fact in self.engine.facts),
                lambda f: not any(fact.name == 'traffic' and fact.value == 'severe_congestion' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'emergency_evacuation'),
                Fact('decision', '🚨 EMERGENCY: Issue immediate evacuation order')
            ],
            priority=18
        ))
        
        self.engine.add_rule(Rule(
            name="R11: Priority Evacuation - Infrastructure",
            conditions=[
                lambda f: any(fact.name == 'risk' and fact.value == 'high_flood' for fact in self.engine.facts),
                lambda f: any(fact.name == 'infrastructure' and fact.value == 'critical_failure' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'priority_evacuation'),
                Fact('decision', '⚠️ PRIORITY: Evacuate areas with infrastructure failures first')
            ],
            priority=14
        ))
        
        # LEVEL 5: Resource Deployment
        self.engine.add_rule(Rule(
            name="R12: Deploy Emergency Resources",
            conditions=[
                lambda f: any(fact.name == 'action' and 'emergency_evacuation_difficult' in str(fact.value) for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('resource', 'emergency_deployed'),
                Fact('decision', '📋 ACTION: Deploy boats, helicopters, and rescue teams')
            ],
            priority=16
        ))
        
        self.engine.add_rule(Rule(
            name="R13: Deploy Standard Resources",
            conditions=[
                lambda f: any(fact.name == 'action' and fact.value == 'emergency_evacuation' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('resource', 'standard_deployed'),
                Fact('decision', '📋 ACTION: Deploy buses and evacuation vehicles')
            ],
            priority=14
        ))
        
        self.engine.add_rule(Rule(
            name="R14: Deploy Infrastructure Teams",
            conditions=[
                lambda f: any(fact.name == 'infrastructure' and fact.value == 'critical_failure' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('resource', 'infrastructure_teams'),
                Fact('decision', '📋 ACTION: Deploy infrastructure repair teams')
            ],
            priority=12
        ))
        
        # LEVEL 6: Communication
        self.engine.add_rule(Rule(
            name="R15: Issue Public Alert",
            conditions=[
                lambda f: any(fact.name == 'risk' and fact.value in ['extreme_flood', 'high_flood'] for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('decision', '📢 COMMUNICATION: Issue public emergency alert')
            ],
            priority=13
        ))
        
        self.engine.add_rule(Rule(
            name="R16: Activate Emergency Services",
            conditions=[
                lambda f: any(fact.name == 'action' and 'evacuation' in str(fact.value) for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('decision', '📞 COMMUNICATION: Activate all emergency services')
            ],
            priority=13
        ))
    
    
    def _setup_fire_rules(self):
        """Setup fire-specific rules"""
        
        # LEVEL 1: Fire Detection
        self.engine.add_rule(Rule(
            name="F1: Extreme Temperature Detection",
            conditions=[lambda f: f.get('temperature', 0) > 45],
            action=lambda f: [
                Fact('condition', 'extreme_heat'),
                Fact('decision', '🔥 Alert: Extreme temperature detected (>45°C)')
            ],
            priority=10
        ))
        
        self.engine.add_rule(Rule(
            name="F2: High Wind Speed",
            conditions=[lambda f: f.get('wind_speed', 0) > 40],
            action=lambda f: [
                Fact('condition', 'high_wind'),
                Fact('decision', '💨 Alert: High wind speed (>40 km/h) - Fire spread risk')
            ],
            priority=9
        ))
        
        self.engine.add_rule(Rule(
            name="F3: Low Humidity",
            conditions=[lambda f: f.get('humidity', 100) < 30],
            action=lambda f: [
                Fact('condition', 'low_humidity'),
                Fact('decision', '⚠️ Warning: Low humidity (<30%) - Fire risk')
            ],
            priority=8
        ))
        
        # LEVEL 2: Fire Risk Assessment
        self.engine.add_rule(Rule(
            name="F4: EXTREME FIRE RISK",
            conditions=[
                lambda f: any(fact.name == 'condition' and fact.value == 'extreme_heat' for fact in self.engine.facts),
                lambda f: any(fact.name == 'condition' and fact.value == 'high_wind' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('risk', 'extreme_fire'),
                Fact('decision', '🚨 EXTREME FIRE RISK: Immediate evacuation required'),
                Fact('risk_level', 'EXTREME')
            ],
            priority=15
        ))
        
        self.engine.add_rule(Rule(
            name="F5: HIGH FIRE RISK",
            conditions=[
                lambda f: (
                    any(fact.name == 'condition' and fact.value == 'extreme_heat' for fact in self.engine.facts) or
                    (any(fact.name == 'condition' and fact.value == 'high_wind' for fact in self.engine.facts) and
                     any(fact.name == 'condition' and fact.value == 'low_humidity' for fact in self.engine.facts))
                )
            ],
            action=lambda f: [
                Fact('risk', 'high_fire'),
                Fact('decision', '⚠️ HIGH FIRE RISK: Prepare for evacuation'),
                Fact('risk_level', 'HIGH')
            ],
            priority=12
        ))
        
        # LEVEL 3: Fire Response
        self.engine.add_rule(Rule(
            name="F6: Deploy Fire Services",
            conditions=[
                lambda f: any(fact.name == 'risk' and 'fire' in str(fact.value) for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'fire_response'),
                Fact('decision', '🚒 ACTION: Deploy fire brigades and emergency services')
            ],
            priority=14
        ))
        
        self.engine.add_rule(Rule(
            name="F7: Evacuate Downwind Areas",
            conditions=[
                lambda f: any(fact.name == 'risk' and fact.value == 'extreme_fire' for fact in self.engine.facts),
                lambda f: any(fact.name == 'condition' and fact.value == 'high_wind' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'downwind_evacuation'),
                Fact('decision', '🚨 CRITICAL: Evacuate downwind areas immediately'),
                Fact('risk_level', 'CRITICAL')
            ],
            priority=18
        ))
        
        self.engine.add_rule(Rule(
            name="F8: Water Supply Priority",
            conditions=[
                lambda f: any(fact.name == 'risk' and 'fire' in str(fact.value) for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('resource', 'water_supply'),
                Fact('decision', '💧 ACTION: Ensure water supply for firefighting')
            ],
            priority=13
        ))
    
    def _setup_contamination_rules(self):
        """Setup contamination-specific rules"""
        
        # LEVEL 1: Contamination Detection
        self.engine.add_rule(Rule(
            name="C1: High Air Pollution",
            conditions=[lambda f: f.get('air_quality_index', 0) > 300],
            action=lambda f: [
                Fact('condition', 'severe_air_pollution'),
                Fact('decision', '☠️ Alert: Severe air pollution detected (AQI >300)')
            ],
            priority=10
        ))
        
        self.engine.add_rule(Rule(
            name="C2: Water Contamination",
            conditions=[lambda f: f.get('water_contamination', 0) > 0.7],
            action=lambda f: [
                Fact('condition', 'water_contaminated'),
                Fact('decision', '⚠️ Alert: Water contamination detected')
            ],
            priority=10
        ))
        
        self.engine.add_rule(Rule(
            name="C3: Chemical Spill",
            conditions=[lambda f: f.get('chemical_level', 0) > 0.5],
            action=lambda f: [
                Fact('condition', 'chemical_spill'),
                Fact('decision', '☢️ Alert: Chemical spill detected')
            ],
            priority=10
        ))
        
        # LEVEL 2: Contamination Risk
        self.engine.add_rule(Rule(
            name="C4: EXTREME CONTAMINATION RISK",
            conditions=[
                lambda f: (
                    any(fact.name == 'condition' and fact.value == 'severe_air_pollution' for fact in self.engine.facts) and
                    any(fact.name == 'condition' and fact.value == 'water_contaminated' for fact in self.engine.facts)
                )
            ],
            action=lambda f: [
                Fact('risk', 'extreme_contamination'),
                Fact('decision', '🚨 EXTREME CONTAMINATION: Immediate evacuation and shelter-in-place'),
                Fact('risk_level', 'EXTREME')
            ],
            priority=15
        ))
        
        self.engine.add_rule(Rule(
            name="C5: HIGH CONTAMINATION RISK",
            conditions=[
                lambda f: any(fact.name == 'condition' and fact.value in ['severe_air_pollution', 'water_contaminated', 'chemical_spill'] for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('risk', 'high_contamination'),
                Fact('decision', '⚠️ HIGH CONTAMINATION RISK: Avoid affected areas'),
                Fact('risk_level', 'HIGH')
            ],
            priority=12
        ))
        
        # LEVEL 3: Contamination Response
        self.engine.add_rule(Rule(
            name="C6: Deploy Hazmat Teams",
            conditions=[
                lambda f: any(fact.name == 'condition' and fact.value == 'chemical_spill' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'hazmat_response'),
                Fact('decision', '☢️ ACTION: Deploy hazmat teams for containment')
            ],
            priority=16
        ))
        
        self.engine.add_rule(Rule(
            name="C7: Distribute Protective Equipment",
            conditions=[
                lambda f: any(fact.name == 'risk' and 'contamination' in str(fact.value) for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('resource', 'protective_equipment'),
                Fact('decision', '😷 ACTION: Distribute masks and protective equipment')
            ],
            priority=14
        ))
        
        self.engine.add_rule(Rule(
            name="C8: Shut Down Water Supply",
            conditions=[
                lambda f: any(fact.name == 'condition' and fact.value == 'water_contaminated' for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('action', 'water_shutdown'),
                Fact('decision', '🚰 ACTION: Shut down contaminated water supply'),
                Fact('resource', 'emergency_water')
            ],
            priority=15
        ))
        
        self.engine.add_rule(Rule(
            name="C9: Issue Health Advisory",
            conditions=[
                lambda f: any(fact.name == 'risk' and 'contamination' in str(fact.value) for fact in self.engine.facts)
            ],
            action=lambda f: [
                Fact('decision', '📢 COMMUNICATION: Issue public health advisory')
            ],
            priority=13
        ))
    def declare(self, **kwargs):
        """Declare initial facts"""
        for key, value in kwargs.items():
            self.engine.add_fact(key, value)
    
    def reset(self):
        """Reset the engine"""
        self.engine = ExpertSystem()
        self.decisions = []
        self.rules_fired = []
        self.risk_level = "LOW"
        # Re-setup rules based on disaster type
        if self.disaster_type == "flood":
            self._setup_flood_rules()
        elif self.disaster_type == "fire":
            self._setup_fire_rules()
        elif self.disaster_type == "contamination":
            self._setup_contamination_rules()
        else:
            self._setup_flood_rules()
    
    def run(self):
        """Run the expert system"""
        self.engine.run()
        
        # Extract results
        self.rules_fired = self.engine.rules_fired
        self.decisions = [f.value for f in self.engine.facts if f.name == 'decision']
        
        # Determine risk level
        risk_levels = [f.value for f in self.engine.facts if f.name == 'risk_level']
        if 'CRITICAL' in risk_levels:
            self.risk_level = 'CRITICAL'
        elif 'EXTREME' in risk_levels:
            self.risk_level = 'EXTREME'
        elif 'HIGH' in risk_levels:
            self.risk_level = 'HIGH'
        else:
            self.risk_level = 'LOW'




def analyze_with_expert_system(data: Dict[str, Any], disaster_type: str = "flood") -> Dict[str, Any]:
    """
    Analyze data using expert system
    """
    engine = MumbaiEmergencySystem(disaster_type=disaster_type)
    engine.reset()
    
    # Declare initial facts based on disaster type
    if disaster_type == "flood":
        engine.declare(
            rainfall=data.get('rainfall', 0),
            water_level=data.get('water_level', 0),
            traffic_density=data.get('traffic_density', 0),
            failed_infrastructure=data.get('failed_infrastructure', 0)
        )
    elif disaster_type == "fire":
        engine.declare(
            temperature=data.get('temperature', 25),
            wind_speed=data.get('wind_speed', 10),
            humidity=data.get('humidity', 60),
            failed_infrastructure=data.get('failed_infrastructure', 0)
        )
    elif disaster_type == "contamination":
        engine.declare(
            air_quality_index=data.get('air_quality_index', 50),
            water_contamination=data.get('water_contamination', 0),
            chemical_level=data.get('chemical_level', 0),
            failed_infrastructure=data.get('failed_infrastructure', 0)
        )
    
    # Run the engine
    engine.run()
    
    return {
        "disaster_type": disaster_type,
        "risk_level": engine.risk_level,
        "rules_fired": engine.rules_fired,
        "decisions": engine.decisions,
        "total_rules": len(engine.rules_fired),
        "input_data": data
    }


def analyze_ward_expert_system(ward_data: Dict[str, Any], disaster_type: str = "flood") -> Dict[str, Any]:
    """
    Analyze specific ward using expert system
    """
    if disaster_type == "flood":
        return analyze_with_expert_system({
            'rainfall': ward_data.get('rainfall_mm', 0),
            'water_level': ward_data.get('water_level_m', 0),
            'traffic_density': ward_data.get('traffic_density', 0),
            'failed_infrastructure': ward_data.get('failed_infrastructure', 0)
        }, disaster_type)
    elif disaster_type == "fire":
        return analyze_with_expert_system({
            'temperature': ward_data.get('temperature', 25),
            'wind_speed': ward_data.get('wind_speed', 10),
            'humidity': ward_data.get('humidity', 60),
            'failed_infrastructure': ward_data.get('failed_infrastructure', 0)
        }, disaster_type)
    elif disaster_type == "contamination":
        return analyze_with_expert_system({
            'air_quality_index': ward_data.get('air_quality_index', 50),
            'water_contamination': ward_data.get('water_contamination', 0),
            'chemical_level': ward_data.get('chemical_level', 0),
            'failed_infrastructure': ward_data.get('failed_infrastructure', 0)
        }, disaster_type)
