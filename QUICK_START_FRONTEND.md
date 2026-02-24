# ⚡ Quick Start - Frontend Only

## The Problem You're Facing

You're seeing: `ERROR: [Errno 48] Address already in use`

This means something is already running on port 8000.

## Solution

### Option 1: Kill the existing process (Recommended)

**In your terminal, run these commands one by one:**

```bash
# 1. Find what's using port 8000
lsof -ti:8000
```

This will show a number (PID). Then:

```bash
# 2. Kill that process (replace XXXX with the number you saw)
kill -9 XXXX
```

For example, if you saw `12345`, run:
```bash
kill -9 12345
```

### Option 2: Use a different port

If you can't kill the process, use port 8001 instead:

```bash
uvicorn backend.main:app --reload --port 8001
```

Then update `frontend/vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8001',  // Changed from 8000 to 8001
    changeOrigin: true
  }
}
```

---

## Complete Startup Sequence

### Terminal 1 - Backend

```bash
# Navigate to project root
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine

# Kill any existing process on port 8000
kill -9 $(lsof -ti:8000) 2>/dev/null

# Start backend
uvicorn backend.main:app --reload
```

**Wait for this message:**
```
INFO:     Application startup complete.
```

### Terminal 2 - Frontend

```bash
# Navigate to frontend
cd /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**Wait for this message:**
```
➜  Local:   http://localhost:8081/
```

### Open Browser

Go to: **http://localhost:8081**

---

## One-Line Commands

### Kill process on port 8000
```bash
kill -9 $(lsof -ti:8000) 2>/dev/null || echo "Port 8000 is free"
```

### Start backend
```bash
uvicorn backend.main:app --reload
```

### Start frontend (in new terminal)
```bash
cd frontend && npm install && npm run dev
```

---

## Verify Everything Works

### 1. Check Backend
```bash
curl http://localhost:8000/api/health/live
```

Should return: `{"status":"alive"}`

### 2. Check Frontend
Open browser to: http://localhost:8081

Should see: AI Strategic Risk Engine dashboard

### 3. Test API Connection
In the browser:
1. Go to City Overview
2. If you see city stats, connection works!

---

## Still Having Issues?

### Backend won't start
```bash
# Check Python version
python3 --version

# Should be 3.8 or higher

# Check if backend files exist
ls backend/main.py

# Should show: backend/main.py
```

### Frontend won't start
```bash
# Check Node version
node --version

# Should be 18 or higher

# Check if frontend files exist
ls frontend/package.json

# Should show: frontend/package.json
```

### Can't connect to backend
1. Make sure backend terminal shows "Application startup complete"
2. Try: `curl http://localhost:8000/api/health/live`
3. Check for errors in backend terminal

---

## What You Should See

### Backend Terminal
```
INFO:     Will watch for changes in these directories: ['/Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Frontend Terminal
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:8081/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Browser
- Dark themed dashboard
- Sidebar with 8 menu items
- City Overview page showing stats
- No errors in console (F12)

---

## Next Steps

Once both are running:

1. **Explore**: Click through all 8 dashboard sections
2. **Run Simulation**: Go to "Disaster Sim" and run an earthquake
3. **Check XAI**: View decision explanations
4. **Monitor Metrics**: Check resilience scores

---

## Stop Everything

### Stop Backend
In Terminal 1: Press `Ctrl+C`

### Stop Frontend  
In Terminal 2: Press `Ctrl+C`

---

🚀 **You're all set! Enjoy the system!**
