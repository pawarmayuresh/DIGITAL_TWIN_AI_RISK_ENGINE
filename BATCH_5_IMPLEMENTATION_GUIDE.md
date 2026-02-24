# 🟦 BATCH 5 - DIGITAL TWIN CORE Implementation Guide

**Status:** Ready to Start  
**Prerequisites:** Batches 1-4 Completed ✅  
**Estimated Time:** 2-3 weeks  
**Complexity:** High

---

## 🎯 BATCH 5 GOAL

Create a realistic city modeling system with population dynamics, economic activity, and critical asset management that integrates with the existing grid, disaster, and cascading failure systems.

**Expected Outcome:** City behaves like a dynamic system with realistic population and economic responses to disasters.

---

## 📋 IMPLEMENTATION CHECKLIST

### Phase 1: Core Models (Week 1)

#### 1.1 City Model (`backend/core/digital_twin/city_model.py`)

**Purpose:** Top-level city state and behavior

**Key Components:**
```python
class CityModel:
    - city_id: str
    - name: str
    - total_population: int
    - total_area_km2: float
    - gdp: float
    - baseline_state: Dict
    - current_state: Dict
    - critical_assets: List[CriticalAsset]
    - infrastructure_graph: InfrastructureGraph
    - grid_manager: GridManager
    
    Methods:
    - initialize_baseline()
    - update_state(time_step)
    - calculate_city_metrics()
    - get_resilience_score()
    - export_state()
```

**Integration Points:**
- Links to GridManager (Batch 2)
- Links to InfrastructureGraph (Batch 4)
- Provides city-level metrics for analytics

---

#### 1.2 Population Model (`backend/core/digital_twin/population_model.py`)

**Purpose:** Demographics, movement, and behavior simulation

**Key Components:**
```python
class PopulationModel:
    - total_population: int
    - demographics: Dict[str, int]  # age groups
    - population_by_zone: Dict[str, int]
    - vulnerability_factors: Dict[str, float]
    - evacuation_capacity: float
    
    Methods:
    - initialize_population(grid_manager)
    - distribute_population_to_cells()
    - calculate_evacuation_demand()
    - update_population_status(disaster_impacts)
    - get_casualties_estimate()
    - get_displaced_population()
```

**Demographics Structure:**
```python
{
    "children": 15000,      # 0-17 years
    "adults": 50000,        # 18-64 years
    "elderly": 10000,       # 65+ years
    "vulnerable": 5000      # disabled, chronic illness
}
```

**Integration Points:**
- Reads from GridManager cell population
- Updates based on DisasterManager impacts
- Provides data for SpatialImpactCalculator

---

#### 1.3 Economic Model (`backend/core/digital_twin/economic_model.py`)

**Purpose:** Economic activity and impact calculation

**Key Components:**
```python
class EconomicModel:
    - gdp: float
    - sectors: Dict[str, EconomicSector]
    - employment_rate: float
    - business_continuity_index: float
    
class EconomicSector:
    - name: str  # retail, manufacturing, services, etc.
    - gdp_contribution: float
    - employment: int
    - infrastructure_dependencies: List[str]
    - disruption_tolerance: float
    
    Methods:
    - calculate_economic_loss(infrastructure_status)
    - estimate_recovery_time()
    - calculate_business_disruption()
```

**Sectors to Model:**
- Retail & Commerce
- Manufacturing
- Services (healthcare, education)
- Technology
- Tourism
- Government

**Integration Points:**
- Depends on InfrastructureGraph status
- Provides loss estimates for analytics
- Influences recovery prioritization

---

### Phase 2: Asset Management (Week 1-2)

#### 2.1 Critical Asset Registry (`backend/core/digital_twin/critical_asset_registry.py`)

**Purpose:** Track hospitals, schools, utilities, emergency services

**Key Components:**
```python
class AssetType(Enum):
    HOSPITAL = "hospital"
    SCHOOL = "school"
    FIRE_STATION = "fire_station"
    POLICE_STATION = "police_station"
    WATER_TREATMENT = "water_treatment"
    POWER_PLANT = "power_plant"
    SHELTER = "shelter"
    FOOD_DISTRIBUTION = "food_distribution"

class CriticalAsset:
    - asset_id: str
    - asset_type: AssetType
    - name: str
    - location: Tuple[int, int]  # grid coordinates
    - capacity: int
    - operational_status: float  # 0.0 to 1.0
    - dependencies: List[str]  # infrastructure node IDs
    - service_radius_km: float
    
class CriticalAssetRegistry:
    - assets: Dict[str, CriticalAsset]
    
    Methods:
    - register_asset(asset)
    - get_assets_by_type(asset_type)
    - get_assets_in_radius(location, radius)
    - update_asset_status(infrastructure_graph)
    - calculate_service_coverage(grid_manager)
```

