# Mumbai Digital Twin - Troubleshooting Guide

## 🔍 Problem: Frontend Not Fetching Real Data from Backend

### Step 1: Verify Backend is Running

```bash
# Check if backend process is running
ps aux | grep uvicorn

# Test health endpoint
curl http://localhost:8000/api/health/live

# Expected response:
# {"status":"healthy","timestamp":"..."}
```

If backend is NOT running:
```bash
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 2: Test Mumbai API Endpoints

Run the test script:
```bash
chmod +x test_backend_api.sh
./test_backend_api.sh
```

Or test manually:
```bash
# Test wards endpoint
curl http://localhost:8000/api/mumbai/wards | python3 -m json.tool

# Expected: Array of ward objects with ward_id, ward_name, population, etc.
```

### Step 3: Check Backend Logs

Look for these messages in the backend terminal:

✅ **Good signs:**
```
✅ All Mumbai data loaded successfully
✅ Mumbai data loader initialized successfully
INFO:     Application startup complete.
```

❌ **Bad signs:**
```
❌ Warning: Could not load Mumbai data
FileNotFoundError: [Errno 2] No such file or directory
ModuleNotFoundError: No module named 'pandas'
```

### Step 4: Check Frontend Console

Open browser DevTools (F12) → Console tab

✅ **Good signs:**
```
🔄 Fetching Mumbai data from backend...
✅ Wards data received: Array(10)
✅ Mumbai data loaded successfully from backend
```

❌ **Bad signs:**
```
❌ Failed to load Mumbai data from backend: Network Error
📦 Loading mock data as fallback...
CORS error: Access-Control-Allow-Origin
```

### Step 5: Check Network Tab

Open DevTools → Network tab → Filter by "XHR"

Look for requests to:
- `http://localhost:8000/api/mumbai/wards`
- `http://localhost:8000/api/mumbai/sensors/rain`
- `http://localhost:8000/api/mumbai/sensors/water`

Check the response:
- **Status 200**: ✅ Working
- **Status 404**: ❌ Endpoint not found
- **Status 500**: ❌ Server error
- **Status 503**: ❌ Data not loaded
- **Failed**: ❌ Backend not running or CORS issue

---

## 🔧 Common Issues and Fixes

### Issue 1: Backend Not Loading Data

**Symptom:** Backend starts but API returns empty data or errors

**Cause:** CSV files not found or pandas not installed

**Fix:**
```bash
# Check if CSV files exist
ls -la data/mumbai/static/
ls -la data/mumbai/realtime/
ls -la data/mumbai/outputs/

# Install pandas if missing
pip3 install pandas

# Restart backend
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Issue 2: CORS Error

**Symptom:** Browser console shows CORS error

**Cause:** Frontend and backend on different origins

**Fix:** Check `backend/config.py` has correct CORS settings:
```python
cors_origins = ["http://localhost:8081", "http://localhost:3000"]
```

### Issue 3: Wrong API URL

**Symptom:** Network requests go to wrong URL

**Cause:** Frontend .env file has wrong API URL

**Fix:**
```bash
# Check frontend/.env
cat frontend/.env

# Should show:
VITE_API_URL=http://localhost:8000

# If wrong, update it:
echo "VITE_API_URL=http://localhost:8000" > frontend/.env

# Restart frontend
cd frontend
npm run dev -- --port 8081
```

### Issue 4: Import Path Error

**Symptom:** Backend logs show `ModuleNotFoundError` or import errors

**Cause:** Incorrect import paths in mumbai_routes.py

**Fix:** The import should be:
```python
from ..data_loaders.mumbai_data_loader import get_mumbai_data_loader
```

NOT:
```python
from backend.data_loaders.mumbai_data_loader import get_mumbai_data_loader
```

### Issue 5: Port Already in Use

**Symptom:** `ERROR: [Errno 48] Address already in use`

**Fix:**
```bash
# Kill process on port 8000
kill -9 $(lsof -ti:8000)

# Or use different port
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Update frontend/.env if using different port
echo "VITE_API_URL=http://localhost:8001" > frontend/.env
```

### Issue 6: Mock Data Showing Instead of Real Data

**Symptom:** Frontend shows "Using Mock Data" badge

**Cause:** Backend not responding or returning errors

**Fix:**
1. Check backend is running: `curl http://localhost:8000/api/health/live`
2. Test Mumbai endpoint: `curl http://localhost:8000/api/mumbai/wards`
3. Check browser console for error messages
4. Verify CORS settings
5. Restart both backend and frontend

