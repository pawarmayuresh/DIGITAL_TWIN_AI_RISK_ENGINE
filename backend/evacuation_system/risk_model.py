"""
Risk Model - Calculates flood risk scores with explainable features
"""
from typing import Dict, Any


class FloodRiskModel:
    """Model for calculating flood risk with explainable features"""
    
    def __init__(self):
        # Feature weights for risk calculation
        self.weights = {
            "water_level": 0.35,
            "rainfall": 0.25,
            "coastal_proximity": 0.20,
            "river_proximity": 0.15,
            "population_density": 0.05
        }
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Predict flood risk score from features"""
        
        # Normalize features
        water_level = min(features.get("water_level", 0) / 3.0, 1.0)  # Max 3m
        rainfall = min(features.get("rainfall", 0) / 100.0, 1.0)  # Max 100mm/hr
        coastal = 1.0 if features.get("coastal_proximity", 0) > 0 else 0.0
        river = 1.0 if features.get("river_proximity", 0) > 0 else 0.0
        population = min(features.get("population_density", 0) / 2000.0, 1.0)  # Max 2000
        
        # Calculate weighted risk score
        risk_score = (
            water_level * self.weights["water_level"] +
            rainfall * self.weights["rainfall"] +
            coastal * self.weights["coastal_proximity"] +
            river * self.weights["river_proximity"] +
            population * self.weights["population_density"]
        )
        
        return {"risk_score": min(risk_score, 1.0)}
    
    def get_feature_contributions(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Get individual feature contributions to risk score"""
        
        # Normalize features
        water_level = min(features.get("water_level", 0) / 3.0, 1.0)
        rainfall = min(features.get("rainfall", 0) / 100.0, 1.0)
        coastal = 1.0 if features.get("coastal_proximity", 0) > 0 else 0.0
        river = 1.0 if features.get("river_proximity", 0) > 0 else 0.0
        population = min(features.get("population_density", 0) / 2000.0, 1.0)
        
        # Calculate contributions
        contributions = {
            "water_level": water_level * self.weights["water_level"],
            "rainfall": rainfall * self.weights["rainfall"],
            "coastal_proximity": coastal * self.weights["coastal_proximity"],
            "river_proximity": river * self.weights["river_proximity"],
            "population_density": population * self.weights["population_density"]
        }
        
        return contributions
    
    def explain_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Get full explanation of risk prediction"""
        
        prediction = self.predict(features)
        contributions = self.get_feature_contributions(features)
        
        # Sort by contribution
        sorted_features = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Generate explanation text
        risk_score = prediction["risk_score"]
        if risk_score >= 0.65:
            risk_level = "HIGH"
            action = "IMMEDIATE_EVACUATION"
        elif risk_score >= 0.30:
            risk_level = "MEDIUM"
            action = "MONITOR_CLOSELY"
        else:
            risk_level = "LOW"
            action = "NORMAL_OPERATIONS"
        
        top_driver = sorted_features[0][0] if sorted_features else "unknown"
        
        explanation = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommended_action": action,
            "feature_contributions": contributions,
            "top_risk_driver": top_driver,
            "top_3_drivers": [f[0] for f in sorted_features[:3]],
            "explanation_text": f"{risk_level} risk ({risk_score:.2f}) primarily driven by {top_driver}"
        }
        
        return explanation


# Global instance
risk_model = FloodRiskModel()
