#!/usr/bin/env python3
"""
Test Twilio SMS - Send to one number first
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def test_twilio():
    print("="*70)
    print("TWILIO SMS TEST")
    print("="*70)
    
    # Check configuration
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_phone = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_phone]):
        print("\n❌ Twilio not configured in .env file!")
        print("\nAdd these lines to .env:")
        print("TWILIO_ACCOUNT_SID=your_sid")
        print("TWILIO_AUTH_TOKEN=your_token")
        print("TWILIO_PHONE_NUMBER=+1234567890")
        return
    
    print(f"\n✅ Configuration found:")
    print(f"   Account SID: {account_sid[:10]}...{account_sid[-5:]}")
    print(f"   From Number: {from_phone}")
    
    # Check if twilio is installed
    try:
        from twilio.rest import Client
        print("✅ Twilio library installed")
    except ImportError:
        print("\n❌ Twilio not installed!")
        print("Run: pip install twilio")
        return
    
    # Get test phone number
    print("\n" + "="*70)
    test_phone = input("Enter YOUR phone number to test (with country code, e.g., +918306579141): ").strip()
    
    if not test_phone:
        print("Cancelled")
        return
    
    # Send test SMS
    print(f"\n📤 Sending test SMS to {test_phone}...")
    
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body="🚨 TEST: Mumbai Disaster Alert System is working! This is a test message.",
            from_=from_phone,
            to=test_phone
        )
        
        print(f"\n✅ SUCCESS!")
        print(f"   Message SID: {message.sid}")
        print(f"   Status: {message.status}")
        print(f"   To: {message.to}")
        print(f"   From: {message.from_}")
        print(f"\n📱 Check your phone in 5-30 seconds!")
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ FAILED: {error_msg}")
        
        if "not a valid phone number" in error_msg.lower():
            print("\n💡 Fix: Check phone number format")
            print("   Should be: +918306579141 (with + and country code)")
        
        elif "not verified" in error_msg.lower() or "trial" in error_msg.lower():
            print("\n💡 Fix: Verify this number in Twilio console")
            print("   1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
            print("   2. Click 'Add a new number'")
            print(f"   3. Enter: {test_phone}")
            print("   4. Verify with code sent to your phone")
            print("\n   OR upgrade to paid account (no verification needed)")
        
        elif "insufficient" in error_msg.lower():
            print("\n💡 Fix: Add credits to your account")
            print("   Go to: https://console.twilio.com/")
        
        else:
            print("\n💡 Check Twilio console for details:")
            print("   https://console.twilio.com/us1/monitor/logs/sms")

if __name__ == "__main__":
    test_twilio()
