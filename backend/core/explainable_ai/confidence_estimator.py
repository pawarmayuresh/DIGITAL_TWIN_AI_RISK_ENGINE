"""
Confidence Estimator - Estimates confidence levels for AI decisions.
"""

from typing import Dict, Any, List, Optional
import math
import statistics


class ConfidenceEstimator:
    """Estimates confidence levels for AI decisions."""
    
    def __init__(self):
        self.confidence_history: List[Dict[str, Any]] = []
    
    def estimate_confidence(
        self,
        decision_data: Dict[str, Any],
        trace_steps: Optional[List[Any]] = None,
        model_uncertainty: Optional[float] = None
    ) -> Dict[str, Any]:
        """Estimate confidence for a decision."""
        
        confidence_factors = {}
        
        # Factor 1: Data quality
        data_quality = self._assess_data_quality(decision_data)
        confidence_factors['data_quality'] = data_quality
        
        # Factor 2: Model agreement (if multiple steps)
        if trace_steps and len(trace_steps) > 1:
            model_agreement = self._calculate_model_agreement(trace_steps)
            confidence_factors['model_agreement'] = model_agreement
        else:
            confidence_factors['model_agreement'] = 0.8
        
        # Factor 3: Historical performance
        historical_confidence = self._get_historical_confidence(decision_data)
        confidence_factors['historical_performance'] = historical_confidence
        
        # Factor 4: Model uncertainty
        if model_uncertainty is not None:
            confidence_factors['model_uncertainty'] = 1.0 - model_uncertainty
        else:
            confidence_factors['model_uncertainty'] = 0.7
        
        # Factor 5: Input completeness
        input_completeness = self._assess_input_completeness(decision_data)
        confidence_factors['input_completeness'] = input_completeness
        
        # Calculate overall confidence (weighted average)
        weights = {
            'data_quality': 0.25,
            'model_agreement': 0.20,
            'historical_performance': 0.20,
            'model_uncertainty': 0.20,
            'input_completeness': 0.15
        }
        
        overall_confidence = sum(
            confidence_factors[k] * weights[k]
            for k in confidence_factors.keys()
        )
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(overall_confidence)
        
        result = {
            'overall_confidence': overall_confidence,
            'confidence_level': confidence_level,
            'confidence_factors': confidence_factors,
            'weights': weights,
            'explanation': self._generate_confidence_explanation(
                overall_confidence,
                confidence_factors
            )
        }
        
        self.confidence_history.append(result)
        return result
    
    def _assess_data_quality(self, data: Dict[str, Any]) -> float:
        """Assess quality of input data."""
        if not data:
            return 0.0
        
        quality_score = 0.0
        total_fields = 0
        
        for key, value in data.items():
            total_fields += 1
            
            # Check if value is present and valid
            if value is None:
                continue
            elif isinstance(value, (int, float)):
                if not math.isnan(value) and not math.isinf(value):
                    quality_score += 1.0
            elif isinstance(value, str):
                if value.strip():
                    quality_score += 1.0
            elif isinstance(value, (list, dict)):
                if value:
                    quality_score += 1.0
            else:
                quality_score += 0.5
        
        return quality_score / max(total_fields, 1)
    
    def _calculate_model_agreement(self, trace_steps: List[Any]) -> float:
        """Calculate agreement between model steps."""
        if len(trace_steps) < 2:
            return 1.0
        
        # Extract confidence from steps
        confidences = []
        for step in trace_steps:
            if hasattr(step, 'confidence'):
                confidences.append(step.confidence)
            elif isinstance(step, dict) and 'confidence' in step:
                confidences.append(step['confidence'])
        
        if not confidences:
            return 0.7
        
        # Calculate variance (lower variance = higher agreement)
        if len(confidences) > 1:
            variance = statistics.variance(confidences)
            # Convert variance to agreement score (0-1)
            agreement = 1.0 / (1.0 + variance)
        else:
            agreement = confidences[0]
        
        return agreement
    
    def _get_historical_confidence(self, decision_data: Dict[str, Any]) -> float:
        """Get confidence based on historical performance."""
        if not self.confidence_history:
            return 0.7  # Default for no history
        
        # Use average of recent confidences
        recent = self.confidence_history[-10:]
        avg_confidence = sum(h['overall_confidence'] for h in recent) / len(recent)
        
        return avg_confidence
    
    def _assess_input_completeness(self, data: Dict[str, Any]) -> float:
        """Assess completeness of input data."""
        if not data:
            return 0.0
        
        # Expected fields for disaster decisions
        expected_fields = [
            'disaster_severity', 'infrastructure_health', 'casualties',
            'resources_available', 'time_step'
        ]
        
        present_fields = sum(1 for field in expected_fields if field in data)
        completeness = present_fields / len(expected_fields)
        
        return completeness
    
    def _determine_confidence_level(self, confidence: float) -> str:
        """Determine confidence level category."""
        if confidence >= 0.9:
            return "very_high"
        elif confidence >= 0.75:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        elif confidence >= 0.4:
            return "low"
        else:
            return "very_low"
    
    def _generate_confidence_explanation(
        self,
        overall_confidence: float,
        factors: Dict[str, float]
    ) -> str:
        """Generate natural language explanation for confidence."""
        level = self._determine_confidence_level(overall_confidence)
        
        # Find strongest and weakest factors
        sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
        strongest = sorted_factors[0]
        weakest = sorted_factors[-1]
        
        explanation = f"Confidence is {level} ({overall_confidence:.2f}). "
        explanation += f"Strongest factor: {strongest[0]} ({strongest[1]:.2f}). "
        
        if weakest[1] < 0.5:
            explanation += f"Weakest factor: {weakest[0]} ({weakest[1]:.2f}), which may need attention."
        
        return explanation
    
    def get_confidence_trend(self, last_n: int = 10) -> Dict[str, Any]:
        """Get trend of confidence over recent decisions."""
        if not self.confidence_history:
            return {'status': 'no_data'}
        
        recent = self.confidence_history[-last_n:]
        confidences = [h['overall_confidence'] for h in recent]
        
        if len(confidences) < 2:
            return {'status': 'insufficient_data'}
        
        # Calculate trend
        first_half = confidences[:len(confidences)//2]
        second_half = confidences[len(confidences)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        trend = 'improving' if avg_second > avg_first else 'declining'
        change = ((avg_second - avg_first) / avg_first) * 100
        
        return {
            'status': 'success',
            'trend': trend,
            'change_percent': change,
            'current_avg': avg_second,
            'previous_avg': avg_first,
            'num_decisions': len(recent)
        }
    
    def identify_low_confidence_factors(
        self,
        confidence_result: Dict[str, Any],
        threshold: float = 0.6
    ) -> List[str]:
        """Identify factors contributing to low confidence."""
        factors = confidence_result['confidence_factors']
        
        low_factors = [
            factor for factor, value in factors.items()
            if value < threshold
        ]
        
        return low_factors
    
    def suggest_improvements(
        self,
        confidence_result: Dict[str, Any]
    ) -> List[str]:
        """Suggest improvements to increase confidence."""
        suggestions = []
        factors = confidence_result['confidence_factors']
        
        if factors.get('data_quality', 1.0) < 0.7:
            suggestions.append("Improve data quality by ensuring all required fields are present and valid")
        
        if factors.get('input_completeness', 1.0) < 0.7:
            suggestions.append("Provide more complete input data for better decision-making")
        
        if factors.get('model_agreement', 1.0) < 0.7:
            suggestions.append("Review model consistency - different components may be giving conflicting signals")
        
        if factors.get('historical_performance', 1.0) < 0.6:
            suggestions.append("Historical performance is low - consider retraining or adjusting the model")
        
        if not suggestions:
            suggestions.append("Confidence is good - no immediate improvements needed")
        
        return suggestions