**Asset Examples:**
```python
# Hospital
{
    "asset_id": "hospital_001",
    "asset_type": "HOSPITAL",
    "name": "Central Hospital",
    "location": (10, 15),
    "capacity": 500,  # beds
    "operational_status": 1.0,
    "dependencies": ["power_node_1", "water_node_2"],
    "service_radius_km": 5.0
}

# Fire Station
{
    "asset_id": "fire_001",
    "asset_type": "FIRE_STATION",
    "name": "Fire Station #1",
    "location": (5, 8),
    "capacity": 20,  # firefighters
    "operational_status": 1.0,
    "dependencies": ["power_node_3", "telecom_node_1"],
    "service_radius_km": 3.0
}
```

**Integration Points:**
- Maps to GridManager cells
- Depends on InfrastructureGraph nodes
- Provides service coverage metrics

---

#### 2.2 Baseline State Manager (`backend/core/digital_twin/baseline_state_manager.py`)

**Purpose:** Save and compare pre/post-disaster states

**Key Components:**
```python
class BaselineStateManager:
    - baseline_snapshot: Dict
    - comparison_metrics: Dict
    
    Methods:
    - capture_baseline(city_model)
    - save_baseline(file_path)
    - load_baseline(file_path)
    - compare_to_baseline(current_state)
    - calculate_deviation_metrics()
    - generate_impact_report()
```

**Baseline Snapshot Structure:**
```python
{
    "timestamp": "2026-02-18T10:00:00Z",
    "city_metrics": {
        "population": 75000,
        "gdp": 5000000000,
        "employment_rate": 0.95
    },
    "infrastructure": {
        "power_grid_health": 1.0,
        "water_system_health": 1.0,
        "telecom_health": 1.0
    },
    "critical_assets": {
        "hospitals_operational": 5,
        "schools_operational": 20,
        "fire_stations_operational": 8
    },
    "grid_state": {
        "total_cells": 400,
        "cells_at_risk": 0
    }
}
```

---

### Phase 3: Integration & Orchestration (Week 2)

#### 3.1 Twin Manager (`backend/core/digital_twin/twin_manager.py`)

**Purpose:** Orchestrate all digital twin components

**Key Components:**
```python
class TwinManager:
    - city_model: CityModel
    - population_model: PopulationModel
    - economic_model: EconomicModel
    - asset_registry: CriticalAssetRegistry
    - baseline_manager: BaselineStateManager
    - grid_manager: GridManager
    - disaster_manager: DisasterManager
    - cascade_engine: CascadingFailureEngine
    
    Methods:
    - initialize_twin(config)
    - run_simulation_step(time_step)
    - apply_disaster_impacts()
    - update_all_models()
    - get_twin_status()
    - export_twin_state()
    - reset_to_baseline()
```

**Simulation Loop:**
```python
def run_simulation_step(self, time_step: int):
    # 1. Propagate disasters
    self.disaster_manager.propagate_all(self.grid_manager, None)
    
    # 2. Calculate infrastructure cascades
    self.cascade_engine.propagate_failures(...)
    
    # 3. Update critical asset status
    self.asset_registry.update_asset_status(self.infrastructure_graph)
    
    # 4. Update population impacts
    self.population_model.update_population_status(disaster_impacts)
    
    # 5. Calculate economic impacts
    economic_loss = self.economic_model.calculate_economic_loss(
        self.infrastructure_graph.get_status()
    )
    
    # 6. Update city state
    self.city_model.update_state(time_step)
    
    return self.get_twin_status()
```

---

### Phase 4: API Integration (Week 2-3)

#### 4.1 Create API Routes (`backend/api/twin_routes.py`)

```python
from fastapi import APIRouter, HTTPException
from ..core.digital_twin import TwinManager

router = APIRouter()

@router.post("/twin/initialize")
async def initialize_twin(config: TwinConfig):
    """Initialize a new digital twin"""
    pass

@router.get("/twin/{twin_id}/status")
async def get_twin_status(twin_id: str):
    """Get current twin state"""
    pass

@router.get("/twin/{twin_id}/population")
async def get_population_status(twin_id: str):
    """Get population metrics"""
    pass

@router.get("/twin/{twin_id}/economy")
async def get_economic_status(twin_id: str):
    """Get economic metrics"""
    pass

@router.get("/twin/{twin_id}/assets")
async def get_critical_assets(twin_id: str):
    """Get critical asset status"""
    pass

@router.post("/twin/{twin_id}/simulate")
async def run_simulation(twin_id: str, steps: int):
    """Run simulation for N steps"""
    pass

@router.get("/twin/{twin_id}/baseline/compare")
async def compare_to_baseline(twin_id: str):
    """Compare current state to baseline"""
    pass
```

---

## 🧪 VALIDATION STRATEGY

