# Troubleshooting: Null/Static Data in Advanced Features

## Problem
Advanced Features page showing:
- Null values (0 teams, 0 zones)
- Static data that doesn't change
- "Loading..." messages that never complete

## Quick Fix (90% of cases)

### Step 1: Hard Refresh Browser
**Mac**: `Cmd + Shift + R`  
**Windows/Linux**: `Ctrl + Shift + R`

This clears the cached JavaScript and loads the new code.

### Step 2: Check Backend is Running
```bash
cd AI_Strategic_Risk_Engine
./check_api_status.sh
```

You should see all ✓ checkmarks. If not, start the backend:
```bash
./start_backend.sh
```

### Step 3: Restart Frontend
```bash
cd frontend
npm start
```

## Detailed Diagnostics

### Check 1: Backend API Status

Run this command:
```bash
curl http://localhost:8001/api/advanced/system/status
```

**Expected**: JSON response with `"external_data_integration":true`  
**If fails**: Backend is not running. Start it with `./start_backend.sh`

### Check 2: LSTM Endpoint

```bash
curl http://localhost:8001/api/advanced/ml/lstm/predict-24h/Kurla | python3 -m json.tool | head -20
```

**Expected**: JSON with `"predictions"` array and risk scores  
**If fails**: Check backend logs for errors

### Check 3: Swarm Endpoint

```bash
curl http://localhost:8001/api/advanced/swarm/status | python3 -m json.tool
```

**Expected**: 
```json
{
    "total_teams": 10,
    "total_zones": 21,
    "team_status": {...}
}
```

**If shows 0 teams/zones**: The auto-initialization didn't work. Manually initialize:
```bash
curl -X POST "http://localhost:8001/api/advanced/swarm/initialize?num_teams=10"
```

### Check 4: External Data Endpoint

```bash
curl http://localhost:8001/api/advanced/external-data/integrated/Kurla | python3 -m json.tool | head -30
```

**Expected**: JSON with `"overall_risk_score"` and `"risk_factors"`  
**If fails**: Check if numpy is installed: `pip install numpy`

### Check 5: Browser Console

1. Open browser (http://localhost:3000)
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Look for errors (red text)

**Common errors**:
- `Failed to fetch`: Backend not running or CORS issue
- `Network error`: Wrong port or backend crashed
- `JSON parse error`: Backend returning invalid data

## Common Issues & Solutions

### Issue 1: CORS Errors in Browser Console

**Symptom**: 
```
Access to fetch at 'http://localhost:8001' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution**: Backend should already have CORS enabled. If not, check `backend/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: Backend Running on Wrong Port

**Check what port backend is using**:
```bash
ps aux | grep uvicorn
```

**Should show**: `--port 8001`

**If different port**: Update frontend API calls or restart backend with correct port

### Issue 3: Old JavaScript Cached

**Symptoms**:
- Code changes don't appear
- Still seeing old behavior
- Console shows old file versions

**Solution**:
1. Hard refresh: `Cmd+Shift+R` / `Ctrl+Shift+R`
2. Clear browser cache completely
3. Open in Incognito/Private window
4. Restart browser

### Issue 4: npm/Node Issues

**Symptom**: Frontend won't start or shows errors

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue 5: Python Dependencies Missing

**Symptom**: Backend crashes or returns errors

**Solution**:
```bash
cd AI_Strategic_Risk_Engine
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install numpy  # Specifically needed for enhancements
```

## Verification Steps

After fixing, verify everything works:

### 1. Run API Status Check
```bash
cd AI_Strategic_Risk_Engine
./check_api_status.sh
```

All should show ✓

### 2. Run Enhancement Tests
```bash
python3 test_enhancements.py
```

Should show: `ALL TESTS PASSED ✓`

### 3. Check Frontend

Open http://localhost:3000/advanced-features

**You should see**:
- ✅ Risk scores between 15% and 85% (NOT 55%)
- ✅ Different scores for different wards
- ✅ "LIVE DATA" badge on LSTM card
- ✅ Green pulsing dot when live mode active
- ✅ "Last updated: Xs ago" timestamp
- ✅ Swarm showing 10 teams, 21 zones
- ✅ Factor breakdown (Weather, Traffic, Sensors)

### 4. Test Auto-Refresh

1. Watch the "Last updated" timer
2. Should update every 30 seconds
3. Risk scores should change slightly
4. Pulsing dot should be visible

## Still Not Working?

### Nuclear Option: Complete Reset

```bash
# 1. Stop everything
pkill -f uvicorn
pkill -f node

# 2. Clean backend
cd AI_Strategic_Risk_Engine
rm -rf __pycache__ backend/__pycache__ backend/**/__pycache__

# 3. Clean frontend
cd frontend
rm -rf node_modules .next build

# 4. Reinstall
npm install

# 5. Start backend
cd ..
./start_backend.sh

# 6. Wait for "Application startup complete"

# 7. Start frontend (new terminal)
cd frontend
npm start

# 8. Hard refresh browser
# Cmd+Shift+R / Ctrl+Shift+R
```

### Check Logs

**Backend logs**:
```bash
tail -f AI_Strategic_Risk_Engine/backend.log
```

**Frontend logs**: Check the terminal where `npm start` is running

### Manual API Test

Open browser and go directly to:
- http://localhost:8001/api/advanced/ml/lstm/predict-24h/Kurla
- http://localhost:8001/api/advanced/swarm/status
- http://localhost:8001/api/advanced/external-data/integrated/Kurla

If these show data in browser, the backend is working and it's a frontend issue.

## Expected Behavior

### LSTM Predictions
- Risk scores: 15% to 85%
- Different for each ward
- Changes based on time of day
- Shows factor breakdown

### External Data
- Overall risk: 20% to 70%
- Weather, traffic, sensor risks shown
- Updates every 30 seconds
- Animated progress bars

### Swarm Intelligence
- 10 teams
- 21 zones (auto-initialized)
- Team status breakdown
- Efficiency percentage

### Weekly Pattern
- 7 days of predictions
- Risk categories (LOW, MODERATE, HIGH, CRITICAL)
- Trend indicator (increasing/decreasing/stable)

## Contact/Debug Info

If still having issues, provide this info:

1. **Backend status**: Output of `./check_api_status.sh`
2. **Browser console**: Screenshot of any errors (F12 → Console)
3. **Network tab**: Check if API calls are being made (F12 → Network)
4. **Backend logs**: Last 50 lines of backend output
5. **Operating system**: Mac/Windows/Linux
6. **Browser**: Chrome/Firefox/Safari version

## Quick Reference

| Component | Port | URL |
|-----------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8001 | http://localhost:8001 |
| API Docs | 8001 | http://localhost:8001/docs |

| Endpoint | Purpose |
|----------|---------|
| `/api/advanced/ml/lstm/predict-24h/{ward}` | LSTM predictions |
| `/api/advanced/swarm/status` | Swarm coordination |
| `/api/advanced/external-data/integrated/{ward}` | Real-time data |
| `/api/advanced/ml/lstm/weekly-pattern/{ward}` | Weekly forecast |

## Success Indicators

✅ Backend returns JSON data  
✅ Frontend makes API calls (check Network tab)  
✅ No CORS errors in console  
✅ Risk scores vary by ward and time  
✅ Auto-refresh works every 30 seconds  
✅ "LIVE DATA" badge visible  
✅ Swarm shows 10 teams, 21 zones  

If all ✅, the system is working correctly!
