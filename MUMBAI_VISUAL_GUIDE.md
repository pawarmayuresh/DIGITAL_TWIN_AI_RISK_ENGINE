# Mumbai Digital Twin - Visual Guide

## 🗺️ Map Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Mumbai Real-Time Disaster Monitor                          │
│  Live ward monitoring with audio alerts                     │
│  [🔊 Audio ON] [🔔 5 Active Alerts]                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────────┐   │
│  │  Mumbai City Map     │  │  Ward Details            │   │
│  │                      │  │                          │   │
│  │  🌊 ARABIAN SEA     │  │  Selected: Kurla (L)     │   │
│  │  ~~~~~~~~~~~~~~~~~~~│  │  Population: 800,000     │   │
│  │                      │  │  Area: 15.0 km²          │   │
│  │     🏙️ Borivali     │  │  Slum %: 48%             │   │
│  │     (R/N)            │  │  Density: 53,333/km²     │   │
│  │                      │  │  Risk: 86% - SEVERE 🔴   │   │
│  │     🏙️ Malad        │  ├──────────────────────────┤   │
│  │     (P/N)            │  │  🚨 Active Alerts        │   │
│  │                      │  │                          │   │
│  │     🏙️ Andheri      │  │  ⚠️ SEVERE FLOOD RISK    │   │
│  │     (K/E)            │  │  in Kurla                │   │
│  │     ✈️ Airport       │  │                          │   │
│  │                      │  │  Recommendations:        │   │
│  │     🌉 Bandra        │  │  • Evacuate low areas    │   │
│  │     (H/E)            │  │  • Avoid flood roads     │   │
│  │                      │  │  • Move to higher floors │   │
│  │  🔵 Mithi River ~~~~ │  │  • Keep supplies ready   │   │
│  │     🏙️ Kurla 🔴     │  │                          │   │
│  │     (L)              │  │  ⚠️ HIGH RISK            │   │
│  │                      │  │  in Andheri East         │   │
│  │     🏙️ Byculla 🔴   │  │                          │   │
│  │     (E)              │  │  Recommendations:        │   │
│  │     🏥 JJ Hospital   │  │  • Monitor updates       │   │
│  │                      │  │  • Prepare evacuation    │   │
│  │     🚉 CST           │  │  • Avoid travel          │   │
│  │                      │  │                          │   │
│  │     🏛️ Gateway       │  └──────────────────────────┘   │
│  │     Colaba (A)       │                               │
│  │                      │                               │
│  │  Legend:             │                               │
│  │  🟢 Very Low         │                               │
│  │  🟡 Low              │                               │
│  │  🟠 Moderate         │                               │
│  │  🟠 High             │                               │
│  │  🔴 Severe           │                               │
│  └──────────────────────┘                               │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  📡 Real-Time Sensor Data                                │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ 🌧️ Rain      │ │ 💧 Water     │ │ 🚗 Traffic   │   │
│  │ Sensors      │ │ Level        │ │ Sensors      │   │
│  │              │ │              │ │              │   │
│  │ E: 45mm 🟡   │ │ Sion: 320cm  │ │ E001: 18km/h │   │
│  │ K/E: 60mm 🟠 │ │ ⚠️ ALERT 🔴  │ │ 🔴 Congested │   │
│  │ L: 72mm 🔴   │ │              │ │              │   │
│  │              │ │ Andheri:     │ │ E002: 40km/h │   │
│  │              │ │ 280cm ✓      │ │ 🟢 Normal    │   │
│  │              │ │              │ │              │   │
│  │              │ │ Kurla:       │ │ E003: 15km/h │   │
│  │              │ │ 190cm ✓      │ │ 🔴 Congested │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  📊 System Status                                        │
├──────────────────────────────────────────────────────────┤
│  [📡 3 Rain Sensors] [💧 3 Water Sensors]               │
│  [🚗 3 Traffic Sensors] [✅ System Online]              │
└──────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Coding

### Risk Levels
- **🟢 Green (0-20%)**: Very Low Risk - Normal conditions
- **🟡 Yellow (20-40%)**: Low Risk - Monitor situation
- **🟠 Orange (40-60%)**: Moderate Risk - Stay alert
- **🟠 Dark Orange (60-80%)**: High Risk - Prepare for action
- **🔴 Red (80-100%)**: Severe Risk - Immediate action required

### Ward Visualization
```
Normal Ward:        High Risk Ward:      Severe Ward:
    🟢                  🟠                  🔴
   ╱  ╲               ╱  ╲               ╱  ╲
  │    │             │    │             │ ⚠️ │
   ╲  ╱               ╲  ╱               ╲  ╱
    ──                  ──                 ──
  Colaba              Andheri            Kurla
   (35%)               (65%)             (86%)
```

