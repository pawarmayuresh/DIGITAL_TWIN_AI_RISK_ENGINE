# SMS Alert System Setup Guide

## 🚨 Current Status
Your SMS alert system is ready but needs SMS service configuration to send actual messages.

## 📱 Registered People
1. **Shambhavi** - +91 88483 99722 (Student, Bandra C5)
2. **Jashwanth Ram** - +91 63024 82236 (Student, Dadar D3)
3. **Shiva** - +91 93475 51809 (Student, Fort B2)
4. **Vaibhavi** - +91 83094 56402 (Student, Kurla E4)
5. **Mayuresh** - +91 83065 79141 (Adult, Colaba A1)
6. **Prof. Hemlatha** - +91 99942 68023 (Professor, Andheri F6)

Each person receives **personalized messages** based on:
- Their current grid location
- Grid risk level (from simulation)
- Their profile (age, mobility, vehicle)
- Best evacuation routes
- Urgency level

---

## ⚡ Quick Setup (Fast2SMS - FREE for India)

### Step 1: Sign Up (2 minutes)
1. Go to: https://www.fast2sms.com/
2. Click "Sign Up" (top right)
3. Enter your details and verify phone/email
4. **Free tier**: 50 SMS/day (perfect for testing!)

### Step 2: Get API Key (1 minute)
1. Login to Fast2SMS dashboard
2. Go to **"Dev API"** section (left menu)
3. Copy your **API Key** (looks like: `xYz123AbC456...`)

### Step 3: Configure System (30 seconds)
1. Open `.env` file in your project root
2. Add your API key:
```bash
FAST2SMS_API_KEY=your_api_key_here
```

### Step 4: Install Dependencies (30 seconds)
```bash
pip install requests
```

### Step 5: Test It! (1 minute)
```bash
# Test without sending (preview messages)
python test_sms_alerts.py

# Actually send SMS
python test_sms_alerts.py --send
```

---

## 🌐 Alternative: Twilio (International, Paid)

If you need international SMS or WhatsApp:

### Setup Twilio
1. Sign up: https://www.twilio.com/try-twilio
2. Get free trial credits ($15)
3. Get Account SID, Auth Token, Phone Number
4. Configure in `.env`:
```bash
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```
5. Install: `pip install twilio`

---

## 🔧 Using the API

### 1. List Registered People
```bash
curl http://localhost:8001/api/alerts/people
```

### 2. Generate Alerts (Preview Only)
```bash
curl -X POST http://localhost:8001/api/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{"send_sms": false}'
```

### 3. Generate & Send SMS
```bash
curl -X POST http://localhost:8001/api/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{"send_sms": true}'
```

### 4. Preview Alert for One Person
```bash
curl http://localhost:8001/api/alerts/preview/mayuresh
```

### 5. Send Only Critical Alerts
```bash
curl -X POST http://localhost:8001/api/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{"send_sms": true, "urgency_filter": "CRITICAL"}'
```

---

## 📊 How It Works

### 1. Grid Simulation Runs
- Your Mumbai grid simulates flood conditions
- Each grid zone gets risk score (0-100%)
- Safety levels: SAFE, MEDIUM_RISK, DANGEROUS

### 2. Alert Engine Analyzes
For each person:
- Checks their current grid location
- Gets grid risk score and water level
- Finds best evacuation route (A* algorithm)
- Considers person's profile (age, mobility, vehicle)

### 3. Personalized Messages Generated
Different messages for different situations:

**Example: Mayuresh (Coastal Area, High Risk)**
```
🚨 ALERT: Mayuresh
⚠️ IMMEDIATE DANGER in Colaba
Risk: 85% | Water: 2.1m

📋 YOUR ACTION PLAN:
1. EVACUATE NOW by car
2. Avoid flooded roads
3. Help elderly neighbors if safe

🗺️ ROUTE: A1 → B1 → B2 → C2
Distance: 4 zones

📞 EMERGENCY:
Police: 100 | Fire: 101
Ambulance: 102 | Disaster: 108

⏱️ 02:30 PM
Stay safe! Updates every 15 min
```

