# Mumbai Digital Twin - Fully Integrated System

## 🎯 Integration Goals

### 1. Mumbai Live → Spatial Grid Integration
- Click ward on Mumbai map → Show detailed spatial grid for that ward
- Real-time flood/fire/contamination visualization
- Cell-level disaster spread simulation

### 2. Ward Selection System
- Dropdown to select any ward
- Click on map to select ward
- Selected ward highlights across all modules
- All data updates based on selected ward

### 3. Disaster Simulation Integration
- Select disaster type (Flood/Fire/Contamination)
- Select ward to simulate
- Real-time spread visualization on spatial grid
- Impact on infrastructure, population, resources
- AI recommendations based on simulation

### 4. Module Interconnections
```
Mumbai Live ←→ Spatial Grid ←→ Disaster Sim
     ↓              ↓                ↓
Infrastructure ← Analytics → Explainability
     ↓              ↓                ↓
  Policy Compare ← Learning → Resilience
```

---

## 📊 Data Flow Architecture

### Current State:
```
Mumbai Live (standalone)
Spatial Grid (standalone)
Disaster Sim (standalone)
❌ No connections
```

### Target State:
```
User selects Ward "Kurla"
    ↓
Mumbai Live highlights Kurla
    ↓
Spatial Grid loads Kurla's 20x20 grid
    ↓
Shows real-time: Flood zones, Fire spread, Contamination
    ↓
Disaster Sim can run scenarios on Kurla
    ↓
Results feed back to all modules
    ↓
Analytics updates KPIs
    ↓
Explainability shows why decisions made
    ↓
Policy Compare suggests best response
```

---

## 🔧 Implementation Steps

### Phase 1: Ward Selection System (30 min)
1. Create global ward selection state
2. Add ward dropdown to all pages
3. Sync selection across modules
4. Highlight selected ward on map

### Phase 2: Mumbai Live → Spatial Grid (45 min)
1. Click ward on Mumbai map
2. Navigate to Spatial Grid page
3. Load ward-specific grid (20x20 cells)
4. Show real-time disaster data per cell

### Phase 3: Disaster Simulation Integration (60 min)
1. Select ward from dropdown
2. Select disaster type (Flood/Fire/Contamination)
3. Set severity (1-10)
4. Run simulation
5. Show spread on spatial grid
6. Update all connected modules

### Phase 4: Real-Time Visualization (45 min)
1. Flood: Blue cells with water level
2. Fire: Red cells with fire intensity
3. Contamination: Yellow cells with contamination level
4. Infrastructure damage overlay
5. Population evacuation routes

### Phase 5: Module Interconnections (60 min)
1. Simulation results → Analytics (update KPIs)
2. Analytics → Explainability (explain impacts)
3. Explainability → Policy Compare (suggest policies)
4. Policy Compare → Learning (train on outcomes)
5. Learning → Resilience (improve resilience score)

---

## 🗺️ Spatial Grid Structure

### Ward Grid Mapping
Each ward divided into 20x20 grid (400 cells)

```
Kurla Ward (L):
┌─────────────────────────┐
│ [0,0]  [0,1]  ... [0,19]│
│ [1,0]  [1,1]  ... [1,19]│
│  ...    ...   ...  ...  │
│[19,0] [19,1] ...[19,19] │
└─────────────────────────┘

Each cell contains:
- Elevation (meters)
- Population density
- Infrastructure type
- Flood risk (0-1)
- Fire risk (0-1)
- Contamination level (0-1)
- Current disaster state
```

### Real-Time Updates
```python
# Every 5 seconds
for cell in grid:
    cell.flood_level = calculate_flood(rainfall, elevation, drainage)
    cell.fire_intensity = calculate_fire(temperature, wind, fuel)
    cell.contamination = calculate_contamination(source, wind, time)
    
    # Spread to neighbors
    spread_disaster(cell, neighbors)
```

---

## 🎮 User Interaction Flow

### Scenario 1: View Ward Details
```
1. User opens Mumbai Live
2. Clicks on "KURLA" ward
3. System:
   - Highlights Kurla on map
   - Shows ward details panel
   - Updates URL: /mumbai-live?ward=L
   - Stores selection in global state
4. User clicks "View Spatial Grid"
5. System:
   - Navigates to /spatial-grid?ward=L
   - Loads Kurla's 20x20 grid
   - Shows current disaster states
```

### Scenario 2: Run Disaster Simulation
```
1. User opens Disaster Simulation
2. Selects ward: "Kurla"
3. Selects disaster: "Flood"
4. Sets severity: 8/10
5. Clicks "Run Simulation"
6. System:
   - Calculates flood spread
   - Updates spatial grid in real-time
   - Shows affected infrastructure
   - Calculates casualties
   - Estimates economic loss
   - Generates AI recommendations
7. Results appear in:
   - Spatial Grid (visual)
   - Analytics (KPIs updated)
   - Explainability (why this happened)
   - Policy Compare (what to do)
```

### Scenario 3: Compare Policies
```
1. User runs flood simulation in Kurla
2. System shows: 500 casualties, ₹200 crore loss
3. User goes to Policy Compare
4. System suggests 3 policies:
   - Policy A: Deploy 10 pumps (cost: ₹5 crore)
   - Policy B: Evacuate 50,000 people (cost: ₹2 crore)
   - Policy C: Build flood barriers (cost: ₹50 crore)
5. User selects Policy A
6. System re-runs simulation with policy
7. Shows: 200 casualties, ₹80 crore loss
8. User sees improvement in all modules
```

