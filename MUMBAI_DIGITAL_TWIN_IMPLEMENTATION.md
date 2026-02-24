# � Mumbai Digital Twin - Real-World Implementation Plan

## 🎯 Project Upgrade: Synthetic → Real Mumbai Data

**Transformation:** Generic city simulation → Mumbai-specific disaster management system

---

## 📊 DATA ASSETS PROVIDED

### ✅ 14 CSV Files with Real Mumbai Data

1. **mumbai_wards.csv** - 10 wards with population, area, slum density
2. **infrastructure_nodes.csv** - Hospitals, power, railway, airport, water
3. **road_nodes.csv** - 5 key road network nodes
4. **road_network_edges.csv** - Road connections with flood risk
5. **rainfall_history.csv** - Historical rainfall events (2005-2023)
6. **flood_events.csv** - Major flood events with casualties & losses
7. **rain_sensors.csv** - Real-time rainfall monitoring
8. **water_level_sensors.csv** - Mithi River & drain monitoring
9. **traffic_density.csv** - Real-time traffic congestion
10. **power_load.csv** - Substation load monitoring
11. **alert_sound_sensors.csv** - Crowd panic detection
12. **ward_risk_scores.csv** - AI-generated risk assessment
13. **explainability_log.csv** - Feature importance for XAI
14. **ai_recommendations.csv** - Action recommendations

### 🗺️ Geographic Coverage
- **Wards:** A (Colaba), E (Byculla), H/E (Bandra East), K/E (Andheri East), P/N (Malad West), R/N (Borivali), L (Kurla)
- **Population:** 185K - 800K per ward
- **Total Coverage:** ~3.4 million people
- **Area:** 72 sq km total

---

## 🏗️ IMPLEMENTATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUMBAI DIGITAL TWIN                          │
│              Real-World Data Integration Layer                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│  STATIC DATA      │ │  REAL-TIME DATA   │ │  HISTORICAL DATA  │
│                   │ │                   │ │                   │
│ • Wards           │ │ • Rain sensors    │ │ • Rainfall hist.  │
│ • Infrastructure  │ │ • Water levels    │ │ • Flood events    │
│ • Road network    │ │ • Traffic         │ │ • Economic loss   │
│ • Population      │ │ • Power load      │ │ • Casualties      │
│                   │ │ • Panic sensors   │ │                   │
└───────────────────┘ └───────────────────┘ └───────────────────┘
                │               │               │
                └───────────────┼───────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ CSV Loader   │  │ Data Cleaner │  │ Validator    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXISTING AI ENGINES                          │
│                                                                 │
│  • Spatial Engine → Mumbai ward grid                           │
│  • Disaster Engine → Flood model (Mithi River)                 │
│  • Cascading Engine → Infrastructure dependencies              │
│  • Digital Twin → Mumbai city state                            │
│  • Multi-Agent → Mumbai stakeholders                           │
│  • Learning Layer → Learn from historical floods               │
│  • Explainable AI → Feature importance (rainfall, slums, etc.) │
│  • Analytics → Mumbai-specific KPIs                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MUMBAI-SPECIFIC FRONTEND                     │
│                                                                 │
│  • Mumbai ward map visualization                               │
│  • Mithi River flood simulation                                │
│  • Real infrastructure network (JJ Hospital, CST, Airport)     │
│  • Historical flood replay (2005, 2020, 2021)                  │
│  • Real-time sensor dashboard                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 FILE STRUCTURE

```
data/
├── mumbai/
│   ├── static/
│   │   ├── mumbai_wards.csv
│   │   ├── infrastructure_nodes.csv
│   │   ├── road_nodes.csv
│   │   └── road_network_edges.csv
│   ├── historical/
│   │   ├── rainfall_history.csv
│   │   └── flood_events.csv
│   ├── realtime/
│   │   ├── rain_sensors.csv
│   │   ├── water_level_sensors.csv
│   │   ├── traffic_density.csv
│   │   ├── power_load.csv
│   │   └── alert_sound_sensors.csv
│   └── outputs/
│       ├── ward_risk_scores.csv
│       ├── explainability_log.csv
│       └── ai_recommendations.csv

backend/
├── data_loaders/
│   ├── mumbai_data_loader.py
│   ├── csv_parser.py
│   └── data_validator.py
├── core/
│   ├── mumbai_twin/
│   │   ├── mumbai_city_model.py
│   │   ├── ward_manager.py
│   │   ├── mithi_river_model.py
│   │   └── mumbai_infrastructure.py
│   └── [existing modules adapted]
└── api/
    └── mumbai_routes.py

frontend/
└── src/
    ├── pages/
    │   ├── MumbaiMap.jsx
    │   ├── MithiRiverMonitor.jsx
    │   ├── WardDashboard.jsx
    │   └── HistoricalFloodReplay.jsx
    └── services/
        └── mumbai_api.js
```

