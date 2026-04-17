"""
Email Alert Sender - FREE Alternative to SMS
Uses Gmail SMTP to send email alerts
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Dict, List


class EmailAlertSender:
    """
    Send alerts via email using Gmail SMTP
    
    Setup (2 minutes):
    1. Use your Gmail account
    2. Enable "App Passwords" in Google Account settings
    3. Set environment variables:
       - EMAIL_SENDER=your_email@gmail.com
       - EMAIL_PASSWORD=your_app_password
    """
    
    def __init__(self):
        self.sender_email = os.getenv('EMAIL_SENDER')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, recipient_email: str, subject: str, message: str) -> Dict:
        """Send email alert"""
        
        if not self.sender_email or not self.sender_password:
            return {
                "success": False,
                "error": "Email credentials not configured",
                "message": "Set EMAIL_SENDER and EMAIL_PASSWORD in .env"
            }
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Plain text version
            text_part = MIMEText(message, 'plain')
            msg.attach(text_part)
            
            # HTML version (prettier)
            html_message = self._format_html(message, subject)
            html_part = MIMEText(html_message, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return {
                "success": True,
                "recipient": recipient_email,
                "subject": subject
            }
        
        except Exception as e:
            return {
                "success": False,
                "recipient": recipient_email,
                "error": str(e)
            }
    
    def _format_html(self, message: str, subject: str) -> str:
        """Format message as HTML email"""
        
        # Convert plain text to HTML with styling
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc3545; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
                .content {{ background: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; }}
                .footer {{ background: #6c757d; color: white; padding: 10px; text-align: center; border-radius: 0 0 5px 5px; font-size: 12px; }}
                .urgent {{ color: #dc3545; font-weight: bold; }}
                .info {{ background: #fff; padding: 15px; margin: 10px 0; border-left: 4px solid #dc3545; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🚨 {subject}</h2>
                </div>
                <div class="content">
                    <div class="info">
                        <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{message}</pre>
                    </div>
                </div>
                <div class="footer">
                    Mumbai Disaster Alert System | Automated Alert
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def send_bulk_emails(self, alerts: List[Dict], email_mapping: Dict[str, str]) -> Dict:
        """
        Send emails to multiple recipients
        
        Args:
            alerts: List of alert dicts
            email_mapping: Dict mapping phone numbers to email addresses
        """
        
        results = {
            "total": len(alerts),
            "sent": 0,
            "failed": 0,
            "details": []
        }
        
        for alert in alerts:
            # Get email for this person
            email = email_mapping.get(alert["phone"])
            
            if not email:
                print(f"⚠️  No email for {alert['person']} ({alert['phone']})")
                results["failed"] += 1
                continue
            
            # Send email
            subject = f"🚨 DISASTER ALERT: {alert['urgency']} - {alert['person']}"
            result = self.send_email(email, subject, alert["message"])
            
            if result["success"]:
                results["sent"] += 1
                print(f"✅ Email sent to {alert['person']} ({email})")
            else:
                results["failed"] += 1
                print(f"❌ Failed to send to {alert['person']}: {result.get('error')}")
            
            results["details"].append({
                "person": alert["person"],
                "email": email,
                "success": result["success"],
                "error": result.get("error")
            })
        
        return results


# Email mapping for the 6 people
EMAIL_MAPPING = {
    "+918848399722": "shambhavi@example.com",  # Replace with real email
    "+916302482236": "jashwanth@example.com",
    "+919347551809": "shiva@example.com",
    "+918309456402": "vaibhavi@example.com",
    "+918306579141": "mayuresh@example.com",
    "+919994268023": "hemlatha@example.com"
}


if __name__ == "__main__":
    print("=== EMAIL ALERT SENDER TEST ===\n")
    
    sender = EmailAlertSender()
    
    # Test email
    test_email = "mayuresh@example.com"  # Replace with your email
    test_subject = "🚨 TEST ALERT"
    test_message = """🚨 ALERT: Test User
⚠️ IMMEDIATE DANGER in Colaba
Risk: 85% | Water: 2.1m

📋 YOUR ACTION PLAN:
1. EVACUATE NOW
2. Move to higher ground
3. Call emergency services

📞 EMERGENCY:
Police: 100 | Fire: 101

⏱️ 02:30 PM
Stay safe!"""
    
    print(f"Sending test email to: {test_email}\n")
    
    result = sender.send_email(test_email, test_subject, test_message)
    
    if result["success"]:
        print("✅ SUCCESS! Email sent")
        print("\nCheck your inbox!")
    else:
        print("❌ FAILED")
        print(f"Error: {result.get('error')}")
        print("\nSetup Instructions:")
        print("1. Use your Gmail account")
        print("2. Enable 2-Step Verification")
        print("3. Generate App Password: https://myaccount.google.com/apppasswords")
        print("4. Set environment variables:")
        print("   export EMAIL_SENDER='your_email@gmail.com'")
        print("   export EMAIL_PASSWORD='your_app_password'")
