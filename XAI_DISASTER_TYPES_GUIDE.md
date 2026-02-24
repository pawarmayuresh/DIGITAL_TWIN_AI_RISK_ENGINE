# XAI Natural Language Explainer - Disaster Type Detection

## Overview
The Natural Language Explainer now automatically detects disaster types based on input features and generates appropriate, context-specific explanations.

## Disaster Type Detection

### 🔥 FIRE
**Trigger Features:**
- `fire_intensity` - Fire intensity level
- `temperature` - Temperature in °C
- `humidity` - Humidity percentage
- `wind_speed` - Wind speed in km/h

**Report Title:** "FIRE HAZARD ASSESSMENT REPORT"

**Example Interventions:**
- Reduce fire intensity through firefighting operations
- Lower temperature through cooling measures
- Increase humidity through water spraying

---

### 🌀 CYCLONE
**Trigger Features:**
- `cyclone_category` - Cyclone category (1-5)
- `wind_velocity` - Wind velocity in km/h
- `storm_surge` - Storm surge height in meters

**Report Title:** "CYCLONE THREAT ANALYSIS REPORT"

**Example Interventions:**
- Natural cyclone weakening (wind reduction)
- Coastal barriers to reduce storm surge
- Evacuation to cyclone shelters

---

### 🌊 FLOOD (Default)
**Trigger Features:**
- `water_level` - Water level in meters
- `rainfall` - Rainfall intensity in mm/hr

**Report Title:** "FLOOD RISK ANALYSIS REPORT"

**Example Interventions:**
- Improve drainage to reduce water level
- Pumping operations
- Natural weather variation (rainfall decrease)

---

### ☣️ CONTAMINATION
**Trigger Features:**
- `contamination_level` - Contamination level index
- `toxicity` - Toxicity index
- `air_quality_index` - AQI value

**Report Title:** "CONTAMINATION RISK REPORT"

**Example Interventions:**
- Decontamination and cleanup operations
- Neutralization and remediation
- Air quality improvement measures

---

### 📋 POLICY
**Trigger Features:**
- `policy_effectiveness` - Policy effectiveness percentage
- `compliance_rate` - Compliance rate percentage
- `implementation_score` - Implementation score

**Report Title:** "POLICY COMPLIANCE ANALYSIS REPORT"

**Example Interventions:**
- Better implementation and enforcement
- Education and incentives
- Enhanced oversight

---

### 🔍 GENERAL
**Trigger:** No specific disaster features detected

**Report Title:** "RISK ASSESSMENT REPORT"

**Example Interventions:**
- Generic risk reduction measures
- Standard monitoring protocols

---

## Common Features (All Disasters)
- `population_density` - Population density (people)
- `risk_score` - Baseline risk score
- `infrastructure` - Infrastructure condition
- `vulnerability_index` - Vulnerability index

---

## Usage Examples

### Example 1: Fire Scenario
```python
features = {
    "fire_intensity": 7.5,
    "temperature": 45.0,
    "humidity": 15.0,
    "population_density": 5000
}
# Generates: "FIRE HAZARD ASSESSMENT REPORT"
# Action: "Immediate evacuation required due to fire spread risk."
```

### Example 2: Cyclone Scenario
```python
features = {
    "cyclone_category": 4,
    "wind_velocity": 180.0,
    "storm_surge": 3.5,
    "population_density": 8000
}
# Generates: "CYCLONE THREAT ANALYSIS REPORT"
# Action: "Evacuation to cyclone shelters is strongly advised."
```

### Example 3: Contamination Scenario
```python
features = {
    "contamination_level": 0.85,
    "toxicity": 0.92,
    "air_quality_index": 350,
    "population_density": 3000
}
# Generates: "CONTAMINATION RISK REPORT"
# Action: "Area evacuation needed due to hazardous contamination levels."
```

### Example 4: Policy Scenario
```python
features = {
    "policy_effectiveness": 0.45,
    "compliance_rate": 0.60,
    "implementation_score": 0.55,
    "population_density": 4000
}
# Generates: "POLICY COMPLIANCE ANALYSIS REPORT"
# Action: "Policy compliance requires enhanced oversight."
```

---

## Testing Different Scenarios

To test different disaster types in the XAI dashboard:

1. **Modify Decision Features**: When logging decisions in `evacuation_routes.py` or other modules, include disaster-specific features
2. **Automatic Detection**: The NL explainer will automatically detect the disaster type
3. **Contextual Reports**: Reports will use appropriate terminology and interventions

---

## Integration Points

### Backend Files:
- `backend/core/explainable_ai/nl_explainer.py` - Main detection and generation logic
- `backend/api/explainability_routes.py` - API endpoints that use the explainer
- `backend/api/evacuation_routes.py` - Decision logging with features

### Frontend Files:
- `frontend/src/pages/DecisionExplainer.jsx` - Displays the generated reports

---

## Benefits

✅ **Automatic Detection**: No manual disaster type specification needed
✅ **Context-Aware**: Explanations match the disaster scenario
✅ **Extensible**: Easy to add new disaster types
✅ **Consistent**: Same API for all disaster types
✅ **Intelligent**: Uses feature presence to determine context

---

## Adding New Disaster Types

To add a new disaster type:

1. Add detection logic in `_detect_disaster_type()`
2. Add feature descriptions in `_explain_feature()`
3. Add action guidance in `explain_risk_decision()`
4. Add interventions in `explain_counterfactual()`
5. Add report title in `generate_summary_report()`

Example for Earthquake:
```python
# In _detect_disaster_type()
elif 'seismic_intensity' in feature_keys or 'magnitude' in feature_keys:
    return 'earthquake'

# In disaster_titles
'earthquake': 'EARTHQUAKE RISK ANALYSIS'
```
