# 🎨 Frontend Setup Guide

## Prerequisites

- Node.js 18+ and npm
- Backend server running on port 8000

## Quick Start

### Option 1: Using the start script

```bash
./start_frontend.sh
```

### Option 2: Manual setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at **http://localhost:8081**

---

## What You'll See

### 1. City Overview (Default Page)
- Population: 500,000
- Infrastructure Health: 85%
- Economic Value: $50B
- Active Disasters: 0

### 2. Disaster Simulation
- Select disaster type (Earthquake, Flood, Wildfire, Pandemic, Cyber Attack)
- Adjust severity (1-10)
- Click "Run Simulation"
- View results

### 3. Decision Explainability
- View recent AI decisions
- See confidence levels
- Inspect decision details
- Review audit logs

### 4. Resilience Dashboard
- Overall resilience: 85/100
- Robustness: 87/100
- Social stability: 78/100
- Infrastructure: 82/100

---

## Connecting to Backend

The frontend automatically connects to the backend at `http://localhost:8000`.

### Start Backend

In a separate terminal:

```bash
# From project root
uvicorn backend.main:app --reload
```

### Verify Connection

1. Open http://localhost:8081
2. Navigate to "City Overview"
3. If data loads, connection is successful

---

## Navigation

Use the sidebar to navigate between sections:

- 🏠 **City Overview** - Real-time city metrics
- 📊 **Spatial Grid** - Grid simulation visualization
- ⚠️ **Disaster Sim** - Run disaster scenarios
- 🔗 **Infrastructure** - Network dependencies
- 🔄 **Policy Compare** - Strategy comparison
- 🛡️ **Resilience** - Resilience metrics
- 🗺️ **Risk Heatmap** - Spatial risk distribution
- 🧠 **XAI** - Decision explanations

---

## Troubleshooting

### Port 8081 already in use

```bash
# Find and kill process on port 8081
lsof -ti:8081 | xargs kill -9

# Or change port in vite.config.js
```

### Cannot connect to backend

1. Verify backend is running: `curl http://localhost:8000/api/health/live`
2. Check proxy configuration in `vite.config.js`
3. Look for CORS errors in browser console

### Dependencies won't install

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## Development

### File Structure

```
frontend/src/
├── components/     # Reusable UI components
├── pages/          # Page components (one per route)
├── services/       # API client and services
├── App.jsx         # Main app with routing
└── main.jsx        # Entry point
```

### Adding a New Page

1. Create `src/pages/MyNewPage.jsx`
2. Add route in `src/App.jsx`
3. Add nav item in `src/components/Layout.jsx`

### Making API Calls

```javascript
import { demoAPI } from '../services/api';

const fetchData = async () => {
  try {
    const response = await demoAPI.runScenario('earthquake');
    console.log(response.data);
  } catch (error) {
    console.error('API error:', error);
  }
};
```

---

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

Built files will be in `frontend/dist/`

---

## Next Steps

1. **Start Backend**: `uvicorn backend.main:app --reload`
2. **Start Frontend**: `./start_frontend.sh` or `cd frontend && npm run dev`
3. **Open Browser**: http://localhost:8081
4. **Explore**: Navigate through different dashboards
5. **Run Simulation**: Go to Disaster Simulation and run a scenario

---

## Support

- Frontend README: `frontend/README.md`
- API Documentation: Check backend API routes
- Batch 11 Summary: `BATCH_11_COMPLETE_SUMMARY.md`

---

🎉 **Enjoy exploring the AI Strategic Risk Engine!**
