# 📱 How to Send SMS - Simple 3-Step Guide

## Current Status
✅ Your system generates personalized alerts for 6 people
❌ SMS not being sent because API key is missing

## Why You're Not Getting SMS
The system needs an SMS service (like Fast2SMS) to actually send messages. Right now it's like having a letter written but no post office to deliver it.

---

## 🚀 3-Step Fix (5 minutes)

### Step 1: Sign Up for Fast2SMS (2 minutes)
1. Open browser: https://www.fast2sms.com/
2. Click "Sign Up" (top right)
3. Enter:
   - Your name
   - Email
   - Phone number (will receive OTP)
   - Password
4. Verify OTP
5. Done! You get 50 FREE SMS per day

### Step 2: Get Your API Key (1 minute)
1. Login to Fast2SMS
2. Click "Dev API" in left menu
3. You'll see your API key (long string like: `xYz123AbC456...`)
4. Click "Copy" button

### Step 3: Add to Your System (30 seconds)
1. Open `.env` file in your project folder
2. Find the line: `FAST2SMS_API_KEY=`
3. Paste your key after the `=`
4. Save file

Example:
```
FAST2SMS_API_KEY=xYz123AbC456DeF789GhI012JkL345MnO678PqR901StU234VwX567YzA890BcD123
```

---

## ✅ Test It!

### Option 1: Quick Test Script
```bash
python3 show_alerts.py --send
```

This will:
- Generate personalized alerts for all 6 people
- Send SMS to all phone numbers
- Show delivery status

### Option 2: Via API
```bash
# Start backend
uvicorn backend.main:app --reload --port 8001

# In another terminal, send alerts
curl -X POST http://localhost:8001/api/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{"send_sms": true}'
```

---

## 📱 What Will Happen

Once configured, when you run the system:

1. **Grid simulation runs** → Calculates risk for each zone
2. **Alert engine analyzes** → Checks each person's location
3. **Messages generated** → Personalized for each person
4. **SMS sent** → Via Fast2SMS API
5. **Phones receive** → Within 5-30 seconds

### Example Flow:
```
Mayuresh in Colaba (A1) → High risk detected (85%)
    ↓
System generates CRITICAL alert with evacuation route
    ↓
Fast2SMS sends SMS to +91 83065 79141
    ↓
Mayuresh receives message on phone
```

---

## 🎯 Who Gets What

Each person gets a DIFFERENT message based on their situation:

| Person | Location | Risk | Message Type |
|--------|----------|------|--------------|
| Shambhavi | Bandra C5 | 71% | CRITICAL - Evacuate now |
| Jashwanth | Dadar D3 | 52% | HIGH - Prepare to evacuate |
| Shiva | Fort B2 | 69% | CRITICAL - Evacuate now |
| Vaibhavi | Kurla E4 | 17% | MODERATE - Stay alert |
| Mayuresh | Colaba A1 | 32% | HIGH - Prepare (has car) |
| Prof. Hemlatha | Andheri F6 | 30% | HIGH - Coordinate students |

---

## 🔍 Verify It's Working

### Check 1: Preview Messages (No SMS)
```bash
python3 show_alerts.py
```
You should see 6 personalized messages

### Check 2: Check Configuration
```bash
cat .env | grep FAST2SMS
```
Should show: `FAST2SMS_API_KEY=your_key_here`

### Check 3: Send Test SMS
```bash
python3 show_alerts.py --send
```
Should show: `✅ Sent: 6`

### Check 4: Check Your Phone
- Wait 5-30 seconds
- Check SMS inbox
- You should receive the personalized message

---

## 🐛 Troubleshooting

### "No SMS received"
**Possible reasons:**
1. API key not added to `.env` correctly
2. Phone number has DND (Do Not Disturb) enabled
3. Network delay (wait 1-2 minutes)
4. Daily limit reached (50 SMS/day on free tier)

**Solutions:**
1. Check `.env` file has correct API key
2. Check Fast2SMS dashboard for delivery status
3. Try sending to different number
4. Check Fast2SMS account balance

### "API key not configured"
```bash
# Check if .env has the key
cat .env | grep FAST2SMS

# If empty, add it:
echo "FAST2SMS_API_KEY=your_key_here" >> .env
```

### "Import error"
```bash
pip install requests
```

### "Failed to send"
- Check internet connection
- Verify API key is correct (copy-paste from Fast2SMS)
- Check Fast2SMS dashboard for error messages
- Try regenerating API key on Fast2SMS

---

## 💰 Cost

**Fast2SMS Free Tier:**
- 50 SMS per day: FREE
- Perfect for testing and demos
- No credit card required

**If you need more:**
- 1000 SMS: ₹200 (~$2.50)
- 5000 SMS: ₹800 (~$10)
- 10000 SMS: ₹1400 (~$17)

---

## 🎓 For Faculty Demo

### Without SMS (Preview Mode)
```bash
python3 show_alerts.py
```
Show the personalized messages on screen

### With SMS (Live Demo)
1. Configure Fast2SMS (5 min before demo)
2. Start backend
3. Run grid simulation
4. Generate alerts: `POST /api/alerts/generate` with `send_sms: true`
5. Show SMS received on actual phones
6. Explain how each message is personalized

---

## 📞 Quick Reference

### Preview Messages
```bash
python3 show_alerts.py
```

### Send SMS
```bash
python3 show_alerts.py --send
```

### API Endpoint
```bash
POST http://localhost:8001/api/alerts/generate
Body: {"send_sms": true}
```

### Check Status
```bash
GET http://localhost:8001/api/alerts/history
```

---

## ✅ Checklist

Before demo:
- [ ] Fast2SMS account created
- [ ] API key copied
- [ ] API key added to `.env` file
- [ ] Tested with `python3 show_alerts.py --send`
- [ ] Verified SMS received on at least one phone
- [ ] Backend running: `uvicorn backend.main:app --reload --port 8001`

---

## 🆘 Still Not Working?

1. **Check .env file**
   ```bash
   cat .env
   ```
   Should show: `FAST2SMS_API_KEY=your_actual_key`

2. **Test API key directly**
   ```bash
   python3 -c "import os; print(os.getenv('FAST2SMS_API_KEY'))"
   ```
   Should print your API key

3. **Check Fast2SMS dashboard**
   - Login to Fast2SMS
   - Check "SMS History" for delivery status
   - Check "Account Balance" for remaining SMS

4. **Try manual test**
   ```python
   import requests
   import os
   
   api_key = os.getenv('FAST2SMS_API_KEY')
   url = "https://www.fast2sms.com/dev/bulkV2"
   
   payload = {
       "authorization": api_key,
       "route": "q",
       "message": "Test from Mumbai Alert System",
       "language": "english",
       "flash": 0,
       "numbers": "8306579141"  # Your number
   }
   
   response = requests.post(url, data=payload)
   print(response.json())
   ```

---

## 📚 More Help

- **Setup Guide**: `SMS_SETUP_GUIDE.md` (detailed)
- **Status**: `SMS_STATUS.md` (what's working)
- **Fast2SMS Docs**: https://docs.fast2sms.com/
- **API Docs**: http://localhost:8001/docs

---

**Bottom Line**: Add your Fast2SMS API key to `.env` file and run `python3 show_alerts.py --send`. That's it!