---

## 🔧 IMPLEMENTATION STEPS

### Phase 1: Data Integration (2-3 hours)

#### Step 1.1: Create Data Directory
```bash
mkdir -p data/mumbai/{static,historical,realtime,outputs}
```

#### Step 1.2: Place CSV Files
- Copy all 14 CSV files to appropriate directories

#### Step 1.3: Create Data Loader
**File:** `backend/data_loaders/mumbai_data_loader.py`

```python
import pandas as pd
from pathlib import Path

class MumbaiDataLoader:
    def __init__(self, data_dir='data/mumbai'):
        self.data_dir = Path(data_dir)
        self.wards = None
        self.infrastructure = None
        self.road_network = None
        # ... other datasets
    
    def load_all(self):
        """Load all Mumbai datasets"""
        self.wards = pd.read_csv(self.data_dir / 'static/mumbai_wards.csv')
        self.infrastructure = pd.read_csv(self.data_dir / 'static/infrastructure_nodes.csv')
        self.road_nodes = pd.read_csv(self.data_dir / 'static/road_nodes.csv')
        self.road_edges = pd.read_csv(self.data_dir / 'static/road_network_edges.csv')
        self.rainfall_history = pd.read_csv(self.data_dir / 'historical/rainfall_history.csv')
        self.flood_events = pd.read_csv(self.data_dir / 'historical/flood_events.csv')
        # ... load others
        
        return self
    
    def get_ward(self, ward_id):
        """Get specific ward data"""
        return self.wards[self.wards['ward_id'] == ward_id].iloc[0]
    
    def get_infrastructure_by_ward(self, ward_id):
        """Get all infrastructure in a ward"""
        return self.infrastructure[self.infrastructure['ward_id'] == ward_id]
```

---

### Phase 2: Mumbai Digital Twin Model (3-4 hours)

#### Step 2.1: Mumbai City Model
**File:** `backend/core/mumbai_twin/mumbai_city_model.py`

```python
from backend.data_loaders.mumbai_data_loader import MumbaiDataLoader

class MumbaiCityModel:
    """
    Digital Twin of Mumbai City
    Based on real ward data, infrastructure, and historical events
    """
    
    def __init__(self):
        self.data_loader = MumbaiDataLoader().load_all()
        self.wards = self._initialize_wards()
        self.infrastructure = self._initialize_infrastructure()
        self.mithi_river = MithiRiverModel()
        
    def _initialize_wards(self):
        """Create ward objects from CSV data"""
        wards = {}
        for _, row in self.data_loader.wards.iterrows():
            wards[row['ward_id']] = {
                'name': row['ward_name'],
                'zone': row['zone'],
                'population': row['population'],
                'area_sqkm': row['area_sqkm'],
                'slum_percent': row['slum_population_percent'],
                'density': row['population_density'],
                'current_flood_level': 0,
                'risk_score': 0
            }
        return wards
    
    def simulate_rainfall(self, ward_id, rainfall_mm):
        """Simulate rainfall impact on specific ward"""
        ward = self.wards[ward_id]
        
        # Calculate flood risk based on real factors
        base_risk = rainfall_mm / 1000  # Normalize
        slum_factor = ward['slum_percent'] / 100 * 0.3  # Slums more vulnerable
        density_factor = ward['density'] / 100000 * 0.2  # Higher density = more risk
        
        flood_risk = base_risk + slum_factor + density_factor
        
        # Check if roads are flood-prone
        ward_roads = self._get_ward_roads(ward_id)
        if any(road['flood_prone_flag'] == 'Yes' for road in ward_roads):
            flood_risk *= 1.5
        
        ward['risk_score'] = min(flood_risk, 1.0)
        ward['current_flood_level'] = rainfall_mm * 0.5  # Simplified
        
        return ward
```

---

### Phase 3: Mithi River Flood Model (2-3 hours)

**File:** `backend/core/mumbai_twin/mithi_river_model.py`

```python
class MithiRiverModel:
    """
    Model of Mithi River - Mumbai's main flood risk
    Based on real water level sensor data
    """
    
    def __init__(self):
        self.segments = {
            'Sion': {'threshold': 300, 'current': 0, 'affected_wards': ['E', 'G/N']},
            'Andheri': {'threshold': 300, 'current': 0, 'affected_wards': ['K/E']},
            'Kurla': {'threshold': 200, 'current': 0, 'affected_wards': ['L', 'M/E']}
        }
    
    def update_water_levels(self, sensor_data):
        """Update from real sensor data"""
        for sensor in sensor_data:
            location = sensor['location']
            if location in self.segments:
                self.segments[location]['current'] = sensor['water_level_cm']
    
    def get_flood_risk(self):
        """Calculate flood risk for each segment"""
        risks = {}
        for location, data in self.segments.items():
            if data['current'] > data['threshold']:
                risk_level = (data['current'] - data['threshold']) / data['threshold']
                risks[location] = {
                    'risk': min(risk_level, 1.0),
                    'affected_wards': data['affected_wards'],
                    'overflow': data['current'] - data['threshold']
                }
        return risks
```

