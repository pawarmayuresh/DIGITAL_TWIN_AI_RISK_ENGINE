"""
Path Explainability - Explains why evacuation paths were selected
"""
from typing import Dict, Any, List, Optional


class PathExplainer:
    """Explains evacuation path decisions"""
    
    def __init__(self):
        self.path_explanations = []
    
    def explain_path_selection(
        self,
        path: List[str],
        path_costs: Dict[str, float],
        avoided_grids: List[Dict[str, Any]],
        selected_reason: str
    ) -> Dict[str, Any]:
        """Generate explanation for why a path was selected"""
        
        # Analyze path characteristics
        total_cost = sum(path_costs.values())
        avg_cost = total_cost / len(path) if path else 0
        
        # Identify high-risk grids avoided
        high_risk_avoided = [g for g in avoided_grids if g.get("risk_score", 0) > 0.7]
        
        # Generate explanation
        explanation = {
            "path_id": f"PATH_{len(self.path_explanations)}",
            "path_length": len(path),
            "total_cost": total_cost,
            "average_cost_per_grid": avg_cost,
            "grids_avoided": len(avoided_grids),
            "high_risk_avoided": len(high_risk_avoided),
            "selection_reason": selected_reason,
            "explanation_text": self._generate_text_explanation(
                path, avoided_grids, high_risk_avoided, selected_reason
            ),
            "safety_score": self._calculate_safety_score(path_costs, avoided_grids)
        }
        
        self.path_explanations.append(explanation)
        return explanation
    
    def _generate_text_explanation(
        self,
        path: List[str],
        avoided_grids: List[Dict[str, Any]],
        high_risk_avoided: List[Dict[str, Any]],
        reason: str
    ) -> str:
        """Generate natural language explanation"""
        
        text_parts = []
        
        # Path length
        text_parts.append(f"Selected path traverses {len(path)} grid zones.")
        
        # Avoided grids
        if high_risk_avoided:
            avoided_names = [g.get("id", "unknown") for g in high_risk_avoided[:3]]
            text_parts.append(
                f"Avoided {len(high_risk_avoided)} high-risk zones including {', '.join(avoided_names)}."
            )
        
        # Selection reason
        text_parts.append(reason)
        
        return " ".join(text_parts)
    
    def _calculate_safety_score(
        self,
        path_costs: Dict[str, float],
        avoided_grids: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall safety score for path"""
        
        # Lower cost = higher safety
        avg_cost = sum(path_costs.values()) / len(path_costs) if path_costs else 1.0
        cost_score = max(0, 1.0 - avg_cost)
        
        # More high-risk grids avoided = higher safety
        high_risk_count = sum(1 for g in avoided_grids if g.get("risk_score", 0) > 0.7)
        avoidance_score = min(1.0, high_risk_count / 10.0)
        
        # Weighted combination
        safety_score = (cost_score * 0.7) + (avoidance_score * 0.3)
        
        return round(safety_score, 3)
    
    def compare_paths(
        self,
        path1_id: str,
        path2_id: str
    ) -> Dict[str, Any]:
        """Compare two evacuation paths"""
        
        path1 = next((p for p in self.path_explanations if p["path_id"] == path1_id), None)
        path2 = next((p for p in self.path_explanations if p["path_id"] == path2_id), None)
        
        if not path1 or not path2:
            return {"error": "Path not found"}
        
        comparison = {
            "path1": path1_id,
            "path2": path2_id,
            "length_difference": path1["path_length"] - path2["path_length"],
            "cost_difference": path1["total_cost"] - path2["total_cost"],
            "safety_difference": path1["safety_score"] - path2["safety_score"],
            "recommendation": ""
        }
        
        # Generate recommendation
        if comparison["safety_difference"] > 0.1:
            comparison["recommendation"] = f"{path1_id} is significantly safer"
        elif comparison["safety_difference"] < -0.1:
            comparison["recommendation"] = f"{path2_id} is significantly safer"
        elif comparison["length_difference"] < 0:
            comparison["recommendation"] = f"{path1_id} is shorter"
        else:
            comparison["recommendation"] = f"{path2_id} is shorter"
        
        return comparison
    
    def get_path_risks(
        self,
        path: List[str],
        grid_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze risks along a path"""
        
        risks = []
        total_risk = 0
        max_risk = 0
        max_risk_grid = None
        
        for grid_id in path:
            grid = grid_data.get(grid_id, {})
            risk_score = grid.get("risk_score", 0)
            
            risks.append({
                "grid_id": grid_id,
                "risk_score": risk_score,
                "water_level": grid.get("water_level", 0),
                "safety_level": grid.get("safety_level", "UNKNOWN")
            })
            
            total_risk += risk_score
            if risk_score > max_risk:
                max_risk = risk_score
                max_risk_grid = grid_id
        
        avg_risk = total_risk / len(path) if path else 0
        
        return {
            "path_risks": risks,
            "average_risk": round(avg_risk, 3),
            "maximum_risk": round(max_risk, 3),
            "highest_risk_grid": max_risk_grid,
            "risk_assessment": "HIGH" if avg_risk > 0.6 else "MEDIUM" if avg_risk > 0.3 else "LOW"
        }


# Global instance
path_explainer = PathExplainer()
