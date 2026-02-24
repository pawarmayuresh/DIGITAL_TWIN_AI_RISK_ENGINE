"""
Logic Programming Engine
Implements FOL-style queries and relational reasoning
"""
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict


class LogicProgram:
    """First-Order Logic Programming Engine"""
    
    def __init__(self):
        self.facts = defaultdict(set)  # predicate_name -> set of tuples
        self.rules = []  # list of (head, body) tuples
        self.query_trace = []
    
    def assert_fact(self, predicate: str, *args):
        """Assert a fact: predicate(arg1, arg2, ...)"""
        self.facts[predicate].add(args)
        self.query_trace.append(f"Asserted: {predicate}{args}")
    
    def assert_rule(self, head: Tuple[str, Tuple], body: List[Tuple[str, Tuple]]):
        """
        Assert a rule: head :- body
        head = (predicate, (args...))
        body = [(predicate, (args...)), ...]
        """
        self.rules.append((head, body))
        head_str = f"{head[0]}{head[1]}"
        body_str = " & ".join(f"{p}{a}" for p, a in body)
        self.query_trace.append(f"Rule: {head_str} <= {body_str}")
    
    def query(self, predicate: str, *args) -> List[Tuple]:
        """
        Query facts and apply rules
        Returns list of matching tuples
        """
        self.query_trace.append(f"Query: {predicate}{args}")
        
        # Check direct facts
        results = set()
        
        # Handle variables (None) in query
        if None in args:
            # Find all matching facts
            for fact_args in self.facts[predicate]:
                if self._matches(args, fact_args):
                    results.add(fact_args)
        else:
            # Exact match
            if args in self.facts[predicate]:
                results.add(args)
        
        # Apply rules
        for head, body in self.rules:
            if head[0] == predicate:
                # Try to unify head with query
                bindings = self._unify(head[1], args)
                if bindings is not None:
                    # Check if body is satisfied
                    if self._check_body(body, bindings):
                        # Substitute bindings in head
                        result = self._substitute(head[1], bindings)
                        results.add(result)
        
        result_list = list(results)
        self.query_trace.append(f"Results: {result_list}")
        return result_list
    
    def query_all(self, predicate: str) -> List[Tuple]:
        """Query all instances of a predicate"""
        return self.query(predicate, *[None] * self._get_arity(predicate))
    
    def _get_arity(self, predicate: str) -> int:
        """Get arity (number of arguments) of predicate"""
        if predicate in self.facts and self.facts[predicate]:
            return len(next(iter(self.facts[predicate])))
        return 1
    
    def _matches(self, pattern: Tuple, fact: Tuple) -> bool:
        """Check if pattern matches fact (None is wildcard)"""
        if len(pattern) != len(fact):
            return False
        return all(p is None or p == f for p, f in zip(pattern, fact))
    
    def _unify(self, pattern: Tuple, query: Tuple) -> Dict:
        """Unify pattern with query, return variable bindings"""
        if len(pattern) != len(query):
            return None
        
        bindings = {}
        for p, q in zip(pattern, query):
            if isinstance(p, str) and p.startswith("?"):
                # Variable in pattern
                if p in bindings:
                    if bindings[p] != q and q is not None:
                        return None
                else:
                    if q is not None:
                        bindings[p] = q
            elif q is None:
                # Wildcard in query
                continue
            elif p != q:
                return None
        
        return bindings
    
    def _substitute(self, pattern: Tuple, bindings: Dict) -> Tuple:
        """Substitute variables in pattern with bindings"""
        return tuple(bindings.get(p, p) if isinstance(p, str) and p.startswith("?") else p 
                    for p in pattern)
    
    def _check_body(self, body: List[Tuple[str, Tuple]], bindings: Dict) -> bool:
        """Check if all predicates in body are satisfied"""
        for pred, args in body:
            # Substitute variables
            subst_args = self._substitute(args, bindings)
            # Check if fact exists
            if subst_args not in self.facts[pred]:
                # Try to derive it
                results = self.query(pred, *subst_args)
                if not results:
                    return False
        return True
    
    def analyze_ward_dependencies(self, ward_data: Dict) -> Dict:
        """
        Analyze ward using logic programming
        """
        self.query_trace = []
        
        # Assert facts from real-time data
        for ward_id, data in ward_data.items():
            if data.get("rainfall_mm", 0) > 50:
                self.assert_fact("HeavyRainfall", ward_id)
            
            if data.get("water_level_m", 0) > 2.0:
                self.assert_fact("HighWaterLevel", ward_id)
            
            if data.get("traffic_density", 0) > 0.7:
                self.assert_fact("TrafficCongestion", ward_id)
        
        # Define rules
        # FloodRisk(W) :- HeavyRainfall(W) & HighWaterLevel(W)
        self.assert_rule(
            ("FloodRisk", ("?W",)),
            [("HeavyRainfall", ("?W",)), ("HighWaterLevel", ("?W",))]
        )
        
        # EvacuationDifficult(W) :- FloodRisk(W) & TrafficCongestion(W)
        self.assert_rule(
            ("EvacuationDifficult", ("?W",)),
            [("FloodRisk", ("?W",)), ("TrafficCongestion", ("?W",))]
        )
        
        # Query all wards with flood risk
        flood_wards = self.query_all("FloodRisk")
        evacuation_wards = self.query_all("EvacuationDifficult")
        
        return {
            "facts_asserted": len(self.facts),
            "rules_defined": len(self.rules),
            "flood_risk_wards": [w[0] for w in flood_wards],
            "evacuation_difficult_wards": [w[0] for w in evacuation_wards],
            "query_trace": self.query_trace,
            "all_facts": {k: list(v) for k, v in self.facts.items()}
        }
