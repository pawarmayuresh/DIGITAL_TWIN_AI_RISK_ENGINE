"""
Batch 10 Demo - Analytics Engine
Demonstrates quantitative performance metrics and analytics.
"""

from .kpi_calculator import KPICalculator
from .economic_loss_estimator import EconomicLossEstimator
from .resilience_index import ResilienceIndex
from .social_stability_index import SocialStabilityIndex
from .simulation_statistics import SimulationStatisticsTracker
from .benchmarking_framework import BenchmarkingFramework
from .resilience_dashboard import ResilienceDashboardMetrics
from .scenario_comparator import ScenarioComparator


def demo_kpi_calculator():
    """Demo: KPI calculation."""
    print("\n=== KPI Calculator Demo ===")
    
    calculator = KPICalculator()
    
    # Sample simulation data
    simulation_data = {
        'casualties': 75,
        'initial_population_at_risk': 1000,
        'response_time': 45,
        'resources_used': 4000,
        'resources_available': 5000,
        'infrastructure_health': 85,
        'population_evacuated': 900,
        'population_at_risk': 1000,
        'economic_loss': 800000
    }
    
    # Calculate KPIs
    kpis = calculator.calculate_kpis(simulation_data)
    
    print(f"Calculated {len(kpis)} KPIs:")
    for name, kpi in list(kpis.items())[:5]:
        print(f"  {name}: {kpi.value:.2f} {kpi.unit} (Status: {kpi.status}, Trend: {kpi.trend})")
    
    # Get summary
    summary = calculator.get_kpi_summary(kpis)
    print(f"\nSummary: {summary['status_counts']}")
    print(f"Critical KPIs: {summary['critical_kpis']}")
    
    return calculator


def demo_economic_loss_estimator():
    """Demo: Economic loss estimation."""
    print("\n=== Economic Loss Estimator Demo ===")
    
    estimator = EconomicLossEstimator()
    
    disaster_data = {
        'severity': 7.5,
        'infrastructure_health': 75,
        'duration_days': 3,
        'affected_area_km2': 50,
        'population_affected': 50000,
        'casualties': 100,
        'injured': 300
    }
    
    city_data = {
        'infrastructure_value': 50000000,
        'daily_business_value': 2000000,
        'property_value_per_km2': 10000000
    }
    
    # Estimate losses
    losses = estimator.estimate_losses(disaster_data, city_data)
    
    print(f"Total Economic Loss: ${losses.total_loss:,.2f}")
    print(f"  Infrastructure Damage: ${losses.infrastructure_damage:,.2f}")
    print(f"  Business Interruption: ${losses.business_interruption:,.2f}")
    print(f"  Property Damage: ${losses.property_damage:,.2f}")
    
    # Get breakdown percentages
    percentages = estimator.get_loss_breakdown_percentages(losses)
    print(f"\nLoss Breakdown:")
    for category, pct in list(percentages.items())[:3]:
        print(f"  {category}: {pct:.1f}%")
    
    return estimator


def demo_resilience_index():
    """Demo: Resilience index calculation."""
    print("\n=== Resilience Index Demo ===")
    
    resilience = ResilienceIndex()
    
    city_data = {
        'infrastructure_health': 85,
        'building_code_compliance': 0.9,
        'backup_systems': 0.7,
        'resource_stockpiles': 0.8,
        'resources_available': 5000
    }
    
    disaster_response = {
        'resources_mobilized': 4000,
        'response_time': 25
    }
    
    # Calculate resilience
    score = resilience.calculate_resilience(city_data, disaster_response)
    
    print(f"Overall Resilience Score: {score.overall_score:.2f}/100")
    print(f"  Robustness: {score.robustness:.2f}")
    print(f"  Redundancy: {score.redundancy:.2f}")
    print(f"  Resourcefulness: {score.resourcefulness:.2f}")
    print(f"  Rapidity: {score.rapidity:.2f}")
    
    category = resilience.get_resilience_category(score.overall_score)
    print(f"\nResilience Category: {category}")
    
    return resilience


def demo_social_stability():
    """Demo: Social stability index."""
    print("\n=== Social Stability Index Demo ===")
    
    stability = SocialStabilityIndex()
    
    population_data = {
        'public_trust_level': 0.75,
        'government_approval': 0.70,
        'community_engagement': 0.65,
        'volunteer_rate': 0.40,
        'gini_coefficient': 0.35,
        'information_reach': 0.85,
        'message_clarity': 0.80
    }
    
    disaster_impact = {
        'resource_distribution_fairness': 0.75
    }
    
    # Calculate stability
    result = stability.calculate_stability(population_data, disaster_impact)
    
    print(f"Overall Stability: {result['overall_stability']:.2f}/100")
    print(f"  Public Trust: {result['public_trust']:.2f}")
    print(f"  Social Cohesion: {result['social_cohesion']:.2f}")
    print(f"  Resource Equity: {result['resource_equity']:.2f}")
    print(f"Stability Level: {result['stability_level']}")
    
    return stability


