# 🧪 Batch Validation Guide

Quick guide to validate your AI Strategic Risk Engine implementation.

---

## 🚀 Quick Start

### 1. Start the Server

```bash
# Option A: Direct Python
uvicorn backend.main:app --reload

# Option B: Docker Compose
docker-compose up
```

Server should start on `http://localhost:8000`

---

### 2. Run Automated Validation

```bash
# Python validation (recommended)
python validate_batches.py

# Bash validation (alternative)
chmod +x validate_batches.sh
./validate_batches.sh
```

**Expected Output:**
```
🔥 AI Strategic Risk Engine - Batch Validation
==================================================

🟥 BATCH 1 - Foundation System Validation
========================================
  Server Running: ✓ PASS
  Health Live Endpoint: ✓ PASS
  Health Ready Endpoint: ✓ PASS
  Version Endpoint: ✓ PASS

🟧 BATCH 2 - Spatial Grid Simulation Validation
==============================================
  Module: grid_manager.py: ✓ PASS
  Module: grid_cell.py: ✓ PASS
  ...

📊 VALIDATION SUMMARY
==================================================
🟥 Batch 1 (Foundation):        4/4 (100%)
🟧 Batch 2 (Spatial Grid):      6/6 (100%)
🟨 Batch 3 (Disaster Engine):   5/5 (100%)
🟩 Batch 4 (Cascading Engine):  6/6 (100%)

OVERALL: 21/21 tests passed (100%)

✅ System is ready for Batch 5 implementation!
```

---

## 🧪 Manual Testing

### Test 1: Health Endpoints

```bash
# Test live endpoint
curl http://localhost:8000/api/health/live
# Expected: {"status":"alive"}

# Test ready endpoint
curl http://localhost:8000/api/health/ready
# Expected: {"status":"ready"}

# Test version endpoint
curl http://localhost:8000/api/health/version
# Expected: {"version":"0.1.0","env":"development"}
```

---

### Test 2: Disaster Scenarios

```bash
# Flood scenario
curl http://localhost:8000/api/demo/run/flood

# Earthquake cascade
curl http://localhost:8000/api/demo/run/earthquake-cascade

# Pandemic spread
curl http://localhost:8000/api/demo/run/pandemic

# Multi-disaster
curl http://localhost:8000/api/demo/run/multi-disaster

# Cyber attack
curl http://localhost:8000/api/demo/run/cyber-cascade

# Cascading failure
curl http://localhost:8000/api/demo/run/cascade-demo
```

**Expected Response Format:**
```json
{
  "scenario": "flood",
  "total_cells_affected": 156,
  "population_affected": 15600,
  "infrastructure_failures": 23,
  "critical_zones": 8
}
```

---

### Test 3: Demo Scripts

```bash
# Batch 2: Spatial Grid
python -m backend.core.spatial_engine.demo_batch2

# Batch 3: Disaster Engine
python -m backend.core.disaster_engine.demo_batch3

# Batch 4: Cascading Failures
python -m backend.core.cascading_engine.demo_batch4

# Batch 4: Integration
python -m backend.core.cascading_engine.demo_batch4_integration
```

---

## 📋 Validation Checklist

### Batch 1: Foundation System
- [ ] Server starts without errors
- [ ] `/api/health/live` returns 200 OK
- [ ] `/api/health/ready` returns 200 OK
- [ ] `/api/health/version` returns version info
- [ ] Database connects successfully
- [ ] Logs show no errors

### Batch 2: Spatial Grid Simulation
- [ ] Grid creates 400 cells (20x20)
- [ ] Cells have metadata (population, zone)
- [ ] Neighbor relationships work
- [ ] Diffusion spreads intensity
- [ ] Risk heatmaps generate
- [ ] Simulation loop executes

### Batch 3: Disaster Engine
- [ ] Flood scenario runs successfully
- [ ] Earthquake scenario runs successfully
- [ ] Pandemic scenario runs successfully
- [ ] Multi-disaster scenario runs successfully
- [ ] Cyber attack scenario runs successfully
- [ ] All scenarios return valid JSON

