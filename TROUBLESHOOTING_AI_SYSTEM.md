# 🔧 Troubleshooting AI System

## Issue: Simulation Shows 0 Affected Cells

### Root Causes:
1. Grid not initialized with disaster hotspots
2. AI engine not receiving correct grid data
3. Severity not being applied to spread rate
4. Frontend not refreshing after code changes

---

## ✅ Quick Fixes

### Fix 1: Hard Refresh Frontend
```bash
# In browser, press:
Cmd + Shift + R (Mac)
Ctrl + Shift + R (Windows/Linux)

# Or clear cache:
# Chrome: DevTools → Network → Disable cache
# Then reload page
```

### Fix 2: Restart Dev Server
```bash
# Stop frontend (Ctrl+C in terminal)
cd frontend
rm -rf .vite  # Clear Vite cache
npm run dev
```

### Fix 3: Check Browser Console
```
1. Open DevTools (F12 or Cmd+Option+I)
2. Go to Console tab
3. Look for errors in red
4. Common errors:
   - "IntelligentDisasterSimulator is not defined"
   - "Cannot read property 'simulateStep' of undefined"
   - Import errors
```

### Fix 4: Verify AI Engine Import
```javascript
// In DisasterSimulation.jsx, check this line exists:
import { IntelligentDisasterSimulator } from '../services/aiEngine';

// If error, check file exists:
ls -la frontend/src/services/aiEngine.js
```

---

## 🧪 Test AI Engine Manually

### Test 1: Check Grid Initialization
```javascript
// In browser console:
console.log('Grid:', grid);
// Should show 20x20 array with floodLevel, fireIntensity, contamination

// Check for hotspots:
grid.forEach((row, y) => {
  row.forEach((cell, x) => {
    if (cell.floodLevel > 0.3) {
      console.log(`Hotspot at [${x},${y}]: ${cell.floodLevel}`);
    }
  });
});
```

### Test 2: Check AI Simulator
```javascript
// In browser console after clicking "Run Simulation":
console.log('Simulator:', simulatorRef.current);
// Should show IntelligentDisasterSimulator object

// Test one step:
const result = simulatorRef.current.simulateStep();
console.log('AI Results:', result);
// Should show decisions, evacuationPaths, resourceAllocation
```

### Test 3: Check Severity Impact
```javascript
// Run simulation with severity 3:
// Expected: 1-2 hotspots, slow spread

// Run simulation with severity 10:
// Expected: 5 hotspots, fast spread

// Compare affected cells after 10 steps
```

---

## 🔍 Debugging Steps

### Step 1: Verify Files Exist
```bash
ls -la frontend/src/services/aiEngine.js
ls -la frontend/src/pages/DisasterSimulation.jsx
ls -la frontend/src/context/WardContext.jsx
```

### Step 2: Check for Syntax Errors
```bash
cd frontend
npm run build
# Look for errors in output
```

### Step 3: Check Network Requests
```
1. Open DevTools → Network tab
2. Run simulation
3. Look for failed requests (red)
4. Check if backend is responding
```

### Step 4: Check State Updates
```javascript
// Add console.logs in DisasterSimulation.jsx:

const updateSimulation = () => {
  console.log('🔄 Update simulation called');
  console.log('Simulator exists:', !!simulatorRef.current);
  
  if (simulatorRef.current) {
    const aiResults = simulatorRef.current.simulateStep();
    console.log('AI Results:', aiResults);
    console.log('Decisions:', aiResults.decisions.length);
    console.log('Evacuations:', aiResults.evacuationPaths.length);
  }
  
  // ... rest of code
};
```

---

## 🎯 Expected Behavior

### Severity 3/10:
- **Hotspots**: 1-2 initial disaster points
- **Spread Rate**: 30% per step
- **Affected Cells**: 10-30 after 50 steps
- **Evacuations**: 0-5 cells
- **AI Decisions**: 5-15 decisions

