"""
Benchmarking Framework - Compares performance against benchmarks.
"""

from typing import Dict, Any, List, Optional


class BenchmarkingFramework:
    """Framework for benchmarking disaster response performance."""
    
    def __init__(self):
        self.benchmarks: Dict[str, Dict[str, float]] = {
            'industry_standard': {
                'response_time': 30,
                'casualties_per_1000': 1.0,
                'economic_loss_ratio': 0.05,
                'recovery_time_days': 30
            },
            'best_practice': {
                'response_time': 15,
                'casualties_per_1000': 0.5,
                'economic_loss_ratio': 0.02,
                'recovery_time_days': 15
            }
        }
        self.comparison_results: List[Dict[str, Any]] = []
    
    def compare_to_benchmark(
        self,
        actual_metrics: Dict[str, float],
        benchmark_name: str = 'industry_standard'
    ) -> Dict[str, Any]:
        """Compare actual metrics to benchmark."""
        
        if benchmark_name not in self.benchmarks:
            return {'error': 'Benchmark not found'}
        
        benchmark = self.benchmarks[benchmark_name]
        comparison = {}
        
        for metric, benchmark_value in benchmark.items():
            actual_value = actual_metrics.get(metric, 0)
            
            # Calculate performance ratio
            if benchmark_value != 0:
                ratio = actual_value / benchmark_value
            else:
                ratio = 1.0
            
            # Determine if lower is better
            lower_is_better = metric in ['response_time', 'casualties_per_1000', 'economic_loss_ratio', 'recovery_time_days']
            
            if lower_is_better:
                performance = 'exceeds' if ratio < 1.0 else 'meets' if ratio <= 1.2 else 'below'
            else:
                performance = 'exceeds' if ratio > 1.0 else 'meets' if ratio >= 0.8 else 'below'
            
            comparison[metric] = {
                'actual': actual_value,
                'benchmark': benchmark_value,
                'ratio': ratio,
                'performance': performance
            }
        
        result = {
            'benchmark_name': benchmark_name,
            'comparison': comparison,
            'overall_performance': self._calculate_overall_performance(comparison)
        }
        
        self.comparison_results.append(result)
        return result
    
    def _calculate_overall_performance(self, comparison: Dict) -> str:
        """Calculate overall performance rating."""
        exceeds = sum(1 for v in comparison.values() if v['performance'] == 'exceeds')
        meets = sum(1 for v in comparison.values() if v['performance'] == 'meets')
        total = len(comparison)
        
        score = (exceeds * 2 + meets) / (total * 2)
        
        if score >= 0.8:
            return 'excellent'
        elif score >= 0.6:
            return 'good'
        elif score >= 0.4:
            return 'acceptable'
        else:
            return 'needs_improvement'
    
    def add_benchmark(self, name: str, metrics: Dict[str, float]):
        """Add a custom benchmark."""
        self.benchmarks[name] = metrics
    
    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmarks."""
        return {
            'available_benchmarks': list(self.benchmarks.keys()),
            'total_comparisons': len(self.comparison_results)
        }
