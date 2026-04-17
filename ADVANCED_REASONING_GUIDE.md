# Advanced Knowledge Engine - Multiple Reasoning Strategies

## Overview

The enhanced Knowledge Engine now supports **7 different reasoning strategies** that provide dynamic, varied analysis after each grid simulation. Each strategy offers unique insights and reasoning patterns.

## Reasoning Strategies

### 1. 🔍 Abductive Reasoning
**Purpose:** Find the best explanation for observed phenomena

**How it works:**
- Given observations (symptoms), find the most likely cause
- Evaluates multiple hypotheses based on:
  - Coverage: How many observations does it explain?
  - Parsimony: How simple is the explanation?
  - Prior probability: How likely is this cause?

**Example:**
```
Observations: ["high_water_level", "heavy_rainfall", "flooded_streets"]

Hypotheses:
1. Monsoon Flood (explains all 3, prior: 60%)
2. Dam Breach (explains 2, prior: 20%)
3. Drainage Blockage (explains 2, prior: 40%)

Result: Monsoon Flood is best explanation (score: 0.85)
```

**Use Case:** Diagnosing the root cause of a disaster

---

### 2. 🔄 Analogical Reasoning
**Purpose:** Learn from similar past cases

**How it works:**
- Compares current situation to historical cases
- Calculates similarity using feature matching
- Recommends solutions that worked in similar situations

**Example:**
```
Current: {rainfall: 80mm, water_level: 2.5m, traffic: 0.8}

Similar Past Case (2019):
  Features: {rainfall: 75mm, water_level: 2.3m, traffic: 0.7}
  Solution: "evacuate_low_lying_areas"
  Outcome: "successful"
  Similarity: 0.92

Recommendation: Apply same solution
```

**Use Case:** Leveraging historical disaster response experience

---

### 3. 🌫️ Fuzzy Reasoning
**Purpose:** Handle imprecise and vague information

**How it works:**
- Converts crisp values to fuzzy memberships (low, medium, high)
- Applies fuzzy rules (IF-THEN with fuzzy logic)
- Defuzzifies to get crisp risk score

**Example:**
```
Input: rainfall = 65mm

Fuzzification:
  - low: 0.0
  - medium: 0.5
  - high: 0.7
  - extreme: 0.0

Fuzzy Rule: IF rainfall is high AND water_level is high THEN risk is high

Defuzzification: Risk score = 0.72
```

**Use Case:** Dealing with uncertain sensor readings and vague concepts

---

### 4. 📊 Probabilistic Reasoning (Bayesian)
**Purpose:** Update beliefs based on evidence

**How it works:**
- Uses Bayes' theorem: P(Cause|Evidence) = P(Evidence|Cause) × P(Cause) / P(Evidence)
- Calculates posterior probabilities for different disaster types
- Identifies most likely scenario

**Example:**
```
Evidence: {heavy_rain: true, high_temperature: false}

Prior Probabilities:
  - Flood: 30%
  - Fire: 10%
  - Contamination: 5%

Posterior Probabilities (after evidence):
  - Flood: 78%
  - Fire: 8%
  - Contamination: 4%

Conclusion: Flood is most likely (78% confidence)
```

**Use Case:** Determining disaster type from multiple indicators

---

### 5. ⏰ Temporal Reasoning
**Purpose:** Analyze time-based patterns and sequences

**How it works:**
- Detects causal sequences (A causes B)
- Identifies concurrent events
- Predicts future events based on patterns

**Example:**
```
Events:
  10:00 - rainfall_started
  11:30 - water_rising
  11:45 - traffic_jam

Patterns Detected:
  1. Causal: rainfall_started → water_rising (90 min gap)
  2. Concurrent: water_rising & traffic_jam (15 min gap)

Prediction: flooding_reported expected in 60 minutes
```

**Use Case:** Predicting disaster progression and timing

---

### 6. 🧠 Meta-Reasoning
**Purpose:** Choose the best reasoning strategy for the problem

**How it works:**
- Analyzes problem characteristics
- Scores each reasoning strategy
- Recommends most appropriate approach

