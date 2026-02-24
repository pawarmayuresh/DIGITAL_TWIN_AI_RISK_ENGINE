# 🚀 START HERE - Complete Urban Evacuation System

## ✅ System Status: READY TO RUN

The evacuation system has been tested and is working correctly!

---

## 📋 Quick Start (3 Steps)

### Step 1: Start Backend Server

Open Terminal 1 and run:

```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
./start_backend.sh
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Step 2: Start Frontend

Open Terminal 2 and run:

```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
npm run dev
```

You should see:
```
VITE ready in XXX ms
Local: http://localhost:8081/
```

### Step 3: Open Browser

Navigate to: **http://localhost:8081**

Click on **"Urban Evacuation"** in the menu

---

## 🎯 What You'll See

### Urban Evacuation Page Features:

1. **20x20 Mumbai Grid** with named zones (A1-T20)
   - 🟢 Green = Safe zones
   - 🟡 Yellow = Medium risk
   - 🔴 Red = Dangerous zones

2. **Human Agents** (👤 emoji)
   - Created in dangerous zones
   - Follow A* evacuation paths
   - Health bars show condition
   - Age groups: child, adult, elderly

3. **Car Agents** (🚗 emoji)
   - 5 rescue vehicles
   - Automatically assigned to danger zones
   - Pick up people and transport to safety
   - Animated movement

4. **Real-Time Activity Log**
   - Shows all evacuation events
   - Color-coded by type
   - Scrollable history

5. **Statistics Dashboard**
   - Grid statistics
   - Human evacuation progress
   - Car trip counts and distances
   - Completion rates

---

## 🎮 How to Use

### Initialize System:
1. Click **"Initialize Grid"** - Creates 20x20 Mumbai grid
2. Click **"Deploy Human Agents"** - Places people in danger zones
3. Click **"Deploy Cars"** - Adds 5 rescue vehicles
4. Click **"Start Evacuation"** - Begins simulation

### Watch the Evacuation:
- Human agents (👤) walk along green A* paths
- Cars (🚗) drive to danger zones, pick up people, drive to safety
- Activity log shows real-time events
- Statistics update automatically

### Controls:
- **Real-time Updates** checkbox - Refreshes grid data every 3 seconds
- **Ward Selection** - Focus on specific Mumbai ward
- **Step-by-step** - Manual control of simulation

---

## 🔧 System Architecture

### Backend Components:
- `grid_engine.py` - 20x20 Mumbai grid with safety levels
- `pathfinder.py` - A* algorithm for human evacuation
- `car_pathfinder.py` - A* algorithm for car routing
- `human_agent_sim.py` - Human agent behavior and movement
- `car_agent.py` - Car agent with 5-state machine
- `car_evacuation_manager.py` - Orchestrates multiple cars
- `evacuation_routes.py` - FastAPI endpoints

### Frontend Components:
- `UrbanEvacuation.jsx` - Main evacuation UI
- Real-time grid visualization
- Agent rendering and animation
- Activity logging system
- Statistics dashboard

### Data Sources:
- `data/mumbai/realtime/water_level_sensors.csv`
- `data/mumbai/realtime/rain_sensors.csv`
- `data/mumbai/realtime/traffic_density.csv`

---

## 🧪 Testing

Run the test script to verify everything works:

```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
python3 test_evacuation_system.py
```

Expected output:
```
✅ ALL TESTS PASSED - EVACUATION SYSTEM WORKING!
```

---

## 🐛 Troubleshooting

### Backend won't start?

**Problem**: `ModuleNotFoundError: No module named 'backend'`

**Solution**: You must run from the project directory!

```bash
# Check where you are
pwd

# Should show: /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine
# If not, navigate there:
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine

# Then start backend
./start_backend.sh
```

### Port already in use?

```bash
# Check what's using port 8001
lsof -i :8001

# Kill the process
kill -9 <PID>
```

### Frontend can't connect?

1. Verify backend is running: `curl http://localhost:8001/api/health/live`
2. Check browser console for errors
3. Ensure CORS is enabled (already configured)

### No agents showing?

1. Click "Initialize Grid" first
2. Then "Deploy Human Agents"
3. Then "Deploy Cars"
4. Finally "Start Evacuation"

---

## 📊 Key Features Implemented

✅ **Named Grid System** - A1 to T20 (20x20 Mumbai zones)
✅ **A* Pathfinding** - Optimal evacuation routes avoiding danger
✅ **Human Agents** - Age groups, health, movement simulation
✅ **Car Agents** - 5-state machine (IDLE, MOVING, LOADING, etc.)
✅ **Real-Time Data** - Mumbai sensor CSV integration
✅ **Activity Logging** - Complete event history
✅ **Statistics Dashboard** - Live metrics and progress
✅ **Simultaneous Visualization** - Both humans and cars visible
✅ **Smart Positioning** - Agents don't overlap on same grid
✅ **Health Tracking** - Agents lose health in dangerous zones
✅ **Multi-Trip Cars** - Cars return for more people if needed

---

## 📁 Important Files

### Startup Scripts:
- `start_backend.sh` - Backend startup script
- `test_evacuation_system.py` - System verification test

### Documentation:
- `START_HERE.md` - This file
- `BACKEND_STARTUP_GUIDE.md` - Detailed backend instructions
- `CAR_EVACUATION_COMPLETE.md` - Car system documentation

### Backend Code:
- `backend/evacuation_system/` - All evacuation logic
- `backend/api/evacuation_routes.py` - API endpoints

### Frontend Code:
- `frontend/src/pages/UrbanEvacuation.jsx` - Main UI

---

## 🎓 For Faculty Presentation

### Demo Flow:
1. Show the 20x20 Mumbai grid with color-coded zones
2. Deploy human agents - explain age groups and health
3. Deploy cars - show 5 rescue vehicles
4. Start evacuation - watch real-time simulation
5. Point out A* green paths
6. Show activity log with events
7. Explain statistics (trips, evacuated count, distances)
8. Toggle real-time updates to show dynamic data

### Key Points to Highlight:
- Real Mumbai data from CSV sensors
- A* pathfinding algorithm implementation
- Multi-agent system (humans + cars)
- State machine for car behavior
- Real-time visualization
- Complete event logging
- Scalable architecture

---

## 🚀 Next Steps

The system is complete and ready to use! Just follow the Quick Start steps above.

If you need to make changes:
1. Backend changes: Edit files in `backend/evacuation_system/`
2. Frontend changes: Edit `frontend/src/pages/UrbanEvacuation.jsx`
3. API changes: Edit `backend/api/evacuation_routes.py`

The system will auto-reload when you save changes (both backend and frontend have hot-reload enabled).

---

## 📞 Need Help?

1. Check `BACKEND_STARTUP_GUIDE.md` for backend issues
2. Run `python3 test_evacuation_system.py` to verify system
3. Check browser console for frontend errors
4. Check terminal for backend errors

---

**System Status**: ✅ FULLY OPERATIONAL
**Last Tested**: Working perfectly
**Ready for**: Faculty presentation and demo
