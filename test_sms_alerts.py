#!/usr/bin/env python3
"""
Test SMS Alert System
Demonstrates personalized alerts for each person
"""

import sys
sys.path.insert(0, 'backend')

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

def main():
    print("="*70)
    print("PERSONALIZED SMS ALERT SYSTEM - DEMONSTRATION")
    print("="*70)
    
    # Initialize systems
    print("\n1. Initializing Grid Engine...")
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    print(f"   ✓ Created {len(grid_engine.grids)} grid zones")
    
    print("\n2. Initializing Pathfinder...")
    pathfinder = EvacuationPathfinder(grid_engine)
    print("   ✓ A* pathfinding ready")
    
    print("\n3. Initializing Alert Engine...")
    alert_engine = PersonalizedAlertEngine()
    print(f"   ✓ Registered {len(alert_engine.people)} people")
    
    # Show registered people
    print("\n" + "="*70)
    print("REGISTERED PEOPLE:")
    print("="*70)
    for person_id, person in alert_engine.people.items():
        grid = grid_engine.get_grid(person.current_grid)
        print(f"\n{person.name}")
        print(f"  Phone: {person.phone}")
        print(f"  Location: {person.current_grid} ({grid.name if grid else 'Unknown'})")
        print(f"  Profile: {person.age_group}, Mobility: {person.mobility}, Vehicle: {person.has_vehicle}")
        if grid:
            print(f"  Current Risk: {grid.risk_score*100:.0f}% ({grid.safety_level.value})")
    
    # Generate alerts
    print("\n" + "="*70)
    print("GENERATING PERSONALIZED ALERTS...")
    print("="*70)
    
    alerts = alert_engine.generate_all_alerts(grid_engine, {}, pathfinder)
    
    print(f"\n✓ Generated {len(alerts)} personalized alerts")
    
    # Show each alert
    for i, alert in enumerate(alerts, 1):
        print("\n" + "="*70)
        print(f"ALERT #{i}: {alert['person']} ({alert['urgency']})")
        print("="*70)
        print(f"Phone: {alert['phone']}")
        print(f"Location: {alert['grid']}")
        print("\nMESSAGE:")
        print("-"*70)
        print(alert['message'])
        print("-"*70)
    
    # Summary
    print("\n" + "="*70)
    print("ALERT SUMMARY")
    print("="*70)
    
    urgency_counts = {}
    for alert in alerts:
        urgency = alert['urgency']
        urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
    
    print(f"\nTotal Alerts: {len(alerts)}")
    for urgency, count in sorted(urgency_counts.items()):
        print(f"  {urgency}: {count}")
    
    print("\n" + "="*70)
    print("TWILIO SMS SETUP (Optional)")
    print("="*70)
    print("\nTo actually send SMS messages:")
    print("1. Sign up at https://www.twilio.com/try-twilio")
    print("2. Get Account SID, Auth Token, and Phone Number")
    print("3. Set environment variables:")
    print("   export TWILIO_ACCOUNT_SID='your_sid'")
    print("   export TWILIO_AUTH_TOKEN='your_token'")
    print("   export TWILIO_PHONE_NUMBER='+1234567890'")
    print("4. Install: pip install twilio")
    print("5. Run: python test_sms_alerts.py --send")
    
    # Check if --send flag
    if '--send' in sys.argv:
        print("\n" + "="*70)
        print("SENDING SMS MESSAGES...")
        print("="*70)
        results = alert_engine.send_all_alerts(alerts)
        print(f"\n✓ Sent: {results['sent']}")
        print(f"✗ Failed: {results['failed']}")
        print(f"\nBy Urgency:")
        for urgency, count in results['by_urgency'].items():
            print(f"  {urgency}: {count}")
    
    print("\n" + "="*70)
    print("API ENDPOINTS AVAILABLE:")
    print("="*70)
    print("\nGET  /api/alerts/people")
    print("     - List all registered people")
    print("\nPOST /api/alerts/generate")
    print("     - Generate alerts for all people")
    print("     - Body: {\"send_sms\": false, \"urgency_filter\": \"CRITICAL\"}")
    print("\nGET  /api/alerts/preview/{person_id}")
    print("     - Preview alert for specific person")
    print("     - Example: /api/alerts/preview/mayuresh")
    print("\nGET  /api/alerts/history")
    print("     - View alert history")
    print("\nGET  /api/alerts/setup-instructions")
    print("     - Get Twilio setup guide")
    
    print("\n" + "="*70)
    print("SYSTEM READY!")
    print("="*70)
    print("\nBackend running at: http://localhost:8001")
    print("API Docs: http://localhost:8001/docs")
    print("\n")

if __name__ == "__main__":
    main()
