#!/usr/bin/env python3
"""
Batch 10 Validation Script - Analytics Engine
Validates all analytics components are working correctly.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from core.analytics_engine import (
    KPICalculator,
    EconomicLossEstimator,
    ResilienceIndex,
    SocialStabilityIndex,
    SimulationStatisticsTracker,
    BenchmarkingFramework,
    ResilienceDashboardMetrics,
    ScenarioComparator
)


def validate_kpi_calculator():
    """Validate KPI calculator."""
    print("✓ Testing KPI Calculator...")
    
    calculator = KPICalculator()
    
    simulation_data = {
        'casualties': 50,
        'initial_population_at_risk': 1000,
        'response_time': 30,
        'resources_used': 3000,
        'resources_available': 5000
    }
    
    kpis = calculator.calculate_kpis(simulation_data)
    assert len(kpis) > 0, "No KPIs calculated"
    assert 'casualties' in kpis, "Missing casualties KPI"
    
    summary = calculator.get_kpi_summary(kpis)
    assert 'total_kpis' in summary, "Missing summary"
    
    print("  ✓ KPI calculator validated")
    return True


def validate_economic_loss_estimator():
    """Validate economic loss estimator."""
    print("✓ Testing Economic Loss Estimator...")
    
    estimator = EconomicLossEstimator()
    
    disaster_data = {'severity': 7.0, 'duration_days': 2, 'population_affected': 10000}
    city_data = {'infrastructure_value': 10000000}
    
    losses = estimator.estimate_losses(disaster_data, city_data)
    assert losses.total_loss > 0, "No losses calculated"
    assert hasattr(losses, 'infrastructure_damage'), "Missing infrastructure damage"
    
    print("  ✓ Economic loss estimator validated")
    return True


def validate_resilience_index():
    """Validate resilience index."""
    print("✓ Testing Resilience Index...")
    
    resilience = ResilienceIndex()
    
    city_data = {'infrastructure_health': 80, 'backup_systems': 0.7}
    response_data = {'resources_mobilized': 3000, 'response_time': 30}
    
    score = resilience.calculate_resilience(city_data, response_data)
    assert 0 <= score.overall_score <= 100, "Invalid resilience score"
    assert hasattr(score, 'robustness'), "Missing robustness"
    
    category = resilience.get_resilience_category(score.overall_score)
    assert category in ['highly_resilient', 'resilient', 'moderately_resilient', 'vulnerable'], "Invalid category"
    
    print("  ✓ Resilience index validated")
    return True


def validate_social_stability():
    """Validate social stability index."""
    print("✓ Testing Social Stability Index...")
    
    stability = SocialStabilityIndex()
    
    pop_data = {'public_trust_level': 0.7, 'community_engagement': 0.6}
    impact_data = {'resource_distribution_fairness': 0.8}
    
    result = stability.calculate_stability(pop_data, impact_data)
    assert 'overall_stability' in result, "Missing overall stability"
    assert 0 <= result['overall_stability'] <= 100, "Invalid stability score"
    
    print("  ✓ Social stability index validated")
    return True


def validate_simulation_statistics():
    """Validate simulation statistics tracker."""
    print("✓ Testing Simulation Statistics Tracker...")
    
    tracker = SimulationStatisticsTracker()
    
    tracker.record_simulation('sim_1', 'earthquake', 120.0, 50, {})
    tracker.record_simulation('sim_2', 'flood', 130.0, 55, {})
    
    stats = tracker.get_statistics()
    assert stats['total_simulations'] == 2, "Incorrect simulation count"
    assert 'avg_duration_seconds' in stats, "Missing average duration"
    
    print("  ✓ Simulation statistics tracker validated")
    return True


def validate_benchmarking():
    """Validate benchmarking framework."""
    print("✓ Testing Benchmarking Framework...")
    
    framework = BenchmarkingFramework()
    
    metrics = {'response_time': 25, 'casualties_per_1000': 0.8}
    comparison = framework.compare_to_benchmark(metrics)
    
    assert 'comparison' in comparison, "Missing comparison"
    assert 'overall_performance' in comparison, "Missing overall performance"
    
    print("  ✓ Benchmarking framework validated")
    return True


def validate_resilience_dashboard():
    """Validate resilience dashboard metrics."""
    print("✓ Testing Resilience Dashboard Metrics...")
    
    dashboard = ResilienceDashboardMetrics()
    
    kpis = {'summary': {'critical_kpis': []}}
    resilience = {'overall_score': 75}
    economic = {'total_loss': 1000000}
    social = {'overall_stability': 70}
    sim_stats = {'total_simulations': 5}
    
    dash_data = dashboard.generate_dashboard(kpis, resilience, economic, social, sim_stats)
    
    assert 'summary' in dash_data, "Missing summary"
    assert 'alerts' in dash_data, "Missing alerts"
    assert 'recommendations' in dash_data, "Missing recommendations"
    
    print("  ✓ Resilience dashboard metrics validated")
    return True


def validate_scenario_comparator():
    """Validate scenario comparator."""
    print("✓ Testing Scenario Comparator...")
    
    comparator = ScenarioComparator()
    
    comparator.add_scenario('s1', {}, {'casualties': 100, 'economic_loss': 1000000})
    comparator.add_scenario('s2', {}, {'casualties': 150, 'economic_loss': 1500000})
    
    comparison = comparator.compare_scenarios(['s1', 's2'])
    
    assert 'best_scenario' in comparison, "Missing best scenario"
    assert 'worst_scenario' in comparison, "Missing worst scenario"
    assert 'summary' in comparison, "Missing summary"
    
    print("  ✓ Scenario comparator validated")
    return True


def run_all_validations():
    """Run all validation tests."""
    print("\n" + "="*60)
    print("BATCH 10 VALIDATION - ANALYTICS ENGINE")
    print("="*60 + "\n")
    
    tests = [
        ("KPI Calculator", validate_kpi_calculator),
        ("Economic Loss Estimator", validate_economic_loss_estimator),
        ("Resilience Index", validate_resilience_index),
        ("Social Stability Index", validate_social_stability),
        ("Simulation Statistics", validate_simulation_statistics),
        ("Benchmarking Framework", validate_benchmarking),
        ("Resilience Dashboard", validate_resilience_dashboard),
        ("Scenario Comparator", validate_scenario_comparator)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ✗ {test_name} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"VALIDATION COMPLETE: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_validations()
    sys.exit(0 if success else 1)