def demo_simulation_statistics():
    """Demo: Simulation statistics tracking."""
    print("\n=== Simulation Statistics Demo ===")
    
    tracker = SimulationStatisticsTracker()
    
    # Record some simulations
    for i in range(3):
        tracker.record_simulation(
            simulation_id=f"sim_{i}",
            disaster_type='earthquake',
            duration_seconds=120 + i * 10,
            steps=50 + i * 5,
            final_state={'casualties': 100 - i * 10}
        )
    
    # Get statistics
    stats = tracker.get_statistics()
    print(f"Total Simulations: {stats['total_simulations']}")
    print(f"Average Duration: {stats['avg_duration_seconds']:.2f}s")
    print(f"Average Steps: {stats['avg_steps']:.1f}")
    
    # Performance metrics
    perf = tracker.get_performance_metrics()
    print(f"Performance Trend: {perf.get('performance_trend', 'N/A')}")
    
    return tracker


def demo_benchmarking():
    """Demo: Benchmarking framework."""
    print("\n=== Benchmarking Framework Demo ===")
    
    framework = BenchmarkingFramework()
    
    actual_metrics = {
        'response_time': 25,
        'casualties_per_1000': 0.75,
        'economic_loss_ratio': 0.03,
        'recovery_time_days': 20
    }
    
    # Compare to benchmark
    comparison = framework.compare_to_benchmark(actual_metrics, 'industry_standard')
    
    print(f"Benchmark: {comparison['benchmark_name']}")
    print(f"Overall Performance: {comparison['overall_performance']}")
    
    for metric, data in list(comparison['comparison'].items())[:2]:
        print(f"  {metric}: {data['performance']} (actual: {data['actual']}, benchmark: {data['benchmark']})")
    
    return framework


def demo_resilience_dashboard():
    """Demo: Resilience dashboard metrics."""
    print("\n=== Resilience Dashboard Demo ===")
    
    dashboard = ResilienceDashboardMetrics()
    
    # Mock data
    kpis = {'summary': {'critical_kpis': [], 'status_counts': {'good': 8, 'warning': 2}}}
    resilience_score = {'overall_score': 75}
    economic_losses = {'total_loss': 1000000}
    social_stability = {'overall_stability': 70}
    simulation_stats = {'total_simulations': 10}
    
    # Generate dashboard
    dash_data = dashboard.generate_dashboard(
        kpis, resilience_score, economic_losses,
        social_stability, simulation_stats
    )
    
    print(f"Overall Status: {dash_data['summary']['overall_status']}")
    print(f"Key Message: {dash_data['summary']['key_message']}")
    print(f"Alerts: {len(dash_data['alerts'])}")
    print(f"Recommendations: {len(dash_data['recommendations'])}")
    
    return dashboard


def demo_scenario_comparator():
    """Demo: Scenario comparison."""
    print("\n=== Scenario Comparator Demo ===")
    
    comparator = ScenarioComparator()
    
    # Add scenarios
    comparator.add_scenario(
        'scenario_a',
        {'disaster_type': 'earthquake', 'severity': 7.0},
        {'casualties': 100, 'economic_loss': 1000000, 'response_time': 30}
    )
    
    comparator.add_scenario(
        'scenario_b',
        {'disaster_type': 'earthquake', 'severity': 7.5},
        {'casualties': 150, 'economic_loss': 1500000, 'response_time': 25}
    )
    
    # Compare scenarios
    comparison = comparator.compare_scenarios(['scenario_a', 'scenario_b'])
    
    print(f"Best Scenario: {comparison['best_scenario']['scenario_id']}")
    print(f"Worst Scenario: {comparison['worst_scenario']['scenario_id']}")
    print(f"Summary: {comparison['summary']}")
    
    return comparator


def run_all_demos():
    """Run all Batch 10 demos."""
    print("\n" + "="*60)
    print("BATCH 10 - ANALYTICS ENGINE DEMONSTRATIONS")
    print("="*60)
    
    # Run individual demos
    calculator = demo_kpi_calculator()
    estimator = demo_economic_loss_estimator()
    resilience = demo_resilience_index()
    stability = demo_social_stability()
    tracker = demo_simulation_statistics()
    framework = demo_benchmarking()
    dashboard = demo_resilience_dashboard()
    comparator = demo_scenario_comparator()
    
    print("\n" + "="*60)
    print("BATCH 10 COMPLETE - QUANTITATIVE METRICS AVAILABLE")
    print("="*60)
    
    return {
        'kpi_calculator': calculator,
        'economic_estimator': estimator,
        'resilience_index': resilience,
        'social_stability': stability,
        'simulation_tracker': tracker,
        'benchmarking': framework,
        'dashboard': dashboard,
        'scenario_comparator': comparator
    }


if __name__ == "__main__":
    run_all_demos()
