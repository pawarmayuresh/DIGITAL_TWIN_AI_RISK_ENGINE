# 🏗️ System Architecture Visual Guide
## AI Strategic Risk Engine - Complete Architecture

---

## 🎯 HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                    http://localhost:8081                            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ City         │  │ Disaster     │  │ Spatial      │            │
│  │ Overview     │  │ Simulation   │  │ Grid         │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Infrastructure│  │ Policy       │  │ Resilience   │            │
│  │ Graph        │  │ Comparison   │  │ Dashboard    │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐                               │
│  │ Risk         │  │ Decision     │                               │
│  │ Heatmap      │  │ Explainer    │                               │
│  └──────────────┘  └──────────────┘                               │
│                                                                     │
│                    React 18 + Vite + React Router                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ REST API (JSON over HTTP)
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                         API GATEWAY                                 │
│                    http://localhost:8000                            │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Health   │ │ Demo     │ │ Twin     │ │Strategic │             │
│  │ Routes   │ │ Routes   │ │ Routes   │ │ Routes   │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Agent    │ │ Learning │ │Explainab.│ │Analytics │             │
│  │ Routes   │ │ Routes   │ │ Routes   │ │ Routes   │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
│  ┌──────────┐                                                      │
│  │ Spatial  │                                                      │
│  │ Routes   │                                                      │
│  └──────────┘                                                      │
│                                                                     │
│                         FastAPI Framework                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Function Calls
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                      CORE AI ENGINES                                │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 2: Spatial Engine                                     │  │
│  │ • GridManager: 20x20 spatial grid                           │  │
│  │ • DiffusionModel: Disaster propagation                      │  │
│  │ • GridCell: Individual cell state                           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 3: Disaster Engine                                    │  │
│  │ • EarthquakeModel: Seismic simulation                       │  │
│  │ • FloodModel: Hydraulic flow                                │  │
│  │ • WildfireModel: Fire spread                                │  │
│  │ • PandemicModel: Disease propagation                        │  │
│  │ • CyberAttackModel: Network attacks                         │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 4: Cascading Engine                                   │  │
│  │ • InfrastructureGraph: Network topology                     │  │
│  │ • CascadingFailureEngine: Failure propagation               │  │
│  │ • RecoveryModel: Restoration planning                       │  │
│  │ • StabilityCalculator: Network stability                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 5: Digital Twin                                       │  │
│  │ • TwinManager: State orchestration                          │  │
│  │ • CityModel: City representation                            │  │
│  │ • PopulationModel: Demographics                             │  │
│  │ • EconomicModel: Economic simulation                        │  │
│  │ • BaselineStateManager: Comparison baseline                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 6: Strategic AI                                       │  │
│  │ • Planner: A* search for optimal plans                      │  │
│  │ • PolicyLibrary: Response strategies                        │  │
│  │ • ResourceAllocator: Resource optimization                  │  │
│  │ • ScenarioComparator: Strategy comparison                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 7: Multi-Agent System                                 │  │
│  │ • AgentManager: Agent coordination                          │  │
│  │ • GovernmentAgent: Policy decisions                         │  │
│  │ • EmergencyAgent: Response operations                       │  │
│  │ • InfrastructureAgent: System management                    │  │
│  │ • CitizenAgent: Population behavior                         │  │
│  │ • CoalitionBuilder: Agent cooperation                       │  │
│  │ • NegotiationEngine: Conflict resolution                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 8: Learning Layer (RL)                                │  │
│  │ • RLAgent: Policy learning                                  │  │
│  │ • ExperienceStore: Memory buffer (10K+ episodes)            │  │
│  │ • RewardModel: Objective function                           │  │
│  │ • AdaptivePolicyLearner: Policy optimization                │  │
│  │ • TrainingPipeline: Training orchestration                  │  │
│  │ • SimulationTrainer: Episode generation                     │  │
│  │ • PolicyEvaluator: Performance testing                      │  │
│  │ • CheckpointManager: Model persistence                      │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 9: Explainable AI                                     │  │
│  │ • DecisionTracer: Decision logging                          │  │
│  │ • CausalGraphGenerator: Cause-effect analysis               │  │
│  │ • SHAPExplainer: Feature importance                         │  │
│  │ • CounterfactualAnalyzer: Alternative scenarios             │  │
│  │ • ConfidenceEstimator: Uncertainty quantification           │  │
│  │ • TransparencyReportBuilder: Human explanations             │  │
│  │ • AuditLogInterpreter: Log analysis                         │  │
│  │ • ExplanationIntegrator: Unified explanations               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ BATCH 10: Analytics Engine                                  │  │
│  │ • KPICalculator: 11+ performance metrics                    │  │
│  │ • EconomicLossEstimator: Financial impact                   │  │
│  │ • ResilienceIndexCalculator: 4D resilience                  │  │
│  │ • SocialStabilityIndex: Social cohesion                     │  │
│  │ • SimulationStatisticsTracker: Data aggregation             │  │
│  │ • BenchmarkingFramework: Performance comparison             │  │
│  │ • ResilienceDashboardMetrics: Dashboard data                │  │
│  │ • ScenarioComparator: Multi-scenario analysis               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAM

