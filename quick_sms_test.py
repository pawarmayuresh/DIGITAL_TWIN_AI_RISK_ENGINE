#!/usr/bin/env python3
"""
Quick SMS Test - See what messages will be sent
Run this to preview personalized alerts without sending SMS
"""

import os
import sys

# Add backend to path
sys.path.insert(0, 'backend')

def test_fast2sms_config():
    """Check if Fast2SMS is configured"""
    api_key = os.getenv('FAST2SMS_API_KEY')
    
    print("="*70)
    print("SMS SERVICE CONFIGURATION CHECK")
    print("="*70)
    
    if api_key and api_key.strip():
        print("✅ Fast2SMS API Key: Configured")
        print(f"   Key: {api_key[:10]}...{api_key[-5:]}")
        return True
    else:
        print("❌ Fast2SMS API Key: NOT CONFIGURED")
        print("\n📝 Quick Setup:")
        print("1. Go to: https://www.fast2sms.com/")
        print("2. Sign up (FREE - 50 SMS/day)")
        print("3. Get API key from dashboard")
        print("4. Add to .env file:")
        print("   FAST2SMS_API_KEY=your_api_key_here")
        print("\n💡 You can still preview messages without API key!")
        return False

def preview_alerts():
    """Preview all personalized alerts"""
    
    from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
    from backend.evacuation_system.grid_engine import MumbaiGridEngine
    from backend.evacuation_system.pathfinder import EvacuationPathfinder
    
    print("\n" + "="*70)
    print("INITIALIZING SYSTEMS...")
    print("="*70)
    
    # Initialize
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    pathfinder = EvacuationPathfinder(grid_engine)
    alert_engine = PersonalizedAlertEngine()
    
    print(f"✅ Grid Engine: {len(grid_engine.grids)} zones")
    print(f"✅ Pathfinder: A* algorithm ready")
    print(f"✅ Alert Engine: {len(alert_engine.people)} people registered")
    
    # Generate alerts
    print("\n" + "="*70)
    print("GENERATING PERSONALIZED ALERTS...")
    print("="*70)
    
    alerts = alert_engine.generate_all_alerts(grid_engine, {}, pathfinder)
    
    # Show summary
    urgency_counts = {}
    for alert in alerts:
        urgency = alert['urgency']
        urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
    
    print(f"\n📊 Generated {len(alerts)} alerts:")
    for urgency, count in sorted(urgency_counts.items()):
        emoji = "🔴" if urgency == "CRITICAL" else "🟡" if urgency == "HIGH" else "🟢"
        print(f"   {emoji} {urgency}: {count}")
    
    # Show each alert
    print("\n" + "="*70)
    print("PERSONALIZED MESSAGES")
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
        print(f"📏 Length: {len(alert['message'])} characters")
        print(f"\n{'-'*70}")
        print(alert['message'])
        print(f"{'-'*70}")
        
        # Pause between messages for readability
        if i < len(alerts):
            input("\nPress Enter to see next alert...")
    
    return alerts, alert_engine

def send_test_sms(alerts, alert_engine):
    """Try to send one test SMS"""
    
    print("\n" + "="*70)
    print("SEND TEST SMS")
    print("="*70)
    
    # Check if configured
    api_key = os.getenv('FAST2SMS_API_KEY')
    if not api_key or not api_key.strip():
        print("❌ Cannot send SMS - API key not configured")
        print("   Configure Fast2SMS first (see SMS_SETUP_GUIDE.md)")
        return
    
    print("\n📱 Available people:")
    for i, alert in enumerate(alerts, 1):
        print(f"   {i}. {alert['person']} ({alert['phone']}) - {alert['urgency']}")
    
    try:
        choice = input("\nEnter number to send test SMS (or 0 to skip): ").strip()
        
        if choice == "0":
            print("Skipped")
            return
        
        idx = int(choice) - 1
        if 0 <= idx < len(alerts):
            test_alert = alerts[idx]
            
            print(f"\n📤 Sending SMS to {test_alert['person']}...")
            print(f"   Phone: {test_alert['phone']}")
            
            success = alert_engine.send_sms(test_alert, method="fast2sms")
            
            if success:
                print("\n✅ SMS SENT SUCCESSFULLY!")
                print("   Check your phone in a few seconds")
            else:
                print("\n❌ SMS FAILED")
                print("   Check API key and phone number")
        else:
            print("Invalid choice")
    
    except ValueError:
        print("Invalid input")
    except KeyboardInterrupt:
        print("\nCancelled")

def main():
    print("\n" + "="*70)
    print("🚨 PERSONALIZED SMS ALERT SYSTEM - QUICK TEST")
    print("="*70)
    print("\nThis script will:")
    print("1. Check SMS service configuration")
    print("2. Generate personalized alerts for all 6 people")
    print("3. Show you what messages will be sent")
    print("4. Optionally send a test SMS")
    print("\n" + "="*70)
    
    # Check configuration
    is_configured = test_fast2sms_config()
    
    # Preview alerts
    try:
        alerts, alert_engine = preview_alerts()
        
        # Offer to send test
        if is_configured:
            print("\n" + "="*70)
            send_choice = input("\nWould you like to send a test SMS? (y/n): ").strip().lower()
            if send_choice == 'y':
                send_test_sms(alerts, alert_engine)
        
        # Final summary
        print("\n" + "="*70)
        print("✅ TEST COMPLETE")
        print("="*70)
        print("\n📚 Next Steps:")
        print("1. Configure Fast2SMS (see SMS_SETUP_GUIDE.md)")
        print("2. Start backend: uvicorn backend.main:app --reload --port 8001")
        print("3. Use API to send alerts: POST /api/alerts/generate")
        print("4. API Docs: http://localhost:8001/docs")
        print("\n💡 Tip: Each person gets a different message based on their")
        print("   location, profile, and current grid risk level!")
        print()
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure backend dependencies are installed:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)