**Example:**
```
Problem Characteristics:
  - has_past_cases: true
  - has_uncertainty: true
  - has_temporal_data: false

Strategy Scores:
  - Analogical: 0.8 (has past cases)
  - Fuzzy: 0.7 (has uncertainty)
  - Probabilistic: 0.6 (has uncertainty)
  - Temporal: 0.0 (no temporal data)

Recommendation: Use Analogical Reasoning
```

**Use Case:** Automatically selecting optimal reasoning approach

---

### 7. 🔀 Hybrid Reasoning
**Purpose:** Combine multiple strategies for robust analysis

**How it works:**
- Auto-selects appropriate strategies based on data
- Applies each strategy independently
- Combines results using weighted averaging

**Example:**
```
Data: {rainfall: 75, water_level: 2.8, events: [...]}

Strategies Applied:
  1. Fuzzy → Risk: 0.72
  2. Probabilistic → Risk: 0.68
  3. Temporal → Risk: 0.65

Combined Risk: 0.70 (weighted average)
Risk Level: HIGH
```

**Use Case:** Comprehensive analysis using multiple perspectives

---

## Dynamic Reasoning After Grid Simulation

### How It Works

After each grid simulation step, the system **cycles through different reasoning strategies**:

```
Step 0: Fuzzy Reasoning
Step 1: Probabilistic Reasoning
Step 2: Temporal Reasoning
Step 3: Abductive Reasoning
Step 4: Analogical Reasoning
Step 5: Hybrid Reasoning
Step 6: Fuzzy Reasoning (cycle repeats)
```

This ensures **different reasoning and insights every time**!

### Example Progression

**Simulation Step 1 (Fuzzy):**
```
Strategy: Fuzzy Reasoning
Conclusion: "Fuzzy analysis: Risk level HIGH with score 0.75"
Reasoning: Rainfall is "high" (0.7 membership), water level is "high" (0.8 membership)
```

**Simulation Step 2 (Probabilistic):**
```
Strategy: Probabilistic Reasoning
Conclusion: "Bayesian inference: Most likely flood with 78% confidence"
Reasoning: Evidence strongly supports flood hypothesis over fire or contamination
```

**Simulation Step 3 (Temporal):**
```
Strategy: Temporal Reasoning
Conclusion: "Temporal analysis: Found 2 patterns, 1 prediction"
Reasoning: Rainfall → Water rising pattern detected, flooding predicted in 60 min
```

**Simulation Step 4 (Abductive):**
```
Strategy: Abductive Reasoning
Conclusion: "Best explanation is monsoon_flood with 0.85 score"
Reasoning: Monsoon flood explains all observations with high coverage and prior probability
```

**Simulation Step 5 (Analogical):**
```
Strategy: Analogical Reasoning
Conclusion: "Recommended solution is immediate_evacuation"
Reasoning: Current situation 92% similar to 2019 case where evacuation was successful
```

**Simulation Step 6 (Hybrid):**
```
Strategy: Hybrid Reasoning
Conclusion: "Combined risk score 0.73, level HIGH"
Reasoning: Fuzzy (0.75) + Probabilistic (0.68) + Temporal (0.65) = 0.73 average
```

---

## API Endpoints

### Individual Strategy Endpoints

#### 1. Abductive Reasoning
```http
POST /api/knowledge/advanced/abductive
Content-Type: application/json

{
  "observations": ["high_water_level", "heavy_rainfall"],
  "hypotheses": [
    {
      "name": "monsoon_flood",
      "explains": ["high_water_level", "heavy_rainfall"],
      "prior": 0.6
    }
  ]
}
```

#### 2. Analogical Reasoning
```http
POST /api/knowledge/advanced/analogical
Content-Type: application/json

{
  "current_situation": {
    "features": {"rainfall": 80, "water_level": 2.5}
  },
  "past_cases": [
    {
      "id": "case_2019",
      "features": {"rainfall": 75, "water_level": 2.3},
      "solution": "evacuate"
    }
  ]
}
```

#### 3. Fuzzy Reasoning
```http
POST /api/knowledge/advanced/fuzzy
Content-Type: application/json

{
  "rainfall": 65,
  "water_level": 2.3,
  "traffic_density": 0.75
}
```