### Severity 7/10:
- **Hotspots**: 3-4 initial disaster points
- **Spread Rate**: 70% per step
- **Affected Cells**: 100-200 after 50 steps
- **Evacuations**: 20-50 cells
- **AI Decisions**: 50-100 decisions

### Severity 10/10:
- **Hotspots**: 5 initial disaster points
- **Spread Rate**: 100% per step
- **Affected Cells**: 300-400 after 50 steps
- **Evacuations**: 100-200 cells
- **AI Decisions**: 150-250 decisions

---

## 🐛 Common Errors & Solutions

### Error 1: "IntelligentDisasterSimulator is not a constructor"
**Solution**:
```javascript
// Check export in aiEngine.js:
export class IntelligentDisasterSimulator { ... }

// Check import in DisasterSimulation.jsx:
import { IntelligentDisasterSimulator } from '../services/aiEngine';
```

### Error 2: "Cannot read property 'simulateStep' of undefined"
**Solution**:
```javascript
// Add null check:
if (simulatorRef.current) {
  const aiResults = simulatorRef.current.simulateStep();
  // ... use results
}
```

### Error 3: "grid is not defined"
**Solution**:
```javascript
// Make sure grid is initialized before creating simulator:
useEffect(() => {
  initializeGrid();
}, [selectedWard, selectedDisaster, severity]);
```

### Error 4: All cells showing same disaster level
**Solution**:
```javascript
// Check spread function uses severity:
spreadRate = 0.15 * this.severity; // NOT just 0.15
```

---

## 📊 Verification Checklist

After fixes, verify:

- [ ] Grid shows 20x20 cells
- [ ] Yellow borders show infrastructure
- [ ] Initial hotspots visible (colored cells)
- [ ] Clicking "Run Simulation" starts animation
- [ ] Progress bar moves 0% → 100%
- [ ] Affected cells count increases
- [ ] Casualties count increases
- [ ] Evacuated count increases (if severity > 6)
- [ ] AI Decision cards appear below grid
- [ ] Evacuation Paths section shows A* routes
- [ ] Resource Allocation shows CSP results
- [ ] Simulation logs show AI messages

---

## 🚀 Full Reset Procedure

If nothing works, do a complete reset:

```bash
# 1. Stop all processes
# Press Ctrl+C in both terminals

# 2. Clear all caches
cd ~/DIGITAL_TWIN/AI_Strategic_Risk_Engine
rm -rf frontend/.vite
rm -rf frontend/node_modules/.vite
rm -rf frontend/dist

# 3. Reinstall dependencies
cd frontend
npm install

# 4. Restart backend
cd ..
./start_backend.sh

# 5. In NEW terminal, restart frontend
cd frontend
npm run dev

# 6. Hard refresh browser
# Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# 7. Test simulation
# - Select ward
# - Set severity to 7
# - Click Run Simulation
# - Watch for AI decisions
```

---

## 📞 Still Not Working?

### Check These:

1. **Node Version**: `node --version` (should be 16+)
2. **Python Version**: `python3 --version` (should be 3.8+)
3. **Port Conflicts**: `lsof -ti:8001` and `lsof -ti:8081`
4. **File Permissions**: `ls -la frontend/src/services/`
5. **Git Status**: `git status` (uncommitted changes?)

### Get Detailed Logs:

```bash
# Backend logs
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload --log-level debug

# Frontend logs
cd frontend
npm run dev -- --debug
```

### Share Error Details:

If still broken, share:
1. Browser console errors (screenshot)
2. Backend terminal output
3. Frontend terminal output
4. Network tab (failed requests)

---

## ✅ Success Indicators

You'll know it's working when you see:

1. **Grid Animation**: Cells changing color as disaster spreads
2. **AI Decision Cards**: Appearing with confidence scores
3. **Evacuation Paths**: Showing A* routes
4. **Resource Allocation**: CSP results with utilization
5. **Statistics Updating**: Affected cells, casualties increasing
6. **Logs Flowing**: AI messages in simulation log

**If you see all 6, the AI system is working! 🎉**
