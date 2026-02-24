"""
Inference Engine - Forward and Backward Chaining
"""

class InferenceEngine:
    """Inference Engine for Forward and Backward Chaining"""
    
    def __init__(self, kb):
        self.kb = kb
    
    def forward_chain(self, max_iterations=100):
        """
        Forward Chaining - Data-driven reasoning
        Start from facts and derive new conclusions
        """
        self.kb.clear_inference_trace()
        self.kb.add_trace("Starting Forward Chaining")
        
        iteration = 0
        inferred = True
        
        while inferred and iteration < max_iterations:
            inferred = False
            iteration += 1
            
            for rule in self.kb.rules:
                premises = rule["premises"]
                conclusion = rule["conclusion"]
                rule_name = rule["name"]
                
                # Check if all premises are satisfied
                if premises.issubset(self.kb.facts) and conclusion not in self.kb.facts:
                    # Trigger rule
                    self.kb.add_fact(conclusion)
                    self.kb.add_trace(
                        f"Rule triggered: {rule_name}",
                        rule_name=rule_name,
                        premises=premises,
                        conclusion=conclusion
                    )
                    inferred = True
        
        self.kb.add_trace(f"Forward Chaining completed in {iteration} iterations")
        return self.kb.facts
    
    def backward_chain(self, goal, visited=None):
        """
        Backward Chaining - Goal-driven reasoning
        Start from goal and work backwards to check if achievable
        """
        if visited is None:
            visited = set()
            self.kb.clear_inference_trace()
            self.kb.add_trace(f"Starting Backward Chaining for goal: {goal}")
        
        # Goal already satisfied
        if goal in self.kb.facts:
            self.kb.add_trace(f"Goal '{goal}' already satisfied")
            return True
        
        # Avoid cycles
        if goal in visited:
            return False
        
        visited.add(goal)
        
        # Try to find a rule that concludes the goal
        for rule in self.kb.rules:
            if rule["conclusion"] == goal:
                rule_name = rule["name"]
                premises = rule["premises"]
                
                self.kb.add_trace(
                    f"Checking rule: {rule_name}",
                    rule_name=rule_name,
                    premises=premises,
                    conclusion=goal
                )
                
                # Check if all premises can be satisfied
                if all(self.backward_chain(p, visited) for p in premises):
                    self.kb.add_trace(f"Goal '{goal}' is achievable via {rule_name}")
                    return True
        
        self.kb.add_trace(f"Goal '{goal}' is NOT achievable")
        return False
    
    def second_order_reasoning(self, district):
        """
        Second-Order Logic - Reasoning about predicates
        Generalize rules across predicate categories
        """
        from .knowledge_base import Predicate
        
        self.kb.add_trace(f"Applying Second-Order Reasoning for {district}")
        
        # Check economic indicators
        for fact in self.kb.facts:
            if isinstance(fact, Predicate):
                if fact.name in self.kb.economic_indicators and fact.args[0] == district:
                    economic_risk = Predicate("EconomicRisk", district)
                    if economic_risk not in self.kb.facts:
                        self.kb.add_fact(economic_risk)
                        self.kb.add_trace(
                            f"Second-Order: ANY economic indicator high → EconomicRisk({district})",
                            conclusion=economic_risk
                        )
        
        # Check infrastructure indicators
        for fact in self.kb.facts:
            if isinstance(fact, Predicate):
                if fact.name in self.kb.infrastructure_indicators and fact.args[0] == district:
                    infra_risk = Predicate("InfrastructureRisk", district)
                    if infra_risk not in self.kb.facts:
                        self.kb.add_fact(infra_risk)
                        self.kb.add_trace(
                            f"Second-Order: ANY infrastructure failure → InfrastructureRisk({district})",
                            conclusion=infra_risk
                        )
        
        # Check social indicators
        for fact in self.kb.facts:
            if isinstance(fact, Predicate):
                if fact.name in self.kb.social_indicators and fact.args[0] == district:
                    social_risk = Predicate("SocialRisk", district)
                    if social_risk not in self.kb.facts:
                        self.kb.add_fact(social_risk)
                        self.kb.add_trace(
                            f"Second-Order: ANY social indicator high → SocialRisk({district})",
                            conclusion=social_risk
                        )
        
        return self.kb.facts
