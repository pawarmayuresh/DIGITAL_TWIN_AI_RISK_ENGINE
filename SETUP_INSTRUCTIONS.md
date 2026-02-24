# 🚀 Quick Setup Instructions

## Problem: `uvicorn: command not found`

This means the Python dependencies aren't installed yet.

---

## ✅ Solution: Install Dependencies

### Option 1: Install Globally (Quick)

```bash
# Install all dependencies
pip3 install -r requirements.txt

# Verify uvicorn is installed
pip3 list | grep uvicorn

# Start the server
uvicorn backend.main:app --reload
```

---

### Option 2: Use Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn backend.main:app --reload
```

---

### Option 3: Run with Python Module (No Install Needed)

```bash
# Install dependencies first
pip3 install -r requirements.txt

# Run using python -m
python3 -m uvicorn backend.main:app --reload
```

---

### Option 4: Use Docker (Isolated)

```bash
# Build and run with docker-compose
docker-compose up

# Server will be available at http://localhost:8000
```

---

## 🧪 Verify Installation

After installing, verify everything works:

```bash
# Check uvicorn is installed
python3 -m uvicorn --version

# Or if installed globally
uvicorn --version

# Should show something like: "Running uvicorn 0.22.0"
```

---

## 🚀 Start the Server

Once dependencies are installed, start the server:

```bash
# Method 1: Direct command
uvicorn backend.main:app --reload

# Method 2: Python module
python3 -m uvicorn backend.main:app --reload

# Method 3: With virtual environment
source venv/bin/activate
uvicorn backend.main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/AI_Strategic_Risk_Engine']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🧪 Test the Server

Once running, test in another terminal:

```bash
# Test health endpoint
curl http://localhost:8000/api/health/live

# Expected: {"status":"alive"}
```

---

## ❌ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Dependencies not installed
```bash
pip3 install -r requirements.txt
```

---

### Issue: `ModuleNotFoundError: No module named 'backend'`

**Solution:** Running from wrong directory
```bash
# Make sure you're in the project root
cd AI_Strategic_Risk_Engine
python3 -m uvicorn backend.main:app --reload
```

---

### Issue: `Address already in use`

**Solution:** Port 8000 is already taken
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn backend.main:app --reload --port 8001
```

---

### Issue: Database connection errors

**Solution:** Check .env file exists
```bash
# Create .env if missing
cat > .env << EOF
DATABASE_URL=sqlite:///./dev.db
APP_ENV=development
APP_VERSION=0.1.0
EOF
```

---

## 📋 Complete Setup Checklist

- [ ] Python 3.11+ installed (you have 3.13.7 ✅)
- [ ] Navigate to project root directory
- [ ] Install dependencies: `pip3 install -r requirements.txt`
- [ ] Create .env file (if missing)
- [ ] Start server: `uvicorn backend.main:app --reload`
- [ ] Test health endpoint: `curl http://localhost:8000/api/health/live`
- [ ] Run validation: `python3 validate_batches.py`

---

## 🎯 Quick Start (Copy-Paste)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Start server
python3 -m uvicorn backend.main:app --reload

# In another terminal, test
curl http://localhost:8000/api/health/live

# Run validation
python3 validate_batches.py
```

---

## ✅ Success!

When you see this, you're ready:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Then proceed with validation and Batch 5 implementation!
