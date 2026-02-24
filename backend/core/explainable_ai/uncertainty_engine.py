"""
Uncertainty Engine - Monte Carlo simulation for confidence intervals
"""
import random
from typing import Dict, Any, List, Callable
import statistics


class UncertaintyEngine:
    """Estimates uncertainty and confidence intervals using Monte Carlo simulation"""
    
    def __init__(self, num_simulations: int = 100):
        self.num_simulations = num_simulations
        self.simulation_results = []
    
    def estimate_uncertainty(
        self,
        model_fn: Callable,
        input_features: Dict[str, Any],
        noise_level: float = 0.1
    ) -> Dict[str, Any]:
        """Run Monte Carlo simulation to estimate prediction uncertainty"""
        
        predictions = []
        
        for _ in range(self.num_simulations):
            # Add noise to input features
            noisy_input = self._add_noise(input_features, noise_level)
            
            # Get prediction
            prediction = model_fn(noisy_input)
            
            # Extract numeric value
            if isinstance(prediction, dict):
                pred_value = prediction.get("risk_score", 0)
            else:
                pred_value = float(prediction)
            
            predictions.append(pred_value)
        
        # Calculate statistics
        mean_pred = statistics.mean(predictions)
        std_pred = statistics.stdev(predictions) if len(predictions) > 1 else 0
        min_pred = min(predictions)
        max_pred = max(predictions)
        
        # Calculate confidence interval (95%)
        sorted_preds = sorted(predictions)
        ci_lower_idx = int(0.025 * len(sorted_preds))
        ci_upper_idx = int(0.975 * len(sorted_preds))
        ci_lower = sorted_preds[ci_lower_idx]
        ci_upper = sorted_preds[ci_upper_idx]
        
        # Calculate confidence score (inverse of variance)
        confidence = max(0, min(1, 1.0 - (std_pred * 2)))
        
        result = {
            "mean_prediction": round(mean_pred, 3),
            "std_deviation": round(std_pred, 3),
            "confidence_score": round(confidence, 3),
            "confidence_interval_95": {
                "lower": round(ci_lower, 3),
                "upper": round(ci_upper, 3)
            },
            "range": {
                "min": round(min_pred, 3),
                "max": round(max_pred, 3)
            },
            "num_simulations": self.num_simulations,
            "interpretation": self._interpret_uncertainty(std_pred, confidence)
        }
        
        self.simulation_results.append(result)
        return result
    
    def _add_noise(
        self,
        features: Dict[str, Any],
        noise_level: float
    ) -> Dict[str, Any]:
        """Add random noise to features"""
        
        noisy_features = {}
        
        for key, value in features.items():
            if isinstance(value, (int, float)):
                # Add Gaussian noise
                noise = random.gauss(0, noise_level * abs(value))
                noisy_features[key] = max(0, value + noise)  # Ensure non-negative
            else:
                noisy_features[key] = value
        
        return noisy_features
    
    def _interpret_uncertainty(
        self,
        std_dev: float,
        confidence: float
    ) -> str:
        """Generate interpretation of uncertainty"""
        
        if confidence > 0.85:
            return "HIGH confidence - prediction is very reliable"
        elif confidence > 0.70:
            return "MEDIUM confidence - prediction is moderately reliable"
        else:
            return "LOW confidence - prediction has high uncertainty"
    
    def estimate_sensor_reliability(
        self,
        sensor_readings: List[float],
        expected_range: tuple = (0, 100)
    ) -> Dict[str, Any]:
        """Estimate reliability of sensor data"""
        
        if not sensor_readings:
            return {"reliability": 0, "status": "NO_DATA"}
        
        # Check for outliers
        mean_val = statistics.mean(sensor_readings)
        std_val = statistics.stdev(sensor_readings) if len(sensor_readings) > 1 else 0
        
        outliers = []
        for reading in sensor_readings:
            if abs(reading - mean_val) > 3 * std_val:
                outliers.append(reading)
        
        # Check range violations
        out_of_range = [r for r in sensor_readings if r < expected_range[0] or r > expected_range[1]]
        
        # Calculate reliability score
        outlier_penalty = len(outliers) / len(sensor_readings)
        range_penalty = len(out_of_range) / len(sensor_readings)
        variance_penalty = min(1.0, std_val / mean_val) if mean_val > 0 else 0
        
        reliability = max(0, 1.0 - (outlier_penalty + range_penalty + variance_penalty * 0.5))
        
        # Determine status
        if reliability > 0.8:
            status = "RELIABLE"
        elif reliability > 0.5:
            status = "MODERATE"
        else:
            status = "UNRELIABLE"
        
        return {
            "reliability_score": round(reliability, 3),
            "status": status,
            "outliers_detected": len(outliers),
            "out_of_range_count": len(out_of_range),
            "variance": round(std_val, 3),
            "recommendation": self._sensor_recommendation(status)
        }
    
    def _sensor_recommendation(self, status: str) -> str:
        """Generate recommendation based on sensor status"""
        
        if status == "RELIABLE":
            return "Sensor data is reliable, safe to use for decisions"
        elif status == "MODERATE":
            return "Sensor data has some issues, use with caution"
        else:
            return "Sensor data is unreliable, consider recalibration or replacement"
    
    def model_variance_analysis(
        self,
        predictions: List[float]
    ) -> Dict[str, Any]:
        """Analyze variance across multiple model predictions"""
        
        if len(predictions) < 2:
            return {"error": "Need at least 2 predictions"}
        
        mean_pred = statistics.mean(predictions)
        variance = statistics.variance(predictions)
        std_dev = statistics.stdev(predictions)
        
        # Calculate coefficient of variation
        cv = (std_dev / mean_pred * 100) if mean_pred > 0 else 0
        
        return {
            "mean_prediction": round(mean_pred, 3),
            "variance": round(variance, 4),
            "std_deviation": round(std_dev, 3),
            "coefficient_of_variation": round(cv, 2),
            "interpretation": f"{'Low' if cv < 10 else 'Medium' if cv < 30 else 'High'} variance across models"
        }


# Global instance
uncertainty_engine = UncertaintyEngine(num_simulations=100)