---

## 🔗 API Endpoints Needed

### Ward Selection
```
GET  /api/wards/select/{ward_id}
POST /api/wards/select
GET  /api/wards/current
```

### Spatial Grid
```
GET  /api/spatial/grid/{ward_id}
GET  /api/spatial/cell/{ward_id}/{x}/{y}
POST /api/spatial/update-cell
GET  /api/spatial/disasters/{ward_id}
```

### Disaster Simulation
```
POST /api/simulation/run
GET  /api/simulation/status/{sim_id}
GET  /api/simulation/results/{sim_id}
POST /api/simulation/stop/{sim_id}
```

### Integration
```
GET  /api/integration/ward-summary/{ward_id}
POST /api/integration/sync-modules
GET  /api/integration/cross-module-data
```

---

## 📱 UI Components Needed

### 1. Ward Selector Component
```jsx
<WardSelector 
  selectedWard={selectedWard}
  onWardChange={handleWardChange}
  showOnAllPages={true}
/>
```

### 2. Spatial Grid Viewer
```jsx
<SpatialGrid
  wardId={selectedWard}
  showDisasters={true}
  showInfrastructure={true}
  interactive={true}
  onCellClick={handleCellClick}
/>
```

### 3. Disaster Simulator
```jsx
<DisasterSimulator
  wardId={selectedWard}
  disasterType={disasterType}
  severity={severity}
  onSimulationComplete={handleResults}
/>
```

### 4. Integration Dashboard
```jsx
<IntegrationDashboard
  selectedWard={selectedWard}
  modules={['mumbai-live', 'spatial-grid', 'disaster-sim']}
  showConnections={true}
/>
```

---

## 🎨 Visual Design

### Mumbai Live with Ward Selection
```
┌─────────────────────────────────────────────────┐
│ 🌆 Mumbai Real-Time Monitor                     │
│ Ward: [Kurla ▼] [View Spatial Grid] [Simulate] │
├─────────────────────────────────────────────────┤
│  Map          │  Ward Details                   │
│  [Mumbai]     │  Name: Kurla                    │
│  [Kurla 🔴]   │  Population: 800,000            │
│               │  Risk: 88% SEVERE               │
│               │  [View Grid] [Simulate]         │
└─────────────────────────────────────────────────┘
```

### Spatial Grid with Disasters
```
┌─────────────────────────────────────────────────┐
│ 🗺️ Spatial Grid - Kurla                         │
│ [Flood 🔵] [Fire 🔴] [Contamination 🟡]         │
├─────────────────────────────────────────────────┤
│  Grid (20x20)     │  Cell Details               │
│  ████████████     │  Cell: [10,15]              │
│  ████🔵🔵████     │  Flood: 2.5m                │
│  ████🔵🔵████     │  Population: 200            │
│  ████████████     │  Infrastructure: Hospital   │
│                   │  Status: EVACUATE           │
└─────────────────────────────────────────────────┘
```

### Disaster Simulation
```
┌─────────────────────────────────────────────────┐
│ 🌊 Disaster Simulation                          │
│ Ward: [Kurla ▼]  Type: [Flood ▼]  Severity: 8  │
│ [▶ Run] [⏸ Pause] [⏹ Stop] [🔄 Reset]          │
├─────────────────────────────────────────────────┤
│  Simulation Progress: 45%                       │
│  Time: 2h 30m (simulated)                       │
│  Affected Cells: 156/400                        │
│  Casualties: 234                                │
│  Economic Loss: ₹145 crore                      │
│  [View on Grid] [View Analytics]                │
└─────────────────────────────────────────────────┘
```

---

## ✅ Success Criteria

### Ward Selection
- [ ] Dropdown works on all pages
- [ ] Click ward on map selects it
- [ ] Selection persists across pages
- [ ] All modules update when ward changes

### Spatial Grid Integration
- [ ] Click ward → Navigate to grid
- [ ] Grid shows 20x20 cells
- [ ] Real-time disaster visualization
- [ ] Cell details on hover/click

### Disaster Simulation
- [ ] Select ward, type, severity
- [ ] Run simulation button works
- [ ] Real-time progress shown
- [ ] Results update all modules

### Module Interconnections
- [ ] Simulation → Analytics (KPIs update)
- [ ] Analytics → Explainability (reasons shown)
- [ ] Explainability → Policy (suggestions)
- [ ] Policy → Learning (training data)
- [ ] Learning → Resilience (score improves)

---

## 🚀 Implementation Priority

### Must Have (Week 1):
1. Ward selection system
2. Mumbai Live → Spatial Grid navigation
3. Basic disaster simulation

### Should Have (Week 2):
4. Real-time disaster visualization
5. Module interconnections
6. Cross-module data sync

### Nice to Have (Week 3):
7. Advanced simulations
8. Policy optimization
9. Learning from simulations

---

## 📝 Next Steps

1. **Review this plan** - Does it match your vision?
2. **Prioritize features** - What's most important?
3. **Start implementation** - Begin with ward selection
4. **Test integration** - Ensure modules connect
5. **Iterate** - Improve based on feedback

---

**Ready to build the fully integrated Mumbai Digital Twin! 🚀**
