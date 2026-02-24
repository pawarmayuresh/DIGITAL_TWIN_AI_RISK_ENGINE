"""
Decision Logger - Structured logging for all AI decisions
"""
import json
import time
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class DecisionLogger:
    """Logs all AI decisions with structured format for explainability"""
    
    def __init__(self, log_file: str = "data/mumbai/outputs/decision_log.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.decisions: List[Dict] = []
        self._load_existing()
    
    def _load_existing(self):
        """Load existing decisions from file"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    self.decisions = json.load(f)
            except:
                self.decisions = []
    
    def log_risk_decision(
        self,
        ward_id: str,
        risk_score: float,
        features: Dict[str, float],
        action: str,
        confidence: float,
        feature_contributions: Dict[str, float] = None
    ) -> str:
        """Log a risk assessment decision"""
        decision_id = f"RISK_{ward_id}_{int(time.time())}"
        
        decision = {
            "decision_id": decision_id,
            "decision_type": "risk_assessment",
            "ward_id": ward_id,
            "timestamp": datetime.now().isoformat(),
            "risk_score": round(risk_score, 3),
            "features_used": {k: round(v, 3) for k, v in features.items()},
            "selected_action": action,
            "confidence": round(confidence, 3),
            "feature_contributions": {k: round(v, 3) for k, v in (feature_contributions or {}).items()}
        }
        
        self.decisions.append(decision)
        self._save()
        return decision_id
    
    def log_evacuation_decision(
        self,
        grid_id: str,
        path_selected: List[str],
        path_cost: float,
        alternatives_considered: int,
        reason: str
    ) -> str:
        """Log an evacuation path decision"""
        decision_id = f"EVAC_{grid_id}_{int(time.time())}"
        
        decision = {
            "decision_id": decision_id,
            "decision_type": "evacuation_path",
            "grid_id": grid_id,
            "timestamp": datetime.now().isoformat(),
            "path_selected": path_selected,
            "path_cost": round(path_cost, 3),
            "alternatives_considered": alternatives_considered,
            "reason": reason
        }
        
        self.decisions.append(decision)
        self._save()
        return decision_id
    
    def log_agent_decision(
        self,
        agent_id: str,
        decision_type: str,
        context: Dict[str, Any],
        action_taken: str,
        reasoning: str
    ) -> str:
        """Log an agent decision"""
        decision_id = f"AGENT_{agent_id}_{int(time.time())}"
        
        decision = {
            "decision_id": decision_id,
            "decision_type": decision_type,
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "action_taken": action_taken,
            "reasoning": reasoning
        }
        
        self.decisions.append(decision)
        self._save()
        return decision_id
    
    def get_recent_decisions(self, limit: int = 50) -> List[Dict]:
        """Get recent decisions"""
        return self.decisions[-limit:]
    
    def get_decisions_by_type(self, decision_type: str) -> List[Dict]:
        """Get decisions by type"""
        return [d for d in self.decisions if d.get("decision_type") == decision_type]
    
    def get_decisions_by_ward(self, ward_id: str) -> List[Dict]:
        """Get decisions for specific ward"""
        return [d for d in self.decisions if d.get("ward_id") == ward_id]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get decision statistics"""
        if not self.decisions:
            return {
                "total_decisions": 0,
                "by_type": {},
                "avg_confidence": 0,
                "recent_count": 0
            }
        
        by_type = {}
        confidences = []
        
        for d in self.decisions:
            dtype = d.get("decision_type", "unknown")
            by_type[dtype] = by_type.get(dtype, 0) + 1
            
            if "confidence" in d:
                confidences.append(d["confidence"])
        
        return {
            "total_decisions": len(self.decisions),
            "by_type": by_type,
            "avg_confidence": round(sum(confidences) / len(confidences), 3) if confidences else 0,
            "recent_count": min(50, len(self.decisions))
        }
    
    def _save(self):
        """Save decisions to file"""
        # Keep only last 1000 decisions to prevent file bloat
        if len(self.decisions) > 1000:
            self.decisions = self.decisions[-1000:]
        
        with open(self.log_file, 'w') as f:
            json.dump(self.decisions, f, indent=2)


# Global instance
decision_logger = DecisionLogger()
