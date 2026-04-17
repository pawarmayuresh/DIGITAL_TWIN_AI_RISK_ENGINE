# FACULTY PRESENTATION QUICK GUIDE
## AI Strategic Risk Engine - Mumbai Digital Twin

**5-Minute Overview for Faculty Presentation**

---

## WHAT IS THIS SYSTEM?

An AI-powered Digital Twin of Mumbai that simulates disaster scenarios and provides intelligent evacuation planning with complete explainability.

**Key Innovation:** 7-layer AI architecture combining multiple AI techniques (symbolic, probabilistic, learning, explainable)

---

## SYSTEM AT A GLANCE

### Technology Stack
- **Backend:** Python + FastAPI
- **Frontend:** React + Vite
- **AI:** Custom implementations (A*, Bayesian Networks, Symbolic Logic)
- **Data:** Mumbai ward data, sensor data, historical floods

### URLs
- **Frontend:** http://localhost:8081
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

---

## 7 AI LAYERS EXPLAINED

### Layer 1: Grid Engine (Spatial)
- **What:** Divides Mumbai into 20×20 grid (400 zones)
- **File:** `backend/evacuation_system/grid_engine.py`
- **Key Function:** `MumbaiGridEngine._initialize_grids()`
- **Output:** Grid zones with risk scores, water levels, safety status

### Layer 2: A* Pathfinding (Search)
- **What:** Finds optimal evacuation routes avoiding danger
- **File:** `backend/evacuation_system/pathfinder.py`
- **Key Function:** `EvacuationPathfinder.find_path(start, goal)`
- **Algorithm:** A* with heuristic = Manhattan distance + risk penalty

### Layer 3: Multi-Agent System (Behavior)
- **What:** Simulates people and vehicles evacuating
- **Files:** `human_agent_sim.py`, `car_agent.py`
- **Agents:** 100+ human agents, 10+ car agents
- **Behavior:** Age-based speed, health tracking, state machines

### Layer 4: Bayesian Network (Probabilistic)
- **What:** Models infrastructure failure propagation
- **File:** `backend/core/infrastructure/bayesian_network.py`
- **Key Concept:** P(Hospital fails | Power fails, Water fails)
- **Output:** Failure probabilities, cascading predictions

### Layer 5: Knowledge Engine (Symbolic)
- **What:** Rule-based reasoning using logic
- **File:** `backend/core/knowledge_engine/knowledge_base.py`
- **Logic Types:** Propositional, First-Order, Second-Order
- **Example Rule:** IF RainIntensity > 50 AND WaterLevel > 1.0 THEN FloodActive

### Layer 6: Learning Layer (Adaptive)
- **What:** Learns from simulation outcomes
- **File:** `backend/core/learning_layer/simulation_trainer.py`
- **Method:** Reinforcement learning
- **Improves:** Evacuation strategies, resource allocation

### Layer 7: Explainable AI (Transparency)
- **What:** Explains every AI decision
- **File:** `backend/core/explainable_ai/path_explainer.py`
- **Output:** Natural language explanations, reasoning traces
- **Example:** "Route selected because it avoids 3 high-risk zones and is 35% safer"

---

## KEY DATASETS

### 1. mumbai_wards.csv
- Ward boundaries, population, elevation, flood history
- Used for: Grid initialization, risk baseline

### 2. infrastructure_nodes.csv
- Power stations, hospitals, water treatment, emergency services
- Used for: Bayesian network construction

### 3. flood_events.csv
- Historical Mumbai floods (2005, 2017, 2019)
- Used for: Model training, validation

### 4. Real-time Sensors (Simulated)
- rain_sensors.csv: Rainfall intensity
- water_level_sensors.csv: Flood levels
- Used for: Real-time grid updates

---

## HOW IT WORKS: COMPLETE FLOW