### Test 1: City Model Initialization
```python
# Create city
city = CityModel(
    city_id="test_city_001",
    name="Test City",
    total_population=75000,
    total_area_km2=100.0,
    gdp=5_000_000_000
)

# Verify
assert city.total_population == 75000
assert city.name == "Test City"
```

### Test 2: Population Distribution
```python
# Initialize population model
pop_model = PopulationModel(total_population=75000)
pop_model.distribute_population_to_cells(grid_manager)

# Verify
total_distributed = sum(
    cell.metadata.population_density 
    for cell in grid_manager.cells.values()
)
assert total_distributed > 0
```

### Test 3: Economic Impact Calculation
```python
# Create economic model
econ_model = EconomicModel(gdp=5_000_000_000)

# Simulate infrastructure damage
infrastructure_status = {
    "power": 0.5,  # 50% operational
    "water": 0.7,
    "telecom": 0.8
}

# Calculate loss
loss = econ_model.calculate_economic_loss(infrastructure_status)
assert loss > 0
```

### Test 4: Critical Asset Mapping
```python
# Register assets
registry = CriticalAssetRegistry()
hospital = CriticalAsset(
    asset_id="hospital_001",
    asset_type=AssetType.HOSPITAL,
    location=(10, 10),
    capacity=500
)
registry.register_asset(hospital)

# Verify
assets = registry.get_assets_by_type(AssetType.HOSPITAL)
assert len(assets) == 1
```

### Test 5: Baseline Comparison
```python
# Capture baseline
baseline_mgr = BaselineStateManager()
baseline_mgr.capture_baseline(city_model)

# Simulate disaster
# ... run disaster scenario ...

# Compare
deviation = baseline_mgr.compare_to_baseline(city_model.current_state)
assert deviation["population_affected"] > 0
```

### Test 6: Full Integration
```python
# Initialize twin manager
twin_mgr = TwinManager()
twin_mgr.initialize_twin(config)

# Run simulation
for step in range(30):
    status = twin_mgr.run_simulation_step(step)
    print(f"Step {step}: {status}")

# Verify
assert twin_mgr.city_model.current_state != twin_mgr.baseline_manager.baseline_snapshot
```

---

## 📊 APPROVAL CRITERIA

Before marking Batch 5 as complete, verify:

- [ ] City model tracks population, GDP, and area
- [ ] Population model distributes across grid cells
- [ ] Population responds to disaster impacts
- [ ] Economic model calculates sector-based losses
- [ ] Economic impacts reflect infrastructure status
- [ ] Critical asset registry manages all asset types
- [ ] Assets map to grid coordinates
- [ ] Asset status updates based on infrastructure
- [ ] Baseline manager captures snapshots
- [ ] Baseline comparison generates deviation metrics
- [ ] Twin manager orchestrates all components
- [ ] Simulation loop integrates all systems
- [ ] API endpoints expose twin data
- [ ] All validation tests pass
- [ ] Demo scenario runs end-to-end

---

## 🚀 GETTING STARTED

### Step 1: Create Directory Structure
```bash
mkdir -p backend/core/digital_twin
touch backend/core/digital_twin/__init__.py
```

### Step 2: Start with City Model
```bash
# Create the file
touch backend/core/digital_twin/city_model.py

# Implement basic structure
# See implementation template above
```

### Step 3: Add Population Model
```bash
touch backend/core/digital_twin/population_model.py
```

### Step 4: Continue with remaining components...

---

## 💡 IMPLEMENTATION TIPS

1. **Start Simple:** Begin with basic data structures, add complexity later
2. **Test Early:** Write validation tests as you build each component
3. **Integrate Incrementally:** Connect one component at a time to existing systems
4. **Use Type Hints:** Maintain type safety throughout
5. **Document Assumptions:** City modeling involves many assumptions - document them
6. **Reuse Existing Code:** Leverage GridManager, InfrastructureGraph patterns

---

## 🔗 DEPENDENCIES

**Batch 5 depends on:**
- ✅ Batch 2: GridManager for spatial mapping
- ✅ Batch 3: DisasterManager for impact data
- ✅ Batch 4: InfrastructureGraph for dependencies

**Batch 5 enables:**
- Batch 6: Strategic AI (needs city state for planning)
- Batch 7: Multi-Agent System (agents represent city stakeholders)
- Batch 10: Analytics (needs city metrics)

---

## 📝 NEXT STEPS AFTER BATCH 5

Once Batch 5 is complete and validated:

1. **Update API documentation** with new twin endpoints
2. **Create demo scenarios** showing city response to disasters
3. **Validate integration** with existing batches
4. **Get stakeholder approval** using validation checklist
5. **Proceed to Batch 6** (Strategic AI & Planning)

---

**Ready to start? Let's build the Digital Twin Core! 🏙️**
