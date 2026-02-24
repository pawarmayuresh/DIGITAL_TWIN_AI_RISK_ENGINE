"""
SHAP Explainer - Provides feature importance explanations using SHAP-like values.
"""

from typing import Dict, Any, List, Optional, Callable
import math


class SHAPExplainer:
    """Explains model predictions using SHAP-like feature importance."""
    
    def __init__(self):
        self.baseline_values: Dict[str, Any] = {}
        self.explanations: List[Dict[str, Any]] = []
    
    def set_baseline(self, baseline: Dict[str, Any]):
        """Set baseline values for comparison."""
        self.baseline_values = baseline.copy()
    
    def explain_prediction(
        self,
        model_fn: Callable,
        input_features: Dict[str, Any],
        feature_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Explain a model prediction using SHAP-like values."""
        
        if feature_names is None:
            feature_names = list(input_features.keys())
        
        # Get baseline prediction
        if not self.baseline_values:
            self.baseline_values = {k: 0 for k in feature_names}
        
        baseline_output = model_fn(self.baseline_values)
        actual_output = model_fn(input_features)
        
        # Calculate SHAP values for each feature
        shap_values = {}
        feature_contributions = {}
        
        for feature in feature_names:
            # Create input with feature removed (set to baseline)
            modified_input = input_features.copy()
            modified_input[feature] = self.baseline_values.get(feature, 0)
            
            # Get prediction without this feature
            output_without_feature = model_fn(modified_input)
            
            # SHAP value = difference in output
            shap_value = self._calculate_difference(actual_output, output_without_feature)
            shap_values[feature] = shap_value
            
            # Calculate contribution percentage
            total_diff = self._calculate_difference(actual_output, baseline_output)
            if total_diff != 0:
                contribution = (shap_value / total_diff) * 100
            else:
                contribution = 0
            
            feature_contributions[feature] = contribution
        
        # Sort by absolute SHAP value
        sorted_features = sorted(
            shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        explanation = {
            'input_features': input_features,
            'baseline_output': baseline_output,
            'actual_output': actual_output,
            'shap_values': shap_values,
            'feature_contributions': feature_contributions,
            'top_features': [f[0] for f in sorted_features[:5]],
            'feature_ranking': sorted_features
        }
        
        self.explanations.append(explanation)
        return explanation
    
    def _calculate_difference(self, output1: Any, output2: Any) -> float:
        """Calculate difference between two outputs."""
        if isinstance(output1, dict) and isinstance(output2, dict):
            # For dict outputs, use a key metric
            key = list(output1.keys())[0] if output1 else 'value'
            val1 = output1.get(key, 0)
            val2 = output2.get(key, 0)
            return self._numeric_diff(val1, val2)
        else:
            return self._numeric_diff(output1, output2)
    
    def _numeric_diff(self, val1: Any, val2: Any) -> float:
        """Calculate numeric difference."""
        try:
            return float(val1) - float(val2)
        except (TypeError, ValueError):
            return 0.0
    
    def explain_feature_importance(
        self,
        feature_name: str,
        explanation: Dict[str, Any]
    ) -> str:
        """Generate natural language explanation for a feature."""
        shap_value = explanation['shap_values'].get(feature_name, 0)
        contribution = explanation['feature_contributions'].get(feature_name, 0)
        
        if abs(shap_value) < 0.01:
            return f"{feature_name} has minimal impact on the decision."
        
        direction = "increases" if shap_value > 0 else "decreases"
        magnitude = "significantly" if abs(contribution) > 20 else "moderately" if abs(contribution) > 10 else "slightly"
        
        return f"{feature_name} {magnitude} {direction} the output by {abs(contribution):.1f}%."
    
    def get_top_features_explanation(
        self,
        explanation: Dict[str, Any],
        top_n: int = 3
    ) -> str:
        """Get explanation for top N features."""
        top_features = explanation['top_features'][:top_n]
        
        explanations = []
        for feature in top_features:
            exp = self.explain_feature_importance(feature, explanation)
            explanations.append(exp)
        
        return " ".join(explanations)
    
    def visualize_shap_values(
        self,
        explanation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create visualization data for SHAP values."""
        shap_values = explanation['shap_values']
        
        # Prepare data for bar chart
        features = list(shap_values.keys())
        values = list(shap_values.values())
        
        # Sort by absolute value
        sorted_indices = sorted(
            range(len(values)),
            key=lambda i: abs(values[i]),
            reverse=True
        )
        
        return {
            'chart_type': 'bar',
            'features': [features[i] for i in sorted_indices],
            'shap_values': [values[i] for i in sorted_indices],
            'colors': ['red' if v < 0 else 'green' for v in [values[i] for i in sorted_indices]],
            'title': 'Feature Importance (SHAP Values)'
        }
    
    def compare_predictions(
        self,
        explanation1: Dict[str, Any],
        explanation2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two predictions."""
        
        # Find features with biggest difference
        shap1 = explanation1['shap_values']
        shap2 = explanation2['shap_values']
        
        differences = {}
        for feature in set(shap1.keys()) | set(shap2.keys()):
            val1 = shap1.get(feature, 0)
            val2 = shap2.get(feature, 0)
            differences[feature] = abs(val1 - val2)
        
        sorted_diffs = sorted(differences.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'biggest_differences': sorted_diffs[:5],
            'output_difference': self._calculate_difference(
                explanation1['actual_output'],
                explanation2['actual_output']
            ),
            'explanation': f"The predictions differ mainly due to: {', '.join([d[0] for d in sorted_diffs[:3]])}"
        }
