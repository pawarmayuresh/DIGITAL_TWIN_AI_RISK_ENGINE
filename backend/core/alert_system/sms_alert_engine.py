"""
Personalized SMS Alert System
Sends location-specific disaster warnings and action recommendations
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class Person:
    """Represents a person with location and contact info"""
    name: str
    phone: str
    current_grid: str  # Grid ID like "A1", "B2"
    age_group: str  # "student", "adult", "elderly", "professor"
    mobility: str  # "high", "medium", "low"
    has_vehicle: bool = False
    special_needs: List[str] = None
    
    def __post_init__(self):
        if self.special_needs is None:
            self.special_needs = []


class PersonalizedAlertEngine:
    """
    Generates personalized SMS alerts based on:
    - Person's current location (grid)
    - Grid risk level
    - Person's characteristics (age, mobility)
    - Available evacuation routes
    - Real-time situation
    """
    
    def __init__(self):
        # Register people with their locations
        self.people: Dict[str, Person] = {}
        self.alert_history: List[Dict] = []
        self._register_people()
    
    def _register_people(self):
        """Register all people with their details"""
        
        # Students
        self.people["shambhavi"] = Person(
            name="Shambhavi",
            phone="+918848399722",
            current_grid="C5",  # Bandra area
            age_group="student",
            mobility="high",
            has_vehicle=False
        )
        
        self.people["jashwanth"] = Person(
            name="Jashwanth Ram",
            phone="+916302482236",
            current_grid="D3",  # Dadar area
            age_group="student",
            mobility="high",
            has_vehicle=False
        )
        
        self.people["shiva"] = Person(
            name="Shiva",
            phone="+919347551809",
            current_grid="B2",  # Fort area
            age_group="student",
            mobility="high",
            has_vehicle=False
        )
        
        self.people["vaibhavi"] = Person(
            name="Vaibhavi",
            phone="+918309456402",
            current_grid="E4",  # Kurla area
            age_group="student",
            mobility="high",
            has_vehicle=False
        )
        
        self.people["mayuresh"] = Person(
            name="Mayuresh",
            phone="+918306579141",
            current_grid="A1",  # Colaba area (high risk coastal)
            age_group="adult",
            mobility="high",
            has_vehicle=True
        )
        
        # Professor
        self.people["prof_hemlatha"] = Person(
            name="Prof. Hemlatha",
            phone="+919994268023",
            current_grid="F6",  # Andheri area
            age_group="professor",
            mobility="medium",
            has_vehicle=True,
            special_needs=["priority_evacuation"]
        )
    
    def generate_personalized_alert(
        self,
        person: Person,
        grid_data: Dict,
        situation: Dict,
        evacuation_path: Optional[List[Dict]] = None
    ) -> Dict[str, str]:
        """
        Generate personalized alert message based on person's situation
        
        Returns:
            Dict with 'message' and 'urgency' level
        """
        
        grid = grid_data
        risk_score = grid.get('risk_score', 0.5)
        safety_level = grid.get('safety_level', 'MEDIUM_RISK')
        water_level = grid.get('water_level', 0)
        
        # Determine urgency
        if safety_level == 'DANGEROUS' or risk_score > 0.7:
            urgency = "CRITICAL"
        elif safety_level == 'MEDIUM_RISK' or risk_score > 0.4:
            urgency = "HIGH"
        else:
            urgency = "MODERATE"
        
        # Build personalized message
        message_parts = []
        
        # Greeting
        message_parts.append(f"🚨 ALERT: {person.name}")
        
        # Situation assessment
        if urgency == "CRITICAL":
            message_parts.append(f"\n⚠️ IMMEDIATE DANGER in {grid.get('name', person.current_grid)}")
            message_parts.append(f"Risk: {risk_score*100:.0f}% | Water: {water_level:.1f}m")
        elif urgency == "HIGH":
            message_parts.append(f"\n⚠️ HIGH RISK in {grid.get('name', person.current_grid)}")
            message_parts.append(f"Risk: {risk_score*100:.0f}% | Water: {water_level:.1f}m")
        else:
            message_parts.append(f"\n⚠️ ALERT for {grid.get('name', person.current_grid)}")
            message_parts.append(f"Risk: {risk_score*100:.0f}%")
        
        # Personalized actions based on characteristics
        message_parts.append("\n\n📋 YOUR ACTION PLAN:")
        
        if urgency == "CRITICAL":
            # Critical situation - immediate evacuation
            if person.has_vehicle:
                message_parts.append("\n1. EVACUATE NOW by car")
                message_parts.append("2. Avoid flooded roads")
                if person.age_group == "adult":
                    message_parts.append("3. Help elderly neighbors if safe")
            else:
                message_parts.append("\n1. EVACUATE IMMEDIATELY on foot")
                message_parts.append("2. Move to higher ground")
                if person.mobility == "high":
                    message_parts.append("3. Help others if possible")
            
            # Add evacuation route if available
            if evacuation_path and len(evacuation_path) > 1:
                route = " → ".join([p.get('grid_id', '') for p in evacuation_path[:4]])
                message_parts.append(f"\n\n🗺️ ROUTE: {route}")
                message_parts.append(f"Distance: {len(evacuation_path)} zones")
            
            # Emergency contacts
            message_parts.append("\n\n📞 EMERGENCY:")
            message_parts.append("Police: 100 | Fire: 101")
            message_parts.append("Ambulance: 102 | Disaster: 108")
            
        elif urgency == "HIGH":
            # High risk - prepare to evacuate
            message_parts.append("\n1. Prepare to evacuate")
            message_parts.append("2. Pack essentials (documents, medicine, water)")
            message_parts.append("3. Charge phone fully")
            
            if person.has_vehicle:
                message_parts.append("4. Keep vehicle ready")
            
            if person.age_group == "student":
                message_parts.append("5. Stay with group, inform family")
            elif person.age_group == "professor":
                message_parts.append("5. Coordinate with students")
            
            message_parts.append("\n\n⏰ Be ready to move in 30 minutes")
            
        else:
            # Moderate risk - stay alert
            message_parts.append("\n1. Stay indoors if safe")
            message_parts.append("2. Monitor updates")
            message_parts.append("3. Keep emergency kit ready")
            message_parts.append("4. Avoid unnecessary travel")
        
        # Specific advice based on person type
        if person.age_group == "student":
            message_parts.append("\n\n👥 STUDENT ADVICE:")
            message_parts.append("- Stay with friends")
            message_parts.append("- Inform family of location")
            message_parts.append("- Follow campus instructions")
        
        elif person.age_group == "professor":
            message_parts.append("\n\n👨‍🏫 FACULTY RESPONSIBILITY:")
            message_parts.append("- Account for all students")
            message_parts.append("- Coordinate with admin")
            message_parts.append("- Lead evacuation if needed")
        
        # Safety tips based on situation
        if water_level > 1.0:
            message_parts.append("\n\n💧 FLOOD SAFETY:")
            message_parts.append("- Don't walk in water >knee deep")
            message_parts.append("- Avoid electrical areas")
            message_parts.append("- Move to upper floors")
        
        # Shelter information
        if urgency in ["CRITICAL", "HIGH"]:
            message_parts.append("\n\n🏠 NEAREST SHELTERS:")
            message_parts.append("- Municipal School (2km N)")
            message_parts.append("- Community Center (1.5km E)")
            message_parts.append("- Sports Complex (3km NE)")
        
        # Timestamp
        message_parts.append(f"\n\n⏱️ {datetime.now().strftime('%I:%M %p')}")
        message_parts.append("Stay safe! Updates every 15 min")
        
        return {
            "message": "".join(message_parts),
            "urgency": urgency,
            "person": person.name,
            "phone": person.phone,
            "grid": person.current_grid
        }
    
    def generate_all_alerts(
        self,
        grid_engine,
        situation: Dict,
        pathfinder = None
    ) -> List[Dict]:
        """Generate alerts for all registered people"""
        
        alerts = []
        
        for person_id, person in self.people.items():
            # Get person's grid data
            grid = grid_engine.get_grid(person.current_grid)
            if not grid:
                continue
            
            grid_data = {
                'name': grid.name,
                'risk_score': grid.risk_score,
                'safety_level': grid.safety_level.value,
                'water_level': grid.water_level,
                'rainfall': grid.rainfall
            }
            
            # Find evacuation path if in danger
            evacuation_path = None
            if grid.safety_level.value in ['DANGEROUS', 'MEDIUM_RISK'] and pathfinder:
                safe_zone = pathfinder.find_nearest_safe_zone(grid)
                if safe_zone:
                    path_result = pathfinder.find_path(grid, safe_zone)
                    if path_result and path_result.get('success'):
                        evacuation_path = path_result.get('path', [])
            
            # Generate personalized alert
            alert = self.generate_personalized_alert(
                person,
                grid_data,
                situation,
                evacuation_path
            )
            
            alerts.append(alert)
            
            # Log alert
            self.alert_history.append({
                "timestamp": datetime.now(),
                "person": person.name,
                "grid": person.current_grid,
                "urgency": alert["urgency"],
                "message_length": len(alert["message"])
            })
        
        return alerts
    
    def send_sms_via_twilio(self, alert: Dict) -> bool:
        """
        Send SMS using Twilio API
        
        Setup required:
        1. pip install twilio
        2. Set environment variables:
           - TWILIO_ACCOUNT_SID
           - TWILIO_AUTH_TOKEN
           - TWILIO_PHONE_NUMBER
        
        Note: Trial accounts can only send to verified numbers
        """
        try:
            from twilio.rest import Client
            
            # Get Twilio credentials from environment
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_phone = os.getenv('TWILIO_PHONE_NUMBER')
            
            if not all([account_sid, auth_token, from_phone]):
                print("⚠️ Twilio credentials not configured")
                print(f"Would send to {alert['phone']}: {alert['message'][:100]}...")
                return False
            
            # Initialize Twilio client
            client = Client(account_sid, auth_token)
            
            # Truncate message if too long (Twilio limit: 1600 chars)
            message_text = alert['message']
            if len(message_text) > 1600:
                message_text = message_text[:1597] + "..."
            
            # Send SMS
            message = client.messages.create(
                body=message_text,
                from_=from_phone,
                to=alert['phone']
            )
            
            print(f"✅ SMS sent to {alert['person']} ({alert['phone']})")
            print(f"   Message SID: {message.sid}")
            print(f"   Status: {message.status}")
            return True
            
        except ImportError:
            print("⚠️ Twilio not installed. Run: pip install twilio")
            print(f"Would send to {alert['phone']}:")
            print(alert['message'])
            return False
        
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Failed to send SMS to {alert['person']}: {error_msg}")
            
            # Helpful error messages
            if "not a valid phone number" in error_msg.lower():
                print(f"   💡 Check phone number format: {alert['phone']}")
            elif "not verified" in error_msg.lower() or "trial" in error_msg.lower():
                print(f"   💡 Trial account: Verify this number at:")
                print(f"      https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
            elif "insufficient" in error_msg.lower():
                print(f"   💡 Insufficient credits. Check balance at:")
                print(f"      https://console.twilio.com/")
            
            return False
    
    def send_sms_via_fast2sms(self, alert: Dict) -> bool:
        """
        Send SMS using Fast2SMS (Free for India)
        
        Setup:
        1. Sign up at https://www.fast2sms.com/
        2. Get API key
        3. Set: export FAST2SMS_API_KEY='your_key'
        """
        try:
            from backend.core.alert_system.free_sms_sender import FreeSMSSender
            
            sender = FreeSMSSender()
            result = sender.send_sms(alert['phone'], alert['message'])
            
            if result['success']:
                print(f"✅ SMS sent to {alert['person']} ({alert['phone']})")
                return True
            else:
                print(f"❌ Failed: {result.get('error')}")
                return False
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def send_sms(self, alert: Dict, method: str = "fast2sms") -> bool:
        """
        Send SMS using specified method
        
        Args:
            alert: Alert dict with phone, message, person
            method: "fast2sms" (free, India) or "twilio" (paid, global)
        """
        if method == "fast2sms":
            return self.send_sms_via_fast2sms(alert)
        else:
            return self.send_sms_via_twilio(alert)
    
    def send_all_alerts(self, alerts: List[Dict], method: str = "fast2sms") -> Dict:
        """
        Send all alerts and return summary
        
        Args:
            alerts: List of alert dicts
            method: "fast2sms" (free, India) or "twilio" (paid, global)
        """
        
        results = {
            "total": len(alerts),
            "sent": 0,
            "failed": 0,
            "by_urgency": {
                "CRITICAL": 0,
                "HIGH": 0,
                "MODERATE": 0
            }
        }
        
        for alert in alerts:
            # Count by urgency
            results["by_urgency"][alert["urgency"]] += 1
            
            # Send SMS using specified method
            success = self.send_sms(alert, method)
            
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def get_alert_summary(self) -> Dict:
        """Get summary of all alerts sent"""
        
        if not self.alert_history:
            return {"total_alerts": 0}
        
        return {
            "total_alerts": len(self.alert_history),
            "people_alerted": len(set(a["person"] for a in self.alert_history)),
            "critical_alerts": sum(1 for a in self.alert_history if a["urgency"] == "CRITICAL"),
            "last_alert": self.alert_history[-1]["timestamp"].isoformat() if self.alert_history else None
        }


# Example usage
if __name__ == "__main__":
    print("=== Personalized SMS Alert System ===\n")
    
    # This would be integrated with your grid engine
    # For demo, showing what messages would look like
    
    alert_engine = PersonalizedAlertEngine()
    
    print("Registered People:")
    for person_id, person in alert_engine.people.items():
        print(f"  - {person.name} ({person.phone})")
        print(f"    Location: {person.current_grid}, {person.age_group}, Vehicle: {person.has_vehicle}")
    
    print("\n" + "="*50)
    print("\nSample Alert Messages:\n")
    
    # Sample grid data for demonstration
    sample_grids = {
        "A1": {  # Mayuresh - Coastal, high risk
            "name": "Colaba",
            "risk_score": 0.85,
            "safety_level": "DANGEROUS",
            "water_level": 2.1,
            "rainfall": 95
        },
        "C5": {  # Shambhavi - Medium risk
            "name": "Bandra West",
            "risk_score": 0.55,
            "safety_level": "MEDIUM_RISK",
            "water_level": 0.8,
            "rainfall": 65
        },
        "F6": {  # Prof Hemlatha - Low risk
            "name": "Andheri",
            "risk_score": 0.25,
            "safety_level": "SAFE",
            "water_level": 0.3,
            "rainfall": 35
        }
    }
    
    # Generate sample alerts
    for person_id, person in list(alert_engine.people.items())[:3]:
        grid_data = sample_grids.get(person.current_grid, sample_grids["C5"])
        
        alert = alert_engine.generate_personalized_alert(
            person,
            grid_data,
            {},
            None
        )
        
        print(f"\n{'='*50}")
        print(f"Alert for: {alert['person']} ({alert['urgency']})")
        print(f"Phone: {alert['phone']}")
        print(f"{'='*50}")
        print(alert['message'])
        print()
