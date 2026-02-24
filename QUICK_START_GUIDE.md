# 🚀 Quick Start Guide - Running on Localhost

## Prerequisites

Before starting, ensure you have:
- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- Terminal/Command Prompt access

---

## Step 1: Backend Setup (FastAPI)

### 1.1 Navigate to Project Directory
```bash
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine
```

### 1.2 Install Python Dependencies
```bash
# Install required packages
pip install fastapi uvicorn pandas numpy python-dotenv
```

### 1.3 Start Backend Server
```bash
# Run from project root directory
uvicorn backend.main:app --reload --port 8001
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Backend is now running at:** `http://localhost:8001`

**Test it:** Open browser and go to `http://localhost:8001/docs` to see API documentation

---

## Step 2: Frontend Setup (React + Vite)

### 2.1 Open New Terminal Window
Keep the backend terminal running and open a new terminal

### 2.2 Navigate to Frontend Directory
```bash
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
```

### 2.3 Install Node Dependencies (First Time Only)
```bash
npm install
```

### 2.4 Start Frontend Development Server
```bash
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:8082/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

**Frontend is now running at:** `http://localhost:8082`

---

## Step 3: Access the Application

### Open Your Browser
Navigate to: **http://localhost:8082**

You should see the Mumbai Digital Twin dashboard!

---

## 🎯 Quick Demo Workflow

### 1. Select a Ward
- Go to **Mumbai Live** page
- Click on any ward (e.g., "Borivali", "Kurla", "Andheri East")
- Ward will be highlighted and selected

### 2. Run Urban Evacuation Simulation
- Navigate to **Urban Evacuation** page
- Click **"Quick Start All Systems"** button
- Watch as:
  - Human agents evacuate on foot 👤
  - Rescue cars pick up people 🚗
  - Real-time statistics update

### 3. View XAI Explanations
- Navigate to **Decision Explainer** page
- See all 7 levels of XAI:
  - **Level 1-2**: Decision logs and feature analysis
  - **Level 3**: Counterfactual "what-if" scenarios
  - **Level 4+7**: Causal relationships and natural language reports
  - **Level 6**: Monte Carlo uncertainty analysis
- Click on any decision to see detailed explanations

---

## 📁 Project Structure

```
AI_Strategic_Risk_Engine/
├── backend/                    # FastAPI Backend (Port 8001)
│   ├── main.py                # Main FastAPI app
│   ├── api/                   # API routes
│   │   ├── evacuation_routes.py
│   │   ├── explainability_routes.py
│   │   └── mumbai_routes.py
│   ├── core/                  # Core logic
│   │   └── explainable_ai/   # 7-level XAI system
│   └── evacuation_system/    # Grid, pathfinding, agents
│
├── frontend/                  # React Frontend (Port 8082)
│   ├── src/
│   │   ├── pages/            # Main pages
│   │   │   ├── MumbaiMapRealtime.jsx
│   │   │   ├── UrbanEvacuation.jsx
│   │   │   └── DecisionExplainer.jsx
│   │   ├── context/          # Ward context
│   │   └── services/         # API calls
│   └── package.json
│
└── data/                      # Mumbai data files
    └── mumbai/
        ├── static/           # Ward data, infrastructure
        ├── realtime/         # Sensor data
        └── outputs/          # Generated logs
```

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'backend'`
```bash
# Solution: Run uvicorn from project root
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine
uvicorn backend.main:app --reload --port 8001
```

**Problem:** Port 8001 already in use
```bash
# Solution: Kill existing process or use different port
lsof -ti:8001 | xargs kill -9
# Or use different port
uvicorn backend.main:app --reload --port 8002
```

**Problem:** Missing Python packages
```bash
# Install all dependencies
pip install fastapi uvicorn pandas numpy python-dotenv pydantic
```

---

### Frontend Issues

**Problem:** Port 8082 already in use
```bash
# Solution: Kill existing process
lsof -ti:8082 | xargs kill -9
# Then restart
npm run dev
```

**Problem:** `npm: command not found`
```bash
# Solution: Install Node.js
# Visit https://nodejs.org/ and download installer
# Or use Homebrew on macOS
brew install node
```

**Problem:** API connection errors (CORS)
- Make sure backend is running on port 8001
- Check browser console for errors
- Verify API URLs in frontend code point to `http://localhost:8001`