```
1. Sensor detects heavy rain (85mm/hr) in Colaba
   ↓
2. Grid Engine marks Colaba as DANGEROUS
   ↓
3. Multi-Agent creates 20 people in danger zone
   ↓
4. A* Pathfinding calculates safe routes to Bandra
   ↓
5. Bayesian Network predicts power failure (35% probability)
   ↓
6. Knowledge Engine infers: EvacuationRequired = TRUE
   ↓
7. Agents start moving along calculated paths
   ↓
8. Learning Layer records outcome for future improvement
   ↓
9. XAI explains: "Evacuation triggered because rain exceeds 
   threshold and 20 people at risk. Route avoids 8 dangerous zones."
```

---

## A* ALGORITHM EXPLAINED

**Problem:** Find shortest + safest path from danger zone to safe zone

**Solution:** A* with custom cost function

```python
# Cost function
f_cost = g_cost + h_cost

# g_cost = actual cost from start
g_cost = distance + risk_penalty + water_penalty

# h_cost = estimated cost to goal
h_cost = manhattan_distance + safety_penalty

# Movement cost
cost = 1.0 + (risk_score × 10) + (water_level × 3)
```

**Why A*?**
- Optimal: Guaranteed shortest path
- Efficient: Explores fewer nodes than Dijkstra
- Flexible: Custom cost function for safety

---

## BAYESIAN NETWORK EXPLAINED

**Problem:** Predict infrastructure failures and cascades

**Solution:** Probabilistic graphical model

**Example:**
```
Power Station → Hospital
P(Hospital fails | Power healthy) = 0.02
P(Hospital fails | Power failed) = 0.40

Evidence: Heavy rain
→ P(Power fails) increases from 0.05 to 0.35
→ P(Hospital fails) increases from 0.02 to 0.42
```

**Significance:**
- Models uncertainty (not deterministic)
- Captures dependencies (cascading failures)
- Integrates real-time evidence (sensor data)

---

## KNOWLEDGE ENGINE EXPLAINED

**Problem:** Make logical decisions based on rules

**Solution:** Symbolic AI with forward/backward chaining

**Example Rules:**
```
Rule 1: IF RainIntensity > 50 AND WaterLevel > 1.0 
        THEN FloodActive

Rule 2: IF FloodActive AND PopulationDensity > 5000 
        THEN EvacuationRequired

Rule 3: IF EvacuationRequired AND InfrastructureDamaged 
        THEN DeployEmergencyServices
```

**Inference:**
```
Facts: RainIntensity=85, WaterLevel=2.0, Population=8000
Apply Rule 1: FloodActive = TRUE
Apply Rule 2: EvacuationRequired = TRUE
Apply Rule 3: DeployEmergencyServices = TRUE
```

---

## GRID SIMULATION EXPLAINED

**Grid Structure:**
- 20 rows × 20 columns = 400 zones
- Each zone: ~1-2 km² of Mumbai
- Real ward mapping: A1=Colaba, E5=Bandra, etc.

**Grid Properties:**
```python
GridZone {
    id: "A1"
    risk_score: 0.75        # 0.0 to 1.0
    water_level: 1.8        # meters
    rainfall: 65.5          # mm/hour
    safety_level: DANGEROUS # SAFE, MEDIUM_RISK, DANGEROUS
    population: 8000        # people in zone
    is_passable: false      # can agents move through?
}
```

**Real-time Updates:**
```python
# Sensor data arrives
water_level = 2.1m
rainfall = 85mm/hr

# Recalculate risk
water_risk = min(1.0, 2.1 / 2.0) = 1.0
rain_risk = min(1.0, 85 / 100.0) = 0.85
risk_score = (1.0 × 0.6) + (0.85 × 0.4) = 0.94

# Update safety
if risk_score > 0.7: safety = DANGEROUS
```

---

## HUMAN BEHAVIOR SIMULATION

**Agent Types:**
- Child: speed=0.8, vulnerable
- Adult: speed=1.0, normal
- Elderly: speed=0.6, slow