### Batch 4: Cascading Failure Engine
- [ ] Infrastructure graph builds
- [ ] Failures propagate through network
- [ ] Recovery model allocates resources
- [ ] Stability metrics calculate
- [ ] Integration with disasters works
- [ ] Cascade demo API returns results

---

## 🐛 Troubleshooting

### Server Won't Start

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version (need 3.11+)
python --version

# Try running from project root
cd AI_Strategic_Risk_Engine
uvicorn backend.main:app --reload
```

---

### Database Connection Failed

**Problem:** `Database connection failed` in logs

**Solution:**
```bash
# Check .env file exists
cat .env

# Should contain:
# DATABASE_URL=sqlite:///./dev.db

# Or for PostgreSQL:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/strategic_risk

# Start PostgreSQL if using docker-compose
docker-compose up -d db
```

---

### API Returns 500 Error

**Problem:** Scenarios return Internal Server Error

**Solution:**
```bash
# Check server logs for detailed error
# Common issues:
# 1. Missing dependencies (numpy, scipy, networkx)
pip install numpy scipy networkx

# 2. Import path issues
# Make sure you're in the project root directory

# 3. Module not found
# Check all __init__.py files exist in core directories
```

---

### Validation Script Fails

**Problem:** `python validate_batches.py` shows failures

**Solution:**
```bash
# 1. Make sure server is running first
uvicorn backend.main:app --reload

# 2. In another terminal, run validation
python validate_batches.py

# 3. Check specific failures
# - If health endpoints fail: server not running
# - If file checks fail: files missing or wrong directory
# - If API tests fail: check server logs for errors
```

---

## 📊 Understanding Results

### Pass Rate Interpretation

- **100%:** Perfect! Ready to proceed
- **80-99%:** Good, minor issues to fix
- **60-79%:** Some problems, review failures
- **<60%:** Critical issues, don't proceed

### Common Failure Patterns

1. **All Batch 1 tests fail**
   - Server not running
   - Wrong port (should be 8000)
   - Firewall blocking

2. **Batch 2 tests fail**
   - Files missing
   - Wrong directory structure
   - Import errors

3. **Batch 3/4 API tests fail**
   - Server running but errors in code
   - Check server logs
   - Missing dependencies

---

## 📝 Approval Process

### After Validation Passes:

1. **Document Results**
   - Save validation output
   - Note any warnings or issues
   - Record pass rates

2. **Review Code Quality**
   - Check for proper error handling
   - Verify type hints present
   - Ensure documentation exists

3. **Test Edge Cases**
   - Try invalid inputs
   - Test with large grids
   - Test multiple simultaneous disasters

4. **Get Sign-Off**
   - Fill out approval checklist in BATCH_STATUS_ANALYSIS.md
   - Get stakeholder approval
   - Document approval date

5. **Proceed to Next Batch**
   - Review BATCH_5_IMPLEMENTATION_GUIDE.md
   - Plan implementation
   - Start development

---

## 🎯 Success Criteria

Your system is ready for Batch 5 when:

✅ All validation tests pass (80%+ minimum)  
✅ All API endpoints return valid responses  
✅ Demo scripts execute without errors  
✅ Server logs show no critical errors  
✅ Database connects successfully  
✅ Code quality meets standards  
✅ Stakeholder approval obtained  

---

## 📚 Additional Resources

- **BATCH_STATUS_ANALYSIS.md** - Detailed batch analysis
- **BATCH_5_IMPLEMENTATION_GUIDE.md** - Next steps
- **PROJECT_STATUS_SUMMARY.md** - Overall project status
- **README.md** - Project overview

---

## 🆘 Need Help?

If validation fails or you encounter issues:

1. Check server logs for detailed errors
2. Review troubleshooting section above
3. Verify all dependencies installed
4. Ensure correct directory structure
5. Check Python version (3.11+ required)

---

**Good luck with validation! 🚀**