```
USER INPUT
    │
    ├─► Select Disaster Type (Earthquake, Flood, etc.)
    ├─► Set Severity (1-10)
    └─► Click "Run Simulation"
    │
    ▼
FRONTEND (React)
    │
    └─► API Call: POST /api/demo/run/earthquake
    │
    ▼
API GATEWAY (FastAPI)
    │
    └─► Route to Demo Routes
    │
    ▼
DISASTER ENGINE
    │
    ├─► Calculate Initial Impact
    │   ├─► Seismic intensity at epicenter
    │   ├─► Affected radius
    │   └─► Initial damage
    │
    ▼
SPATIAL ENGINE
    │
    ├─► Propagate Disaster Across Grid
    │   ├─► Diffusion model (10 timesteps)
    │   ├─► Update each cell intensity
    │   └─► Calculate spatial distribution
    │
    ▼
CASCADING ENGINE
    │
    ├─► Calculate Infrastructure Impact
    │   ├─► Identify damaged nodes
    │   ├─► Propagate failures to dependents
    │   └─► Calculate cascade depth
    │
    ▼
DIGITAL TWIN
    │
    ├─► Update City State
    │   ├─► Population affected
    │   ├─► Infrastructure damage
    │   ├─► Economic impact
    │   └─► Compare to baseline
    │
    ▼
MULTI-AGENT SYSTEM
    │
    ├─► Simulate Agent Responses
    │   ├─► Government: Policy decisions
    │   ├─► Emergency: Response actions
    │   ├─► Infrastructure: Repair priorities
    │   └─► Citizens: Evacuation behavior
    │
    ▼
STRATEGIC AI
    │
    ├─► Generate Response Plans
    │   ├─► A* search for optimal plan
    │   ├─► Resource allocation
    │   └─► Policy recommendations
    │
    ▼
LEARNING LAYER
    │
    ├─► Store Experience
    │   ├─► State: City condition
    │   ├─► Action: Response strategy
    │   ├─► Reward: Outcome quality
    │   └─► Next State: Result
    │
    ▼
EXPLAINABLE AI
    │
    ├─► Log Decision
    │   ├─► Decision trace
    │   ├─► Feature importance (SHAP)
    │   ├─► Confidence score
    │   └─► Audit log entry
    │
    ▼
ANALYTICS ENGINE
    │
    ├─► Calculate Metrics
    │   ├─► KPIs (casualties, damage, cost)
    │   ├─► Economic losses (6 components)
    │   ├─► Resilience index (4 dimensions)
    │   └─► Social stability
    │
    ▼
API RESPONSE
    │
    └─► Return JSON with all results
    │
    ▼
FRONTEND
    │
    └─► Display Results in UI
        ├─► Update grid visualization
        ├─► Show metrics
        ├─► Display recommendations
        └─► Update all dashboards
```