#### 4. Probabilistic Reasoning
```http
POST /api/knowledge/advanced/probabilistic
Content-Type: application/json

{
  "evidence": {
    "heavy_rain": true,
    "high_temperature": false
  }
}
```

#### 5. Temporal Reasoning
```http
POST /api/knowledge/advanced/temporal
Content-Type: application/json

{
  "events": [
    {"event": "rainfall_started", "time": "10:00"},
    {"event": "water_rising", "time": "11:30"}
  ]
}
```

#### 6. Meta-Reasoning
```http
POST /api/knowledge/advanced/meta
Content-Type: application/json

{
  "has_past_cases": true,
  "has_uncertainty": true,
  "has_temporal_data": false
}
```

#### 7. Hybrid Reasoning
```http
POST /api/knowledge/advanced/hybrid
Content-Type: application/json

{
  "data": {
    "rainfall": 75,
    "water_level": 2.8,
    "events": [...]
  },
  "strategies": ["fuzzy", "probabilistic"]
}
```

### Grid Simulation Analysis Endpoint

**The main endpoint for dynamic reasoning after grid simulation:**

```http
POST /api/knowledge/advanced/grid-simulation-analysis
Content-Type: application/json

{
  "ward": "Kurla",
  "rainfall_mm": 85,
  "water_level_m": 2.7,
  "traffic_density": 0.82,
  "temperature": 31,
  "failed_infrastructure": 3,
  "evacuation_progress": 0.45,
  "simulation_step": 15,
  "events": [
    {"event": "heavy_rain_detected", "time": "10:00"},
    {"event": "water_level_rising", "time": "11:00"}
  ]
}
```

**Response:**
```json
{
  "ward": "Kurla",
  "simulation_step": 15,
  "primary_strategy": "temporal",
  "primary_conclusion": "Temporal analysis: Found 2 patterns, 1 prediction",
  "reasoning_results": {
    "temporal": {...},
    "expert_system": {...}
  },
  "expert_conclusion": "Expert system: HIGH risk, 8 rules fired",
  "recommendations": [
    "⚠️ HIGH RISK: Prepare for evacuation",
    "Alert emergency services"
  ],
  "average_risk_score": 0.73,
  "next_strategy": "abductive"
}
```

---

## Integration with Frontend

### Calling After Grid Simulation

```javascript
// After each simulation step
const analyzeSimulation = async (simulationData) => {
  const response = await fetch(
    'http://localhost:8001/api/knowledge/advanced/grid-simulation-analysis',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ward: selectedWard,
        rainfall_mm: simulationData.rainfall,
        water_level_m: simulationData.waterLevel,
        traffic_density: simulationData.traffic,
        temperature: simulationData.temperature,
        failed_infrastructure: simulationData.failedInfra,
        simulation_step: currentStep,
        events: simulationData.events
      })
    }
  );
  
  const result = await response.json();
  
  // Display reasoning
  console.log(`Strategy: ${result.primary_strategy}`);
  console.log(`Conclusion: ${result.primary_conclusion}`);
  console.log(`Recommendations:`, result.recommendations);
  
  // Show next strategy
  console.log(`Next analysis will use: ${result.next_strategy}`);
};
```

### Displaying Results

```javascript
// Show reasoning in UI
<div className="reasoning-panel">
  <h3>🧠 AI Reasoning Analysis</h3>
  
  <div className="strategy-badge">
    Strategy: {result.primary_strategy.toUpperCase()}
  </div>
  
  <div className="conclusion">
    {result.primary_conclusion}
  </div>
  
  <div className="expert-system">
    {result.expert_conclusion}
  </div>
  
  <div className="recommendations">
    <h4>Recommendations:</h4>
    {result.recommendations.map((rec, i) => (
      <div key={i} className="recommendation">{rec}</div>
    ))}
  </div>
  
  <div className="risk-score">
    Average Risk: {(result.average_risk_score * 100).toFixed(0)}%
  </div>
  
  <div className="next-strategy">
    Next: {result.next_strategy}
  </div>
</div>
```

---

## Comparison of Strategies

