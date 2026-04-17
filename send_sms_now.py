#!/usr/bin/env python3
"""
Send SMS Now - Loads .env file properly
"""

import os
import sys

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, using environment variables")

# Add backend to path
sys.path.insert(0, 'backend')

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

def main():
    print("="*70)
    print("🚨 SENDING SMS ALERTS")
    print("="*70)
    
    # Check API key
    api_key = os.getenv('FAST2SMS_API_KEY')
    if not api_key or not api_key.strip():
        print("\n❌ FAST2SMS_API_KEY not found!")
        print("\nTry running:")
        print('export FAST2SMS_API_KEY="NvVX6FZGDKwEPhC7lUq1I8zpuRLOJ0THbxaWrBy2oMdQAig94YaiXH7PUO3efwWnkE2b8QDz1psvAVhM"')
        print("python3 send_sms_now.py")
        return
    
    print(f"✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
    
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
        print(f"   Message: {alert['message'][:100]}...")
    
    # Confirm
    print("\n" + "="*70)
    confirm = input("\nSend SMS to all 6 people? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Cancelled")
        return
    
    # Send SMS
    print("\n" + "="*70)
    print("SENDING SMS...")
    print("="*70)
    
    results = alert_engine.send_all_alerts(alerts, method="fast2sms")
    
    print(f"\n✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print("\n⚠️  Some messages failed. Check:")
        print("1. API key is correct")
        print("2. Fast2SMS account has credits")
        print("3. Phone numbers are valid Indian numbers")
        print("4. Check Fast2SMS dashboard for error details")
    else:
        print("\n🎉 All SMS sent successfully!")
        print("Check phones in 5-30 seconds")
    
    print("\nBy Urgency:")
    for urgency, count in results['by_urgency'].items():
        print(f"  {urgency}: {count}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