### Pulsing Animation (High Risk)
```
Frame 1:    Frame 2:    Frame 3:    Frame 4:
   🔴          🔴          🔴          🔴
  ╱  ╲       ╱    ╲     ╱      ╲   ╱        ╲
 │    │     │      │   │        │ │          │
  ╲  ╱       ╲    ╱     ╲      ╱   ╲        ╱
   ──          ──          ──          ──
```

---

## 📍 Geographic Layout

### Mumbai Map (North to South)

```
                    NORTH
                      ↑
                      
    🌊 ARABIAN SEA    │    THANE CREEK 🌊
    ~~~~~~~~~~~~~~~   │   ~~~~~~~~~~~~~~~
                      │
         🏙️ Borivali  │
         (R/N)        │
                      │
         🏙️ Malad     │
         (P/N)        │
                      │
         🏙️ Andheri   │   🏙️ Chembur
         (K/E)        │   (M/E)
         ✈️ Airport   │
                      │
         🌉 Bandra    │   🏙️ Kurla
         (H/E)        │   (L)
                      │
    ~~~~ Mithi River ~~~~
                      │
         🏙️ Mahim     │
         (G/N)        │
                      │
         🏙️ Byculla   │   🏙️ Parel
         (E)          │   (F/S)
         🏥 Hospital  │
                      │
         🚉 CST       │
         (C,D)        │
                      │
         🏛️ Gateway   │
         Colaba (A)   │
                      │
                      ↓
                    SOUTH
```

---

## 📊 Data Flow Visualization

### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    CSV DATA FILES                        │
├─────────────────────────────────────────────────────────┤
│  Static (4)  │  Historical (3)  │  Real-Time (5)  │  AI (3) │
│  • Wards     │  • Rainfall      │  • Rain         │  • Risk │
│  • Infra     │  • Floods        │  • Water        │  • Explain │
│  • Roads     │  • Cyclones      │  • Traffic      │  • Recommend │
│  • Edges     │                  │  • Power        │         │
│              │                  │  • Alerts       │         │
└──────┬───────┴──────────┬───────┴────────┬────────┴─────────┘
       │                  │                │
       ↓                  ↓                ↓
┌─────────────────────────────────────────────────────────┐
│              MUMBAI DATA LOADER (Python)                 │
│              Pandas DataFrames + Methods                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (20+ Routes)                │
│  /wards  /sensors  /risk-scores  /recommendations       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓ HTTP/JSON
┌─────────────────────────────────────────────────────────┐
│              REACT FRONTEND (Axios)                      │
│              Mumbai Map Component                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│              USER INTERFACE (Browser)                    │
│  Interactive Map • Real-Time Data • Alerts • Audio      │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Risk Calculation Visualization

### Feature Importance
```
Risk Score Calculation for Ward E (Byculla):

Rainfall (35%)        ████████████████████████████████████ 45mm
Water Level (25%)     █████████████████████████ 320cm (ALERT!)
Slum Density (18%)    ██████████████████ 35%
Drain Stress (12%)    ████████████ High
Traffic (10%)         ██████████ 82% congestion

                      ↓
              Composite Risk: 0.80 (80%)
              Severity: SEVERE 🔴
```

### Risk Distribution Across Mumbai
```
Ward    Risk    Severity    Population    Visualization
────────────────────────────────────────────────────────
R/N     38%     Low         710,000       ████░░░░░░
P/N     62%     High        580,000       ██████░░░░
K/E     65%     High        460,000       ██████░░░░
H/E     58%     Moderate    290,000       █████░░░░░
L       86%     SEVERE      800,000       ████████░░ 🔴
G/N     60%     High        240,000       ██████░░░░
E       80%     SEVERE      189,986       ████████░░ 🔴
F/S     68%     High        220,000       ██████░░░░
D       55%     Moderate    174,996       █████░░░░░
C       48%     Moderate    196,993       ████░░░░░░
B       42%     Moderate    157,811       ████░░░░░░
A       35%     Low         185,014       ███░░░░░░░
M/E     52%     Moderate    350,000       █████░░░░░
```

---

## 🚨 Alert System Visualization

### Alert Levels
```
┌─────────────────────────────────────────────────────┐
│  SEVERE ALERT 🔴                                    │
│  Ward: Kurla (L)                                    │
│  Risk: 86%                                          │
│  🔊 AUDIO ALERT ACTIVE                              │
│                                                      │
│  Immediate Actions Required:                        │
│  ✓ Evacuate low-lying areas                        │
│  ✓ Avoid travel on flood-prone roads               │
│  ✓ Move to higher floors                           │
│  ✓ Keep emergency supplies ready                   │
│                                                      │
│  Affected Population: ~800,000                      │
│  Expected Impact: High casualties, infrastructure   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  HIGH ALERT 🟠                                      │
│  Ward: Andheri East (K/E)                          │
│  Risk: 65%                                          │
│                                                      │
│  Recommended Actions:                               │
│  • Monitor weather updates                          │
│  • Prepare for possible evacuation                 │
│  • Avoid unnecessary travel                        │
│                                                      │
│  Affected Population: ~460,000                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  MODERATE ALERT 🟡                                  │
│  Ward: Bandra East (H/E)                           │
│  Risk: 58%                                          │
│                                                      │
│  Advisory:                                          │
│  • Stay alert to weather conditions                │
│  • Keep emergency contacts ready                   │
│  • Monitor local news                              │
└─────────────────────────────────────────────────────┘
```

