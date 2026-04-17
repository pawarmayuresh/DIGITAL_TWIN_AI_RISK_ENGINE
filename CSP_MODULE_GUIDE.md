# CSP (Constraint Satisfaction Problem) Module - Complete Guide

## Overview

The CSP Module demonstrates how the AI Strategic Risk Engine uses Constraint Satisfaction Problems to solve complex disaster management optimization challenges. This module visualizes 4 different types of CSP problems with real-time solving and interactive visualization.

## What is CSP?

A Constraint Satisfaction Problem (CSP) consists of:

1. **Variables (X₁, X₂, ..., Xₙ)**: Decision variables that need values
2. **Domains (D₁, D₂, ..., Dₙ)**: Possible values each variable can take
3. **Constraints**: Rules that must be satisfied
   - **Hard Constraints**: MUST be satisfied (mandatory)
   - **Soft Constraints**: Should be optimized (preferences)

## CSP Types in the System

### 1. Resource Allocation CSP 🚑

**Problem**: Allocate rescue teams to disaster zones

**Variables**: 
- `team_0`, `team_1`, ..., `team_n` → which zone each team is assigned to

**Domains**: 
- Each team can be assigned to any zone: `[Z1, Z2, Z3, ...]`

**Hard Constraints**:
- Each zone must have at least 1 team
- High priority zones (priority ≥ 4) need at least 2 teams

**Soft Constraints**:
- Minimize total travel distance

**Example Solution**:
```
team_0 → Z1
team_1 → Z1  (Z1 is high priority, needs 2 teams)
team_2 → Z2
team_3 → Z3
team_4 → Z3  (Z3 is high priority, needs 2 teams)
```

**Visualization**:
- Team assignments shown as cards
- Zone coverage displayed with team counts
- Color-coded by priority level

---

### 2. Evacuation Scheduling CSP 📅

**Problem**: Schedule evacuation times for different areas

**Variables**: 
- `area_A1`, `area_A2`, ..., `area_An` → which time slot each area evacuates

**Domains**: 
- Time slots: `[T0_immediate, T1_1hour, T2_2hours, T3_3hours]`

**Hard Constraints**:
- High risk areas (risk > 0.7) must evacuate in first 2 time slots
- Adjacent areas cannot evacuate simultaneously (traffic conflicts)

**Soft Constraints**:
- Minimize total evacuation time
- Complete all evacuations within 3 hours

**Example Solution**:
```
T0_immediate: [A1, A3]  (high risk areas)
T1_1hour: [A2]
T2_2hours: [A4]
T3_3hours: []
```

**Visualization**:
- Timeline showing which areas evacuate when
- Progress bars showing slot utilization
- Color-coded by urgency

---

### 3. Shelter Assignment CSP 🏠

**Problem**: Assign evacuee groups to shelters

**Variables**: 
- `group_G1`, `group_G2`, ..., `group_Gn` → which shelter each group goes to

**Domains**: 
- Available shelters: `[S1, S2, S3, ...]`

**Hard Constraints**:
- Shelter capacity cannot be exceeded
- Special needs groups must go to shelters with medical facilities

**Soft Constraints**:
- Minimize distance from origin to shelter
- Balance utilization across shelters

**Example Solution**:
```
group_G1 (200 people) → S1 (capacity: 300)
group_G2 (150 people, special needs) → S1 (has medical facility)
group_G3 (180 people) → S2 (capacity: 250)
group_G4 (100 people) → S3 (capacity: 200)
```

**Visualization**:
- Shelter utilization bars (percentage filled)
- Color-coded: Green (<70%), Orange (70-90%), Red (>90%)
- Shows assigned/capacity for each shelter

---

### 4. Route Selection CSP 🛣️

**Problem**: Select evacuation routes for different areas

**Variables**: 
- `area_A1`, `area_A2`, ..., `area_An` → which route each area uses

**Domains**: 
- Available routes: `[R1, R2, R3, ...]`

**Hard Constraints**:
- Only safe routes can be used (risk < 0.5)
- Route capacity limits (max areas per route)

**Soft Constraints**:
- Minimize total distance
- Use multiple routes (load balancing)

**Example Solution**:
```
area_A1 → R1 (risk: 0.3, safe)
area_A2 → R3 (risk: 0.2, safest)
area_A3 → R1 (within capacity)
area_A4 → R2 (risk: 0.4, safe)
```

**Visualization**:
- Route cards showing assigned areas
- Risk level indicators (Safe/High Risk)
- Usage vs capacity display

---

## Solving Algorithm

### Backtracking Search with MRV Heuristic

The system uses an intelligent backtracking algorithm:

1. **Select Variable** (MRV - Minimum Remaining Values)
   - Choose the variable with the smallest domain first
   - Reduces search space early

2. **Try Values**
   - For each possible value in the domain
   - Assign value to variable

3. **Check Constraints**
   - Verify all hard constraints are satisfied
   - If violated, backtrack immediately

4. **Recurse**
   - If consistent, continue to next variable
   - If complete, return solution

5. **Backtrack**
   - If no value works, undo assignment
   - Try different value or previous variable

**Performance Metrics**:
- **Iterations**: Total assignment attempts
- **Backtracks**: Times algorithm had to undo assignments
- **Constraints Satisfied**: Number of constraints met

---

## How to Use the Module

### 1. Access the Module

Navigate to: **CSP Solver** in the sidebar (🧩 icon)

### 2. Solve All CSP Types

Click the **"Solve All CSP"** button to:
- Solve all 4 CSP types simultaneously
- Generate realistic disaster scenarios
- Display solutions with visualizations

### 3. View Results

The interface shows:

**Summary Dashboard**:
- Problems Solved (4/4)
- Total Iterations
- Total Backtracks
- CSP Types

