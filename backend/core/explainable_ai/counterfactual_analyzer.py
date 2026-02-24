"""
Counterfactual Analyzer - Generates "what-if" scenarios to explain decisions.
"""

from typing import Dict, Any, List, Optional, Callable
import copy


class CounterfactualAnalyzer:
    """Analyzes counterfactual scenarios to explain decisions."""
    
    def __init__(self):
        self.counterfactuals: List[Dict[str, Any]] = []
    
    def generate_counterfactual(
        self,
        model_fn: Callable,
        original_input: Dict[str, Any],
        original_output: Any,
        target_output: Optional[Any] = None,
        features_to_change: Optional[List[str]] = None,
        max_changes: int = 3
    ) -> Dict[str, Any]:
        """Generate a counterfactual explanation."""
        
        if features_to_change is None:
            features_to_change = list(original_input.keys())
        
        # Try to find minimal changes that lead to different output
        best_counterfactual = None
        min_changes = float('inf')
        
        # Try single feature changes first
        for feature in features_to_change:
            for change_factor in [0.5, 0.8, 1.2, 1.5, 2.0]:
                modified_input = copy.deepcopy(original_input)
                original_value = modified_input[feature]
                
                # Apply change
                if isinstance(original_value, (int, float)):
                    modified_input[feature] = original_value * change_factor
                elif isinstance(original_value, bool):
                    modified_input[feature] = not original_value
                elif isinstance(original_value, str):
                    modified_input[feature] = f"modified_{original_value}"
                else:
                    continue
                
                # Test new output
                new_output = model_fn(modified_input)
                
                # Check if output changed significantly
                if self._outputs_differ(original_output, new_output, target_output):
                    num_changes = 1
                    if num_changes < min_changes:
                        min_changes = num_changes
                        best_counterfactual = {
                            'modified_input': modified_input,
                            'new_output': new_output,
                            'changes': {feature: {
                                'original': original_value,
                                'modified': modified_input[feature],
                                'change_factor': change_factor
                            }},
                            'num_changes': num_changes
                        }
        
        # If no single change works, try combinations
        if best_counterfactual is None and max_changes > 1:
            best_counterfactual = self._try_multiple_changes(
                model_fn,
                original_input,
                original_output,
                target_output,
                features_to_change,
                max_changes
            )
        
        if best_counterfactual is None:
            return {
                'success': False,
                'message': 'Could not find counterfactual with given constraints'
            }
        
        # Generate explanation
        explanation = self._generate_counterfactual_explanation(
            original_input,
            original_output,
            best_counterfactual
        )
        
        result = {
            'success': True,
            'original_input': original_input,
            'original_output': original_output,
            'counterfactual_input': best_counterfactual['modified_input'],
            'counterfactual_output': best_counterfactual['new_output'],
            'changes': best_counterfactual['changes'],
            'num_changes': best_counterfactual['num_changes'],
            'explanation': explanation
        }
        
        self.counterfactuals.append(result)
        return result
    
    def _outputs_differ(
        self,
        output1: Any,
        output2: Any,
        target_output: Optional[Any] = None
    ) -> bool:
        """Check if two outputs differ significantly."""
        if target_output is not None:
            # Check if output2 is closer to target
            return self._distance(output2, target_output) < self._distance(output1, target_output)
        
        # Check if outputs are different
        if isinstance(output1, dict) and isinstance(output2, dict):
            # Compare key values
            for key in output1.keys():
                if key in output2:
                    if abs(self._to_numeric(output1[key]) - self._to_numeric(output2[key])) > 0.1:
                        return True
            return False
        else:
            return abs(self._to_numeric(output1) - self._to_numeric(output2)) > 0.1
    
    def _distance(self, val1: Any, val2: Any) -> float:
        """Calculate distance between two values."""
        return abs(self._to_numeric(val1) - self._to_numeric(val2))
    
    def _to_numeric(self, val: Any) -> float:
        """Convert value to numeric."""
        if isinstance(val, dict):
            # Use first numeric value
            for v in val.values():
                try:
                    return float(v)
                except (TypeError, ValueError):
                    continue
            return 0.0
        try:
            return float(val)
        except (TypeError, ValueError):
            return 0.0
    
    def _try_multiple_changes(
        self,
        model_fn: Callable,
        original_input: Dict[str, Any],
        original_output: Any,
        target_output: Optional[Any],
        features_to_change: List[str],
        max_changes: int
    ) -> Optional[Dict[str, Any]]:
        """Try combinations of multiple feature changes."""
        # Simplified: try pairs of features
        if max_changes < 2 or len(features_to_change) < 2:
            return None
        
        for i, feature1 in enumerate(features_to_change):
            for feature2 in features_to_change[i+1:]:
                modified_input = copy.deepcopy(original_input)
                changes = {}
                
                # Modify both features
                for feature in [feature1, feature2]:
                    original_value = modified_input[feature]
                    if isinstance(original_value, (int, float)):
                        modified_input[feature] = original_value * 1.5
                        changes[feature] = {
                            'original': original_value,
                            'modified': modified_input[feature],
                            'change_factor': 1.5
                        }
                
                if len(changes) == 2:
                    new_output = model_fn(modified_input)
                    if self._outputs_differ(original_output, new_output, target_output):
                        return {
                            'modified_input': modified_input,
                            'new_output': new_output,
                            'changes': changes,
                            'num_changes': 2
                        }
        
        return None
    
    def _generate_counterfactual_explanation(
        self,
        original_input: Dict[str, Any],
        original_output: Any,
        counterfactual: Dict[str, Any]
    ) -> str:
        """Generate natural language explanation for counterfactual."""
        changes = counterfactual['changes']
        
        if len(changes) == 1:
            feature, change_info = list(changes.items())[0]
            return (f"If {feature} were changed from {change_info['original']} "
                   f"to {change_info['modified']}, the outcome would be different.")
        else:
            feature_list = ", ".join(changes.keys())
            return (f"If {feature_list} were changed, the outcome would be different. "
                   f"This shows these features are critical to the decision.")
    
    def explain_decision_boundary(
        self,
        model_fn: Callable,
        input_features: Dict[str, Any],
        feature_name: str,
        num_points: int = 10
    ) -> Dict[str, Any]:
        """Explore how output changes as a feature varies."""
        
        original_value = input_features[feature_name]
        if not isinstance(original_value, (int, float)):
            return {'error': 'Feature must be numeric'}
        
        # Test range of values
        min_val = original_value * 0.5
        max_val = original_value * 2.0
        step = (max_val - min_val) / num_points
        
        test_points = []
        outputs = []
        
        for i in range(num_points + 1):
            test_value = min_val + i * step
            modified_input = copy.deepcopy(input_features)
            modified_input[feature_name] = test_value
            
            output = model_fn(modified_input)
            test_points.append(test_value)
            outputs.append(self._to_numeric(output))
        
        # Find where output changes most
        max_change_idx = 0
        max_change = 0
        for i in range(len(outputs) - 1):
            change = abs(outputs[i+1] - outputs[i])
            if change > max_change:
                max_change = change
                max_change_idx = i
        
        return {
            'feature': feature_name,
            'test_points': test_points,
            'outputs': outputs,
            'decision_boundary': test_points[max_change_idx],
            'explanation': (f"The decision changes most significantly when {feature_name} "
                          f"is around {test_points[max_change_idx]:.2f}")
        }
    
    def get_minimal_changes(
        self,
        counterfactual: Dict[str, Any]
    ) -> List[str]:
        """Get list of minimal changes needed."""
        if not counterfactual.get('success'):
            return []
        
        changes = counterfactual['changes']
        return [f"Change {k} from {v['original']} to {v['modified']}" 
                for k, v in changes.items()]