---

## 🧪 Complete Testing Procedure

### 1. Test Backend Independently

```bash
# Start backend
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, test endpoints
curl http://localhost:8000/api/health/live
curl http://localhost:8000/api/mumbai/wards | python3 -m json.tool
curl http://localhost:8000/api/mumbai/sensors/rain | python3 -m json.tool
```

Expected output for wards:
```json
[
  {
    "ward_id": "A",
    "ward_name": "Colaba",
    "zone": "South",
    "population": 185014,
    "area_sqkm": 3.5,
    "slum_population_percent": 12,
    "population_density": 52861,
    "risk_score": 0.5,
    "severity_level": "Moderate"
  },
  ...
]
```

### 2. Test Frontend API Calls

Open browser console and run:
```javascript
// Test API connection
fetch('http://localhost:8000/api/mumbai/wards')
  .then(r => r.json())
  .then(data => console.log('Wards:', data))
  .catch(err => console.error('Error:', err));

// Test rain sensors
fetch('http://localhost:8000/api/mumbai/sensors/rain')
  .then(r => r.json())
  .then(data => console.log('Rain sensors:', data))
  .catch(err => console.error('Error:', err));
```

### 3. Check Real-Time Updates

1. Open Mumbai Real-Time page
2. Open browser console
3. Watch for messages every 5 seconds:
   ```
   🔄 Updating real-time sensor data...
   ✅ Real-time data updated
   ```

---

## 📋 Checklist

Before asking for help, verify:

- [ ] Backend is running on port 8000
- [ ] Backend logs show "✅ All Mumbai data loaded successfully"
- [ ] `curl http://localhost:8000/api/health/live` returns success
- [ ] `curl http://localhost:8000/api/mumbai/wards` returns ward data
- [ ] CSV files exist in `data/mumbai/` directories
- [ ] Frontend is running on port 8081
- [ ] `frontend/.env` has `VITE_API_URL=http://localhost:8000`
- [ ] Browser console shows no CORS errors
- [ ] Network tab shows requests to `/api/mumbai/*` endpoints
- [ ] Requests return status 200 (not 404, 500, or Failed)

---

## 🚀 Quick Reset

If nothing works, try a complete reset:

```bash
# 1. Kill all processes
pkill -f uvicorn
pkill -f vite

# 2. Clear any cached data
rm -rf frontend/node_modules/.vite
rm -rf backend/__pycache__
rm -rf backend/**/__pycache__

# 3. Reinstall dependencies
cd backend
pip3 install -r ../requirements.txt
cd ../frontend
npm install

# 4. Start backend
cd ../backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 5. In new terminal, start frontend
cd frontend
npm run dev -- --port 8081

# 6. Open browser
open http://localhost:8081
```

---

## 📞 Still Not Working?

### Collect Debug Information

Run these commands and share the output:

```bash
# 1. Backend status
curl -v http://localhost:8000/api/health/live

# 2. Mumbai wards endpoint
curl -v http://localhost:8000/api/mumbai/wards

# 3. Check CSV files
ls -la data/mumbai/static/
ls -la data/mumbai/realtime/
ls -la data/mumbai/outputs/

# 4. Check Python packages
pip3 list | grep -E "(fastapi|uvicorn|pandas)"

# 5. Check Node packages
cd frontend && npm list | grep -E "(axios|vite|react)"
```

### Check Browser Console

1. Open DevTools (F12)
2. Go to Console tab
3. Copy all error messages (especially red ones)
4. Go to Network tab
5. Filter by "XHR"
6. Click on failed requests
7. Check "Response" tab for error details

---

## ✅ Success Indicators

You'll know it's working when you see:

### Backend Terminal:
```
✅ All Mumbai data loaded successfully
✅ Mumbai data loader initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Browser Console:
```
🔄 Fetching Mumbai data from backend...
✅ Wards data received: Array(10)
✅ Mumbai data loaded successfully from backend
🔄 Updating real-time sensor data...
✅ Real-time data updated
```

### Frontend UI:
- Green "Backend Connected" badge
- Ward circles colored by risk (not all same color)
- Sensor data showing actual values (not "Loading...")
- Alerts showing for high-risk wards (Kurla, Byculla)
- Real-time updates every 5 seconds

---

**Good luck! The system should work once backend is properly serving data. 🚀**
