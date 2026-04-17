#!/usr/bin/env python3
"""
Test Fast2SMS API directly to diagnose the issue
"""

import requests
import os
import json

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

api_key = os.getenv('FAST2SMS_API_KEY')

print("="*70)
print("FAST2SMS API DIAGNOSTIC TEST")
print("="*70)

if not api_key:
    print("\n❌ No API key found!")
    print("Set it with: export FAST2SMS_API_KEY='your_key'")
    exit(1)

print(f"\n✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
print(f"   Length: {len(api_key)} characters")

# Test phone number (Mayuresh)
test_phone = "8306579141"
test_message = "Test from Mumbai Alert System"

print(f"\n📱 Test Phone: +91 {test_phone}")
print(f"📝 Test Message: {test_message}")

# Try different API endpoints and methods
print("\n" + "="*70)
print("TESTING DIFFERENT API CONFIGURATIONS...")
print("="*70)

# Test 1: Original bulkV2 endpoint with route 'q'
print("\n1️⃣  Testing: bulkV2 endpoint with route 'q'")
url1 = "https://www.fast2sms.com/dev/bulkV2"
payload1 = {
    "authorization": api_key,
    "route": "q",
    "message": test_message,
    "language": "english",
    "flash": 0,
    "numbers": test_phone
}
headers1 = {"cache-control": "no-cache"}

try:
    response1 = requests.post(url1, data=payload1, headers=headers1, timeout=10)
    print(f"   Status: {response1.status_code}")
    print(f"   Response: {response1.text}")
    result1 = response1.json()
    if result1.get("return"):
        print("   ✅ SUCCESS!")
    else:
        print(f"   ❌ FAILED: {result1.get('message')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Try with route 'dlt'
print("\n2️⃣  Testing: bulkV2 endpoint with route 'dlt'")
payload2 = {
    "authorization": api_key,
    "route": "dlt",
    "message": test_message,
    "language": "english",
    "flash": 0,
    "numbers": test_phone
}

try:
    response2 = requests.post(url1, data=payload2, headers=headers1, timeout=10)
    print(f"   Status: {response2.status_code}")
    print(f"   Response: {response2.text}")
    result2 = response2.json()
    if result2.get("return"):
        print("   ✅ SUCCESS!")
    else:
        print(f"   ❌ FAILED: {result2.get('message')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Try with sender_id
print("\n3️⃣  Testing: With sender_id parameter")
payload3 = {
    "authorization": api_key,
    "sender_id": "FSTSMS",
    "message": test_message,
    "language": "english",
    "route": "p",
    "numbers": test_phone
}

try:
    response3 = requests.post(url1, data=payload3, headers=headers1, timeout=10)
    print(f"   Status: {response3.status_code}")
    print(f"   Response: {response3.text}")
    result3 = response3.json()
    if result3.get("return"):
        print("   ✅ SUCCESS!")
    else:
        print(f"   ❌ FAILED: {result3.get('message')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 4: Try bulk endpoint
print("\n4️⃣  Testing: /dev/bulk endpoint")
url4 = "https://www.fast2sms.com/dev/bulk"
payload4 = {
    "authorization": api_key,
    "sender_id": "FSTSMS",
    "message": test_message,
    "route": "v3",
    "numbers": test_phone
}

try:
    response4 = requests.post(url4, data=payload4, headers=headers1, timeout=10)
    print(f"   Status: {response4.status_code}")
    print(f"   Response: {response4.text}")
    result4 = response4.json()
    if result4.get("return"):
        print("   ✅ SUCCESS!")
    else:
        print(f"   ❌ FAILED: {result4.get('message')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 5: Check if it's an API v2 key
print("\n5️⃣  Testing: With Authorization header instead of payload")
headers5 = {
    "authorization": api_key,
    "Content-Type": "application/json"
}
payload5 = {
    "route": "q",
    "message": test_message,
    "language": "english",
    "flash": 0,
    "numbers": test_phone
}

try:
    response5 = requests.post(url1, json=payload5, headers=headers5, timeout=10)
    print(f"   Status: {response5.status_code}")
    print(f"   Response: {response5.text}")
    result5 = response5.json()
    if result5.get("return"):
        print("   ✅ SUCCESS!")
    else:
        print(f"   ❌ FAILED: {result5.get('message')}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("="*70)

print("\n📋 NEXT STEPS:")
print("\n1. Check Fast2SMS Dashboard:")
print("   - Go to: https://www.fast2sms.com/dashboard")
print("   - Check 'API Keys' section")
print("   - Make sure you're using the correct API key type")
print("   - Check if account is verified")
print("   - Check SMS credits balance")

print("\n2. Verify API Key Type:")
print("   - Fast2SMS has different key types (Dev API, Production API)")
print("   - Make sure you're using 'Dev API' key for testing")

print("\n3. Check Account Status:")
print("   - Some accounts need phone/email verification")
print("   - Free accounts may have restrictions")

print("\n4. Alternative: Use Twilio")
print("   - More reliable for production")
print("   - Sign up: https://www.twilio.com/try-twilio")
print("   - Get $15 free credits")

print()