---

## 🧩 MODULE INTERACTION DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                    SIMULATION ORCHESTRATION                     │
│                                                                 │
│  User Initiates Simulation                                      │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                              │
│  │   Disaster   │──────┐                                       │
│  │    Engine    │      │                                       │
│  └──────────────┘      │                                       │
│         │              │                                       │
│         │ Impact Data  │                                       │
│         ▼              │                                       │
│  ┌──────────────┐      │                                       │
│  │   Spatial    │◄─────┘                                       │
│  │    Engine    │                                              │
│  └──────────────┘                                              │
│         │                                                       │
│         │ Grid State                                           │
│         ▼                                                       │
│  ┌──────────────┐                                              │
│  │  Cascading   │                                              │
│  │    Engine    │                                              │
│  └──────────────┘                                              │
│         │                                                       │
│         │ Infrastructure Damage                                │
│         ▼                                                       │
│  ┌──────────────┐      ┌──────────────┐                       │
│  │   Digital    │◄────►│  Multi-Agent │                       │
│  │     Twin     │      │    System    │                       │
│  └──────────────┘      └──────────────┘                       │
│         │                      │                               │
│         │ City State           │ Agent Actions                 │
│         ▼                      ▼                               │
│  ┌──────────────┐      ┌──────────────┐                       │
│  │  Strategic   │◄────►│   Learning   │                       │
│  │      AI      │      │     Layer    │                       │
│  └──────────────┘      └──────────────┘                       │
│         │                      │                               │
│         │ Recommendations      │ Policy Updates                │
│         ▼                      ▼                               │
│  ┌──────────────┐      ┌──────────────┐                       │
│  │ Explainable  │◄────►│  Analytics   │                       │
│  │      AI      │      │    Engine    │                       │
│  └──────────────┘      └──────────────┘                       │
│         │                      │                               │
│         │ Explanations         │ Metrics                       │
│         └──────────┬───────────┘                               │
│                    ▼                                           │
│            ┌──────────────┐                                    │
│            │  API Gateway │                                    │
│            └──────────────┘                                    │
│                    │                                           │
│                    ▼                                           │
│            ┌──────────────┐                                    │
│            │   Frontend   │                                    │
│            └──────────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎓 LEARNING CYCLE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│              REINFORCEMENT LEARNING CYCLE                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. OBSERVE STATE                                         │  │
│  │    • City condition                                      │  │
│  │    • Infrastructure health                               │  │
│  │    • Resource availability                               │  │
│  │    • Disaster severity                                   │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 2. SELECT ACTION (Policy)                                │  │
│  │    • Evacuate population                                 │  │
│  │    • Allocate resources                                  │  │
│  │    • Deploy emergency services                           │  │
│  │    • Repair infrastructure                               │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 3. EXECUTE IN SIMULATION                                 │  │
│  │    • Run disaster simulation                             │  │
│  │    • Apply selected actions                              │  │
│  │    • Calculate outcomes                                  │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 4. OBSERVE NEXT STATE                                    │  │
│  │    • Updated city condition                              │  │
│  │    • Casualties                                          │  │
│  │    • Damage levels                                       │  │
│  │    • Recovery progress                                   │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 5. CALCULATE REWARD                                      │  │
│  │    • Lives saved: +1000 per person                       │  │
│  │    • Damage prevented: +100 per unit                     │  │
│  │    • Action cost: -1 per dollar                          │  │
│  │    • Recovery speed: +50 per day faster                  │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 6. STORE EXPERIENCE                                      │  │
│  │    • (State, Action, Reward, Next State)                 │  │
│  │    • Add to experience buffer                            │  │
│  │    • Buffer size: 10,000+ episodes                       │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 7. TRAIN POLICY                                          │  │
│  │    • Sample batch from experience                        │  │
│  │    • Calculate policy gradient                           │  │
│  │    • Update neural network weights                       │  │
│  │    • Improve action selection                            │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   └────────────────┐                           │
│                                    │                           │
│                   ┌────────────────┘                           │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 8. REPEAT (Better Policy Each Time)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  After 10,000+ episodes: Optimal disaster response policy      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 EXPLAINABILITY FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION EXPLANATION                         │
│                                                                 │
│  AI Makes Decision: "Evacuate Zone A"                          │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ DECISION TRACER                                          │  │
│  │ • Records full decision context                          │  │
│  │ • Timestamp: 2024-01-15 14:30:00                         │  │
│  │ • Decision ID: dec_12345                                 │  │
│  │ • Input features: [risk=0.8, pop=5000, time=2hrs]       │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ SHAP EXPLAINER                                           │  │
│  │ • Feature importance:                                    │  │
│  │   - Risk level: 45% influence                            │  │
│  │   - Population: 30% influence                            │  │
│  │   - Time available: 15% influence                        │  │
│  │   - Resources: 10% influence                             │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ CAUSAL GRAPH                                             │  │
│  │ • High risk → Evacuation needed                          │  │
│  │ • Large population → More resources required             │  │
│  │ • Limited time → Immediate action                        │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ COUNTERFACTUAL ANALYZER                                  │  │
│  │ • What if risk was lower? → Shelter in place            │  │
│  │ • What if more time? → Gradual evacuation                │  │
│  │ • What if fewer people? → Partial evacuation             │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ CONFIDENCE ESTIMATOR                                     │  │
│  │ • Decision confidence: 87%                               │  │
│  │ • Data quality: High                                     │  │
│  │ • Model uncertainty: Low                                 │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ TRANSPARENCY REPORT                                      │  │
│  │ "Evacuation recommended because:                         │  │
│  │  1. Risk level (0.8) exceeds safety threshold (0.6)     │  │
│  │  2. 5,000 people in affected zone                       │  │
│  │  3. Only 2 hours before disaster peak                   │  │
│  │  4. Historical data shows 87% success rate              │  │
│  │  5. Alternative (shelter) has 45% success rate"         │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                            │
│                   ▼                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ AUDIT LOG                                                │  │
│  │ • Permanent record stored                                │  │
│  │ • Accessible for review                                  │  │
│  │ • Compliance ready                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Result: Fully explainable, auditable decision                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 TECHNOLOGY STACK

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ React 18          │ Modern UI framework                  │  │
│  │ Vite              │ Fast build tool & dev server         │  │
│  │ React Router      │ Client-side routing                  │  │
│  │ Axios             │ HTTP client for API calls            │  │
│  │ Lucide React      │ Icon library                         │  │
│  │ SVG               │ Custom visualizations                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Python 3.x        │ Core language                        │  │
│  │ FastAPI           │ Modern web framework                 │  │
│  │ Uvicorn           │ ASGI server                          │  │
│  │ Pydantic          │ Data validation                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML LIBRARIES                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ NumPy             │ Numerical computing                  │  │
│  │ SciPy             │ Scientific algorithms                │  │
│  │ NetworkX          │ Graph algorithms                     │  │
│  │ Custom RL         │ Reinforcement learning               │  │
│  │ Custom XAI        │ Explainability algorithms            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      ARCHITECTURE                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ RESTful API       │ HTTP/JSON communication              │  │
│  │ Modular Design    │ 11 independent modules               │  │
│  │ Microservices     │ Ready for distributed deployment     │  │
│  │ CORS Enabled      │ Cross-origin support                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 SHOW THIS TO FACULTY

This visual guide demonstrates:
1. **System Complexity**: 11 integrated AI modules
2. **Data Flow**: Complete simulation pipeline
3. **AI Integration**: RL, multi-agent, XAI working together
4. **Professional Architecture**: Production-ready design
5. **Full-Stack Implementation**: Frontend + Backend + AI

**Key Message:** This is not just a visualization tool - it's a complete AI system for disaster management with sophisticated algorithms, learning capabilities, and explainability.