---

### Phase 4: API Routes (1-2 hours)

**File:** `backend/api/mumbai_routes.py`

```python
from fastapi import APIRouter
from backend.core.mumbai_twin.mumbai_city_model import MumbaiCityModel
from backend.data_loaders.mumbai_data_loader import MumbaiDataLoader

router = APIRouter(prefix="/api/mumbai", tags=["mumbai"])

mumbai_twin = MumbaiCityModel()
data_loader = MumbaiDataLoader().load_all()

@router.get("/wards")
async def get_all_wards():
    """Get all Mumbai wards"""
    return mumbai_twin.wards

@router.get("/ward/{ward_id}")
async def get_ward(ward_id: str):
    """Get specific ward details"""
    return mumbai_twin.wards.get(ward_id)

@router.get("/infrastructure")
async def get_infrastructure():
    """Get all infrastructure nodes"""
    return data_loader.infrastructure.to_dict('records')

@router.get("/mithi-river/status")
async def get_mithi_status():
    """Get Mithi River current status"""
    return mumbai_twin.mithi_river.get_flood_risk()

@router.post("/simulate/rainfall")
async def simulate_rainfall(ward_id: str, rainfall_mm: float):
    """Simulate rainfall on specific ward"""
    result = mumbai_twin.simulate_rainfall(ward_id, rainfall_mm)
    return result

@router.get("/historical/floods")
async def get_historical_floods():
    """Get historical flood events"""
    return data_loader.flood_events.to_dict('records')

@router.post("/simulate/historical/{event_id}")
async def replay_historical_flood(event_id: str):
    """Replay historical flood event (e.g., 2005 Mumbai floods)"""
    event = data_loader.flood_events[
        data_loader.flood_events['event_id'] == event_id
    ].iloc[0]
    
    # Simulate the historical event
    affected_wards = event['affected_wards'].split(',')
    results = {}
    
    for ward_id in affected_wards:
        results[ward_id] = mumbai_twin.simulate_rainfall(
            ward_id.strip(), 
            event['water_level_cm'] * 2  # Convert water level to rainfall
        )
    
    return {
        'event': event.to_dict(),
        'simulation_results': results
    }
```

---

### Phase 5: Frontend Mumbai Map (2-3 hours)

**File:** `frontend/src/pages/MumbaiMap.jsx`

