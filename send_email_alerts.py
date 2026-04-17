#!/usr/bin/env python3
"""
Send Email Alerts - FREE Alternative to SMS
"""

import os
import sys
sys.path.insert(0, 'backend')

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.core.alert_system.email_alert_sender import EmailAlertSender, EMAIL_MAPPING
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

def main():
    print("="*70)
    print("📧 EMAIL ALERT SYSTEM")
    print("="*70)
    
    # Check email configuration
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        print("\n⚠️  Email not configured")
        print("\n📝 Quick Setup (2 minutes):")
        print("1. Use your Gmail account")
        print("2. Enable 2-Step Verification in Google Account")
        print("3. Generate App Password:")
        print("   https://myaccount.google.com/apppasswords")
        print("4. Add to .env file:")
        print("   EMAIL_SENDER=your_email@gmail.com")
        print("   EMAIL_PASSWORD=your_16_char_app_password")
        print("\n💡 Or just demo the alerts without sending:")
        print("   python3 show_alerts.py")
        return
    
    print(f"\n✅ Email configured: {sender_email}")
    
    # Initialize systems
    print("\n" + "="*70)
    print("INITIALIZING...")
    print("="*70)
    
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    pathfinder = EvacuationPathfinder(grid_engine)
    alert_engine = PersonalizedAlertEngine()
    email_sender = EmailAlertSender()
    
    print(f"✅ Grid: {len(grid_engine.grids)} zones")
    print(f"✅ Alert Engine: {len(alert_engine.people)} people")
    
    # Generate alerts
    print("\n" + "="*70)
    print("GENERATING ALERTS...")
    print("="*70)
    
    alerts = alert_engine.generate_all_alerts(grid_engine, {}, pathfinder)
    
    print(f"✅ Generated {len(alerts)} alerts")
    
    # Show email mapping
    print("\n" + "="*70)
    print("EMAIL RECIPIENTS:")
    print("="*70)
    
    for alert in alerts:
        email = EMAIL_MAPPING.get(alert["phone"], "NOT_SET")
        print(f"{alert['person']:20} {alert['phone']:15} → {email}")
    
    print("\n⚠️  NOTE: Update EMAIL_MAPPING in email_alert_sender.py with real emails")
    
    # Confirm
    print("\n" + "="*70)
    confirm = input("\nSend email alerts to all 6 people? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Cancelled")
        return
    
    # Send emails
    print("\n" + "="*70)
    print("SENDING EMAILS...")
    print("="*70)
    
    results = email_sender.send_bulk_emails(alerts, EMAIL_MAPPING)
    
    print(f"\n✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    
    if results['sent'] > 0:
        print("\n🎉 Emails sent! Check inboxes in a few seconds")
    
    if results['failed'] > 0:
        print("\n⚠️  Some emails failed. Check:")
        print("1. Email addresses are correct in EMAIL_MAPPING")
        print("2. Gmail App Password is correct")
        print("3. Internet connection is working")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