---

## 📡 Sensor Network Visualization

### Mithi River Monitoring
```
    Thane Creek
         │
         ↓
    ┌────────┐
    │ Sensor │ WS003: Kurla Storm Drain
    │ 190cm  │ Threshold: 200cm ✓
    └────────┘
         │
         ↓ Mithi River Flow
    ┌────────┐
    │ Sensor │ WS002: Andheri
    │ 280cm  │ Threshold: 300cm ✓
    └────────┘
         │
         ↓
    ┌────────┐
    │ Sensor │ WS001: Sion
    │ 320cm  │ Threshold: 300cm ⚠️ ALERT!
    └────────┘
         │
         ↓
    Arabian Sea
```

### Rain Sensor Network
```
         North
           ↑
           
    RS003 (L)      RS002 (K/E)
    72mm 🔴        60mm 🟠
           
           
    RS001 (E)
    45mm 🟡
           
           ↓
         South
```

---

## 🎬 Animation States

### Normal State
```
Ward: Colaba (A)
Risk: 35% (Low)

    🟢
   ╱  ╲
  │    │  ← Static, no animation
   ╲  ╱
    ──
  Colaba
```

### High Risk State
```
Ward: Andheri (K/E)
Risk: 65% (High)

    🟠
   ╱  ╲
  │ ⚠️ │  ← Slow pulse (2s cycle)
   ╲  ╱
    ──
  Andheri
```

### Severe Risk State
```
Ward: Kurla (L)
Risk: 86% (Severe)

    🔴
   ╱  ╲
  │ 🚨 │  ← Fast pulse (1s cycle)
   ╲  ╱    + Audio alert
    ──
   Kurla
```

---

## 📱 Responsive Layout

### Desktop View (1920x1080)
```
┌────────────────────────────────────────────────────────┐
│  Header: Mumbai Real-Time Disaster Monitor             │
├──────────────────┬─────────────────────────────────────┤
│                  │                                      │
│  Mumbai Map      │  Ward Details                       │
│  (550x650)       │  + Alerts                           │
│                  │  (Scrollable)                       │
│                  │                                      │
├──────────────────┴─────────────────────────────────────┤
│  Sensor Data (3 columns)                               │
│  [Rain] [Water] [Traffic]                              │
├────────────────────────────────────────────────────────┤
│  System Status (4 cards)                               │
└────────────────────────────────────────────────────────┘
```

### Tablet View (768x1024)
```
┌────────────────────────────┐
│  Header                    │
├────────────────────────────┤
│  Mumbai Map                │
│  (Full width)              │
├────────────────────────────┤
│  Ward Details              │
├────────────────────────────┤
│  Alerts                    │
├────────────────────────────┤
│  Sensor Data (2 columns)   │
├────────────────────────────┤
│  System Status (2x2)       │
└────────────────────────────┘
```

---

## 🎨 Theme Colors

### Background
- Primary: `#0a0e1a` (Dark blue-black)
- Secondary: `#1e293b` (Slate)
- Card: `#1e293b` with opacity

### Risk Colors
- Very Low: `#10b981` (Green)
- Low: `#84cc16` (Light green)
- Moderate: `#f59e0b` (Amber)
- High: `#f97316` (Orange)
- Severe: `#ef4444` (Red)

### Water Features
- Arabian Sea: `#1e3a8a` (Deep blue)
- Mithi River: `#06b6d4` (Cyan)
- Water sensors: `#60a5fa` (Light blue)

### UI Elements
- Text: `#ffffff` (White)
- Secondary text: `#94a3b8` (Gray)
- Borders: `#334155` (Dark gray)
- Hover: `#3b82f6` (Blue)

---

## 🎯 Interactive Elements

### Clickable Wards
```
Before Click:          After Click:
    🟠                    🟠
   ╱  ╲                 ╱  ╲
  │    │    →          │ ✓ │  + Details panel updates
   ╲  ╱                 ╲  ╱
    ──                    ──
  Andheri               Andheri
```

### Audio Toggle
```
OFF State:             ON State:
┌──────────────┐      ┌──────────────┐
│ 🔇 Audio OFF │  →   │ 🔊 Audio ON  │
└──────────────┘      └──────────────┘
                      (Plays alerts)
```

### Alert Counter
```
No Alerts:            Active Alerts:
┌──────────────┐      ┌──────────────┐
│ 🔔 0 Alerts  │      │ 🔔 5 Alerts  │
│   (Green)    │      │   (Red)      │
└──────────────┘      └──────────────┘
```

---

**This visual guide helps understand the Mumbai Digital Twin interface and interactions.**