**Behavior:**
```python
# Each timestep
for agent in agents:
    if agent.status == EVACUATING:
        next_grid = agent.path[agent.path_index + 1]
        
        if next_grid.is_passable():
            agent.move_to(next_grid)
            
            # Health decreases in risky areas
            if next_grid.risk_score > 0.6:
                agent.health -= int(risk_score × 5)
        
        if agent.current_grid == agent.destination:
            agent.status = SAFE
```

---

## API EXAMPLES

### Start Evacuation
```bash
# Reset grid
curl -X POST http://localhost:8001/api/evacuation/reset-all

# Create agents
curl -X POST http://localhost:8001/api/evacuation/create-agents \
  -H "Content-Type: application/json" \
  -d '{"agents_per_zone": 5}'

# Assign paths
curl -X POST http://localhost:8001/api/evacuation/assign-paths

# Simulate
curl -X POST http://localhost:8001/api/evacuation/simulation-step
```

### Query Knowledge Engine
```bash
curl -X POST http://localhost:8001/api/knowledge/query \
  -H "Content-Type: application/json" \
  -d '{
    "ward": "A",
    "rain_intensity": 85,
    "water_level": 2.0
  }'
```

### Update Infrastructure
```bash
curl -X POST http://localhost:8001/api/infrastructure/network/update \
  -H "Content-Type: application/json" \
  -d '{
    "RainIntensity": 0.8,
    "FloodLevel": 0.6
  }'
```

---

## HOW TO RUN

### Terminal 1: Backend
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
uvicorn backend.main:app --reload --port 8001
```

### Terminal 2: Frontend
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
npm run dev
```

### Access
- Frontend: http://localhost:8081
- API Docs: http://localhost:8001/docs

---

## DEMO SCRIPT FOR FACULTY

### 1. Show API Documentation (1 min)
- Open http://localhost:8001/docs
- Show interactive Swagger UI
- Demonstrate endpoint testing

### 2. Show Frontend Dashboard (1 min)
- Open http://localhost:8081
- Navigate through pages
- Show grid visualization

### 3. Run Evacuation Simulation (2 min)
- Click "Urban Evacuation"
- Click "Reset Grid"
- Click "Create Agents"
- Click "Start Simulation"
- Watch agents move in real-time
- Show statistics updating

### 4. Explain AI Layers (1 min)
- Point to grid (Layer 1)
- Show paths (Layer 2)
- Show agents (Layer 3)
- Open Infrastructure page (Layer 4)
- Open Knowledge Engine (Layer 5)
- Show explanations (Layer 7)

---

## KEY POINTS FOR FACULTY

### Innovation
✓ 7-layer AI architecture (unique)
✓ Hybrid AI (symbolic + probabilistic + learning)
✓ Complete explainability (every decision explained)

### Completeness
✓ Full-stack system (backend + frontend)
✓ Real Mumbai data
✓ 20+ API endpoints
✓ Interactive visualization

### Impact
✓ Saves lives in disasters
✓ Evidence-based policy making
✓ Emergency responder training
✓ Infrastructure planning

### Technical Depth
✓ A* pathfinding implementation
✓ Bayesian network inference
✓ Symbolic logic engine
✓ Multi-agent simulation
✓ Reinforcement learning

---

## QUESTIONS & ANSWERS

**Q: Why 7 layers?**
A: Each layer uses a different AI technique. Together they provide comprehensive disaster management.

**Q: Why not just neural networks?**
A: Hybrid AI is more reliable and explainable. Neural networks are black boxes; our system explains every decision.

**Q: How accurate are predictions?**
A: Based on historical Mumbai flood data (2005, 2017, 2019). Validated against real events.

**Q: Can it scale to larger cities?**
A: Yes, grid size is configurable. Can handle 50×50 (2500 zones) or more.

**Q: Is it production-ready?**
A: Proof of concept. Needs real sensor integration and extensive testing for production.

---

## FULL DOCUMENTATION

For complete details, see: `COMPREHENSIVE_FACULTY_DOCUMENTATION.md`

- 50+ pages
- 15,000+ words
- Every function explained
- All algorithms detailed
- Complete API reference
- Step-by-step examples

---

**END OF QUICK GUIDE**