```javascript
import { useState, useEffect } from 'react';
import { MapPin, AlertTriangle } from 'lucide-react';
import Card from '../components/Card';
import { mumbaiAPI } from '../services/api';

const MumbaiMap = () => {
  const [wards, setWards] = useState({});
  const [selectedWard, setSelectedWard] = useState(null);
  const [infrastructure, setInfrastructure] = useState([]);

  useEffect(() => {
    loadMumbaiData();
  }, []);

  const loadMumbaiData = async () => {
    const wardsData = await mumbaiAPI.getWards();
    const infraData = await mumbaiAPI.getInfrastructure();
    setWards(wardsData.data);
    setInfrastructure(infraData.data);
  };

  const getRiskColor = (riskScore) => {
    if (riskScore > 0.8) return '#ef4444';
    if (riskScore > 0.6) return '#f97316';
    if (riskScore > 0.4) return '#f59e0b';
    return '#10b981';
  };

  // Ward positions on map (approximate)
  const wardPositions = {
    'A': { x: 200, y: 450 },  // Colaba (South)
    'E': { x: 220, y: 400 },  // Byculla
    'H/E': { x: 180, y: 300 }, // Bandra East
    'K/E': { x: 160, y: 200 }, // Andheri East
    'P/N': { x: 140, y: 150 }, // Malad West
    'R/N': { x: 120, y: 80 },  // Borivali
    'L': { x: 200, y: 250 }    // Kurla
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Mumbai Digital Twin</h1>
        <p>Real-time ward monitoring and flood risk assessment</p>
      </div>

      <div className="grid-2">
        <Card title="Mumbai Ward Map">
          <svg width="400" height="500" style={{ border: '1px solid #334155' }}>
            {/* Mumbai coastline (simplified) */}
            <path
              d="M 50 50 L 50 450 L 150 480 L 250 450 L 250 50 Z"
              fill="#1e293b"
              stroke="#3b82f6"
              strokeWidth="2"
            />
            
            {/* Wards */}
            {Object.entries(wards).map(([wardId, ward]) => {
              const pos = wardPositions[wardId];
              if (!pos) return null;
              
              return (
                <g key={wardId}>
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={Math.sqrt(ward.population) / 100}
                    fill={getRiskColor(ward.risk_score)}
                    opacity="0.7"
                    style={{ cursor: 'pointer' }}
                    onClick={() => setSelectedWard(ward)}
                  />
                  <text
                    x={pos.x}
                    y={pos.y - 30}
                    fontSize="12"
                    fill="white"
                    textAnchor="middle"
                  >
                    {wardId}
                  </text>
                </g>
              );
            })}
            
            {/* Infrastructure */}
            {infrastructure.map((infra, idx) => (
              <g key={idx}>
                <MapPin
                  x={wardPositions[infra.ward_id]?.x - 8}
                  y={wardPositions[infra.ward_id]?.y - 8}
                  size={16}
                  color="#fbbf24"
                />
              </g>
            ))}
          </svg>
        </Card>

        <Card title="Ward Details">
          {selectedWard ? (
            <div className="status-list">
              <div className="status-item">
                <span className="status-label">Ward</span>
                <span>{selectedWard.name}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Population</span>
                <span>{selectedWard.population.toLocaleString()}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Slum Population</span>
                <span>{selectedWard.slum_percent}%</span>
              </div>
              <div className="status-item">
                <span className="status-label">Risk Score</span>
                <span className="status-badge" style={{
                  backgroundColor: getRiskColor(selectedWard.risk_score)
                }}>
                  {(selectedWard.risk_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          ) : (
            <div className="loading">Select a ward to view details</div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default MumbaiMap;
```

---

## 🎯 KEY FEATURES TO IMPLEMENT

### 1. Historical Flood Replay
- Replay 2005 Mumbai floods (944mm rainfall, 1000 casualties)
- Replay 2020, 2021 events
- Show actual vs predicted outcomes

### 2. Real-Time Sensor Dashboard
- Rain sensors (RS001, RS002, RS003)
- Water level sensors (Mithi River)
- Traffic congestion
- Power grid status
- Panic detection (sound sensors)

### 3. Ward-Specific Risk Assessment
- Combine rainfall + slum density + drainage + traffic
- Generate explainability logs (feature importance)
- AI recommendations for each ward

### 4. Infrastructure Dependency Graph
- JJ Hospital → Power → Water
- CST Railway → Power
- Airport → Power + Water
- Show cascading failures

### 5. Mithi River Monitoring
- Real-time water levels
- Threshold alerts
- Affected wards prediction
- Overflow simulation

---

## 📊 ENHANCED CO MAPPING WITH MUMBAI DATA

### CO1 - Agents (Mumbai-Specific)
- **BMC Agent** (Brihanmumbai Municipal Corporation)
- **Railway Agent** (Central/Western Railway)
- **Airport Authority Agent**
- **Citizen Agents** (different behavior by ward/slum density)

### CO2 - Search (Mumbai-Specific)
- A* for evacuation routes (avoid flood-prone roads)
- Dijkstra for ambulance routing to JJ/KEM hospitals
- BFS for Mithi River cascade analysis

### CO3 - CSP (Mumbai-Specific)
- Resource allocation across 10 wards
- Budget constraints (Mumbai BMC budget)
- Priority: High-risk wards (E, L) first

### CO4 - Probability (Mumbai-Specific)
- HMM: Public mood during monsoon
- Bayesian: Rainfall → Flood → Casualties
- Historical data: Learn from 2005, 2020, 2021 events

### CO5 - Learning (Mumbai-Specific)
- RL agent learns from historical floods
- Reward: Minimize casualties (actual historical data)
- Train on 2005-2023 rainfall patterns

---

## 🎓 FACULTY PRESENTATION UPGRADE

### New Opening:
> "I've built a Digital Twin of Mumbai City using real data - 10 wards, actual infrastructure like JJ Hospital and CST station, historical flood events including the 2005 disaster, and real-time sensor data. The system can replay historical floods and predict future risks using AI."

### Demo Flow:
1. Show Mumbai map with real wards
2. Replay 2005 flood (944mm, 1000 casualties)
3. Show Mithi River monitoring
4. Demonstrate AI recommendations for Ward E (Byculla)
5. Show explainability: Why is Ward E high risk? (Rainfall 35%, Slum density 18%)

---

**This transforms your project from a generic simulation to a real-world Mumbai disaster management system!** 🌆

Would you like me to start implementing these components?
