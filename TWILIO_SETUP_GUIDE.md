# 📱 Twilio SMS Setup - Complete Guide

## Why Twilio?
- ✅ More reliable than Fast2SMS
- ✅ $15 free trial credits (enough for ~2000 SMS)
- ✅ Works internationally
- ✅ Better delivery rates
- ✅ Professional service

---

## 🚀 Step-by-Step Setup (5 minutes)

### Step 1: Sign Up (2 minutes)

1. **Go to Twilio:**
   - Open: https://www.twilio.com/try-twilio
   - Click "Sign up and start building"

2. **Fill in details:**
   - Email address
   - Password
   - First name
   - Last name

3. **Verify email:**
   - Check your email
   - Click verification link

4. **Verify phone:**
   - Enter your phone number
   - Enter the code they send you

5. **Answer questions:**
   - "Which Twilio product?" → Select "SMS"
   - "What do you plan to build?" → Select "Alerts & Notifications"
   - "How do you want to build?" → Select "With code"
   - "What's your preferred language?" → Select "Python"

---

### Step 2: Get Credentials (2 minutes)

After signup, you'll see the Twilio Console:

1. **Account SID:**
   - You'll see it on the dashboard
   - Looks like: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Click the copy icon

2. **Auth Token:**
   - Click "Show" next to Auth Token
   - Copy the token
   - Looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Get Phone Number:**
   - Click "Get a Trial Number" button
   - Twilio will assign you a number
   - Click "Choose this Number"
   - Your number looks like: `+1 234 567 8900`

---

### Step 3: Add to `.env` File (30 seconds)

Open your `.env` file and add these lines:

```bash
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+12345678900
```

**Example with real values:**
```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcd
TWILIO_AUTH_TOKEN=abcdef1234567890abcdef1234567890
TWILIO_PHONE_NUMBER=+15551234567
```

**Important:**
- No spaces around the `=`
- No quotes around the values
- Phone number includes `+` and country code

---

### Step 4: Install Twilio Library (30 seconds)

```bash
pip install twilio
```

---

### Step 5: Test It! (1 minute)

**Test with one number first:**

```bash
python3 test_twilio.py
```

This will:
1. Check your configuration
2. Ask for your phone number
3. Send a test SMS
4. Show you if it worked

---

## ⚠️ IMPORTANT: Trial Account Limitations

### Trial accounts can ONLY send to VERIFIED phone numbers!

You need to verify each of the 6 phone numbers before sending:

1. **Go to Verified Numbers:**
   - https://console.twilio.com/us1/develop/phone-numbers/manage/verified

2. **Add each number:**
   - Click "Add a new number"
   - Enter: `+918848399722` (Shambhavi)
   - Twilio sends verification code
   - Enter the code
   - Repeat for all 6 numbers

3. **Numbers to verify:**
   - +918848399722 (Shambhavi)
   - +916302482236 (Jashwanth)
   - +919347551809 (Shiva)
   - +918309456402 (Vaibhavi)
   - +918306579141 (Mayuresh)
   - +919994268023 (Prof. Hemlatha)

### Alternative: Upgrade Account

- Upgrade to paid account (no verification needed)
- Add $20 credit
- Can send to any number
- Cost: ~$0.0075 per SMS

---

## 🧪 Testing Steps

### Test 1: Check Configuration

```bash
cat .env | grep TWILIO
```

Should show your credentials.

### Test 2: Test Twilio Connection

```bash
python3 test_twilio.py
```

Enter YOUR phone number to test.

### Test 3: Send to All 6 People

```bash
python3 send_sms_twilio.py
```

This will send personalized alerts to all 6 numbers.

---

## 📊 What Happens When You Send

1. **Script generates alerts:**
   - Analyzes grid conditions
   - Creates personalized messages
   - Calculates urgency levels

2. **Twilio sends SMS:**
   - Each message sent via Twilio API
   - Delivery within 5-30 seconds
   - Status tracked in Twilio console

3. **People receive SMS:**
   - Each person gets their unique message
   - Different based on location and profile
   - Includes evacuation routes and advice

---

## 💰 Cost

### Trial Account:
- $15 free credits
- ~2000 SMS included
- Perfect for testing and demos

### Paid Account:
- ~$0.0075 per SMS (India)
- ~$0.01 per SMS (US)
- Pay as you go

### For 6 people:
- 1 alert = 6 SMS = ~$0.045
- 100 alerts = $4.50
- Very affordable!

---

## 🔍 Troubleshooting

### "The number is unverified"

**Problem:** Trial account can only send to verified numbers

**Solution:**
1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Add and verify each phone number
3. OR upgrade to paid account

---

### "Invalid phone number"

**Problem:** Wrong phone number format

**Solution:**
- Must include `+` and country code
- India: `+918306579141`
- US: `+15551234567`
- No spaces or dashes

---

### "Insufficient credits"

**Problem:** Trial credits used up

**Solution:**
1. Go to: https://console.twilio.com/
2. Add credits to account
3. Or wait for trial to reset

---

### "Authentication failed"

**Problem:** Wrong Account SID or Auth Token

**Solution:**
1. Check Twilio console for correct values
2. Make sure no extra spaces in `.env`
3. Restart terminal after updating `.env`

---

## 📱 Check Delivery Status

1. **Twilio Console:**
   - Go to: https://console.twilio.com/us1/monitor/logs/sms
   - See all sent messages
   - Check delivery status
   - View error messages

2. **In Script:**
   - Script shows success/failure for each SMS
   - Displays message SID
   - Shows helpful error messages

---

## 🎯 Quick Commands

### Test configuration:
```bash
python3 test_twilio.py
```

### Send to all 6 people:
```bash
python3 send_sms_twilio.py
```

### Demo without sending:
```bash
python3 demo_alerts.py
```

### Check .env file:
```bash
cat .env | grep TWILIO
```

---

## ✅ Checklist

Before sending SMS:

- [ ] Signed up for Twilio
- [ ] Got Account SID
- [ ] Got Auth Token
- [ ] Got Twilio phone number
- [ ] Added all 3 to `.env` file
- [ ] Installed twilio: `pip install twilio`
- [ ] Tested with `python3 test_twilio.py`
- [ ] Verified all 6 phone numbers (trial account)
- [ ] Ready to send!

---

## 🆘 Still Having Issues?

1. **Check Twilio Console:**
   - https://console.twilio.com/
   - Look for error messages
   - Check SMS logs

2. **Verify Configuration:**
   ```bash
   python3 test_twilio.py
   ```

3. **Use Demo Mode:**
   ```bash
   python3 demo_alerts.py
   ```
   Shows alerts without sending

4. **Try Email Instead:**
   ```bash
   python3 send_email_alerts.py
   ```
   More reliable alternative

---

## 📚 Resources

- **Twilio Console:** https://console.twilio.com/
- **Verify Numbers:** https://console.twilio.com/us1/develop/phone-numbers/manage/verified
- **SMS Logs:** https://console.twilio.com/us1/monitor/logs/sms
- **Twilio Docs:** https://www.twilio.com/docs/sms
- **Pricing:** https://www.twilio.com/sms/pricing

---

**Bottom Line:** Twilio is more reliable than Fast2SMS. Takes 5 minutes to setup, $15 free credits, works great!