**Individual CSP Cards**:
- Problem type and icon
- Status (SOLVED/NO_SOLUTION)
- Iterations and backtracks
- Visual solution representation

### 4. Interpret Solutions

Each CSP card displays:
- **Green status**: Solution found successfully
- **Red status**: No solution (constraints too restrictive)
- **Iterations**: How many attempts were made
- **Backtracks**: How many times algorithm reversed decisions

---

## API Endpoints

### Get All CSP Solutions
```http
GET /api/csp/solve-all?scenario=flood
```

**Response**:
```json
{
  "scenario": "flood",
  "timestamp": "2024-01-15T10:30:00",
  "csp_problems": [
    {
      "type": "Resource Allocation CSP",
      "status": "solved",
      "solution": {...},
      "iterations": 45,
      "backtracks": 12
    },
    ...
  ],
  "summary": {
    "total_problems": 4,
    "solved": 4,
    "total_iterations": 180,
    "total_backtracks": 45
  }
}
```

### Individual CSP Endpoints

```http
POST /api/csp/resource-allocation
POST /api/csp/evacuation-scheduling
POST /api/csp/shelter-assignment
POST /api/csp/route-selection
```

### Get CSP Information
```http
GET /api/csp/info
```

Returns detailed information about CSP formulation and types.

---

## Faculty Presentation Points

### 1. Problem Complexity
- "CSP is NP-complete - exponential time complexity"
- "Our system solves 4 different CSP types in real-time"
- "Demonstrates practical AI application in disaster management"

### 2. Algorithm Intelligence
- "Uses MRV heuristic to reduce search space"
- "Backtracking with constraint propagation"
- "Handles both hard and soft constraints"

### 3. Real-World Application
- "Resource allocation: Deploy teams optimally"
- "Scheduling: Coordinate evacuations without conflicts"
- "Assignment: Match evacuees to appropriate shelters"
- "Routing: Select safe, efficient evacuation routes"

### 4. Visualization Benefits
- "Interactive UI shows solution process"
- "Metrics display algorithm efficiency"
- "Color-coded visualizations for quick understanding"
- "Real-time solving demonstrates system capability"

---

## Course Outcomes Mapping

### CO1: Understand AI Techniques
- ✅ CSP formulation and solving
- ✅ Constraint propagation
- ✅ Heuristic search strategies

### CO2: Apply AI to Real Problems
- ✅ Disaster resource allocation
- ✅ Evacuation scheduling
- ✅ Shelter assignment optimization

### CO3: Implement AI Systems
- ✅ Backtracking algorithm implementation
- ✅ MRV heuristic integration
- ✅ Constraint checking system

### CO4: Analyze Algorithm Performance
- ✅ Iteration and backtrack metrics
- ✅ Time complexity analysis
- ✅ Solution quality evaluation

### CO5: Design Intelligent Systems
- ✅ Multi-CSP solver architecture
- ✅ API design for CSP services
- ✅ Interactive visualization system

---

## Technical Implementation

### Backend (Python)
- **File**: `backend/core/csp/csp_solver.py`
- **Classes**: 
  - `CSPSolver` (base class)
  - `DisasterResourceAllocationCSP`
  - `EvacuationSchedulingCSP`
  - `ShelterAssignmentCSP`
  - `RouteSelectionCSP`
- **Algorithm**: Backtracking with MRV heuristic

### API Layer (FastAPI)
- **File**: `backend/api/csp_routes.py`
- **Endpoints**: 6 endpoints for CSP operations
- **Integration**: Connected to main FastAPI app

### Frontend (React)
- **File**: `frontend/src/pages/CSPVisualization.jsx`
- **Components**: 
  - CSP info cards
  - Solution visualizations
  - Interactive controls
- **Styling**: Consistent with system theme

---

## Demo Script

1. **Introduction** (30 seconds)
   - "Let me show you our CSP solver module"
   - "It solves 4 different optimization problems"

2. **Click Solve** (10 seconds)
   - Click "Solve All CSP" button
   - Watch real-time solving

3. **Explain Results** (2 minutes)
   - Point to summary metrics
   - Show each CSP type
   - Explain one solution in detail

4. **Highlight Features** (1 minute)
   - "Notice the iterations and backtracks"
   - "Color-coded visualizations"
   - "All constraints satisfied"

5. **Connect to Theory** (30 seconds)
   - "This demonstrates NP-complete problem solving"
   - "Real-world AI application"
   - "Practical disaster management"

---

## Troubleshooting

### No Solution Found
- **Cause**: Constraints too restrictive
- **Solution**: Relax soft constraints or add more resources

### High Backtracks
- **Cause**: Poor variable ordering
- **Solution**: MRV heuristic helps minimize this

### Slow Solving
- **Cause**: Large problem size
- **Solution**: Constraint propagation reduces search space

---

## Future Enhancements

1. **Dynamic CSP Generation**
   - User-defined variables and constraints
   - Custom disaster scenarios

2. **Visualization Improvements**
   - Animated solving process
   - Step-by-step constraint checking

3. **Advanced Algorithms**
   - Arc consistency (AC-3)
   - Forward checking
   - Constraint learning

4. **Performance Optimization**
   - Parallel CSP solving
   - Caching solutions
   - Incremental solving

---

## Summary

The CSP Module demonstrates:
- ✅ 4 different CSP types for disaster management
- ✅ Intelligent backtracking algorithm with MRV heuristic
- ✅ Real-time solving with performance metrics
- ✅ Interactive visualizations for each CSP type
- ✅ Complete API integration
- ✅ Production-ready implementation

This module showcases advanced AI techniques applied to real-world disaster management challenges, making it an excellent demonstration of practical AI system design and implementation.
