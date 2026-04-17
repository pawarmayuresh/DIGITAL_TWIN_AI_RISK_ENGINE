#!/usr/bin/env python3
"""
Show All Personalized Alerts - Non-interactive
"""

import os
import sys
sys.path.insert(0, 'backend')

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

def main():
    print("="*70)
    print("🚨 PERSONALIZED SMS ALERTS - ALL MESSAGES")
    print("="*70)
    
    # Check SMS configuration
    api_key = os.getenv('FAST2SMS_API_KEY')
    if api_key and api_key.strip():
        print("✅ Fast2SMS: CONFIGURED")
    else:
        print("⚠️  Fast2SMS: NOT CONFIGURED (messages will be previewed only)")
        print("   Setup: See SMS_SETUP_GUIDE.md")
    
    print("\n" + "="*70)
    print("INITIALIZING...")
    print("="*70)
    
    # Initialize systems
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    pathfinder = EvacuationPathfinder(grid_engine)
    alert_engine = PersonalizedAlertEngine()
    
    print(f"✅ Grid: {len(grid_engine.grids)} zones")
    print(f"✅ Pathfinder: Ready")
    print(f"✅ Alert Engine: {len(alert_engine.people)} people")
    
    # Generate alerts
    print("\n" + "="*70)
    print("GENERATING ALERTS...")
    print("="*70)
    
    alerts = alert_engine.generate_all_alerts(grid_engine, {}, pathfinder)
    
    # Count by urgency
    urgency_counts = {}
    for alert in alerts:
        urgency = alert['urgency']
        urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
    
    print(f"\n📊 Generated {len(alerts)} alerts:")
    for urgency in ['CRITICAL', 'HIGH', 'MODERATE']:
        count = urgency_counts.get(urgency, 0)
        if count > 0:
            emoji = "🔴" if urgency == "CRITICAL" else "🟡" if urgency == "HIGH" else "🟢"
            print(f"   {emoji} {urgency}: {count}")
    
    # Show all alerts
    print("\n" + "="*70)
    print("ALL PERSONALIZED MESSAGES")
    print("="*70)
    
    for i, alert in enumerate(alerts, 1):
        urgency_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟡",
            "MODERATE": "🟢"
        }
        
        print(f"\n{'='*70}")
        print(f"{urgency_emoji[alert['urgency']]} ALERT #{i}: {alert['person']} ({alert['urgency']})")
        print(f"{'='*70}")
        print(f"📱 Phone: {alert['phone']}")
        print(f"📍 Location: {alert['grid']}")
        print(f"📏 Length: {len(alert['message'])} chars")
        print(f"\n{'-'*70}")
        print(alert['message'])
        print(f"{'-'*70}\n")
    
    # Summary
    print("\n" + "="*70)
    print("✅ SUMMARY")
    print("="*70)
    print(f"\nTotal Alerts: {len(alerts)}")
    print(f"People: {len(alert_engine.people)}")
    print(f"\nBy Urgency:")
    for urgency in ['CRITICAL', 'HIGH', 'MODERATE']:
        count = urgency_counts.get(urgency, 0)
        if count > 0:
            print(f"  {urgency}: {count}")
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    
    if not (api_key and api_key.strip()):
        print("\n📝 To send actual SMS:")
        print("1. Sign up: https://www.fast2sms.com/ (FREE)")
        print("2. Get API key from dashboard")
        print("3. Add to .env: FAST2SMS_API_KEY=your_key")
        print("4. Run: python show_alerts.py --send")
    else:
        print("\n✅ SMS service configured!")
        print("To send these alerts:")
        print("  python show_alerts.py --send")
        print("\nOr use API:")
        print("  POST http://localhost:8001/api/alerts/generate")
        print("  Body: {\"send_sms\": true}")
    
    # Send if requested
    if '--send' in sys.argv:
        if not (api_key and api_key.strip()):
            print("\n❌ Cannot send - API key not configured")
        else:
            print("\n" + "="*70)
            print("SENDING SMS...")
            print("="*70)
            
            results = alert_engine.send_all_alerts(alerts, method="fast2sms")
            
            print(f"\n✅ Sent: {results['sent']}")
            print(f"❌ Failed: {results['failed']}")
            print(f"\nBy Urgency:")
            for urgency, count in results['by_urgency'].items():
                print(f"  {urgency}: {count}")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