| Strategy | Best For | Strengths | Limitations |
|----------|----------|-----------|-------------|
| **Abductive** | Diagnosis | Finds root causes | Requires good hypotheses |
| **Analogical** | Learning from history | Uses past experience | Needs case database |
| **Fuzzy** | Vague data | Handles imprecision | Requires rule definition |
| **Probabilistic** | Uncertainty | Quantifies confidence | Needs probability data |
| **Temporal** | Time series | Predicts sequences | Requires event history |
| **Meta** | Strategy selection | Optimizes approach | Overhead of analysis |
| **Hybrid** | Comprehensive | Multiple perspectives | Computationally expensive |

---

## Advanced Features

### 1. Reasoning History Tracking

```http
GET /api/knowledge/advanced/history
```

Returns:
```json
{
  "history": [
    {"strategy": "fuzzy", "timestamp": "2024-01-15T10:30:00"},
    {"strategy": "probabilistic", "timestamp": "2024-01-15T10:31:00"}
  ],
  "statistics": {
    "total_inferences": 25,
    "strategy_counts": {
      "fuzzy": 8,
      "probabilistic": 7,
      "temporal": 5,
      "abductive": 3,
      "analogical": 2
    },
    "most_used_strategy": "fuzzy"
  }
}
```

### 2. Clear History

```http
POST /api/knowledge/advanced/clear-history
```

---

## Faculty Presentation Points

### Key Innovations

1. **Multiple Reasoning Paradigms**
   - 7 different AI reasoning strategies
   - Each provides unique insights
   - Demonstrates breadth of AI knowledge

2. **Dynamic Strategy Selection**
   - Cycles through strategies automatically
   - Different reasoning each simulation step
   - Shows adaptability and intelligence

3. **Hybrid Approach**
   - Combines multiple strategies
   - Weighted fusion of results
   - More robust than single strategy

4. **Real-World Application**
   - Applied to Mumbai disaster management
   - Handles uncertain, imprecise data
   - Provides actionable recommendations

### Demo Script

1. **Show Fuzzy Reasoning**
   - "Notice how it handles vague concepts like 'high' rainfall"
   - "Converts 65mm to fuzzy memberships"
   - "Applies fuzzy rules and defuzzifies to 0.72 risk"

2. **Show Probabilistic Reasoning**
   - "Uses Bayesian inference to update beliefs"
   - "Given heavy rain evidence, calculates 78% flood probability"
   - "More confident than simple rule-based systems"

3. **Show Temporal Reasoning**
   - "Analyzes event sequences over time"
   - "Detects causal patterns: rainfall → flooding"
   - "Predicts future events based on patterns"

4. **Show Grid Simulation Integration**
   - "After each simulation step, different reasoning"
   - "Step 1: Fuzzy, Step 2: Probabilistic, Step 3: Temporal"
   - "Demonstrates dynamic, adaptive AI"

### Technical Highlights

- **Abductive Reasoning**: Implements inference to best explanation (IBE)
- **Fuzzy Logic**: Membership functions, fuzzy rules, defuzzification
- **Bayesian Networks**: Conditional probabilities, posterior inference
- **Temporal Logic**: Event sequences, causal patterns, predictions
- **Meta-Reasoning**: Strategy selection based on problem characteristics

---

## Testing

### Test All Strategies

```bash
# Test fuzzy reasoning
curl -X POST http://localhost:8001/api/knowledge/advanced/fuzzy \
  -H "Content-Type: application/json" \
  -d '{"rainfall": 65, "water_level": 2.3}'

# Test probabilistic reasoning
curl -X POST http://localhost:8001/api/knowledge/advanced/probabilistic \
  -H "Content-Type: application/json" \
  -d '{"evidence": {"heavy_rain": true}}'

# Test grid simulation analysis
curl -X POST http://localhost:8001/api/knowledge/advanced/grid-simulation-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "ward": "Kurla",
    "rainfall_mm": 85,
    "water_level_m": 2.7,
    "simulation_step": 0
  }'
```

---

## Conclusion

The enhanced Knowledge Engine provides:

✅ **7 different reasoning strategies**  
✅ **Dynamic strategy cycling** (different reasoning each time)  
✅ **Hybrid approach** (combines multiple strategies)  
✅ **Real-time integration** with grid simulation  
✅ **Actionable recommendations** based on reasoning  
✅ **History tracking** and statistics  

This demonstrates advanced AI concepts and provides practical disaster management insights!
