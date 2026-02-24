"""
Knowledge Base - Stores facts and rules
Supports Propositional Logic, First-Order Logic (FOL), and Second-Order Logic (SOL)
"""

class Predicate:
    """First-Order Logic Predicate"""
    def __init__(self, name, *args):
        self.name = name
        self.args = args
    
    def __repr__(self):
        if self.args:
            return f"{self.name}({', '.join(str(a) for a in self.args)})"
        return self.name
    
    def __eq__(self, other):
        return isinstance(other, Predicate) and \
               self.name == other.name and \
               self.args == other.args
    
    def __hash__(self):
        return hash((self.name, self.args))
    
    def to_dict(self):
        return {
            "type": "predicate",
            "name": self.name,
            "args": list(self.args)
        }


class KnowledgeBase:
    """Knowledge Base for storing facts and rules"""
    
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.inference_trace = []
        
        # Second-Order Logic: Categories of predicates
        self.economic_indicators = {"UnemploymentHigh", "InflationHigh", "GDPLow"}
        self.infrastructure_indicators = {"PowerFailed", "WaterFailed", "HospitalFailed"}
        self.social_indicators = {"SocialUnrest", "CrimeHigh", "ProtestsActive"}
    
    def add_fact(self, fact):
        """Add a fact to the knowledge base"""
        if isinstance(fact, str):
            self.facts.add(fact)
        elif isinstance(fact, Predicate):
            self.facts.add(fact)
        else:
            raise ValueError(f"Invalid fact type: {type(fact)}")
    
    def add_rule(self, premises, conclusion, rule_name=None):
        """
        Add a rule to the knowledge base
        premises: list of facts required
        conclusion: fact to infer
        """
        rule = {
            "premises": set(premises) if not isinstance(premises, set) else premises,
            "conclusion": conclusion,
            "name": rule_name or f"Rule_{len(self.rules) + 1}"
        }
        self.rules.append(rule)
    
    def has_fact(self, fact):
        """Check if a fact exists"""
        return fact in self.facts
    
    def get_facts_by_predicate(self, predicate_name):
        """Get all facts with a specific predicate name (FOL)"""
        return [f for f in self.facts if isinstance(f, Predicate) and f.name == predicate_name]
    
    def clear_inference_trace(self):
        """Clear the inference trace"""
        self.inference_trace = []
    
    def add_trace(self, message, rule_name=None, premises=None, conclusion=None):
        """Add an entry to the inference trace"""
        self.inference_trace.append({
            "message": message,
            "rule_name": rule_name,
            "premises": list(premises) if premises else [],
            "conclusion": str(conclusion) if conclusion else None
        })
    
    def get_state_dict(self):
        """Get current state as dictionary"""
        return {
            "facts": [str(f) for f in self.facts],
            "rules": [
                {
                    "name": r["name"],
                    "premises": [str(p) for p in r["premises"]],
                    "conclusion": str(r["conclusion"])
                }
                for r in self.rules
            ],
            "inference_trace": self.inference_trace
        }
    
    def __str__(self):
        facts_str = "\n  ".join(str(f) for f in self.facts)
        rules_str = "\n  ".join(
            f"{r['name']}: {{{', '.join(str(p) for p in r['premises'])}}} → {r['conclusion']}"
            for r in self.rules
        )
        return f"Facts:\n  {facts_str}\n\nRules:\n  {rules_str}"
