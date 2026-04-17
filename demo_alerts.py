#!/usr/bin/env python3
"""
Demo Alert System - Perfect for Faculty Presentation
Shows all personalized alerts without sending anything
"""

import sys
sys.path.insert(0, 'backend')

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

def print_box(text, width=70, char="="):
    """Print text in a box"""
    print(char * width)
    print(text.center(width))
    print(char * width)

def main():
    print("\n")
    print_box("🚨 MUMBAI DISASTER ALERT SYSTEM", char="=")
    print_box("Personalized SMS Alert Demo", char="-")
    print("\n")
    
    # Initialize
    print("⚙️  Initializing systems...")
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    pathfinder = EvacuationPathfinder(grid_engine)
    alert_engine = PersonalizedAlertEngine()
    
    print(f"✅ Grid Engine: {len(grid_engine.grids)} zones")
    print(f"✅ Pathfinder: A* algorithm ready")
    print(f"✅ Alert Engine: {len(alert_engine.people)} people registered")
    
    # Generate alerts
    print("\n⚙️  Analyzing grid conditions and generating personalized alerts...")
    alerts = alert_engine.generate_all_alerts(grid_engine, {}, pathfinder)
    
    # Count by urgency
    urgency_counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0}
    for alert in alerts:
        urgency_counts[alert['urgency']] += 1
    
    print(f"✅ Generated {len(alerts)} personalized alerts\n")
    
    # Summary
    print_box("📊 ALERT SUMMARY", char="=")
    print(f"\n  Total Alerts: {len(alerts)}")
    print(f"  🔴 CRITICAL: {urgency_counts['CRITICAL']} (Immediate evacuation required)")
    print(f"  🟡 HIGH:     {urgency_counts['HIGH']} (Prepare to evacuate)")
    print(f"  🟢 MODERATE: {urgency_counts['MODERATE']} (Stay alert)")
    print()
    
    # Show each alert
    for i, alert in enumerate(alerts, 1):
        urgency_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟡",
            "MODERATE": "🟢"
        }
        
        print("\n")
        print_box(f"{urgency_emoji[alert['urgency']]} ALERT #{i}: {alert['person']}", char="=")
        
        print(f"\n  Urgency Level: {alert['urgency']}")
        print(f"  Phone Number:  {alert['phone']}")
        print(f"  Location:      {alert['grid']}")
        print(f"  Message Size:  {len(alert['message'])} characters")
        
        print(f"\n  {'─' * 68}")
        print(f"  MESSAGE CONTENT:")
        print(f"  {'─' * 68}\n")
        
        # Print message with indentation
        for line in alert['message'].split('\n'):
            print(f"  {line}")
        
        print(f"\n  {'─' * 68}")
        
        # Pause between alerts
        if i < len(alerts):
            input("\n  ⏎ Press Enter to see next alert...")
    
    # Final summary
    print("\n")
    print_box("✅ DEMO COMPLETE", char="=")
    
    print("\n📋 KEY FEATURES DEMONSTRATED:\n")
    print("  ✅ Personalized messages for each person")
    print("  ✅ Different urgency levels based on location")
    print("  ✅ Evacuation routes included (A* pathfinding)")
    print("  ✅ Profile-based customization (student/professor/adult)")
    print("  ✅ Vehicle and mobility considerations")
    print("  ✅ Emergency contacts and shelter information")
    print("  ✅ Real-time risk assessment integration")
    
    print("\n🔧 SYSTEM INTEGRATION:\n")
    print("  • Grid Engine: Simulates Mumbai flood zones")
    print("  • Bayesian Network: Calculates risk scores")
    print("  • A* Pathfinding: Finds optimal evacuation routes")
    print("  • Policy Engine: Determines best actions")
    print("  • Alert Engine: Generates personalized messages")
    
    print("\n📱 DELIVERY OPTIONS:\n")
    print("  • SMS (Fast2SMS, Twilio)")
    print("  • Email (Gmail SMTP)")
    print("  • WhatsApp (Twilio)")
    print("  • Telegram Bot")
    print("  • Web Dashboard")
    print("  • Push Notifications")
    
    print("\n💡 FOR FACULTY:\n")
    print("  This demo shows how the system generates unique,")
    print("  personalized alerts for each person based on:")
    print("  - Their current location in the grid")
    print("  - Real-time risk assessment")
    print("  - Personal characteristics (age, mobility, vehicle)")
    print("  - Available evacuation routes")
    print("  - Urgency level of the situation")
    
    print("\n  Each message is different because each person's")
    print("  situation is different!")
    
    print("\n" + "="*70)
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo cancelled by user\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
