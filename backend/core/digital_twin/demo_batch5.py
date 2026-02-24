"""
Batch 5 Demo - Digital Twin Core

Demonstrates the complete digital twin functionality including:
- City modeling
- Population dynamics
- Economic impacts
- Critical asset management
- Baseline comparison
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.digital_twin import (
    TwinManager,
    CityModel,
    PopulationModel,
    EconomicModel,
    CriticalAssetRegistry,
    BaselineStateManager
)
from core.spatial_engine import GridManager, CellMetadata, ZoningEngine
from core.cascading_engine import InfrastructureGraph, InfrastructureNode, InfrastructureNodeType
from core.disaster_engine import DisasterManager, DisasterEvent, DisasterType


def demo_1_city_model():
    """Demo 1: Basic city model initialization"""
    print("\n" + "="*60)
    print("DEMO 1: City Model Initialization")
    print("="*60)
    
    # Create a simple city
    city = CityModel(
        city_id="city_001",
        name="Demo City",
        total_population=75000,
        total_area_km2=100.0,
        gdp=5_000_000_000
    )
    
    print(f"\n✓ City created: {city.name}")
    print(f"  Population: {city.total_population:,}")
    print(f"  Area: {city.total_area_km2} km²")
    print(f"  GDP: ${city.gdp:,.0f}")
    
    # Calculate metrics
    metrics = city.calculate_city_metrics()
    print(f"\n📊 City Metrics:")
    print(f"  Infrastructure Health: {metrics.infrastructure_health * 100:.1f}%")
    print(f"  Resilience Score: {metrics.resilience_score:.3f}")
    print(f"  Employment Rate: {metrics.employment_rate * 100:.1f}%")
    
    # Get status summary
    status = city.get_status_summary()
    print(f"\n📋 Status Summary:")
    for key, value in status.items():
        print(f"  {key}: {value}")


def demo_2_population_model():
    """Demo 2: Population model with demographics"""
    print("\n" + "="*60)
    print("DEMO 2: Population Model")
    print("="*60)
    
    # Create population model
    pop_model = PopulationModel(total_population=75000)
    
    print(f"\n✓ Population model created")
    print(f"  Total Population: {pop_model.total_population:,}")
    
    # Show demographics
    demo = pop_model.demographics
    print(f"\n👥 Demographics:")
    print(f"  Children (0-17): {demo.children:,} ({demo.children/demo.total*100:.1f}%)")
    print(f"  Adults (18-64): {demo.adults:,} ({demo.adults/demo.total*100:.1f}%)")
    print(f"  Elderly (65+): {demo.elderly:,} ({demo.elderly/demo.total*100:.1f}%)")
    print(f"  Vulnerable: {demo.vulnerable:,} ({demo.vulnerable/demo.total*100:.1f}%)")
    
    # Calculate vulnerability
    vuln = pop_model.get_population_vulnerability()
    print(f"\n⚠️  Vulnerability Analysis:")
    print(f"  At-Risk Population: {vuln['at_risk_population']:,}")
    print(f"  Vulnerability Index: {vuln['vulnerability_index']:.3f}")
    
    # Simulate disaster impact
    disaster_impacts = {
        "total_cells_affected": 50,
        "population_affected": 15000,
        "average_severity": 0.6
    }
    pop_model.update_population_status(disaster_impacts)
    
    print(f"\n💥 After Disaster Impact:")
    print(f"  Casualties: {pop_model.casualties:,}")
    print(f"  Displaced: {pop_model.displaced:,}")
    
    # Evacuation demand
    evac = pop_model.calculate_evacuation_demand()
    print(f"\n🚨 Evacuation Analysis:")
    print(f"  Evacuation Needed: {evac['evacuation_needed']:,}")
    print(f"  Evacuation Capacity: {evac['evacuation_capacity']:,}")
    print(f"  Can Evacuate All: {evac['can_evacuate_all']}")


def demo_3_economic_model():
    """Demo 3: Economic model with sectors"""
    print("\n" + "="*60)
    print("DEMO 3: Economic Model")
    print("="*60)
    
    # Create economic model
    econ_model = EconomicModel(gdp=5_000_000_000, total_employment=45000)
    
    print(f"\n✓ Economic model created")
    print(f"  GDP: ${econ_model.gdp:,.0f}")
    print(f"  Total Employment: {econ_model.total_employment:,}")
    
    # Show sectors
    print(f"\n🏭 Economic Sectors:")
    for sector_id, sector in econ_model.sectors.items():
        print(f"  {sector.name}:")
        print(f"    GDP Contribution: ${sector.gdp_contribution:,.0f}")
        print(f"    Employment: {sector.employment:,}")
        print(f"    Disruption Tolerance: {sector.disruption_tolerance:.2f}")
    
    # Simulate infrastructure damage
    infrastructure_status = {
        "power": 0.6,  # 60% operational
        "water": 0.8,
        "telecom": 0.7,
        "transport": 0.5
    }
    
    loss = econ_model.calculate_economic_loss(infrastructure_status)
    
    print(f"\n💰 Economic Impact Analysis:")
    print(f"  Daily Economic Loss: ${loss:,.2f}")
    print(f"  Total Economic Loss: ${econ_model.total_economic_loss:,.2f}")
    print(f"  Business Continuity Index: {econ_model.business_continuity_index:.3f}")
    
    # Recovery estimate
    recovery = econ_model.estimate_recovery_time(infrastructure_status)
    print(f"\n🔄 Recovery Estimate:")
    print(f"  Estimated Recovery Days: {recovery['estimated_recovery_days']}")
    print(f"  Emergency Phase: {recovery['emergency_phase_days']} days")
    print(f"  Restoration Phase: {recovery['restoration_phase_days']} days")


def demo_4_critical_assets():
    """Demo 4: Critical asset registry"""
    print("\n" + "="*60)
    print("DEMO 4: Critical Asset Registry")
    print("="*60)
    
    # Create asset registry
    registry = CriticalAssetRegistry()
    
    # Initialize default assets
    registry.initialize_default_assets(grid_width=20, grid_height=20)
    
    print(f"\n✓ Asset registry created")
    print(f"  Total Assets: {len(registry.assets)}")
    
    # Show operational summary
    summary = registry.get_operational_summary()
    print(f"\n🏥 Asset Summary:")
    print(f"  Total Assets: {summary['total_assets']}")
    print(f"  Operational: {summary['operational_assets']}")
    
    print(f"\n📊 Assets by Type:")
    for asset_type, data in summary['by_type'].items():
        print(f"  {asset_type}:")
        print(f"    Total: {data['total']}")
        print(f"    Operational: {data['operational']} ({data['operational_percentage']:.1f}%)")


def demo_5_baseline_comparison():
    """Demo 5: Baseline state management"""
    print("\n" + "="*60)
    print("DEMO 5: Baseline State Management")
    print("="*60)
    
    # Create models
    city = CityModel(
        city_id="city_001",
        name="Demo City",
        total_population=75000,
        total_area_km2=100.0,
        gdp=5_000_000_000
    )
    
    pop_model = PopulationModel(total_population=75000)
    econ_model = EconomicModel(gdp=5_000_000_000)
    
    # Create baseline manager
    baseline_mgr = BaselineStateManager()
    
    # Capture baseline
    baseline = baseline_mgr.capture_baseline(city, pop_model, econ_model)
    
    print(f"\n✓ Baseline captured")
    print(f"  Timestamp: {baseline['timestamp']}")
    print(f"  Population: {baseline['city_metrics']['population']:,}")
    print(f"  GDP: ${baseline['city_metrics']['gdp']:,.0f}")
    
    # Simulate disaster impact
    pop_model.casualties = 500
    pop_model.displaced = 5000
    econ_model.total_economic_loss = 50_000_000
    
    # Capture current state
    current = baseline_mgr.capture_baseline(city, pop_model, econ_model)
    
    # Compare
    comparison = baseline_mgr.compare_to_baseline(current)
    
    print(f"\n📊 Baseline Comparison:")
    print(f"  Population Impact:")
    print(f"    Casualties: {comparison['population_impact']['casualties']}")
    print(f"    Displaced: {comparison['population_impact']['displaced']}")
    print(f"  Economic Impact:")
    print(f"    Economic Loss: ${comparison['economic_impact']['economic_loss']:,.0f}")
    
    # Generate impact report
    report = baseline_mgr.generate_impact_report()
    print(f"\n📋 Impact Report:")
    print(f"  Overall Severity: {report['overall_severity']:.3f}")
    print(f"  Severity Level: {report['severity_level']}")


def demo_6_full_twin_integration():
    """Demo 6: Complete twin manager integration"""
    print("\n" + "="*60)
    print("DEMO 6: Full Twin Manager Integration")
    print("="*60)
    
    # Create twin manager
    twin_mgr = TwinManager()
    
    # Create grid
    grid = GridManager(width=20, height=20, cell_size=1.0)
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    
    # Create infrastructure
    infra_graph = InfrastructureGraph()
    for i in range(5):
        infra_graph.add_node(
            node_id=f"power_node_{i+1}",
            node_type=InfrastructureNodeType.POWER_PLANT,
            location=(i * 4, 10),
            capacity=1000.0
        )
    
    # Initialize twin
    result = twin_mgr.initialize_twin(
        city_id="demo_city_001",
        city_name="Demo City",
        total_population=75000,
        total_area_km2=100.0,
        gdp=5_000_000_000,
        grid_manager=grid,
        infrastructure_graph=infra_graph
    )
    
    print(f"\n✓ Twin initialized")
    print(f"  City: {result['city_name']}")
    print(f"  Population: {result['population']:,}")
    print(f"  Critical Assets: {result['critical_assets']}")
    print(f"  Grid Size: {result['grid_size']}")
    
    # Run simulation steps
    print(f"\n🔄 Running simulation...")
    for step in range(5):
        status = twin_mgr.run_simulation_step()
        print(f"  Step {step + 1}: Time step {status['time_step']}")
    
    # Get final status
    final_status = twin_mgr.get_twin_status()
    print(f"\n📊 Final Status:")
    print(f"  Time Step: {final_status['time_step']}")
    print(f"  City Resilience: {final_status['city']['resilience_score']}")
    print(f"  Infrastructure Health: {final_status['city']['infrastructure_health']}")
    
    # Get resilience metrics
    resilience = twin_mgr.get_resilience_metrics()
    print(f"\n🛡️  Resilience Metrics:")
    for key, value in resilience.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("BATCH 5 - DIGITAL TWIN CORE DEMONSTRATIONS")
    print("="*60)
    
    try:
        demo_1_city_model()
        demo_2_population_model()
        demo_3_economic_model()
        demo_4_critical_assets()
        demo_5_baseline_comparison()
        demo_6_full_twin_integration()
        
        print("\n" + "="*60)
        print("✅ ALL BATCH 5 DEMOS COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
