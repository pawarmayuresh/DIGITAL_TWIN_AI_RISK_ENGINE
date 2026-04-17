#!/usr/bin/env python3
"""
Send SMS via Twilio - More Reliable than Fast2SMS
"""

import os
import sys
sys.path.insert(0, 'backend')

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

def main():
    print("="*70)
    print("📱 TWILIO SMS ALERT SYSTEM")
    print("="*70)
    
    # Check Twilio configuration
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_phone = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, from_phone]):
        print("\n❌ Twilio not configured!")
        print("\n📝 Setup Instructions:")
        print("1. Sign up: https://www.twilio.com/try-twilio")
        print("2. Get Account SID, Auth Token, Phone Number")
        print("3. Add to .env file:")
        print("   TWILIO_ACCOUNT_SID=ACxxxxx...")
        print("   TWILIO_AUTH_TOKEN=your_token")
        print("   TWILIO_PHONE_NUMBER=+1234567890")
        print("4. Install: pip install twilio")
        print("5. Run this script again")
        print("\n💡 Or demo without sending:")
        print("   python3 demo_alerts.py")
        return
    
    print(f"\n✅ Twilio configured")
    print(f"   Account SID: {account_sid[:10]}...{account_sid[-5:]}")
    print(f"   From Number: {from_phone}")
    
    # Check if twilio is installed
    try:
        from twilio.rest import Client
        print("✅ Twilio library installed")
    except ImportError:
        print("\n❌ Twilio library not installed!")
        print("Run: pip install twilio")
        return
    
    # Initialize systems
    print("\n" + "="*70)
    print("INITIALIZING...")
    print("="*70)
    
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    pathfinder = EvacuationPathfinder(grid_engine)
    alert_engine = PersonalizedAlertEngine()
    
    print(f"✅ Grid: {len(grid_engine.grids)} zones")
    print(f"✅ Alert Engine: {len(alert_engine.people)} people")
    
    # Generate alerts
    print("\n" + "="*70)
    print("GENERATING ALERTS...")
    print("="*70)
    
    alerts = alert_engine.generate_all_alerts(grid_engine, {}, pathfinder)
    
    print(f"✅ Generated {len(alerts)} alerts")
    
    # Show what will be sent
    print("\n" + "="*70)
    print("ALERTS TO BE SENT:")
    print("="*70)
    
    for i, alert in enumerate(alerts, 1):
        print(f"\n{i}. {alert['person']} ({alert['urgency']})")
        print(f"   Phone: {alert['phone']}")
        print(f"   Grid: {alert['grid']}")
        print(f"   Message: {alert['message'][:80]}...")
    
    # Important note about trial account
    print("\n" + "="*70)
    print("⚠️  IMPORTANT: TWILIO TRIAL ACCOUNT LIMITATIONS")
    print("="*70)
    print("\nTrial accounts can only send to VERIFIED phone numbers.")
    print("\nTo verify a number:")
    print("1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("2. Click 'Add a new number'")
    print("3. Enter phone number and verify with code")
    print("\nYou need to verify all 6 phone numbers before sending!")
    print("\nAlternatively, upgrade to paid account (no verification needed)")
    
    # Confirm
    print("\n" + "="*70)
    confirm = input("\nHave you verified all phone numbers? Send SMS? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("\nCancelled. Verify phone numbers first!")
        print("\nOr use demo mode: python3 demo_alerts.py")
        return
    
    # Send SMS
    print("\n" + "="*70)
    print("SENDING SMS VIA TWILIO...")
    print("="*70)
    
    results = alert_engine.send_all_alerts(alerts, method="twilio")
    
    print(f"\n✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print("\n⚠️  Some messages failed. Common reasons:")
        print("1. Phone numbers not verified (trial account)")
        print("2. Invalid phone number format")
        print("3. Insufficient credits")
        print("4. Check Twilio console for details:")
        print("   https://console.twilio.com/us1/monitor/logs/sms")
    else:
        print("\n🎉 All SMS sent successfully!")
        print("Check phones in 5-30 seconds")
    
    print("\nBy Urgency:")
    for urgency, count in results['by_urgency'].items():
        print(f"  {urgency}: {count}")
    
    print("\n💰 Cost: ~$0.0075 per SMS (trial credits used)")
    print("Trial balance: Check at https://console.twilio.com/")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
