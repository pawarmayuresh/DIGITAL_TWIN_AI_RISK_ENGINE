"""
API Routes for SMS Alert System
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.core.alert_system.sms_alert_engine import PersonalizedAlertEngine
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder

router = APIRouter(prefix="/api/alerts", tags=["SMS Alerts"])

# Global instances
alert_engine = PersonalizedAlertEngine()
grid_engine = None  # Will be set from evacuation system
pathfinder = None


class AlertTrigger(BaseModel):
    """Request to trigger alerts"""
    send_sms: bool = False  # Set to True to actually send SMS
    urgency_filter: Optional[str] = None  # "CRITICAL", "HIGH", "MODERATE"


@router.get("/people")
async def list_registered_people():
    """List all registered people with their locations"""
    
    people_list = []
    for person_id, person in alert_engine.people.items():
        people_list.append({
            "id": person_id,
            "name": person.name,
            "phone": person.phone,
            "current_grid": person.current_grid,
            "age_group": person.age_group,
            "mobility": person.mobility,
            "has_vehicle": person.has_vehicle,
            "special_needs": person.special_needs
        })
    
    return {
        "total_people": len(people_list),
        "people": people_list
    }


@router.post("/generate")
async def generate_alerts(trigger: AlertTrigger):
    """
    Generate personalized alerts for all registered people
    
    This analyzes current grid conditions and generates
    personalized SMS messages for each person based on:
    - Their current location
    - Grid risk level
    - Their personal characteristics
    - Available evacuation routes
    """
    
    global grid_engine, pathfinder
    
    # Import from evacuation system
    if grid_engine is None:
        from backend.api.evacuation_routes import grid_engine as evac_grid
        from backend.api.evacuation_routes import pathfinder as evac_pathfinder
        grid_engine = evac_grid
        pathfinder = evac_pathfinder
    
    if grid_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Grid engine not initialized. Please reset evacuation grid first."
        )
    
    # Generate alerts
    try:
        alerts = alert_engine.generate_all_alerts(
            grid_engine,
            {},
            pathfinder
        )
        
        # Filter by urgency if specified
        if trigger.urgency_filter:
            alerts = [a for a in alerts if a["urgency"] == trigger.urgency_filter.upper()]
        
        # Send SMS if requested
        send_results = None
        if trigger.send_sms:
            send_results = alert_engine.send_all_alerts(alerts)
        
        return {
            "success": True,
            "alerts_generated": len(alerts),
            "alerts": [
                {
                    "person": a["person"],
                    "phone": a["phone"],
                    "grid": a["grid"],
                    "urgency": a["urgency"],
                    "message_preview": a["message"][:200] + "..." if len(a["message"]) > 200 else a["message"],
                    "message_length": len(a["message"])
                }
                for a in alerts
            ],
            "sms_sent": send_results if trigger.send_sms else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview/{person_id}")
async def preview_alert(person_id: str):
    """
    Preview alert message for a specific person
    without sending SMS
    """
    
    global grid_engine, pathfinder
    
    if person_id not in alert_engine.people:
        raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found")
    
    # Import from evacuation system
    if grid_engine is None:
        from backend.api.evacuation_routes import grid_engine as evac_grid
        from backend.api.evacuation_routes import pathfinder as evac_pathfinder
        grid_engine = evac_grid
        pathfinder = evac_pathfinder
    
    if grid_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Grid engine not initialized. Please reset evacuation grid first."
        )
    
    person = alert_engine.people[person_id]
    
    # Get grid data
    grid = grid_engine.get_grid(person.current_grid)
    if not grid:
        raise HTTPException(status_code=404, detail=f"Grid '{person.current_grid}' not found")
    
    grid_data = {
        'name': grid.name,
        'risk_score': grid.risk_score,
        'safety_level': grid.safety_level.value,
        'water_level': grid.water_level,
        'rainfall': grid.rainfall
    }
    
    # Find evacuation path
    evacuation_path = None
    if grid.safety_level.value in ['DANGEROUS', 'MEDIUM_RISK'] and pathfinder:
        safe_zone = pathfinder.find_nearest_safe_zone(grid)
        if safe_zone:
            path_result = pathfinder.find_path(grid, safe_zone)
            if path_result and path_result.get('success'):
                evacuation_path = path_result.get('path', [])
    
    # Generate alert
    alert = alert_engine.generate_personalized_alert(
        person,
        grid_data,
        {},
        evacuation_path
    )
    
    return {
        "person": {
            "name": person.name,
            "phone": person.phone,
            "grid": person.current_grid,
            "age_group": person.age_group,
            "has_vehicle": person.has_vehicle
        },
        "grid_status": grid_data,
        "alert": alert,
        "evacuation_path": evacuation_path[:5] if evacuation_path else None
    }


@router.get("/history")
async def get_alert_history():
    """Get history of all alerts sent"""
    
    summary = alert_engine.get_alert_summary()
    
    recent_alerts = alert_engine.alert_history[-10:] if alert_engine.alert_history else []
    
    return {
        "summary": summary,
        "recent_alerts": [
            {
                "timestamp": a["timestamp"].isoformat(),
                "person": a["person"],
                "grid": a["grid"],
                "urgency": a["urgency"],
                "message_length": a["message_length"]
            }
            for a in recent_alerts
        ]
    }


@router.post("/test/send-one")
async def test_send_one_sms(person_id: str):
    """
    Test sending SMS to one person
    Requires Twilio configuration
    """
    
    if person_id not in alert_engine.people:
        raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found")
    
    # Generate alert for this person
    alerts = await generate_alerts(AlertTrigger(send_sms=False))
    
    person_alert = next(
        (a for a in alerts["alerts"] if a["person"] == alert_engine.people[person_id].name),
        None
    )
    
    if not person_alert:
        raise HTTPException(status_code=404, detail="Alert not generated")
    
    # Reconstruct full alert
    full_alert = {
        "person": person_alert["person"],
        "phone": person_alert["phone"],
        "message": person_alert["message_preview"],  # In real scenario, get full message
        "urgency": person_alert["urgency"]
    }
    
    # Try to send
    success = alert_engine.send_sms_via_twilio(full_alert)
    
    return {
        "success": success,
        "person": person_alert["person"],
        "phone": person_alert["phone"],
        "message": "SMS sent successfully" if success else "SMS sending failed (check Twilio config)"
    }


@router.get("/setup-instructions")
async def get_setup_instructions():
    """Get instructions for setting up Twilio SMS"""
    
    return {
        "service": "Twilio SMS API",
        "steps": [
            "1. Sign up at https://www.twilio.com/try-twilio",
            "2. Get your Account SID and Auth Token from console",
            "3. Get a Twilio phone number",
            "4. Set environment variables:",
            "   export TWILIO_ACCOUNT_SID='your_account_sid'",
            "   export TWILIO_AUTH_TOKEN='your_auth_token'",
            "   export TWILIO_PHONE_NUMBER='+1234567890'",
            "5. Install Twilio: pip install twilio",
            "6. Test with /api/alerts/test/send-one"
        ],
        "alternative": "For demo without Twilio, alerts will be logged to console",
        "registered_numbers": [
            person.phone for person in alert_engine.people.values()
        ]
    }