---

## 🎮 Available Pages

### 1. Mumbai Live (Real-time Map)
- **URL:** `http://localhost:8082/`
- **Features:** Interactive ward map, real-time risk scores, ward selection

### 2. Urban Evacuation
- **URL:** `http://localhost:8082/urban-evacuation`
- **Features:** 
  - 20x20 grid visualization
  - Human agent simulation (A* pathfinding)
  - Car-based evacuation
  - Real-time statistics

### 3. Decision Explainer (XAI Dashboard)
- **URL:** `http://localhost:8082/explainability`
- **Features:**
  - Level 1-2: Decision logs, feature importance
  - Level 3: Counterfactual analysis
  - Level 4: Causal graphs
  - Level 6: Uncertainty quantification
  - Level 7: Natural language explanations

### 4. Risk Heatmap
- **URL:** `http://localhost:8082/risk-heatmap`
- **Features:** Visual risk distribution across Mumbai

### 5. Resilience Dashboard
- **URL:** `http://localhost:8082/resilience`
- **Features:** Infrastructure resilience metrics

### 6. Policy Comparison
- **URL:** `http://localhost:8082/policy-comparison`
- **Features:** Compare different policy scenarios

---

## 🔄 Restart Instructions

### To Restart Backend:
```bash
# In backend terminal, press CTRL+C to stop
# Then restart:
uvicorn backend.main:app --reload --port 8001
```

### To Restart Frontend:
```bash
# In frontend terminal, press CTRL+C to stop
# Then restart:
npm run dev
```

### To Restart Both:
```bash
# Terminal 1 (Backend)
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine
uvicorn backend.main:app --reload --port 8001

# Terminal 2 (Frontend)
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
npm run dev
```

---

## 📊 API Endpoints

### Backend API Documentation
- **Swagger UI:** `http://localhost:8001/docs`
- **ReDoc:** `http://localhost:8001/redoc`

### Key Endpoints:
- `GET /api/evacuation/grid` - Get evacuation grid
- `POST /api/evacuation/initialize-simulation` - Start human evacuation
- `POST /api/evacuation/car/auto-assign` - Start car evacuation
- `GET /api/explainability/decisions/recent` - Get recent decisions
- `GET /api/explainability/global-importance` - Get feature importance
- `POST /api/explainability/counterfactual` - Generate counterfactual
- `POST /api/explainability/uncertainty-analysis` - Run Monte Carlo
- `POST /api/explainability/comprehensive-report` - Generate NL report

---

## 💡 Tips for Best Experience

1. **Always start backend first**, then frontend
2. **Select a ward** before running evacuation simulation
3. **Use Chrome or Firefox** for best compatibility
4. **Keep both terminals open** while using the application
5. **Check browser console** (F12) if something doesn't work
6. **Refresh page** if grid doesn't load properly

---

## 🎓 Demo Sequence for Presentation

1. **Start both servers** (backend + frontend)
2. **Open Mumbai Live** → Select "Kurla" (high risk ward)
3. **Go to Urban Evacuation** → Click "Quick Start All Systems"
4. **Watch simulation** for 30-60 seconds
5. **Navigate to Decision Explainer** → See all XAI levels
6. **Click on different decisions** → Show unique explanations
7. **Switch between tabs** → Demonstrate all 7 levels

---

## 📝 Notes

- Backend runs on **port 8001**
- Frontend runs on **port 8082**
- Grid resets to fresh state on page refresh
- Decisions are logged in memory (cleared on backend restart)
- Real-time updates every 3 seconds
- Simulation runs at 1 step per second

---

## 🆘 Need Help?

If you encounter issues:
1. Check both terminals for error messages
2. Verify ports 8001 and 8082 are not in use
3. Ensure you're in the correct directory
4. Try restarting both servers
5. Check browser console (F12) for frontend errors

---

## ✅ Success Checklist

- [ ] Backend running on http://localhost:8001
- [ ] Frontend running on http://localhost:8082
- [ ] Can access Mumbai Live page
- [ ] Can select a ward
- [ ] Can start evacuation simulation
- [ ] Can see XAI explanations
- [ ] Both human agents and cars visible
- [ ] Real-time updates working

---

**You're all set! Enjoy exploring the Mumbai Digital Twin with Advanced XAI! 🎉**
