"""
Scenario Comparator - Compares different disaster scenarios.
"""

from typing import Dict, Any, List, Optional
import statistics


class ScenarioComparator:
    """Compares and analyzes different disaster scenarios."""
    
    def __init__(self):
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        self.comparisons: List[Dict[str, Any]] = []
    
    def add_scenario(
        self,
        scenario_id: str,
        scenario_data: Dict[str, Any],
        results: Dict[str, Any]
    ):
        """Add a scenario for comparison."""
        self.scenarios[scenario_id] = {
            'data': scenario_data,
            'results': results,
            'metrics': self._extract_metrics(results)
        }
    
    def compare_scenarios(
        self,
        scenario_ids: List[str],
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Compare multiple scenarios."""
        
        if not all(sid in self.scenarios for sid in scenario_ids):
            return {'error': 'One or more scenarios not found'}
        
        scenarios = [self.scenarios[sid] for sid in scenario_ids]
        
        if metrics is None:
            metrics = ['casualties', 'economic_loss', 'response_time', 'infrastructure_health']
        
        comparison = {
            'scenario_ids': scenario_ids,
            'metric_comparison': {},
            'best_scenario': {},
            'worst_scenario': {},
            'summary': {}
        }
        
        # Compare each metric
        for metric in metrics:
            values = []
            for scenario in scenarios:
                value = scenario['metrics'].get(metric, 0)
                values.append(value)
            
            # Determine best/worst (lower is better for most metrics)
            lower_is_better = metric in ['casualties', 'economic_loss', 'response_time']
            
            best_idx = values.index(min(values)) if lower_is_better else values.index(max(values))
            worst_idx = values.index(max(values)) if lower_is_better else values.index(min(values))
            
            comparison['metric_comparison'][metric] = {
                'values': dict(zip(scenario_ids, values)),
                'best_scenario': scenario_ids[best_idx],
                'worst_scenario': scenario_ids[worst_idx],
                'range': max(values) - min(values),
                'avg': statistics.mean(values)
            }
        
        # Overall best/worst
        comparison['best_scenario'] = self._determine_best_scenario(scenarios, scenario_ids)
        comparison['worst_scenario'] = self._determine_worst_scenario(scenarios, scenario_ids)
        
        # Summary
        comparison['summary'] = self._generate_comparison_summary(comparison)
        
        self.comparisons.append(comparison)
        return comparison
    
    def _extract_metrics(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Extract key metrics from results."""
        return {
            'casualties': results.get('casualties', 0),
            'economic_loss': results.get('economic_loss', 0),
            'response_time': results.get('response_time', 0),
            'infrastructure_health': results.get('infrastructure_health', 100),
            'population_evacuated': results.get('population_evacuated', 0),
            'resources_used': results.get('resources_used', 0)
        }
    
    def _determine_best_scenario(
        self,
        scenarios: List[Dict],
        scenario_ids: List[str]
    ) -> Dict[str, Any]:
        """Determine overall best scenario."""
        scores = []
        
        for scenario in scenarios:
            metrics = scenario['metrics']
            # Simple scoring: lower casualties and losses = better
            score = (
                -metrics.get('casualties', 0) * 10 +
                -metrics.get('economic_loss', 0) / 1000000 +
                metrics.get('infrastructure_health', 0) +
                -metrics.get('response_time', 0)
            )
            scores.append(score)
        
        best_idx = scores.index(max(scores))
        return {
            'scenario_id': scenario_ids[best_idx],
            'score': scores[best_idx]
        }
    
    def _determine_worst_scenario(
        self,
        scenarios: List[Dict],
        scenario_ids: List[str]
    ) -> Dict[str, Any]:
        """Determine overall worst scenario."""
        scores = []
        
        for scenario in scenarios:
            metrics = scenario['metrics']
            score = (
                -metrics.get('casualties', 0) * 10 +
                -metrics.get('economic_loss', 0) / 1000000 +
                metrics.get('infrastructure_health', 0) +
                -metrics.get('response_time', 0)
            )
            scores.append(score)
        
        worst_idx = scores.index(min(scores))
        return {
            'scenario_id': scenario_ids[worst_idx],
            'score': scores[worst_idx]
        }
    
    def _generate_comparison_summary(self, comparison: Dict) -> str:
        """Generate natural language summary of comparison."""
        best = comparison['best_scenario']['scenario_id']
        worst = comparison['worst_scenario']['scenario_id']
        
        return f"Scenario {best} performed best overall, while {worst} had the poorest outcomes."
    
    def get_scenario_ranking(self, metric: str) -> List[Dict[str, Any]]:
        """Get scenarios ranked by a specific metric."""
        ranked = []
        
        for scenario_id, scenario in self.scenarios.items():
            value = scenario['metrics'].get(metric, 0)
            ranked.append({
                'scenario_id': scenario_id,
                'value': value
            })
        
        # Sort (lower is better for most metrics)
        lower_is_better = metric in ['casualties', 'economic_loss', 'response_time']
        ranked.sort(key=lambda x: x['value'], reverse=not lower_is_better)
        
        return ranked
    
    def analyze_sensitivity(
        self,
        base_scenario_id: str,
        parameter: str,
        variations: List[float]
    ) -> Dict[str, Any]:
        """Analyze sensitivity to parameter changes."""
        if base_scenario_id not in self.scenarios:
            return {'error': 'Base scenario not found'}
        
        base_scenario = self.scenarios[base_scenario_id]
        
        # This would require running simulations with variations
        # For now, return structure
        return {
            'base_scenario': base_scenario_id,
            'parameter': parameter,
            'variations': variations,
            'results': []  # Would contain results for each variation
        }
