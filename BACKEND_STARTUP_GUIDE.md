# Backend Startup Guide

## The Problem
You were getting `ModuleNotFoundError: No module named 'backend'` because you were running uvicorn from the wrong directory (your home directory `/Users/mayureshpawar` instead of the project directory).

## Solution: Use the Startup Script

### Option 1: Use the startup script (RECOMMENDED)
```bash
# Navigate to project directory first
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine

# Run the startup script
./start_backend.sh
```

### Option 2: Manual startup
```bash
# Navigate to project directory
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine

# Start backend from project root
uvicorn backend.main:app --reload --port 8001
```

## Important Notes

1. **Always run from project root**: The command MUST be run from `/Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine`

2. **Check your current directory**:
   ```bash
   pwd
   # Should output: /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine
   ```

3. **If you're in the wrong directory**:
   ```bash
   cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
   ```

## Verify Backend is Running

Once started, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFilesProcess
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Test the backend:
```bash
curl http://localhost:8001/api/health/live
```

## Start Frontend

In a separate terminal:
```bash
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
npm run dev
```

Frontend will be available at: http://localhost:8081

## Full System Startup

1. Terminal 1 - Backend:
   ```bash
   cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
   ./start_backend.sh
   ```

2. Terminal 2 - Frontend:
   ```bash
   cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine/frontend
   npm run dev
   ```

3. Open browser: http://localhost:8081

4. Navigate to "Urban Evacuation" page to see the car + human agent system

## Troubleshooting

### Still getting ModuleNotFoundError?
```bash
# Check you're in the right directory
pwd

# Should show: /Users/mayureshpawar/DIGITAL_TWIN/AI_Strategic_Risk_Engine
# If not, navigate there:
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
```

### Backend won't start?
```bash
# Check if port 8001 is already in use
lsof -i :8001

# Kill existing process if needed
kill -9 <PID>
```

### Frontend won't connect?
- Ensure backend is running on port 8001
- Check browser console for CORS errors
- Verify frontend is configured to use http://localhost:8001
