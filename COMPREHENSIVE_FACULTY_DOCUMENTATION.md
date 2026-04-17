# COMPREHENSIVE SYSTEM DOCUMENTATION
## AI Strategic Risk Engine - Mumbai Digital Twin

**Prepared for Faculty Presentation**  
**Date:** April 2026  
**System Version:** 1.0

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [Architecture & Technology Stack](#2-architecture--technology-stack)
3. [Data Layer - Datasets Used](#3-data-layer---datasets-used)
4. [Grid Simulation Engine](#4-grid-simulation-engine)
5. [A* Pathfinding Algorithm](#5-a-pathfinding-algorithm)
6. [Human Behavior Simulation](#6-human-behavior-simulation)
7. [Bayesian Network Infrastructure](#7-bayesian-network-infrastructure)
8. [Knowledge Engine (Symbolic AI)](#8-knowledge-engine-symbolic-ai)
9. [7-Layer AI Architecture](#9-7-layer-ai-architecture)
10. [Explainable AI (XAI) System](#10-explainable-ai-xai-system)
11. [FastAPI Backend Architecture](#11-fastapi-backend-architecture)
12. [Frontend React Application](#12-frontend-react-application)
13. [How to Run the System](#13-how-to-run-the-system)
14. [API Documentation with Examples](#14-api-documentation-with-examples)
15. [System Integration Flow](#15-system-integration-flow)

---

## 1. SYSTEM OVERVIEW

### 1.1 What is This System?

This is an **AI-powered Digital Twin** of Mumbai city that simulates disaster scenarios (floods, infrastructure failures) and provides:
- Real-time risk assessment
- Intelligent evacuation planning
- Infrastructure failure prediction
- Policy recommendation

### 1.2 Key Features

1. **Grid-Based City Simulation**: Mumbai divided into 20x20 grid zones
2. **Multi-Agent System**: Human agents + Car agents for evacuation
3. **A* Pathfinding**: Optimal route calculation avoiding danger zones
4. **Bayesian Network**: Probabilistic infrastructure failure modeling
5. **Knowledge Engine**: Rule-based reasoning using symbolic logic
6. **Explainable AI**: Every decision is explained with reasoning
7. **Real-time Updates**: Sensor data integration (rain, water level, traffic)

### 1.3 Problem Statement

**Challenge**: During disasters like Mumbai floods (2005, 2017, 2019), thousands of people need evacuation but:
- No real-time risk assessment
- No optimal evacuation routes
- Infrastructure failures cascade unpredictably
- Emergency services lack decision support

**Our Solution**: AI system that predicts, plans, and explains evacuation strategies in real-time.

---

## 2. ARCHITECTURE & TECHNOLOGY STACK

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Dashboard│  │Evacuation│  │ Risk Map │  │Knowledge │   │
│  │          │  │  System  │  │          │  │  Engine  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND (Python)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API ROUTES LAYER                         │  │
│  │  /evacuation  /infrastructure  /knowledge  /mumbai   │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↕                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           7-LAYER AI ARCHITECTURE                     │  │
│  │  Layer 1: Grid Engine (Spatial)                       │  │
│  │  Layer 2: Pathfinding (A*)                            │  │
│  │  Layer 3: Multi-Agent System                          │  │
│  │  Layer 4: Bayesian Network                            │  │
│  │  Layer 5: Knowledge Engine                            │  │
│  │  Layer 6: Learning Layer                              │  │
│  │  Layer 7: Explainable AI                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Static  │  │Historical│  │ Realtime │  │  Output  │   │
│  │   Data   │  │   Data   │  │  Sensors │  │   Logs   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```


### 2.2 Technology Stack

**Backend:**
- Python 3.13
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (Database ORM)
- NumPy (Numerical computing)
- Pandas (Data processing)

**Frontend:**
- React 18
- Vite (Build tool)
- React Router (Navigation)
- Recharts (Data visualization)
- Axios (HTTP client)
- Lucide React (Icons)

**Database:**
- SQLite (Development)
- PostgreSQL (Production-ready)

**AI/ML Libraries:**
- Custom implementations (A*, Bayesian Networks)
- Symbolic logic engine
- Multi-agent simulation

---

## 3. DATA LAYER - DATASETS USED

### 3.1 Data Directory Structure

```
data/mumbai/
├── static/              # Fixed city data
│   ├── mumbai_wards.csv
│   └── infrastructure_nodes.csv
├── historical/          # Past disaster data
│   └── flood_events.csv
├── realtime/           # Sensor data (simulated)
│   ├── rain_sensors.csv
│   ├── water_level_sensors.csv
│   ├── traffic_density.csv
│   └── alert_sound_sensors.csv
└── outputs/            # Generated results
    ├── ward_risk_scores.csv
    └── explainability_log.csv
```

### 3.2 Dataset Details

#### 3.2.1 mumbai_wards.csv
**Purpose**: Geographic and demographic data for Mumbai wards

**Columns:**
- `ward_id`: Unique identifier (A, B, C, etc.)
- `ward_name`: Name (Colaba, Bandra, Andheri, etc.)
- `latitude`: Geographic coordinate
- `longitude`: Geographic coordinate
- `population`: Number of residents
- `area_sq_km`: Area in square kilometers
- `elevation`: Height above sea level (meters)
- `flood_prone`: Boolean (true/false)

**Sample Data:**
```csv
ward_id,ward_name,latitude,longitude,population,area_sq_km,elevation,flood_prone
A,Colaba,18.9067,72.8147,65000,2.3,5,true
B,Fort,18.9322,72.8347,45000,1.8,8,false
C,Bandra,19.0596,72.8295,180000,16.1,12,false
```

**Usage in System:**
- Grid initialization
- Population density calculation
- Risk score baseline


#### 3.2.2 infrastructure_nodes.csv
**Purpose**: Critical infrastructure locations and dependencies

**Columns:**
- `node_id`: Unique identifier (POWER_001, WATER_002, etc.)
- `node_type`: Category (Utility, Healthcare, IT, Emergency)
- `name`: Facility name
- `ward`: Location ward
- `latitude`, `longitude`: Coordinates
- `capacity`: Service capacity
- `criticality`: Importance score (0-100)
- `dependencies`: Comma-separated list of dependent nodes

**Sample Data:**
```csv
node_id,node_type,name,ward,latitude,longitude,capacity,criticality,dependencies
POWER_001,Utility,Colaba Power Station,A,18.9067,72.8147,500MW,95,
WATER_001,Utility,Bhandup Water Treatment,E,19.1450,72.9350,2500ML,90,POWER_001
HOSP_001,Healthcare,KEM Hospital,C,19.0176,72.8561,2000beds,85,POWER_001,WATER_001
```

**Usage in System:**
- Bayesian network construction
- Cascading failure simulation
- Critical node identification

#### 3.2.3 flood_events.csv
**Purpose**: Historical flood data for training and validation

**Columns:**
- `event_id`: Unique identifier
- `date`: Event date
- `ward_affected`: Ward ID
- `rainfall_mm`: Rainfall in millimeters
- `water_level_m`: Peak water level
- `duration_hours`: Event duration
- `casualties`: Number of casualties
- `economic_loss_cr`: Economic loss in crores

**Sample Data:**
```csv
event_id,date,ward_affected,rainfall_mm,water_level_m,duration_hours,casualties,economic_loss_cr
FLOOD_2005_001,2005-07-26,A,944,2.5,24,419,5000
FLOOD_2017_001,2017-08-29,C,315,1.8,12,23,800
```

**Usage in System:**
- Risk model training
- Pattern recognition
- Validation of predictions

#### 3.2.4 rain_sensors.csv (Real-time)
**Purpose**: Live rainfall monitoring

**Columns:**
- `sensor_id`: Sensor identifier
- `ward`: Location
- `timestamp`: Reading time
- `rainfall_mm_per_hour`: Current rainfall intensity
- `cumulative_24h`: 24-hour cumulative rainfall

**Sample Data:**
```csv
sensor_id,ward,timestamp,rainfall_mm_per_hour,cumulative_24h
RAIN_A_001,A,2026-04-01T14:30:00,45.2,156.8
RAIN_B_001,B,2026-04-01T14:30:00,38.7,142.3
```

**Usage in System:**
- Real-time risk updates
- Grid condition updates
- Alert triggering


#### 3.2.5 water_level_sensors.csv (Real-time)
**Purpose**: Water level monitoring at key locations

**Columns:**
- `sensor_id`: Sensor identifier
- `location`: Specific location name
- `ward`: Ward ID
- `timestamp`: Reading time
- `water_level_m`: Current water level in meters
- `flow_rate`: Water flow rate (m³/s)

**Usage in System:**
- Grid passability determination
- Evacuation route safety assessment
- Infrastructure failure prediction

---

## 4. GRID SIMULATION ENGINE

### 4.1 Overview

The Grid Engine divides Mumbai into a **20x20 grid** (400 zones total), each representing approximately 1-2 km² of the city.

### 4.2 Implementation File

**File:** `backend/evacuation_system/grid_engine.py`

**Key Class:** `MumbaiGridEngine`

### 4.3 GridZone Data Structure

Each grid zone contains:

```python
@dataclass
class GridZone:
    id: str                    # "A1", "B2", etc.
    name: str                  # "Colaba-North", "Bandra-West"
    row: int                   # Grid row (0-19)
    col: int                   # Grid column (0-19)
    latitude: float            # Geographic coordinate
    longitude: float           # Geographic coordinate
    risk_score: float          # 0.0 to 1.0 (flood risk)
    population_density: int    # People per zone
    water_level: float         # Current water level (meters)
    rainfall: float            # Current rainfall (mm/hour)
    infrastructure_status: str # "operational", "damaged", "blocked"
    safety_level: SafetyLevel  # SAFE, MEDIUM_RISK, DANGEROUS
    is_evacuation_point: bool  # Designated safe zone
    ward_id: str              # Link to Mumbai ward
```

### 4.4 Grid Initialization Process

**Function:** `_initialize_grids()` in `MumbaiGridEngine`

**Step-by-step:**

1. **Create 400 grid zones** (20 rows × 20 columns)
2. **Assign geographic coordinates**:
   - Latitude range: 18.90°N to 19.27°N
   - Longitude range: 72.77°E to 72.98°E
3. **Map to real Mumbai areas**:
   - Row 0-2: South Mumbai (Colaba, Fort, Worli)
   - Row 3-5: Central Mumbai (Dadar, Bandra, Kurla)
   - Row 6-12: North Mumbai (Andheri, Goregaon, Borivali)


4. **Calculate risk scores**:
   ```python
   # Coastal areas (low row numbers) have higher flood risk
   coastal_risk = 0.6 if row < 3 else 0.25
   
   # Low-lying areas near Mithi River (middle columns)
   river_risk = 0.55 if 8 <= col <= 12 else 0.20
   
   # Combined base risk
   base_risk = (coastal_risk + river_risk) / 2
   
   # Add randomness for variety
   risk_score = min(1.0, max(0.1, base_risk + random.uniform(-0.1, 0.35)))
   ```

5. **Determine safety levels**:
   ```python
   if risk_score < 0.30 and water_level < 0.5:
       safety = SafetyLevel.SAFE
   elif risk_score < 0.65:
       safety = SafetyLevel.MEDIUM_RISK
   else:
       safety = SafetyLevel.DANGEROUS
   ```

6. **Mark evacuation points**: 15% of safe zones become designated evacuation centers

### 4.5 Real-time Grid Updates

**Function:** `update_from_realtime_data(water_level, rainfall)`

**Process:**
1. Receive sensor data (water level, rainfall)
2. Recalculate risk score:
   ```python
   water_risk = min(1.0, water_level / 2.0)  # 2m = 100% risk
   rain_risk = min(1.0, rainfall / 100.0)    # 100mm/hr = 100% risk
   risk_score = (water_risk * 0.6 + rain_risk * 0.4)
   ```
3. Update safety level based on new risk
4. Update infrastructure status (may become damaged/blocked)

### 4.6 Grid Neighbor System

**Function:** `get_neighbors(grid)` - Returns passable adjacent grids

**4-directional movement:**
```python
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
```

**Passability check:**
```python
def is_passable(self) -> bool:
    return (self.safety_level != SafetyLevel.DANGEROUS and 
            self.infrastructure_status != "blocked" and
            self.water_level < 1.5)
```

### 4.7 Grid Visualization

Each grid has a color code:
- **Green (#10b981)**: SAFE
- **Orange (#f59e0b)**: MEDIUM_RISK
- **Red (#ef4444)**: DANGEROUS

---

## 5. A* PATHFINDING ALGORITHM

### 5.1 Overview

A* (A-star) is a graph traversal algorithm that finds the shortest path between two points while considering both:
- **Distance** (how far to goal)
- **Cost** (safety, water level, infrastructure)

### 5.2 Implementation File

**File:** `backend/evacuation_system/pathfinder.py`

**Key Class:** `EvacuationPathfinder`

### 5.3 A* Algorithm Components

#### 5.3.1 Node Structure

```python
@dataclass
class PathNode:
    grid: GridZone
    g_cost: float  # Actual cost from start
    h_cost: float  # Heuristic cost to goal
    f_cost: float  # Total cost (g + h)
    parent: PathNode  # Previous node in path
```


#### 5.3.2 Heuristic Function

**Purpose:** Estimate cost from current grid to goal

```python
def heuristic(self, grid1: GridZone, grid2: GridZone) -> float:
    # Manhattan distance (grid-based movement)
    distance = abs(grid1.row - grid2.row) + abs(grid1.col - grid2.col)
    
    # Safety penalty (prefer safer routes)
    safety_penalty = grid1.risk_score * 5
    
    return distance + safety_penalty
```

**Why Manhattan Distance?**
- Grid allows only 4-directional movement (no diagonals)
- Manhattan distance = |x1-x2| + |y1-y2|
- More accurate than Euclidean for grid-based systems

#### 5.3.3 Movement Cost Function

**Purpose:** Calculate cost of moving from one grid to another

```python
def get_movement_cost(self, from_grid: GridZone, to_grid: GridZone) -> float:
    base_cost = 1.0
    
    # Risk penalty (dangerous areas cost more)
    risk_penalty = to_grid.risk_score * 10
    
    # Water level penalty (deep water is dangerous)
    water_penalty = to_grid.water_level * 3
    
    # Infrastructure penalty
    if to_grid.infrastructure_status == "damaged":
        infra_penalty = 2
    elif to_grid.infrastructure_status == "blocked":
        return float('inf')  # Cannot pass
    
    total_cost = base_cost + risk_penalty + water_penalty + infra_penalty
    return total_cost
```

### 5.4 A* Algorithm Step-by-Step

**Function:** `find_path(start_grid, goal_grid)`

**Algorithm:**

```
1. Initialize:
   - open_set = priority queue (min-heap)
   - closed_set = set of visited grids
   - Add start node to open_set

2. While open_set is not empty:
   a. Pop node with lowest f_cost (current_node)
   b. If current_node is goal:
      - Reconstruct path
      - Return success
   
   c. Add current_node to closed_set
   
   d. For each neighbor of current_node:
      - Skip if in closed_set
      - Skip if dangerous/blocked
      - Calculate tentative_g_cost = current.g_cost + movement_cost
      - Calculate h_cost = heuristic(neighbor, goal)
      - Calculate f_cost = tentative_g_cost + h_cost
      - Create neighbor_node with costs
      - Add to open_set

3. If open_set becomes empty:
   - No path found
   - Return failure
```

### 5.5 Path Reconstruction

**Function:** `_reconstruct_path(node)`

**Process:**
1. Start from goal node
2. Follow parent pointers backward to start
3. Reverse the path
4. Return list of grids from start to goal

```python
def _reconstruct_path(self, node: PathNode) -> List[Dict]:
    path = []
    current = node
    
    while current:
        path.append({
            "grid_id": current.grid.id,
            "name": current.grid.name,
            "risk_score": current.grid.risk_score,
            "cost": current.g_cost
        })
        current = current.parent
    
    path.reverse()
    return path
```


### 5.6 A* Example Walkthrough

**Scenario:** Evacuate from Colaba (A1) to Bandra Safe Zone (E5)

**Step 1: Initialization**
```
Start: A1 (Colaba, risk=0.75, DANGEROUS)
Goal: E5 (Bandra Safe Zone, risk=0.15, SAFE)

open_set = [PathNode(A1, g=0, h=8, f=8)]
closed_set = {}
```

**Step 2: First Iteration**
```
Current: A1
Neighbors: A2 (right), B1 (down)

A2: risk=0.65, cost=7.5
  g_cost = 0 + 7.5 = 7.5
  h_cost = 7 + 3.25 = 10.25
  f_cost = 17.75

B1: risk=0.55, cost=6.5
  g_cost = 0 + 6.5 = 6.5
  h_cost = 7 + 2.75 = 9.75
  f_cost = 16.25

open_set = [PathNode(B1, f=16.25), PathNode(A2, f=17.75)]
closed_set = {A1}
```

**Step 3: Continue until goal reached**
- Algorithm explores safer routes
- Avoids high-risk zones
- Finds optimal balance between distance and safety

**Final Path:**
```
A1 → B1 → C1 → C2 → D3 → E4 → E5
Total cost: 42.3
Average risk: 0.35 (MEDIUM)
Grids avoided: 12 dangerous zones
```

### 5.7 A* Optimizations

1. **Priority Queue**: Uses heapq for O(log n) operations
2. **Early Termination**: Stops when goal is reached
3. **Closed Set**: Prevents revisiting nodes
4. **Admissible Heuristic**: Never overestimates, guarantees optimal path

---

## 6. HUMAN BEHAVIOR SIMULATION

### 6.1 Overview

Simulates individual people evacuating from dangerous zones to safe zones, each with unique characteristics and behaviors.

### 6.2 Implementation File

**File:** `backend/evacuation_system/human_agent_sim.py`

**Key Classes:**
- `HumanAgent`: Individual person
- `EvacuationSimulator`: Manages all agents

### 6.3 Human Agent Structure

```python
@dataclass
class HumanAgent:
    id: str                    # Unique identifier
    name: str                  # "Person-abc123"
    current_grid: GridZone     # Current location
    destination_grid: GridZone # Target safe zone
    path: List[Dict]          # Evacuation route
    path_index: int           # Current position in path
    status: AgentStatus       # WAITING, EVACUATING, SAFE, STUCK
    speed: float              # Movement speed (grids per step)
    health: int               # 0-100 (decreases in risky areas)
    age_group: str            # "child", "adult", "elderly"
    steps_taken: int          # Total steps moved
```


### 6.4 Agent Behavior Characteristics

#### 6.4.1 Age-Based Speed Variation

```python
if age_group == "child":
    speed = 0.8      # 80% of normal speed
elif age_group == "adult":
    speed = 1.0      # 100% normal speed
elif age_group == "elderly":
    speed = 0.6      # 60% of normal speed
```

#### 6.4.2 Health Degradation

```python
def move_to_next_grid(self, next_grid: GridZone):
    # Health decreases in risky areas
    if next_grid.risk_score > 0.6:
        self.health -= int(next_grid.risk_score * 5)
    
    # Check if reached destination
    if next_grid.id == self.destination_grid.id:
        self.status = AgentStatus.SAFE
```

**Example:**
- Agent enters grid with risk_score = 0.8
- Health loss = 0.8 × 5 = 4 points
- If health reaches 0, agent becomes STUCK

### 6.5 Agent Creation Process

**Function:** `create_agents_in_dangerous_zones(agents_per_zone=5)`

**Process:**
1. Identify all DANGEROUS zones
2. For each dangerous zone:
   - Create 5 agents (configurable)
   - Vary age groups (child, adult, elderly)
   - Assign appropriate speeds
   - Set initial status to WAITING

**Example:**
```
Dangerous Zone: A1 (Colaba)
  Agent 1: Person-a1b2, adult, speed=1.0
  Agent 2: Person-c3d4, child, speed=0.8
  Agent 3: Person-e5f6, elderly, speed=0.6
  Agent 4: Person-g7h8, adult, speed=1.0
  Agent 5: Person-i9j0, adult, speed=1.0
```

### 6.6 Path Assignment

**Function:** `assign_evacuation_paths()`

**Process:**
1. For each WAITING agent:
   - Find nearest safe zone using pathfinder
   - Calculate optimal path using A*
   - Assign path to agent
   - Change status to EVACUATING

```python
safe_zone = pathfinder.find_nearest_safe_zone(agent.current_grid)
path_result = pathfinder.find_path(agent.current_grid, safe_zone)

if path_result["success"]:
    agent.path = path_result["path"]
    agent.destination_grid = safe_zone
    agent.status = AgentStatus.EVACUATING
else:
    agent.status = AgentStatus.STUCK
```

### 6.7 Simulation Step

**Function:** `simulate_step()`

**Process for each time step:**

1. **For each EVACUATING agent:**
   - Check if more path remains
   - Get next grid in path
   - Verify grid is still passable
   - Move agent to next grid
   - Update health based on risk
   - Record movement

2. **Handle blocked paths:**
   - If next grid becomes blocked
   - Mark agent as STUCK
   - (Future: trigger re-routing)

3. **Update statistics:**
   - Count agents by status
   - Calculate average health
   - Compute completion rate

**Return data:**
```python
{
    "step": 42,
    "movements": [
        {
            "agent_id": "abc123",
            "from": {"grid_id": "A1", "row": 0, "col": 0},
            "to": {"grid_id": "A2", "row": 0, "col": 1},
            "health": 95,
            "status": "EVACUATING"
        }
    ],
    "stats": {
        "total_agents": 100,
        "evacuating": 45,
        "safe": 50,
        "stuck": 5,
        "average_health": 87.3,
        "completion_rate": 50.0
    }
}
```


### 6.8 Behavioral Realism

**Factors simulated:**
1. **Age diversity**: Different movement speeds
2. **Health impact**: Risk exposure affects health
3. **Path following**: Agents follow calculated routes
4. **Dynamic obstacles**: React to blocked paths
5. **Completion tracking**: Monitor evacuation progress

**Not yet implemented (future work):**
- Panic behavior
- Group dynamics (families staying together)
- Decision-making under uncertainty
- Communication between agents

---

## 7. BAYESIAN NETWORK INFRASTRUCTURE

### 7.1 Overview

Bayesian Networks model **probabilistic dependencies** between infrastructure nodes. When one node fails (e.g., power station), it affects dependent nodes (e.g., hospitals, water treatment).

### 7.2 Implementation Files

**Files:**
- `backend/core/infrastructure/bayesian_network.py`
- `backend/core/infrastructure/probabilistic_node.py`

**Key Classes:**
- `ProbabilisticNode`: Single infrastructure node
- `InfrastructureBayesianNetwork`: Network of nodes
- `ConditionalProbabilityTable`: CPT for dependencies

### 7.3 Probabilistic Node Structure

```python
class NodeState(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"

class ProbabilisticNode:
    node_id: str              # "POWER_001"
    node_type: str            # "Utility", "Healthcare", "IT", "Emergency"
    name: str                 # "Colaba Power Station"
    ward: str                 # "A"
    
    # Probability distribution
    probabilities: Dict[NodeState, float] = {
        HEALTHY: 0.85,
        DEGRADED: 0.10,
        FAILED: 0.05
    }
    
    # Network connections
    parents: List[Tuple[ProbabilisticNode, float]]  # Dependencies
    children: List[Tuple[ProbabilisticNode, float]] # Dependents
    
    # State tracking
    current_state: NodeState
    previous_state: NodeState
    state_history: List[NodeState]
```

### 7.4 Conditional Probability Tables (CPT)

**Purpose:** Define P(Child fails | Parent states)

**Example CPT for Hospital (depends on Power + Water):**

```python
# P(Hospital fails | Power state, Water state)
CPT = {
    (HEALTHY, HEALTHY): 0.02,   # Both healthy: 2% failure
    (FAILED, HEALTHY): 0.40,    # Power failed: 40% failure
    (HEALTHY, FAILED): 0.35,    # Water failed: 35% failure
    (FAILED, FAILED): 0.75,     # Both failed: 75% failure
    (DEGRADED, HEALTHY): 0.15,  # Power degraded: 15% failure
    (HEALTHY, DEGRADED): 0.15,  # Water degraded: 15% failure
    (DEGRADED, DEGRADED): 0.30, # Both degraded: 30% failure
}
```

**Interpretation:**
- If both Power and Water are HEALTHY, hospital has only 2% chance of failure
- If Power FAILS, hospital failure probability jumps to 40%
- If both fail, hospital has 75% chance of failure


### 7.5 Evidence Integration

**Function:** `apply_evidence_to_nodes()`

**Evidence variables:**
- `RainIntensity`: 0.0 to 1.0
- `FloodLevel`: 0.0 to 1.0
- `CyberAttack`: 0.0 to 1.0
- `PowerStress`: 0.0 to 1.0
- `WaterStress`: 0.0 to 1.0

**Evidence application logic:**

```python
# Power nodes affected by rain and cyber attacks
if "Power" in node.node_id:
    failure_increase = (rain_intensity * 0.15 + 
                       cyber_attack * 0.25 + 
                       power_stress * 0.20)
    node.update_probability(FAILED, failure_increase)

# Water nodes affected by flood
if "Water" in node.node_id:
    failure_increase = (flood_level * 0.20 + 
                       water_stress * 0.15)
    node.update_probability(FAILED, failure_increase)

# Hospitals affected by flood and power
if node.node_type == "Healthcare":
    failure_increase = (flood_level * 0.10 + 
                       power_stress * 0.15)
    node.update_probability(FAILED, failure_increase)
```

**Example:**
```
Initial state:
  POWER_001: P(FAILED) = 0.05

Evidence received:
  RainIntensity = 0.8
  CyberAttack = 0.3

Calculation:
  failure_increase = 0.8 * 0.15 + 0.3 * 0.25 + 0 * 0.20
                   = 0.12 + 0.075
                   = 0.195

Updated state:
  POWER_001: P(FAILED) = 0.05 + 0.195 = 0.245 (24.5%)
```

### 7.6 Belief Propagation

**Function:** `propagate_beliefs()`

**Algorithm:**
1. For each node with parents:
   - Calculate weighted influence from all parents
   - Update child's failure probability

```python
for node in nodes:
    total_failure_influence = 0.0
    total_weight = 0.0
    
    for parent, weight in node.parents:
        parent_failure_prob = parent.probabilities[FAILED]
        parent_degraded_prob = parent.probabilities[DEGRADED]
        
        # Weighted influence
        influence = (parent_failure_prob * 0.8 + 
                    parent_degraded_prob * 0.3) * weight
        total_failure_influence += influence
        total_weight += weight
    
    if total_weight > 0:
        avg_influence = total_failure_influence / total_weight
        node.update_probability(FAILED, avg_influence * 0.5)
```

**Example propagation:**
```
Network:
  POWER_001 (P(FAILED) = 0.30) --[weight=0.8]--> HOSP_001
  WATER_001 (P(FAILED) = 0.20) --[weight=0.6]--> HOSP_001

Calculation for HOSP_001:
  power_influence = (0.30 * 0.8) * 0.8 = 0.192
  water_influence = (0.20 * 0.8) * 0.6 = 0.096
  total_influence = 0.192 + 0.096 = 0.288
  total_weight = 0.8 + 0.6 = 1.4
  avg_influence = 0.288 / 1.4 = 0.206
  
  HOSP_001 failure increase = 0.206 * 0.5 = 0.103 (10.3%)
```

### 7.7 Network Update Cycle

**Function:** `update_network(evidence)`

**Complete update process:**

```
1. Receive evidence (rain, flood, cyber attack)
   ↓
2. Apply evidence to root nodes (Power, Water)
   ↓
3. Propagate beliefs through network
   ↓
4. Update all node states
   ↓
5. Record state history
   ↓
6. Return network state
```

**Timestep example:**
```
Timestep 0: All nodes HEALTHY
Timestep 1: Heavy rain → Power stations DEGRADED
Timestep 2: Continued rain → Power FAILED → Hospitals DEGRADED
Timestep 3: Flood rises → Water treatment FAILED → Hospitals FAILED
```


### 7.8 Significance of Bayesian Networks

**Why Bayesian Networks?**

1. **Uncertainty Modeling**: Real-world infrastructure failures are probabilistic, not deterministic
2. **Dependency Capture**: Models cascading failures (power → hospital → emergency services)
3. **Evidence Integration**: Incorporates real-time sensor data
4. **Predictive Power**: Forecasts future failures before they occur
5. **Explainability**: Shows why a node is likely to fail (parent influences)

**Real-world application:**
- Mumbai 2005 floods: Power failures cascaded to water treatment, hospitals
- Our system predicts this cascade and suggests preventive actions

---

## 8. KNOWLEDGE ENGINE (SYMBOLIC AI)

### 8.1 Overview

The Knowledge Engine uses **symbolic logic** (not neural networks) to reason about disaster scenarios using rules and facts.

### 8.2 Implementation Files

**Files:**
- `backend/core/knowledge_engine/knowledge_base.py`
- `backend/core/knowledge_engine/symbolic_logic.py`
- `backend/core/knowledge_engine/expert_system.py`

### 8.3 Logic Levels Supported

#### 8.3.1 Propositional Logic

**Simple true/false statements:**
```
Facts:
  - FloodActive
  - PowerFailed
  - HospitalOverwhelmed

Rules:
  IF FloodActive AND PowerFailed THEN EmergencyDeclared
```

#### 8.3.2 First-Order Logic (FOL)

**Predicates with variables:**
```
Facts:
  - InDanger(Ward_A)
  - InDanger(Ward_B)
  - HasPower(Ward_C)

Rules:
  ∀x: InDanger(x) ∧ HasPower(x) → EvacuateTo(x)
```

#### 8.3.3 Second-Order Logic (SOL)

**Reasoning about categories of predicates:**
```
Categories:
  EconomicIndicators = {UnemploymentHigh, InflationHigh, GDPLow}
  InfrastructureIndicators = {PowerFailed, WaterFailed, HospitalFailed}

Rules:
  IF (∃P ∈ EconomicIndicators: P is true) AND
     (∃Q ∈ InfrastructureIndicators: Q is true)
  THEN SystemicCrisis
```

### 8.4 Knowledge Base Structure

```python
class KnowledgeBase:
    facts: Set[str | Predicate]  # Known facts
    rules: List[Dict]             # Inference rules
    inference_trace: List[Dict]   # Reasoning log
    
    # Second-order categories
    economic_indicators: Set[str]
    infrastructure_indicators: Set[str]
    social_indicators: Set[str]
```

### 8.5 Rule-Based Reasoning

**Example rules in the system:**

```python
# Rule 1: Flood detection
IF RainIntensity > 50 AND WaterLevel > 1.0
THEN FloodActive

# Rule 2: Evacuation trigger
IF FloodActive AND PopulationDensity > 5000
THEN EvacuationRequired(Ward)

# Rule 3: Infrastructure failure
IF PowerFailed AND WaterFailed
THEN CriticalInfrastructureFailure

# Rule 4: Cascading crisis
IF CriticalInfrastructureFailure AND HospitalFailed
THEN SystemicCrisis
```


### 8.6 Forward Chaining Inference

**Algorithm:**
```
1. Start with known facts
2. For each rule:
   - Check if all premises are satisfied
   - If yes, add conclusion to facts
3. Repeat until no new facts can be inferred
```

**Example execution:**

```
Initial facts:
  - RainIntensity = 75
  - WaterLevel = 1.5
  - PopulationDensity(Ward_A) = 8000

Step 1: Apply Rule 1
  Premises: RainIntensity > 50 ✓, WaterLevel > 1.0 ✓
  Conclusion: Add "FloodActive"
  
Step 2: Apply Rule 2
  Premises: FloodActive ✓, PopulationDensity > 5000 ✓
  Conclusion: Add "EvacuationRequired(Ward_A)"

Step 3: No more rules applicable
  Final facts: {RainIntensity=75, WaterLevel=1.5, 
                PopulationDensity=8000, FloodActive, 
                EvacuationRequired(Ward_A)}
```

### 8.7 Backward Chaining (Goal-Driven)

**Algorithm:**
```
1. Start with a goal (query)
2. Find rules that conclude the goal
3. Recursively prove premises
4. Return true if goal can be proven
```

**Example:**
```
Query: Is EvacuationRequired(Ward_A)?

Step 1: Find rule concluding EvacuationRequired
  Rule: IF FloodActive AND PopulationDensity > 5000 
        THEN EvacuationRequired

Step 2: Prove FloodActive
  Rule: IF RainIntensity > 50 AND WaterLevel > 1.0 
        THEN FloodActive
  Check facts: RainIntensity = 75 ✓, WaterLevel = 1.5 ✓
  Proven: FloodActive

Step 3: Prove PopulationDensity > 5000
  Check facts: PopulationDensity = 8000 ✓
  Proven: PopulationDensity > 5000

Result: EvacuationRequired(Ward_A) is TRUE
```

### 8.8 Expert System Integration

**File:** `backend/core/knowledge_engine/expert_system.py`

**Capabilities:**
1. **Disaster classification**: Identify disaster type and severity
2. **Risk assessment**: Evaluate ward-level risks
3. **Action recommendation**: Suggest evacuation, resource allocation
4. **Explanation generation**: Explain reasoning process

**Example query:**
```python
query = {
    "ward": "A",
    "rain_intensity": 85,
    "water_level": 2.0,
    "population": 65000,
    "infrastructure_status": "damaged"
}

result = expert_system.evaluate(query)

# Output:
{
    "disaster_type": "SEVERE_FLOOD",
    "risk_level": "CRITICAL",
    "actions": [
        "IMMEDIATE_EVACUATION",
        "DEPLOY_EMERGENCY_SERVICES",
        "ACTIVATE_BACKUP_POWER"
    ],
    "reasoning": [
        "Rain intensity (85mm/hr) exceeds critical threshold (50mm/hr)",
        "Water level (2.0m) indicates severe flooding",
        "Population (65000) at high risk",
        "Infrastructure damage compounds the crisis"
    ]
}
```

### 8.9 Significance of Knowledge Engine

**Why Symbolic AI?**

1. **Transparency**: Every decision has explicit rules
2. **Domain expertise**: Encodes expert knowledge from disaster management
3. **Interpretability**: Non-experts can understand reasoning
4. **Reliability**: Deterministic, no "black box" behavior
5. **Complementary**: Works alongside neural networks (hybrid AI)

**Comparison:**

| Aspect | Neural Networks | Symbolic AI |
|--------|----------------|-------------|
| Learning | From data | From rules |
| Explainability | Low | High |
| Data requirement | Large datasets | Expert knowledge |
| Adaptability | High | Medium |
| Reliability | Probabilistic | Deterministic |

**Our approach:** Hybrid system using both!

---

## 9. 7-LAYER AI ARCHITECTURE

### 9.1 Architecture Overview

Our system uses a **layered AI architecture** where each layer has a specific responsibility and builds upon lower layers.

```
┌─────────────────────────────────────────────────────────┐
│ Layer 7: EXPLAINABLE AI (XAI)                          │
│ - Path explanations, decision justification            │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ Layer 6: LEARNING LAYER                                 │
│ - Reinforcement learning, pattern recognition          │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ Layer 5: KNOWLEDGE ENGINE                               │
│ - Symbolic logic, rule-based reasoning                 │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ Layer 4: BAYESIAN NETWORK                               │
│ - Probabilistic inference, uncertainty modeling        │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ Layer 3: MULTI-AGENT SYSTEM                             │
│ - Human agents, car agents, coordination               │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ Layer 2: PATHFINDING (A*)                               │
│ - Route optimization, obstacle avoidance               │
└─────────────────────────────────────────────────────────┘
                         ↑
┌─────────────────────────────────────────────────────────┐
│ Layer 1: GRID ENGINE (SPATIAL)                          │
│ - City representation, real-time updates               │
└─────────────────────────────────────────────────────────┘
```

### 9.2 Layer 1: Grid Engine (Spatial Layer)

**Purpose:** Foundation layer representing physical city space

**Responsibilities:**
- Divide city into grid zones
- Track real-time conditions (water, rain, risk)
- Manage geographic data
- Provide neighbor relationships

**Key Functions:**
- `initialize_grids()`: Create 400 grid zones
- `update_grid_conditions()`: Apply sensor data
- `get_neighbors()`: Return adjacent grids
- `get_dangerous_zones()`: Identify high-risk areas

**Output to Layer 2:**
- Grid topology
- Passability information
- Risk scores

**Files:** `backend/evacuation_system/grid_engine.py`

### 9.3 Layer 2: Pathfinding (Search Layer)

**Purpose:** Find optimal routes through grid space

**Responsibilities:**
- Implement A* algorithm
- Calculate movement costs
- Avoid dangerous zones
- Optimize for safety + distance

**Key Functions:**
- `find_path(start, goal)`: A* pathfinding
- `heuristic()`: Estimate remaining cost
- `get_movement_cost()`: Calculate edge weights
- `find_nearest_safe_zone()`: Locate evacuation points

**Input from Layer 1:** Grid structure, risk scores
**Output to Layer 3:** Optimal paths for agents

**Files:** `backend/evacuation_system/pathfinder.py`


### 9.4 Layer 3: Multi-Agent System

**Purpose:** Simulate individual entities (people, vehicles) with autonomous behavior

**Responsibilities:**
- Create and manage human agents
- Create and manage car agents
- Coordinate evacuation operations
- Track agent states and statistics

**Agent Types:**

1. **Human Agents** (`human_agent_sim.py`):
   - Individual people evacuating
   - Age-based behavior (child, adult, elderly)
   - Health tracking
   - Path following

2. **Car Agents** (`car_agent.py`):
   - Evacuation vehicles
   - State machine (IDLE → MOVING → LOADING → MOVING → UNLOADING)
   - Capacity management (50 people per trip)
   - Mission assignment

**Key Functions:**
- `create_agents_in_dangerous_zones()`: Spawn agents
- `assign_evacuation_paths()`: Give agents routes
- `simulate_step()`: Advance simulation one timestep
- `assign_car_mission()`: Send car to pickup location

**Input from Layer 2:** Evacuation paths
**Output to Layer 4:** Agent positions, evacuation status

**Files:** 
- `backend/evacuation_system/human_agent_sim.py`
- `backend/evacuation_system/car_agent.py`
- `backend/evacuation_system/car_evacuation_manager.py`

### 9.5 Layer 4: Bayesian Network (Probabilistic Layer)

**Purpose:** Model infrastructure dependencies and failure propagation

**Responsibilities:**
- Build infrastructure network graph
- Define conditional probability tables (CPTs)
- Integrate real-time evidence
- Propagate beliefs through network
- Predict cascading failures

**Key Functions:**
- `add_node()`: Add infrastructure node
- `add_dependency()`: Connect nodes
- `apply_evidence_to_nodes()`: Update with sensor data
- `propagate_beliefs()`: Bayesian inference
- `update_network()`: Complete update cycle

**Input from Layer 3:** Agent impacts on infrastructure
**Output to Layer 5:** Infrastructure failure predictions

**Files:**
- `backend/core/infrastructure/bayesian_network.py`
- `backend/core/infrastructure/probabilistic_node.py`
- `backend/core/infrastructure/cascading_failure.py`

### 9.6 Layer 5: Knowledge Engine (Symbolic Layer)

**Purpose:** Rule-based reasoning and expert knowledge

**Responsibilities:**
- Store facts and rules
- Perform logical inference (forward/backward chaining)
- Classify disaster scenarios
- Generate recommendations
- Explain reasoning

**Key Functions:**
- `add_fact()`: Add known fact
- `add_rule()`: Define inference rule
- `forward_chain()`: Derive new facts
- `backward_chain()`: Prove goals
- `query()`: Answer questions

**Input from Layer 4:** Infrastructure states, probabilities
**Output to Layer 6:** Logical conclusions, recommendations

**Files:**
- `backend/core/knowledge_engine/knowledge_base.py`
- `backend/core/knowledge_engine/symbolic_logic.py`
- `backend/core/knowledge_engine/expert_system.py`


### 9.7 Layer 6: Learning Layer

**Purpose:** Improve system performance through experience

**Responsibilities:**
- Learn from simulation outcomes
- Optimize evacuation strategies
- Adapt to changing patterns
- Store and replay experiences

**Key Components:**

1. **Reinforcement Learning:**
   - State: Current grid conditions, agent positions
   - Action: Evacuation decisions, resource allocation
   - Reward: People saved, time taken, resources used
   - Policy: Learned strategy

2. **Experience Replay:**
   - Store successful evacuations
   - Learn from failures
   - Improve future decisions

**Key Functions:**
- `train_from_simulation()`: Learn from outcomes
- `update_policy()`: Improve decision strategy
- `save_checkpoint()`: Store learned model
- `load_checkpoint()`: Restore learned model

**Input from Layer 5:** Scenario outcomes, decisions made
**Output to Layer 7:** Improved strategies, learned patterns

**Files:**
- `backend/core/learning_layer/simulation_trainer.py`
- `backend/core/learning_layer/reinforcement_learning.py`

### 9.8 Layer 7: Explainable AI (XAI Layer)

**Purpose:** Make all AI decisions transparent and understandable

**Responsibilities:**
- Explain path selections
- Justify agent decisions
- Compare alternatives
- Generate natural language explanations
- Log reasoning traces

**Key Functions:**
- `explain_path_selection()`: Why this route?
- `compare_paths()`: Why route A vs route B?
- `get_path_risks()`: What are the dangers?
- `generate_explanation_text()`: Human-readable output

**Input from all layers:** Decisions, states, outcomes
**Output:** Explanations for users/faculty

**Files:**
- `backend/core/explainable_ai/path_explainer.py`
- `backend/core/explainable_ai/decision_explainer.py`

### 9.9 Layer Interaction Example

**Scenario:** Heavy rain starts in Colaba

```
Layer 1 (Grid): 
  - Detects rain_intensity = 85mm/hr
  - Updates Colaba grid risk_score = 0.85
  - Marks as DANGEROUS

Layer 2 (Pathfinding):
  - Recalculates routes avoiding Colaba
  - Finds alternative paths through safer zones

Layer 3 (Multi-Agent):
  - Identifies 500 people in Colaba
  - Assigns new evacuation paths
  - Dispatches 10 cars for pickup

Layer 4 (Bayesian):
  - Predicts power failure probability = 35%
  - Predicts hospital impact = 25%
  - Identifies cascading risks

Layer 5 (Knowledge):
  - Infers: FloodActive = TRUE
  - Infers: EvacuationRequired(Colaba) = TRUE
  - Recommends: Deploy emergency services

Layer 6 (Learning):
  - Records this scenario
  - Updates policy based on outcome
  - Improves future response time

Layer 7 (XAI):
  - Explains: "Colaba evacuation triggered because rain 
    intensity (85mm/hr) exceeds threshold and 500 people 
    are at risk. Alternative routes through Fort selected 
    to avoid flooded areas."
```

---

## 10. EXPLAINABLE AI (XAI) SYSTEM

### 10.1 Why Explainable AI?

**Problem:** Traditional AI systems are "black boxes" - they make decisions but can't explain why.

**Our Solution:** Every decision in our system comes with:
1. **Reasoning trace**: Step-by-step logic
2. **Alternative comparison**: Why this choice vs others
3. **Risk assessment**: What dangers were considered
4. **Natural language**: Human-readable explanations

### 10.2 XAI Components

#### 10.2.1 Path Explanation

**When:** Evacuation route is calculated

**What it explains:**
- Why this path was selected
- What dangers were avoided
- How it compares to direct route
- Safety score calculation

**Example output:**
```json
{
  "path_id": "PATH_001",
  "path_length": 12,
  "total_cost": 42.3,
  "average_cost_per_grid": 3.53,
  "grids_avoided": 8,
  "high_risk_avoided": 3,
  "selection_reason": "Optimal balance of safety and distance",
  "explanation_text": "Selected path traverses 12 grid zones. 
    Avoided 3 high-risk zones including A1, A2, B1. 
    This route is 35% safer than direct path.",
  "safety_score": 0.847,
  "segments": [
    {"from": "A1", "to": "B1", "risk": 0.25, "safety": "SAFE"},
    {"from": "B1", "to": "C1", "risk": 0.30, "safety": "MEDIUM_RISK"}
  ]
}
```

#### 10.2.2 Decision Explanation

**When:** Knowledge engine makes inference

**What it explains:**
- Which rules were applied
- What facts were used
- How conclusion was reached

**Example output:**
```json
{
  "query": "Should Ward A be evacuated?",
  "conclusion": "YES",
  "confidence": 0.95,
  "reasoning_steps": [
    {
      "step": 1,
      "rule": "Flood Detection Rule",
      "premises": ["RainIntensity > 50", "WaterLevel > 1.0"],
      "conclusion": "FloodActive",
      "satisfied": true
    },
    {
      "step": 2,
      "rule": "Evacuation Trigger Rule",
      "premises": ["FloodActive", "PopulationDensity > 5000"],
      "conclusion": "EvacuationRequired(Ward_A)",
      "satisfied": true
    }
  ],
  "facts_used": [
    "RainIntensity = 85mm/hr",
    "WaterLevel = 1.5m",
    "PopulationDensity(Ward_A) = 8000"
  ]
}
```

#### 10.2.3 Infrastructure Failure Explanation

**When:** Bayesian network predicts failure

**What it explains:**
- Why node is likely to fail
- Which dependencies contributed
- Probability breakdown

**Example output:**
```json
{
  "node": "HOSP_001 (KEM Hospital)",
  "failure_probability": 0.42,
  "explanation": "Hospital has 42% failure probability due to:",
  "contributing_factors": [
    {
      "factor": "Power dependency",
      "parent_node": "POWER_001",
      "parent_failure_prob": 0.35,
      "contribution": 0.28,
      "weight": 0.8
    },
    {
      "factor": "Water dependency",
      "parent_node": "WATER_001",
      "parent_failure_prob": 0.20,
      "contribution": 0.12,
      "weight": 0.6
    },
    {
      "factor": "Flood evidence",
      "evidence_value": 0.7,
      "contribution": 0.07
    }
  ],
  "recommendation": "Deploy backup power and water supplies"
}
```


### 10.3 XAI Across All 7 Layers

**Layer 1 (Grid) XAI:**
- "Grid A1 marked DANGEROUS because water_level (2.1m) exceeds threshold (1.5m) and risk_score (0.85) is critical"

**Layer 2 (Pathfinding) XAI:**
- "Path avoids grids A1, A2, B1 due to high risk. Selected route through C1, D2, E3 has 40% lower average risk"

**Layer 3 (Multi-Agent) XAI:**
- "Agent Person-abc123 assigned to Car-5 because: nearest available vehicle (3 grids away), car has capacity (15/50), agent health critical (45%)"

**Layer 4 (Bayesian) XAI:**
- "Power station failure probability increased from 5% to 35% due to: rain evidence (0.8), cyber attack evidence (0.3), cascading from upstream node"

**Layer 5 (Knowledge) XAI:**
- "Evacuation recommended because: Rule 'Flood + High Population → Evacuate' satisfied with facts: FloodActive=TRUE, Population=8000>5000"

**Layer 6 (Learning) XAI:**
- "Strategy improved: Previous simulations showed evacuating via Route B saves 15% more people than Route A in similar conditions"

**Layer 7 (XAI) XAI:**
- "This explanation generated by analyzing: 12 path segments, 8 avoided grids, 3 alternative routes, 5 safety factors"

### 10.4 Explainability Log

**File:** `data/mumbai/outputs/explainability_log.csv`

**Purpose:** Record all explanations for audit and analysis

**Columns:**
```csv
timestamp,decision_type,decision_id,explanation,confidence,factors
2026-04-01T14:30:00,PATH_SELECTION,PATH_001,"Avoided 3 high-risk zones",0.95,"risk_avoidance,distance_optimization"
2026-04-01T14:31:00,EVACUATION_TRIGGER,EVAC_A,"Population at risk",0.98,"flood_active,high_population"
```

### 10.5 Significance of XAI

**Why it matters:**

1. **Trust**: Users trust decisions they understand
2. **Debugging**: Developers can identify errors
3. **Compliance**: Regulatory requirements for AI transparency
4. **Learning**: Humans learn from AI reasoning
5. **Accountability**: Clear responsibility for decisions

**Real-world impact:**
- Emergency managers can justify evacuation orders
- Citizens understand why they must evacuate
- Government can audit AI decisions
- Researchers can improve algorithms

---

## 11. FASTAPI BACKEND ARCHITECTURE

### 11.1 Overview

FastAPI is a modern Python web framework for building APIs with automatic documentation and type validation.

### 11.2 Main Application File

**File:** `backend/main.py`

**Key components:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI(title="AI Strategic Risk Engine")
    
    # Enable CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    # Include routers
    app.include_router(evacuation_router)
    app.include_router(infrastructure_router)
    app.include_router(knowledge_router)
    app.include_router(mumbai_router)
    
    return app

app = create_app()
```


### 11.3 API Route Structure

```
backend/api/
├── __init__.py              # Main router aggregator
├── evacuation_routes.py     # Evacuation simulation endpoints
├── infrastructure_routes.py # Bayesian network endpoints
├── knowledge_routes.py      # Knowledge engine endpoints
├── mumbai_routes.py         # Mumbai-specific data
├── health_routes.py         # System health checks
└── explainability_routes.py # XAI endpoints
```

### 11.4 Key API Endpoints

#### 11.4.1 Evacuation Routes

**File:** `backend/api/evacuation_routes.py`

```python
# Reset and initialize grid
POST /api/evacuation/reset-all
Response: {"message": "Grid reset", "grid_size": "20x20"}

# Get grid data
GET /api/evacuation/grid?ward_id=A
Response: {
  "grids": [...],
  "dangerous_zones": 15,
  "safe_zones": 45
}

# Create human agents
POST /api/evacuation/create-agents
Body: {"agents_per_zone": 5}
Response: {"agents_created": 75, "total_agents": 75}

# Simulate one step
POST /api/evacuation/simulation-step
Response: {
  "step": 42,
  "movements": [...],
  "stats": {"safe": 50, "evacuating": 20}
}

# Get evacuation paths
GET /api/evacuation/paths
Response: {
  "paths": [
    {
      "start_grid": "A1",
      "goal_grid": "E5",
      "path_length": 12,
      "agents_using": 5
    }
  ]
}
```

#### 11.4.2 Infrastructure Routes

**File:** `backend/api/infrastructure_routes.py`

```python
# Get network status
GET /api/infrastructure/network/status
Response: {
  "timestep": 42,
  "total_nodes": 50,
  "average_health": 75.3,
  "critical_nodes": ["POWER_001", "HOSP_003"]
}

# Update with evidence
POST /api/infrastructure/network/update
Body: {
  "RainIntensity": 0.8,
  "FloodLevel": 0.6,
  "CyberAttack": 0.0
}
Response: {"updated": true, "timestep": 43}

# Get cascading failure analysis
GET /api/infrastructure/cascade/analysis
Response: {
  "cascade_events": [
    {
      "source": "POWER_001",
      "affected": ["HOSP_001", "WATER_002"],
      "severity": "HIGH"
    }
  ]
}
```

#### 11.4.3 Knowledge Engine Routes

**File:** `backend/api/knowledge_routes.py`

```python
# Query knowledge base
POST /api/knowledge/query
Body: {
  "ward": "A",
  "rain_intensity": 85,
  "water_level": 2.0
}
Response: {
  "disaster_type": "SEVERE_FLOOD",
  "risk_level": "CRITICAL",
  "actions": ["IMMEDIATE_EVACUATION"],
  "reasoning": [...]
}

# Get inference trace
GET /api/knowledge/trace
Response: {
  "steps": [
    {
      "rule": "Flood Detection",
      "premises": ["RainIntensity > 50"],
      "conclusion": "FloodActive"
    }
  ]
}
```


### 11.5 FastAPI Features Used

#### 11.5.1 Automatic API Documentation

**Swagger UI:** http://localhost:8001/docs

Features:
- Interactive API testing
- Request/response schemas
- Try-it-out functionality
- Authentication testing

**ReDoc:** http://localhost:8001/redoc

Features:
- Clean documentation layout
- Code samples
- Schema visualization

#### 11.5.2 Type Validation with Pydantic

```python
from pydantic import BaseModel

class EvidenceUpdate(BaseModel):
    RainIntensity: float
    FloodLevel: float
    CyberAttack: float

@app.post("/api/infrastructure/network/update")
async def update_network(evidence: EvidenceUpdate):
    # FastAPI automatically validates types
    # Rejects invalid data with clear error messages
    return {"updated": True}
```

#### 11.5.3 Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/data")
async def get_data(db: Session = Depends(get_db)):
    # Database session automatically managed
    return db.query(Model).all()
```

#### 11.5.4 CORS Middleware

**Purpose:** Allow frontend (port 8081) to call backend (port 8001)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["http://localhost:8081"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### 11.6 Request/Response Flow

```
1. Frontend sends HTTP request
   ↓
2. FastAPI receives request
   ↓
3. Middleware processes (CORS, logging)
   ↓
4. Route handler executes
   ↓
5. Pydantic validates data
   ↓
6. Business logic runs (AI layers)
   ↓
7. Response serialized to JSON
   ↓
8. CORS headers added
   ↓
9. Response sent to frontend
```

### 11.7 Error Handling

```python
from fastapi import HTTPException

@app.get("/api/grid/{grid_id}")
async def get_grid(grid_id: str):
    grid = grid_engine.get_grid(grid_id)
    if not grid:
        raise HTTPException(
            status_code=404,
            detail=f"Grid {grid_id} not found"
        )
    return grid.to_dict()
```

**Error response:**
```json
{
  "detail": "Grid Z99 not found"
}
```

---

## 12. FRONTEND REACT APPLICATION

### 12.1 Overview

React single-page application (SPA) providing interactive visualization and control of the AI system.

### 12.2 Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── Layout.jsx
│   │   ├── Card.jsx
│   │   └── Card.css
│   ├── pages/          # Main application pages
│   │   ├── UrbanEvacuation.jsx
│   │   ├── ResilienceDashboard.jsx
│   │   ├── RiskHeatmap.jsx
│   │   ├── KnowledgeEngine.jsx
│   │   └── MumbaiMapRealtime.jsx
│   ├── context/        # State management
│   │   └── WardContext.jsx
│   ├── services/       # API communication
│   │   └── api.js
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── public/             # Static assets
├── index.html          # HTML template
└── package.json        # Dependencies
```


### 12.3 Key Pages

#### 12.3.1 Urban Evacuation Page

**File:** `frontend/src/pages/UrbanEvacuation.jsx`

**Features:**
- 20x20 grid visualization
- Human agent positions (dots)
- Car agent positions (car icons)
- Real-time movement animation
- Control panel (start, pause, reset)
- Statistics display

**Key functions:**
```javascript
// Initialize grid
const initializeGrid = async () => {
  await axios.post('http://localhost:8001/api/evacuation/reset-all');
  await fetchGridData();
};

// Simulation step
const handleSimulationStep = async () => {
  const response = await axios.post(
    'http://localhost:8001/api/evacuation/simulation-step'
  );
  setAgents(response.data.agents);
  setStats(response.data.stats);
};

// Auto-play simulation
useEffect(() => {
  if (isPlaying) {
    const interval = setInterval(() => {
      handleSimulationStep();
    }, 1000);
    return () => clearInterval(interval);
  }
}, [isPlaying]);
```

**Grid rendering:**
```javascript
<div className="grid">
  {gridData.map(grid => (
    <div
      key={grid.id}
      className="grid-cell"
      style={{
        backgroundColor: grid.color,
        opacity: grid.is_passable ? 1 : 0.5
      }}
    >
      {/* Show agents in this grid */}
      {agents
        .filter(a => a.position.grid_id === grid.id)
        .map(agent => (
          <div className="agent-dot" key={agent.id} />
        ))}
    </div>
  ))}
</div>
```

#### 12.3.2 Resilience Dashboard

**File:** `frontend/src/pages/ResilienceDashboard.jsx`

**Features:**
- Infrastructure network visualization
- Bayesian network status
- Cascading failure events
- Vulnerability analysis
- Real-time updates

**Data fetching:**
```javascript
const loadNetworkState = async () => {
  const response = await axios.get(
    'http://localhost:8001/api/infrastructure/network/status'
  );
  setNetworkState(response.data);
};

const loadCascadeEvents = async () => {
  const response = await axios.get(
    'http://localhost:8001/api/infrastructure/cascade/analysis'
  );
  setCascadeEvents(response.data.cascade_events);
};
```

#### 12.3.3 Knowledge Engine Page

**File:** `frontend/src/pages/KnowledgeEngine.jsx`

**Features:**
- Query interface
- Inference trace display
- Rule visualization
- Explanation output

**Query submission:**
```javascript
const handleQuery = async () => {
  const response = await axios.post(
    'http://localhost:8001/api/knowledge/query',
    {
      ward: selectedWard,
      rain_intensity: rainIntensity,
      water_level: waterLevel
    }
  );
  setResult(response.data);
  setReasoningSteps(response.data.reasoning);
};
```

### 12.4 State Management

**Context API:** `frontend/src/context/WardContext.jsx`

```javascript
const WardContext = createContext();

export const WardProvider = ({ children }) => {
  const [selectedWard, setSelectedWard] = useState('A');
  const [wardData, setWardData] = useState(null);
  
  const loadWardData = async (wardId) => {
    const response = await axios.get(
      `http://localhost:8001/api/mumbai/ward/${wardId}`
    );
    setWardData(response.data);
  };
  
  return (
    <WardContext.Provider value={{
      selectedWard,
      setSelectedWard,
      wardData,
      loadWardData
    }}>
      {children}
    </WardContext.Provider>
  );
};
```

### 12.5 Data Visualization

**Library:** Recharts

**Example chart:**
```javascript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

<LineChart data={riskData} width={600} height={300}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="time" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="risk_score" stroke="#ef4444" />
  <Line type="monotone" dataKey="water_level" stroke="#3b82f6" />
</LineChart>
```

---

## 13. HOW TO RUN THE SYSTEM

### 13.1 Prerequisites

**Required software:**
- Python 3.13 (or 3.10+)
- Node.js 18+ and npm
- Git

**Check installations:**
```bash
python3 --version  # Should show 3.13.x
node --version     # Should show v18.x or higher
npm --version      # Should show 9.x or higher
```

### 13.2 Initial Setup

#### Step 1: Clone Repository
```bash
cd ~/DIGITAL_TWIN
git clone <repository-url> AI_Strategic_Risk_Engine
cd AI_Strategic_Risk_Engine
```

#### Step 2: Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

**Key dependencies:**
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- numpy
- pandas
- loguru

#### Step 3: Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

**Key dependencies:**
- react
- react-router-dom
- axios
- recharts
- vite

#### Step 4: Verify Environment File
```bash
cat .env
```

**Should contain:**
```
DATABASE_URL=sqlite:///./dev.db
APP_ENV=development
APP_VERSION=0.1.0
```

### 13.3 Running the System

#### Method 1: Using Startup Scripts (RECOMMENDED)

**Terminal 1 - Backend:**
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
./start_frontend.sh
```

#### Method 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
uvicorn backend.main:app --reload --port 8001
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Terminal 2 - Frontend:**
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
npm run dev
```

**Expected output:**
```
VITE v5.4.21  ready in 1004 ms

➜  Local:   http://localhost:8081/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### 13.4 Accessing the System

**Frontend Application:**
- URL: http://localhost:8081
- Main dashboard with navigation

**Backend API Documentation:**
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

**Health Check:**
```bash
curl http://localhost:8001/api/health/live
```

**Expected response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-04-01T14:30:00"
}
```

### 13.5 Testing the System

#### Test 1: Grid Initialization
```bash
curl -X POST http://localhost:8001/api/evacuation/reset-all
```

#### Test 2: Get Grid Data
```bash
curl http://localhost:8001/api/evacuation/grid?ward_id=A
```

#### Test 3: Create Agents
```bash
curl -X POST http://localhost:8001/api/evacuation/create-agents \
  -H "Content-Type: application/json" \
  -d '{"agents_per_zone": 5}'
```

#### Test 4: Run Simulation Step
```bash
curl -X POST http://localhost:8001/api/evacuation/simulation-step
```

### 13.6 Troubleshooting

#### Problem: Port already in use

**Backend (port 8001):**
```bash
lsof -i :8001
kill -9 <PID>
```

**Frontend (port 8081):**
```bash
lsof -i :8081
kill -9 <PID>
```

#### Problem: Module not found

**Backend:**
```bash
pip3 install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

#### Problem: CORS errors

**Check backend CORS configuration in `backend/main.py`:**
```python
allow_origins=["*"]  # Should allow all origins
```

#### Problem: Database connection failed

**Check .env file exists in project root:**
```bash
ls -la .env
cat .env
```

### 13.7 Stopping the System

**Stop backend:** Press `Ctrl+C` in backend terminal

**Stop frontend:** Press `Ctrl+C` in frontend terminal

**Kill all processes:**
```bash
pkill -f "uvicorn backend.main"
pkill -f "vite"
```

---

## 14. API DOCUMENTATION WITH EXAMPLES

### 14.1 Complete API Reference

#### 14.1.1 Evacuation System APIs

**1. Reset Grid**
```http
POST /api/evacuation/reset-all
```

**Response:**
```json
{
  "message": "Grid reset successfully",
  "grid_size": "20x20",
  "total_grids": 400,
  "dangerous_zones": 45,
  "safe_zones": 120,
  "evacuation_points": 18
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8001/api/evacuation/reset-all
```

**2. Get Grid Data**
```http
GET /api/evacuation/grid?ward_id=A
```

**Response:**
```json
{
  "grid_rows": 20,
  "grid_cols": 20,
  "grids": [
    {
      "id": "A1",
      "name": "Colaba",
      "row": 0,
      "col": 0,
      "latitude": 18.9067,
      "longitude": 72.8147,
      "risk_score": 0.75,
      "population_density": 8000,
      "water_level": 1.8,
      "rainfall": 65.5,
      "infrastructure_status": "operational",
      "safety_level": "DANGEROUS",
      "color": "#ef4444",
      "is_evacuation_point": false,
      "is_passable": false
    }
  ]
}
```

**Example with curl:**
```bash
curl "http://localhost:8001/api/evacuation/grid?ward_id=A"
```

**3. Create Human Agents**
```http
POST /api/evacuation/create-agents
Content-Type: application/json

{
  "agents_per_zone": 5
}
```

**Response:**
```json
{
  "agents_created": 75,
  "total_agents": 75,
  "dangerous_zones": 15,
  "agents_by_age": {
    "child": 25,
    "adult": 25,
    "elderly": 25
  }
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8001/api/evacuation/create-agents \
  -H "Content-Type: application/json" \
  -d '{"agents_per_zone": 5}'
```

**4. Assign Evacuation Paths**
```http
POST /api/evacuation/assign-paths
```

**Response:**
```json
{
  "paths_assigned": 75,
  "agents_evacuating": 70,
  "agents_stuck": 5,
  "average_path_length": 12.3
}
```

**5. Simulate Step**
```http
POST /api/evacuation/simulation-step
```

**Response:**
```json
{
  "step": 42,
  "movements": [
    {
      "agent_id": "abc123",
      "from": {"grid_id": "A1", "row": 0, "col": 0},
      "to": {"grid_id": "A2", "row": 0, "col": 1},
      "health": 95,
      "status": "EVACUATING"
    }
  ],
  "stats": {
    "total_agents": 75,
    "evacuating": 45,
    "safe": 25,
    "stuck": 5,
    "average_health": 87.3,
    "completion_rate": 33.3
  },
  "agents": [...]
}
```

**6. Get Evacuation Paths**
```http
GET /api/evacuation/paths
```

**Response:**
```json
{
  "paths": [
    {
      "start_grid": "A1",
      "goal_grid": "E5",
      "path_ids": ["A1", "B1", "C1", "D2", "E3", "E4", "E5"],
      "path_length": 7,
      "average_risk": 0.35,
      "grids_avoided": 8,
      "agents_using": 5
    }
  ],
  "total_paths": 12
}
```


#### 14.1.2 Infrastructure (Bayesian Network) APIs

**1. Get Network Status**
```http
GET /api/infrastructure/network/status
```

**Response:**
```json
{
  "timestep": 42,
  "nodes": [
    {
      "node_id": "POWER_001",
      "node_type": "Utility",
      "name": "Colaba Power Station",
      "ward": "A",
      "probabilities": {
        "HEALTHY": 0.65,
        "DEGRADED": 0.25,
        "FAILED": 0.10
      },
      "current_state": "HEALTHY",
      "health_score": 77.5,
      "risk_score": 22.5
    }
  ],
  "total_nodes": 50,
  "total_dependencies": 85,
  "average_health": 75.3,
  "average_risk": 24.7,
  "critical_nodes": ["POWER_001", "HOSP_003"]
}
```

**Example with curl:**
```bash
curl http://localhost:8001/api/infrastructure/network/status
```

**2. Update Network with Evidence**
```http
POST /api/infrastructure/network/update
Content-Type: application/json

{
  "RainIntensity": 0.8,
  "FloodLevel": 0.6,
  "CyberAttack": 0.0,
  "PowerStress": 0.5,
  "WaterStress": 0.3
}
```

**Response:**
```json
{
  "updated": true,
  "timestep": 43,
  "evidence_applied": {
    "RainIntensity": 0.8,
    "FloodLevel": 0.6,
    "CyberAttack": 0.0,
    "PowerStress": 0.5,
    "WaterStress": 0.3
  },
  "nodes_affected": 35,
  "average_health_change": -5.2
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8001/api/infrastructure/network/update \
  -H "Content-Type: application/json" \
  -d '{
    "RainIntensity": 0.8,
    "FloodLevel": 0.6,
    "CyberAttack": 0.0,
    "PowerStress": 0.5,
    "WaterStress": 0.3
  }'
```

**3. Get Cascading Failure Analysis**
```http
GET /api/infrastructure/cascade/analysis
```

**Response:**
```json
{
  "cascade_events": [
    {
      "source_node": "POWER_001",
      "affected_nodes": ["HOSP_001", "WATER_002", "DATA_001"],
      "cascade_depth": 2,
      "severity": "HIGH",
      "probability": 0.42,
      "explanation": "Power failure cascades to 3 dependent nodes"
    }
  ],
  "total_cascades": 5,
  "most_vulnerable": "HOSP_001"
}
```

#### 14.1.3 Knowledge Engine APIs

**1. Query Knowledge Base**
```http
POST /api/knowledge/query
Content-Type: application/json

{
  "ward": "A",
  "rain_intensity": 85,
  "water_level": 2.0,
  "population": 65000,
  "infrastructure_status": "damaged"
}
```

**Response:**
```json
{
  "disaster_type": "SEVERE_FLOOD",
  "risk_level": "CRITICAL",
  "confidence": 0.95,
  "actions": [
    "IMMEDIATE_EVACUATION",
    "DEPLOY_EMERGENCY_SERVICES",
    "ACTIVATE_BACKUP_POWER",
    "ESTABLISH_RELIEF_CENTERS"
  ],
  "reasoning": [
    "Rain intensity (85mm/hr) exceeds critical threshold (50mm/hr)",
    "Water level (2.0m) indicates severe flooding",
    "Population (65000) at high risk",
    "Infrastructure damage compounds the crisis"
  ],
  "rules_applied": [
    "Flood Detection Rule",
    "Evacuation Trigger Rule",
    "Critical Infrastructure Rule"
  ]
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8001/api/knowledge/query \
  -H "Content-Type: application/json" \
  -d '{
    "ward": "A",
    "rain_intensity": 85,
    "water_level": 2.0,
    "population": 65000,
    "infrastructure_status": "damaged"
  }'
```

**2. Get Inference Trace**
```http
GET /api/knowledge/trace
```

**Response:**
```json
{
  "inference_steps": [
    {
      "step": 1,
      "rule_name": "Flood Detection Rule",
      "premises": ["RainIntensity > 50", "WaterLevel > 1.0"],
      "conclusion": "FloodActive",
      "satisfied": true
    },
    {
      "step": 2,
      "rule_name": "Evacuation Trigger Rule",
      "premises": ["FloodActive", "PopulationDensity > 5000"],
      "conclusion": "EvacuationRequired(Ward_A)",
      "satisfied": true
    }
  ],
  "total_steps": 2,
  "facts_derived": ["FloodActive", "EvacuationRequired(Ward_A)"]
}
```


#### 14.1.4 Mumbai Data APIs

**1. Get Ward Data**
```http
GET /api/mumbai/ward/A
```

**Response:**
```json
{
  "ward_id": "A",
  "ward_name": "Colaba",
  "latitude": 18.9067,
  "longitude": 72.8147,
  "population": 65000,
  "area_sq_km": 2.3,
  "elevation": 5,
  "flood_prone": true,
  "current_conditions": {
    "rain_intensity": 45.2,
    "water_level": 0.8,
    "risk_score": 0.65
  }
}
```

**2. Get Real-time Sensor Data**
```http
GET /api/mumbai/sensors/realtime
```

**Response:**
```json
{
  "rain_sensors": [
    {
      "sensor_id": "RAIN_A_001",
      "ward": "A",
      "rainfall_mm_per_hour": 45.2,
      "cumulative_24h": 156.8,
      "timestamp": "2026-04-01T14:30:00"
    }
  ],
  "water_level_sensors": [
    {
      "sensor_id": "WATER_A_001",
      "ward": "A",
      "water_level_m": 0.8,
      "flow_rate": 12.5,
      "timestamp": "2026-04-01T14:30:00"
    }
  ]
}
```

### 14.2 API Usage Patterns

#### Pattern 1: Complete Evacuation Simulation

```bash
# Step 1: Reset grid
curl -X POST http://localhost:8001/api/evacuation/reset-all

# Step 2: Create agents
curl -X POST http://localhost:8001/api/evacuation/create-agents \
  -H "Content-Type: application/json" \
  -d '{"agents_per_zone": 5}'

# Step 3: Assign paths
curl -X POST http://localhost:8001/api/evacuation/assign-paths

# Step 4: Run simulation (repeat multiple times)
for i in {1..50}; do
  curl -X POST http://localhost:8001/api/evacuation/simulation-step
  sleep 1
done

# Step 5: Get final statistics
curl http://localhost:8001/api/evacuation/paths
```

#### Pattern 2: Infrastructure Monitoring

```bash
# Step 1: Get initial state
curl http://localhost:8001/api/infrastructure/network/status

# Step 2: Apply disaster evidence
curl -X POST http://localhost:8001/api/infrastructure/network/update \
  -H "Content-Type: application/json" \
  -d '{"RainIntensity": 0.8, "FloodLevel": 0.6}'

# Step 3: Check cascading failures
curl http://localhost:8001/api/infrastructure/cascade/analysis

# Step 4: Monitor over time (repeat)
for i in {1..10}; do
  curl http://localhost:8001/api/infrastructure/network/status
  sleep 5
done
```

#### Pattern 3: Knowledge-Based Decision Making

```bash
# Query for specific ward
curl -X POST http://localhost:8001/api/knowledge/query \
  -H "Content-Type: application/json" \
  -d '{
    "ward": "A",
    "rain_intensity": 85,
    "water_level": 2.0,
    "population": 65000
  }'

# Get reasoning trace
curl http://localhost:8001/api/knowledge/trace
```

---

## 15. SYSTEM INTEGRATION FLOW

### 15.1 Complete System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                          │
│              (Frontend - React Application)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    HTTP REST API Calls
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  API Routes Layer                                   │    │
│  │  - Receive requests                                 │    │
│  │  - Validate data                                    │    │
│  │  - Route to appropriate service                     │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 1: Grid Engine                              │    │
│  │  - Load Mumbai ward data                           │    │
│  │  - Initialize 20x20 grid                           │    │
│  │  - Update with sensor data                         │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 2: Pathfinding                              │    │
│  │  - Calculate A* paths                              │    │
│  │  - Avoid dangerous zones                           │    │
│  │  - Optimize for safety                             │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 3: Multi-Agent System                       │    │
│  │  - Create human agents                             │    │
│  │  - Create car agents                               │    │
│  │  - Simulate movement                               │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 4: Bayesian Network                         │    │
│  │  - Model infrastructure                            │    │
│  │  - Apply evidence                                  │    │
│  │  - Propagate beliefs                               │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 5: Knowledge Engine                         │    │
│  │  - Apply rules                                     │    │
│  │  - Perform inference                               │    │
│  │  - Generate recommendations                        │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 6: Learning Layer                           │    │
│  │  - Learn from outcomes                             │    │
│  │  - Update policies                                 │    │
│  │  - Improve strategies                              │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Layer 7: Explainable AI                           │    │
│  │  - Generate explanations                           │    │
│  │  - Create reasoning traces                         │    │
│  │  - Log decisions                                   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    JSON Response
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA PERSISTENCE                          │
│  - SQLite Database (dev.db)                                 │
│  - CSV Files (outputs/)                                     │
│  - Checkpoint Files (demo_checkpoints/)                     │
└─────────────────────────────────────────────────────────────┘
```


### 15.2 Data Flow Example: Evacuation Scenario

**Scenario:** Heavy rain detected in Colaba (Ward A)

**Step-by-step flow:**

```
1. SENSOR DATA ARRIVES
   - Rain sensor: 85mm/hr
   - Water level sensor: 2.0m
   ↓

2. FRONTEND DETECTS ALERT
   - Dashboard shows red alert
   - User clicks "Start Evacuation"
   ↓

3. API CALL: POST /api/evacuation/reset-all
   - Backend receives request
   ↓

4. LAYER 1 (Grid Engine) ACTIVATES
   - Loads Mumbai ward data from mumbai_wards.csv
   - Creates 20x20 grid (400 zones)
   - Maps Colaba to grids A1, A2, B1, B2
   - Updates risk scores based on sensor data
   - Marks Colaba grids as DANGEROUS
   ↓

5. API CALL: POST /api/evacuation/create-agents
   - Request: {"agents_per_zone": 5}
   ↓

6. LAYER 3 (Multi-Agent) CREATES AGENTS
   - Identifies 4 dangerous zones in Colaba
   - Creates 20 human agents (4 zones × 5 agents)
   - Assigns age groups: 7 children, 7 adults, 6 elderly
   - Sets initial positions in dangerous zones
   ↓

7. API CALL: POST /api/evacuation/assign-paths
   ↓

8. LAYER 2 (Pathfinding) CALCULATES ROUTES
   - For each agent:
     a. Find nearest safe zone (e.g., Bandra E5)
     b. Run A* algorithm
     c. Calculate heuristic: distance + risk penalty
     d. Explore neighbors, avoid dangerous zones
     e. Return optimal path
   - Agent 1: A1 → B1 → C2 → D3 → E4 → E5 (12 steps)
   - Agent 2: A2 → B2 → C3 → D4 → E5 (10 steps)
   ↓

9. LAYER 4 (Bayesian Network) PREDICTS FAILURES
   - Evidence: RainIntensity=0.85, FloodLevel=0.6
   - Updates power station: P(FAILED) = 0.35
   - Propagates to hospital: P(FAILED) = 0.42
   - Identifies cascade risk
   ↓

10. LAYER 5 (Knowledge Engine) REASONS
    - Fact: RainIntensity = 85 > 50
    - Fact: WaterLevel = 2.0 > 1.0
    - Rule: IF RainIntensity > 50 AND WaterLevel > 1.0 THEN FloodActive
    - Conclusion: FloodActive = TRUE
    - Rule: IF FloodActive AND Population > 5000 THEN EvacuationRequired
    - Conclusion: EvacuationRequired(Colaba) = TRUE
    ↓

11. LAYER 7 (XAI) GENERATES EXPLANATION
    - "Evacuation triggered because:"
    - "1. Rain intensity (85mm/hr) exceeds critical threshold"
    - "2. Water level (2.0m) indicates severe flooding"
    - "3. 20 people at immediate risk"
    - "4. Selected routes avoid 8 dangerous zones"
    ↓

12. API CALL: POST /api/evacuation/simulation-step (repeated)
    ↓

13. LAYER 3 (Multi-Agent) SIMULATES MOVEMENT
    - Timestep 1: Agents move from A1 → B1
    - Timestep 2: Agents move from B1 → C2
    - Health decreases in risky zones
    - Cars pick up agents
    - Continue until all safe
    ↓

14. LAYER 6 (Learning) RECORDS OUTCOME
    - Scenario: Heavy rain in Colaba
    - Action: Evacuation via route through Bandra
    - Outcome: 18/20 agents saved (90% success)
    - Time: 45 timesteps
    - Store experience for future learning
    ↓

15. FRONTEND DISPLAYS RESULTS
    - Grid visualization with agent positions
    - Statistics: 18 safe, 2 stuck, 90% completion
    - Explanation panel shows reasoning
    - Charts show risk over time
```

### 15.3 Key Integration Points

**1. Data Layer → Grid Engine**
- CSV files loaded into grid zones
- Real-time sensor data updates grid conditions

**2. Grid Engine → Pathfinding**
- Grid topology and neighbor relationships
- Risk scores and passability information

**3. Pathfinding → Multi-Agent**
- Optimal evacuation routes
- Safe zone locations

**4. Multi-Agent → Bayesian Network**
- Agent positions affect infrastructure load
- Evacuation progress influences resource allocation

**5. Bayesian Network → Knowledge Engine**
- Infrastructure failure probabilities
- Cascading failure predictions

**6. Knowledge Engine → Learning Layer**
- Logical conclusions and recommendations
- Rule satisfaction outcomes

**7. All Layers → Explainable AI**
- Decision traces from each layer
- Reasoning logs and explanations

**8. Backend → Frontend**
- JSON responses via REST API
- Real-time updates via polling

---

## 16. CONCLUSION

### 16.1 System Capabilities Summary

This AI Strategic Risk Engine demonstrates:

1. **Spatial Intelligence**: 20x20 grid representation of Mumbai
2. **Optimal Planning**: A* pathfinding for evacuation routes
3. **Behavioral Simulation**: Multi-agent system with human + vehicle agents
4. **Probabilistic Reasoning**: Bayesian networks for infrastructure
5. **Symbolic Logic**: Rule-based knowledge engine
6. **Adaptive Learning**: Reinforcement learning from outcomes
7. **Transparency**: Explainable AI for all decisions

### 16.2 Technical Achievements

- **7-layer AI architecture** integrating multiple AI paradigms
- **Real-time simulation** with 400 grid zones and 100+ agents
- **Hybrid AI** combining neural and symbolic approaches
- **Full-stack implementation** with modern web technologies
- **Comprehensive API** with 20+ endpoints
- **Interactive visualization** with React frontend

### 16.3 Real-World Applications

- **Disaster Management**: Mumbai flood response planning
- **Urban Planning**: Infrastructure resilience assessment
- **Emergency Services**: Optimal resource allocation
- **Policy Making**: Evidence-based decision support
- **Training**: Emergency responder simulation

### 16.4 Future Enhancements

1. **Machine Learning**: Deep learning for pattern recognition
2. **IoT Integration**: Real sensor data from Mumbai
3. **Mobile App**: Citizen alert and guidance system
4. **3D Visualization**: Immersive city model
5. **Multi-city**: Extend to other Indian cities

### 16.5 Faculty Presentation Tips

**Key Points to Emphasize:**

1. **Novelty**: 7-layer architecture is unique
2. **Completeness**: End-to-end system from data to UI
3. **Explainability**: Every decision is transparent
4. **Scalability**: Can handle larger cities
5. **Impact**: Saves lives in real disasters

**Demo Flow:**
1. Show grid initialization (Layer 1)
2. Demonstrate A* pathfinding (Layer 2)
3. Run evacuation simulation (Layer 3)
4. Display infrastructure failures (Layer 4)
5. Query knowledge engine (Layer 5)
6. Show learning progress (Layer 6)
7. Explain decisions (Layer 7)

**Questions to Anticipate:**
- Why 7 layers? → Each layer has distinct AI technique
- Why not just neural networks? → Hybrid AI is more reliable
- How accurate are predictions? → Based on historical Mumbai data
- Can it scale? → Yes, grid size is configurable
- Is it production-ready? → Proof of concept, needs real sensors

---

## APPENDIX

### A. File Structure Reference

```
AI_Strategic_Risk_Engine/
├── backend/
│   ├── api/                    # API routes
│   ├── core/                   # AI layers
│   │   ├── analytics_engine/
│   │   ├── cascading_engine/
│   │   ├── explainable_ai/
│   │   ├── infrastructure/
│   │   ├── knowledge_engine/
│   │   ├── learning_layer/
│   │   └── multi_agent_system/
│   ├── evacuation_system/      # Grid + agents
│   ├── data_loaders/           # Data processing
│   ├── database/               # Database schemas
│   ├── main.py                 # FastAPI app
│   └── config.py               # Configuration
├── frontend/
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── pages/              # Application pages
│   │   ├── context/            # State management
│   │   └── services/           # API calls
│   └── package.json
├── data/
│   └── mumbai/
│       ├── static/             # Fixed data
│       ├── historical/         # Past events
│       ├── realtime/           # Sensor data
│       └── outputs/            # Results
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

### B. Key Algorithms Pseudocode

**A* Pathfinding:**
```
function A_STAR(start, goal):
    open_set = PriorityQueue()
    open_set.add(start, f_cost=0)
    closed_set = Set()
    
    while open_set not empty:
        current = open_set.pop_min()
        
        if current == goal:
            return reconstruct_path(current)
        
        closed_set.add(current)
        
        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue
            
            g_cost = current.g_cost + movement_cost(current, neighbor)
            h_cost = heuristic(neighbor, goal)
            f_cost = g_cost + h_cost
            
            open_set.add(neighbor, f_cost)
    
    return NO_PATH_FOUND
```

**Bayesian Belief Propagation:**
```
function PROPAGATE_BELIEFS(network):
    for each node in network:
        if node has no parents:
            continue
        
        total_influence = 0
        for each parent in node.parents:
            influence = parent.P(FAILED) * edge_weight
            total_influence += influence
        
        node.P(FAILED) += total_influence * propagation_factor
        normalize_probabilities(node)
```

### C. Contact and Support

**Project Repository:** [GitHub URL]
**Documentation:** This file
**API Docs:** http://localhost:8001/docs
**Issues:** [GitHub Issues URL]

---

**END OF DOCUMENTATION**

**Document Version:** 1.0  
**Last Updated:** April 1, 2026  
**Total Pages:** 50+  
**Total Words:** 15,000+

This documentation covers every aspect of the AI Strategic Risk Engine system, from data structures to API endpoints, from algorithms to user interfaces. Use it as a comprehensive reference for your faculty presentation.
