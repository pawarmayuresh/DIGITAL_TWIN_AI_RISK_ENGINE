"""
Symbolic Logic Engine using SymPy
Provides formal propositional logic with truth tables and consistency checking
"""
from sympy import symbols, And, Or, Not, Implies, satisfiable
from sympy.logic.boolalg import truth_table
from typing import Dict, List, Tuple
import itertools


class SymbolicLogicEngine:
    """Formal symbolic logic reasoning using SymPy"""
    
    def __init__(self):
        self.propositions = {}
        self.expressions = []
        self.truth_tables = {}
    
    def define_proposition(self, name: str, description: str = ""):
        """Define a symbolic proposition"""
        prop = symbols(name)
        self.propositions[name] = {
            "symbol": prop,
            "description": description
        }
        return prop
    
    def create_expression(self, expr, name: str = None):
        """Create and store a logical expression"""
        if name:
            self.expressions.append({"name": name, "expression": expr})
        return expr
    
    def evaluate(self, expr, values: Dict[str, bool]) -> bool:
        """Evaluate expression with given truth values"""
        substitutions = {
            self.propositions[k]["symbol"]: v 
            for k, v in values.items() 
            if k in self.propositions
        }
        return bool(expr.subs(substitutions))
    
    def generate_truth_table(self, expr, prop_names: List[str]) -> List[Dict]:
        """Generate complete truth table for expression"""
        props = [self.propositions[name]["symbol"] for name in prop_names]
        
        # Generate all combinations
        n = len(props)
        table = []
        
        for values in itertools.product([False, True], repeat=n):
            row = dict(zip(prop_names, values))
            substitutions = dict(zip(props, values))
            result = bool(expr.subs(substitutions))
            row["result"] = result
            table.append(row)
        
        return table
    
    def check_satisfiable(self, expr) -> Tuple[bool, Dict]:
        """Check if expression is satisfiable and return model"""
        result = satisfiable(expr)
        if result is False:
            return False, {}
        
        # Convert sympy model to readable format
        model = {str(k): v for k, v in result.items()}
        return True, model
    
    def check_tautology(self, expr) -> bool:
        """Check if expression is a tautology (always true)"""
        return not satisfiable(Not(expr))
    
    def check_contradiction(self, expr) -> bool:
        """Check if expression is a contradiction (always false)"""
        return not satisfiable(expr)
    
    def check_consistency(self, expressions: List) -> Tuple[bool, str]:
        """Check if multiple expressions are mutually consistent"""
        combined = And(*expressions)
        is_sat, model = self.check_satisfiable(combined)
        
        if not is_sat:
            return False, "Expressions are inconsistent (contradiction detected)"
        
        return True, f"Expressions are consistent. Model: {model}"
    
    def analyze_real_time_data(self, data: Dict[str, float]) -> Dict:
        """
        Analyze real-time data using symbolic logic
        Returns logical analysis with truth tables and consistency checks
        """
        # Define propositions based on real-time thresholds
        heavy_rain = self.define_proposition("heavy_rain", "Rainfall > 50mm")
        high_water = self.define_proposition("high_water", "Water level > 2.0m")
        traffic_jam = self.define_proposition("traffic_jam", "Traffic density > 70%")
        infra_fail = self.define_proposition("infra_fail", "Infrastructure failures > 2")
        
        # Create logical rules
        flooding = self.create_expression(
            And(heavy_rain, high_water),
            "flooding_risk"
        )
        
        evacuation = self.create_expression(
            And(flooding, traffic_jam),
            "evacuation_difficult"
        )
        
        emergency = self.create_expression(
            And(evacuation, infra_fail),
            "emergency_declared"
        )
        
        # Evaluate with real data
        rainfall_mm = data.get("avg_rainfall_mm", 0)
        water_m = data.get("avg_water_level_m", 0)
        traffic = data.get("avg_traffic_density", 0)
        failed = data.get("failed_infrastructure", 0)
        
        truth_values = {
            "heavy_rain": rainfall_mm > 50,
            "high_water": water_m > 2.0,
            "traffic_jam": traffic > 0.7,
            "infra_fail": failed > 2
        }
        
        # Evaluate expressions
        flooding_result = self.evaluate(flooding, truth_values)
        evacuation_result = self.evaluate(evacuation, truth_values)
        emergency_result = self.evaluate(emergency, truth_values)
        
        # Generate truth table for main rule
        main_rule = Implies(And(heavy_rain, high_water), flooding)
        truth_table_data = self.generate_truth_table(
            main_rule,
            ["heavy_rain", "high_water"]
        )
        
        # Check consistency
        all_rules = [flooding, evacuation, emergency]
        is_consistent, consistency_msg = self.check_consistency(all_rules)
        
        # Check if emergency rule is a tautology
        is_tautology = self.check_tautology(main_rule)
        
        return {
            "propositions": {
                k: {
                    "description": v["description"],
                    "value": truth_values.get(k, False)
                }
                for k, v in self.propositions.items()
            },
            "evaluations": {
                "flooding_risk": flooding_result,
                "evacuation_difficult": evacuation_result,
                "emergency_declared": emergency_result
            },
            "truth_table": truth_table_data,
            "consistency": {
                "is_consistent": is_consistent,
                "message": consistency_msg
            },
            "formal_properties": {
                "main_rule_is_tautology": is_tautology,
                "main_rule_is_valid": is_tautology
            },
            "symbolic_expressions": {
                "flooding": str(flooding),
                "evacuation": str(evacuation),
                "emergency": str(emergency)
            }
        }
