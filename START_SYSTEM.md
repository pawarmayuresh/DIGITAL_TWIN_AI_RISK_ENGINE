# 🚀 Start AI Strategic Risk Engine

## Quick Start (Recommended)

### Step 1: Stop any existing backend process

```bash
# Find process on port 8000
lsof -ti:8000

# If a PID is shown, kill it
kill -9 <PID>

# Or use the management script
chmod +x manage_backend.sh
./manage_backend.sh stop
```

### Step 2: Start Backend

**Terminal 1:**
```bash
# Make sure you're in the project root
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine

# Start backend
uvicorn backend.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Verify backend is running:**
```bash
curl http://localhost:8000/api/health/live
```

### Step 3: Start Frontend

**Terminal 2:**
```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:8081/
```

### Step 4: Open Browser

Open: **http://localhost:8081**

---

## Alternative: Using Management Scripts

### Backend
```bash
# Stop backend
./manage_backend.sh stop

# Start backend
./manage_backend.sh start

# Check status
./manage_backend.sh status

# Restart
./manage_backend.sh restart
```

### Frontend
```bash
# Start frontend
./start_frontend.sh
```

---

## Troubleshooting

### Error: Address already in use (Port 8000)

**Solution 1: Find and kill the process**
```bash
# Find the process
lsof -ti:8000

# Kill it (replace <PID> with the number shown)
kill -9 <PID>
```

**Solution 2: Use different port**
```bash
# Start backend on port 8001
uvicorn backend.main:app --reload --port 8001

# Update frontend proxy in frontend/vite.config.js
# Change target to 'http://localhost:8001'
```

### Error: Cannot connect to backend

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/api/health/live
   ```

2. **Check backend logs** in Terminal 1

3. **Verify port 8000** is correct in `frontend/vite.config.js`

### Error: npm install fails

```bash
cd frontend

# Clear cache
npm cache clean --force

# Remove old files
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Error: Module not found

```bash
# Make sure you're in the right directory
pwd

# Should show: /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine

# For backend issues, check Python path
python3 -c "import sys; print(sys.path)"

# For frontend issues, check node_modules
ls frontend/node_modules
```

---

## System Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (React + Vite)                │
│  http://localhost:8081                  │
│                                         │
│  - City Overview                        │
│  - Disaster Simulation                  │
│  - Explainability Dashboard             │
│  - Resilience Metrics                   │
└─────────────┬───────────────────────────┘
              │ API Calls
              ▼
┌─────────────────────────────────────────┐
│  Backend (FastAPI + Python)             │
│  http://localhost:8000                  │
│                                         │
│  - Health API                           │
│  - Demo API                             │
│  - Twin API                             │
│  - Strategic AI API                     │
│  - Multi-Agent API                      │
│  - Learning API                         │
│  - Explainability API                   │
│  - Analytics API                        │
└─────────────────────────────────────────┘
```

---

## Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 8081
- [ ] Can access http://localhost:8081
- [ ] City Overview page loads
- [ ] Can navigate between pages
- [ ] No console errors in browser

---

## What to Do Next

1. **Explore Dashboards**: Navigate through all 8 sections
2. **Run Simulation**: Go to Disaster Simulation and run a scenario
3. **Check Explainability**: View decision traces in XAI section
4. **Monitor Metrics**: Check Resilience Dashboard for city health

---

## Stopping the System

### Stop Backend
Press `Ctrl+C` in Terminal 1 (backend terminal)

Or:
```bash
./manage_backend.sh stop
```

### Stop Frontend
Press `Ctrl+C` in Terminal 2 (frontend terminal)

---

## Development Tips

### Backend Development
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health/live
- Logs appear in Terminal 1

### Frontend Development
- Hot reload enabled (changes auto-refresh)
- React DevTools recommended
- Check browser console for errors

### Making Changes
- **Backend**: Edit files in `backend/`, server auto-reloads
- **Frontend**: Edit files in `frontend/src/`, page auto-refreshes

---

## Need Help?

- **Frontend Setup**: See `FRONTEND_SETUP.md`
- **Batch 11 Details**: See `BATCH_11_COMPLETE_SUMMARY.md`
- **API Documentation**: http://localhost:8000/docs (when backend is running)

---

🎉 **Enjoy the AI Strategic Risk Engine!**
