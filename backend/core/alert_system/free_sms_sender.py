"""
Free SMS Sender for India
Uses Fast2SMS API (free tier available)
"""
import requests
import os
from typing import Dict, List


class FreeSMSSender:
    """
    Send SMS using Fast2SMS (India)
    Free tier: 50 SMS/day
    
    Setup:
    1. Sign up at https://www.fast2sms.com/
    2. Get API key from dashboard
    3. Set environment variable: export FAST2SMS_API_KEY='your_key'
    """
    
    def __init__(self):
        self.api_key = os.getenv('FAST2SMS_API_KEY')
        self.api_url = "https://www.fast2sms.com/dev/bulkV2"
    
    def send_sms(self, phone: str, message: str) -> Dict:
        """
        Send SMS to Indian phone number
        
        Args:
            phone: Phone number (with or without +91)
            message: Message text (max 500 chars for free tier)
        
        Returns:
            Dict with success status and details
        """
        
        if not self.api_key:
            return {
                "success": False,
                "error": "FAST2SMS_API_KEY not configured",
                "message": "Set environment variable: export FAST2SMS_API_KEY='your_key'"
            }
        
        # Clean phone number (remove +91 if present)
        clean_phone = phone.replace("+91", "").replace(" ", "").strip()
        
        # Truncate message if too long (Fast2SMS free tier limit)
        if len(message) > 500:
            message = message[:497] + "..."
        
        # Prepare request
        payload = {
            "authorization": self.api_key,
            "route": "q",  # Quick route for transactional SMS
            "message": message,
            "language": "english",
            "flash": 0,
            "numbers": clean_phone
        }
        
        headers = {
            "cache-control": "no-cache"
        }
        
        try:
            response = requests.post(
                self.api_url,
                data=payload,
                headers=headers,
                timeout=10
            )
            
            result = response.json()
            
            if response.status_code == 200 and result.get("return"):
                return {
                    "success": True,
                    "phone": phone,
                    "message_id": result.get("request_id"),
                    "details": result
                }
            else:
                return {
                    "success": False,
                    "phone": phone,
                    "error": result.get("message", "Unknown error"),
                    "details": result
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "phone": phone,
                "error": "Request timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "phone": phone,
                "error": str(e)
            }
    
    def send_bulk_sms(self, alerts: List[Dict]) -> Dict:
        """Send SMS to multiple recipients"""
        
        results = {
            "total": len(alerts),
            "sent": 0,
            "failed": 0,
            "details": []
        }
        
        for alert in alerts:
            result = self.send_sms(alert["phone"], alert["message"])
            
            if result["success"]:
                results["sent"] += 1
                print(f"✅ SMS sent to {alert['person']} ({alert['phone']})")
            else:
                results["failed"] += 1
                print(f"❌ Failed to send to {alert['person']}: {result.get('error')}")
            
            results["details"].append({
                "person": alert["person"],
                "phone": alert["phone"],
                "success": result["success"],
                "error": result.get("error")
            })
        
        return results


class WhatsAppSender:
    """
    Alternative: Send via WhatsApp using Twilio WhatsApp API
    More reliable than SMS, works internationally
    """
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
    
    def send_whatsapp(self, phone: str, message: str) -> Dict:
        """Send WhatsApp message via Twilio"""
        
        if not all([self.account_sid, self.auth_token]):
            return {
                "success": False,
                "error": "Twilio credentials not configured"
            }
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            # Format phone for WhatsApp
            whatsapp_to = f"whatsapp:{phone}"
            
            message_obj = client.messages.create(
                body=message,
                from_=self.whatsapp_from,
                to=whatsapp_to
            )
            
            return {
                "success": True,
                "phone": phone,
                "message_sid": message_obj.sid
            }
        
        except ImportError:
            return {
                "success": False,
                "error": "Twilio not installed. Run: pip install twilio"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Test function
if __name__ == "__main__":
    print("=== FREE SMS SENDER TEST ===\n")
    
    sender = FreeSMSSender()
    
    # Test message
    test_alert = {
        "person": "Test User",
        "phone": "+918306579141",  # Mayuresh's number
        "message": "🚨 TEST ALERT: This is a test message from Mumbai Disaster Alert System. If you receive this, the system is working!"
    }
    
    print("Attempting to send test SMS...")
    print(f"To: {test_alert['phone']}")
    print(f"Message: {test_alert['message']}\n")
    
    result = sender.send_sms(test_alert["phone"], test_alert["message"])
    
    if result["success"]:
        print("✅ SUCCESS! SMS sent successfully")
        print(f"Message ID: {result.get('message_id')}")
    else:
        print("❌ FAILED")
        print(f"Error: {result.get('error')}")
        print(f"\nSetup Instructions:")
        print("1. Go to https://www.fast2sms.com/")
        print("2. Sign up (free)")
        print("3. Get API key from dashboard")
        print("4. Run: export FAST2SMS_API_KEY='your_api_key'")
        print("5. Run this script again")
