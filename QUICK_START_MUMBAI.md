# 🚀 Quick Start - Mumbai System

## ⚡ 3-Step Setup

### Step 1: Start Backend (Terminal 1)
```bash
uvicorn backend.main:app --reload
```

**Wait for:**
```
✅ All Mumbai data loaded successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

**Wait for:**
```
➜  Local:   http://localhost:8081/
```

### Step 3: Open Browser
Navigate to: **http://localhost:8081**

You should see the **Mumbai Real-Time Map**!

---

## ✅ What You Should See

1. **Mumbai Map** with actual geography
2. **10 Wards** (Colaba, Bandra, Andheri, Kurla, etc.)
3. **Arabian Sea** on the left
4. **Mithi River** flowing through the city
5. **Landmarks**: CST, Airport, JJ Hospital
6. **Color-coded risk levels**
7. **Alert panel** on the right
8. **Sensor dashboard** at the bottom

---

## 🎯 Quick Demo Actions

1. **Click on Ward E (Byculla)** - See high risk details
2. **Enable Audio Alerts** - Toggle button at top
3. **Hover over wards** - See pulsing animation for high risk
4. **Check sensor dashboard** - See 7 active sensors
5. **View alerts** - See recommendations panel

---

## 📊 API Test

Open: **http://localhost:8000/docs**

Try these endpoints:
- `GET /api/mumbai/wards` - Get all wards
- `GET /api/mumbai/risk-scores` - Get risk scores
- `GET /api/mumbai/sensors/rain` - Get rain data
- `GET /api/mumbai/mithi-river/status` - Get river status

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
lsof -ti:8000
# Kill the process
kill -9 <PID>
```

### Frontend won't start?
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Data not loading?
Check that all CSV files exist in `data/mumbai/`

---

## 🎓 For Faculty Demo

**Say this:**
> "This is a Real-Time Disaster Monitoring System for Mumbai. It monitors 10 wards from Colaba to Borivali, tracks the Mithi River, and provides audio alerts with specific recommendations. The system learned from the 2005 Mumbai floods where 944mm of rain fell in 24 hours, causing 1000 casualties."

**Then:**
1. Click on Ward E (Byculla)
2. Show risk score and recommendations
3. Enable audio alerts
4. Explain the 5 data sources (rain, water, traffic, power, panic)

---

**That's it! Your system is ready! 🎉**