**Example: Prof. Hemlatha (Safe Area, Low Risk)**
```
🚨 ALERT: Prof. Hemlatha
⚠️ ALERT for Andheri
Risk: 25%

📋 YOUR ACTION PLAN:
1. Stay indoors if safe
2. Monitor updates
3. Keep emergency kit ready
4. Avoid unnecessary travel

👨‍🏫 FACULTY RESPONSIBILITY:
- Account for all students
- Coordinate with admin
- Lead evacuation if needed

⏱️ 02:30 PM
Stay safe! Updates every 15 min
```

### 4. SMS Sent
- Messages sent via Fast2SMS or Twilio
- Each person gets their unique message
- System tracks delivery status

---

## 🧪 Testing Without SMS Service

You can test the system without configuring SMS:

```bash
# Preview all messages
python test_sms_alerts.py

# Use API to preview
curl http://localhost:8001/api/alerts/generate
```

The system will:
- ✅ Generate personalized messages
- ✅ Show what would be sent
- ✅ Calculate urgency levels
- ❌ Not actually send SMS (needs API key)

---

## 🎯 Integration with Your System

The alert system is already integrated with:

1. **Grid Engine** - Gets real-time risk scores
2. **A* Pathfinder** - Finds evacuation routes
3. **Bayesian Network** - Risk assessment
4. **Policy Engine** - Evacuation strategies

When you run grid simulation:
1. Grid conditions update
2. Risk scores recalculated
3. Alert engine generates new messages
4. SMS sent automatically (if configured)

---

## 🔍 Troubleshooting

### "SMS not received"
- ✅ Check API key is correct in `.env`
- ✅ Verify phone number format (+91...)
- ✅ Check Fast2SMS dashboard for delivery status
- ✅ Free tier: 50 SMS/day limit
- ✅ Some numbers may be DND (Do Not Disturb)

### "API key not configured"
```bash
# Check .env file
cat .env | grep FAST2SMS

# Set it if missing
echo "FAST2SMS_API_KEY=your_key_here" >> .env

# Restart backend
# Backend will reload .env automatically
```

### "Import error"
```bash
# Install dependencies
pip install requests
pip install twilio  # Only if using Twilio
```

---

## 📈 Next Steps

1. **Configure Fast2SMS** (5 minutes)
   - Sign up, get API key, add to `.env`

2. **Test with One Person**
   ```bash
   curl -X POST http://localhost:8001/api/alerts/test/send-one?person_id=mayuresh
   ```

3. **Run Full Simulation**
   - Start backend: `uvicorn backend.main:app --reload --port 8001`
   - Trigger grid simulation
   - Generate alerts: `POST /api/alerts/generate` with `{"send_sms": true}`

4. **Monitor Results**
   - Check Fast2SMS dashboard for delivery
   - View history: `GET /api/alerts/history`

---

## 💡 Tips

- **Test Mode**: Use `send_sms: false` to preview messages
- **Urgency Filter**: Send only critical alerts during testing
- **Rate Limits**: Free tier = 50 SMS/day
- **Message Length**: Fast2SMS free tier = 500 chars max
- **DND Numbers**: Some Indian numbers block promotional SMS
- **Best Time**: Send between 9 AM - 9 PM for better delivery

---

## 🎓 For Faculty Demo

Show this flow:
1. "Here are 6 people registered in different Mumbai locations"
2. "Grid simulation shows Colaba (coastal) has 85% risk"
3. "System generates personalized alerts for each person"
4. "Mayuresh in Colaba gets CRITICAL alert with evacuation route"
5. "Prof. Hemlatha in Andheri gets MODERATE alert to stay prepared"
6. "Each message is unique based on their profile and location"
7. "SMS sent automatically via Fast2SMS API"

---

## 📞 Support

- Fast2SMS Support: https://www.fast2sms.com/support
- Twilio Support: https://www.twilio.com/help
- API Docs: http://localhost:8001/docs (when backend running)
