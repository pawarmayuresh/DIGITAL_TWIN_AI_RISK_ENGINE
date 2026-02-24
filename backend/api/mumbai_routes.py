"""
Mumbai API Routes
Real-time disaster monitoring endpoints for Mumbai
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

router = APIRouter(tags=["mumbai"])

# Import data loader
data_loader = None
try:
    from ..data_loaders.mumbai_data_loader import get_mumbai_data_loader
    data_loader = get_mumbai_data_loader()
    print("✅ Mumbai data loader initialized successfully")
except Exception as e:
    print(f"❌ Warning: Could not load Mumbai data: {e}")
    import traceback
    traceback.print_exc()


class RainfallSimulation(BaseModel):
    ward_id: str
    rainfall_mm: float


@router.get("/wards")
async def get_all_wards():
    """Get all Mumbai wards with demographics"""
    if not data_loader:
        raise HTTPException(status_code=503, detail="Mumbai data not loaded. Check backend logs.")
    
    try:
        wards = data_loader.get_all_wards()
        
        # Enrich with risk scores
        risk_scores = {r['ward_id']: r for r in data_loader.get_risk_scores()}
        
        for ward in wards:
            ward_id = ward['ward_id']
            if ward_id in risk_scores:
                ward['risk_score'] = risk_scores[ward_id]['composite_risk']
                ward['severity_level'] = risk_scores[ward_id]['severity_level']
            else:
                ward['risk_score'] = 0.0
                ward['severity_level'] = 'Low'
        
        return wards
    except Exception as e:
        print(f"Error in get_all_wards: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ward/{ward_id}")
async def get_ward(ward_id: str):
    """Get specific ward details"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    ward = data_loader.get_ward(ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail=f"Ward {ward_id} not found")
    
    # Add risk score
    risk = data_loader.get_ward_risk(ward_id)
    if risk:
        ward['risk_score'] = risk['composite_risk']
        ward['severity_level'] = risk['severity_level']
    
    # Add infrastructure
    ward['infrastructure'] = data_loader.get_infrastructure_by_ward(ward_id)
    
    # Add recommendations
    ward['recommendations'] = data_loader.get_recommendations(ward_id)
    
    return ward


@router.get("/infrastructure")
async def get_infrastructure():
    """Get all infrastructure nodes"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_all_infrastructure()


@router.get("/risk-scores")
async def get_risk_scores():
    """Get current risk scores for all wards"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_risk_scores()


@router.get("/recommendations")
async def get_recommendations(ward_id: Optional[str] = None):
    """Get AI recommendations"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_recommendations(ward_id)


@router.get("/explainability/{ward_id}")
async def get_explainability(ward_id: str):
    """Get feature importance for ward risk score"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    features = data_loader.get_explainability(ward_id)
    if not features:
        raise HTTPException(status_code=404, detail=f"No explainability data for ward {ward_id}")
    
    return {
        "ward_id": ward_id,
        "features": features,
        "total_contribution": sum(f['contribution_percent'] for f in features)
    }


@router.get("/sensors/rain")
async def get_rain_sensors():
    """Get rain sensor data"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_rain_sensors()


@router.get("/sensors/water")
async def get_water_sensors():
    """Get water level sensor data (Mithi River)"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    sensors = data_loader.get_water_sensors()
    
    # Add alert status
    for sensor in sensors:
        sensor['is_alert'] = sensor['water_level_cm'] > sensor['alert_threshold']
        sensor['overflow_cm'] = max(0, sensor['water_level_cm'] - sensor['alert_threshold'])
    
    return sensors


@router.get("/sensors/traffic")
async def get_traffic_sensors():
    """Get traffic density data"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_traffic_sensors()


@router.get("/sensors/power")
async def get_power_load():
    """Get power grid status"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_power_load()


@router.get("/sensors/alerts")
async def get_alert_sensors():
    """Get crowd panic sensor data"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_alert_sensors()


@router.get("/historical/floods")
async def get_historical_floods():
    """Get historical flood events"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_historical_floods()


@router.get("/historical/cyclones")
async def get_cyclone_history():
    """Get cyclone history"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_cyclone_history()


@router.get("/historical/rainfall")
async def get_rainfall_history(ward_id: Optional[str] = None):
    """Get rainfall history"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    return data_loader.get_rainfall_history(ward_id)


@router.post("/simulate/rainfall")
async def simulate_rainfall(simulation: RainfallSimulation):
    """Simulate rainfall impact on specific ward"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    ward = data_loader.get_ward(simulation.ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail=f"Ward {simulation.ward_id} not found")
    
    # Calculate flood risk based on rainfall and ward characteristics
    base_risk = min(simulation.rainfall_mm / 1000, 1.0)  # Normalize
    slum_factor = ward['slum_population_percent'] / 100 * 0.3
    density_factor = ward['population_density'] / 100000 * 0.2
    
    flood_risk = min(base_risk + slum_factor + density_factor, 1.0)
    
    # Determine severity
    if flood_risk > 0.8:
        severity = 'Severe'
    elif flood_risk > 0.6:
        severity = 'High'
    elif flood_risk > 0.4:
        severity = 'Moderate'
    else:
        severity = 'Low'
    
    return {
        "ward_id": simulation.ward_id,
        "ward_name": ward['ward_name'],
        "rainfall_mm": simulation.rainfall_mm,
        "flood_risk_score": flood_risk,
        "severity_level": severity,
        "factors": {
            "base_risk": base_risk,
            "slum_factor": slum_factor,
            "density_factor": density_factor
        },
        "recommendations": data_loader.get_recommendations(simulation.ward_id)
    }


@router.post("/simulate/historical/{event_id}")
async def replay_historical_flood(event_id: str):
    """Replay historical flood event"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    floods = data_loader.get_historical_floods()
    event = next((f for f in floods if f['event_id'] == event_id), None)
    
    if not event:
        raise HTTPException(status_code=404, detail=f"Flood event {event_id} not found")
    
    # Parse affected wards
    affected_wards = [w.strip() for w in event['affected_wards'].split(',')]
    
    # Simulate impact on each ward
    results = {}
    for ward_id in affected_wards:
        ward = data_loader.get_ward(ward_id)
        if ward:
            # Estimate rainfall from water level
            estimated_rainfall = event['water_level_cm'] * 2
            
            results[ward_id] = {
                "ward_name": ward['ward_name'],
                "estimated_rainfall_mm": estimated_rainfall,
                "population_affected": int(ward['population'] * 0.3),  # Estimate
                "risk_level": "Severe"
            }
    
    return {
        "event": event,
        "simulation_results": results,
        "total_casualties": event['casualties'],
        "total_economic_loss_crore": event['economic_loss_crore']
    }


@router.get("/mithi-river/status")
async def get_mithi_river_status():
    """Get Mithi River current status"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    water_sensors = data_loader.get_water_sensors()
    mithi_sensors = [s for s in water_sensors if 'Mithi' in s['river_or_drain']]
    
    status = {
        "river_name": "Mithi River",
        "segments": [],
        "overall_status": "Normal",
        "alert_count": 0
    }
    
    for sensor in mithi_sensors:
        is_alert = sensor['water_level_cm'] > sensor['alert_threshold']
        if is_alert:
            status['alert_count'] += 1
            status['overall_status'] = "Alert"
        
        status['segments'].append({
            "location": sensor['location'],
            "water_level_cm": sensor['water_level_cm'],
            "threshold_cm": sensor['alert_threshold'],
            "is_alert": is_alert,
            "overflow_cm": max(0, sensor['water_level_cm'] - sensor['alert_threshold'])
        })
    
    return status


@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """Get summary for main dashboard"""
    if not data_loader:
        return {"error": "Data not loaded"}
    
    wards = data_loader.get_all_wards()
    risk_scores = data_loader.get_risk_scores()
    
    # Calculate statistics
    total_population = sum(w['population'] for w in wards)
    high_risk_wards = [r for r in risk_scores if r['composite_risk'] > 0.6]
    severe_wards = [r for r in risk_scores if r['severity_level'] == 'Severe']
    
    return {
        "total_wards": len(wards),
        "total_population": total_population,
        "high_risk_wards": len(high_risk_wards),
        "severe_wards": len(severe_wards),
        "active_sensors": {
            "rain": len(data_loader.get_rain_sensors()),
            "water": len(data_loader.get_water_sensors()),
            "traffic": len(data_loader.get_traffic_sensors()),
            "power": len(data_loader.get_power_load())
        },
        "mithi_river_status": (await get_mithi_river_status())['overall_status']
    }



# ==================== SPATIAL GRID ENDPOINTS ====================

class SpatialGridRequest(BaseModel):
    ward_id: str
    disaster_type: str = "flood"  # flood, fire, contamination


@router.get("/spatial/grid/{ward_id}")
async def get_spatial_grid(ward_id: str):
    """Get 20x20 spatial grid for a specific ward"""
    if not data_loader:
        raise HTTPException(status_code=503, detail="Mumbai data not loaded")
    
    ward = data_loader.get_ward(ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail=f"Ward {ward_id} not found")
    
    # Generate 20x20 grid with realistic data
    import random
    grid = []
    
    for y in range(20):
        row = []
        for x in range(20):
            # Generate cell data
            elevation = 5 + random.random() * 45  # 5-50m
            is_low_lying = elevation < 15
            near_river = 8 < y < 12  # Middle rows = Mithi River
            
            cell = {
                "x": x,
                "y": y,
                "elevation": round(elevation, 2),
                "population": random.randint(100, 900),
                "infrastructure": random.choice([None, None, None, None, None, None, None, None, None, 
                                                "hospital", "school", "power", "water", "fire_station"]),
                "flood_level": round((random.random() * 0.3 if (is_low_lying or near_river) else 0), 2),
                "fire_intensity": 0,
                "contamination": 0,
                "evacuated": False,
                "damaged": False
            }
            row.append(cell)
        grid.append(row)
    
    # Add disaster hotspots based on ward risk
    risk = data_loader.get_ward_risk(ward_id)
    if risk and risk['composite_risk'] > 0.6:
        hotspots = int(risk['composite_risk'] * 5)
        for _ in range(hotspots):
            x = random.randint(0, 19)
            y = random.randint(0, 19)
            grid[y][x]['flood_level'] = round(0.5 + random.random() * 0.5, 2)
    
    return {
        "ward_id": ward_id,
        "ward_name": ward['ward_name'],
        "grid_size": 20,
        "grid": grid,
        "metadata": {
            "population": ward['population'],
            "risk_score": risk['composite_risk'] if risk else 0,
            "severity_level": risk['severity_level'] if risk else 'Low'
        }
    }


@router.post("/spatial/simulate")
async def simulate_spatial_disaster(request: SpatialGridRequest):
    """Simulate disaster spread on spatial grid"""
    if not data_loader:
        raise HTTPException(status_code=503, detail="Mumbai data not loaded")
    
    ward = data_loader.get_ward(request.ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail=f"Ward {request.ward_id} not found")
    
    # Get grid
    grid_response = await get_spatial_grid(request.ward_id)
    grid = grid_response['grid']
    
    # Simulate disaster spread (simplified)
    import random
    steps = []
    
    for step in range(10):  # 10 simulation steps
        affected = 0
        casualties = 0
        evacuated = 0
        damaged = 0
        
        for y in range(20):
            for x in range(20):
                cell = grid[y][x]
                
                # Spread disaster
                if request.disaster_type == 'flood':
                    if cell['flood_level'] > 0.1:
                        # Spread to neighbors
                        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 20 and 0 <= ny < 20:
                                neighbor = grid[ny][nx]
                                if neighbor['elevation'] < cell['elevation']:
                                    neighbor['flood_level'] = min(1, neighbor['flood_level'] + 0.2)
                        cell['flood_level'] = max(0, cell['flood_level'] - 0.02)
                
                # Calculate impacts
                disaster_level = cell.get(f"{request.disaster_type}_level", 0) if request.disaster_type == 'flood' else \
                                cell.get(f"{request.disaster_type}_intensity", 0) if request.disaster_type == 'fire' else \
                                cell.get(request.disaster_type, 0)
                
                if disaster_level > 0.3:
                    affected += 1
                    casualties += int(cell['population'] * disaster_level * 0.05)
                
                if disaster_level > 0.6 and not cell['evacuated']:
                    cell['evacuated'] = True
                    evacuated += cell['population']
                
                if disaster_level > 0.7 and cell['infrastructure'] and not cell['damaged']:
                    cell['damaged'] = True
                    damaged += 1
        
        steps.append({
            "step": step,
            "affected_cells": affected,
            "casualties": casualties,
            "evacuated": evacuated,
            "infrastructure_damaged": damaged
        })
    
    return {
        "ward_id": request.ward_id,
        "ward_name": ward['ward_name'],
        "disaster_type": request.disaster_type,
        "simulation_steps": steps,
        "final_grid": grid
    }


@router.get("/spatial/disasters/{ward_id}")
async def get_ward_disasters(ward_id: str):
    """Get current disaster states for a ward"""
    if not data_loader:
        raise HTTPException(status_code=503, detail="Mumbai data not loaded")
    
    ward = data_loader.get_ward(ward_id)
    if not ward:
        raise HTTPException(status_code=404, detail=f"Ward {ward_id} not found")
    
    risk = data_loader.get_ward_risk(ward_id)
    
    # Get sensor data
    rain_sensors = [s for s in data_loader.get_rain_sensors() if s.get('ward_id') == ward_id]
    water_sensors = data_loader.get_water_sensors()  # Water sensors don't have ward_id, use all
    
    # Calculate disaster probabilities
    avg_rainfall = sum(s['rainfall_mm'] for s in rain_sensors) / len(rain_sensors) if rain_sensors else 0
    avg_water_level = sum(s['water_level_cm'] for s in water_sensors) / len(water_sensors) if water_sensors else 0
    
    flood_probability = min((avg_rainfall / 500 + avg_water_level / 300) / 2, 1.0)
    fire_probability = 0.1 if avg_rainfall < 10 else 0.02  # Low rainfall = higher fire risk
    contamination_probability = 0.15 if flood_probability > 0.6 else 0.05
    
    return {
        "ward_id": ward_id,
        "ward_name": ward['ward_name'],
        "disasters": {
            "flood": {
                "probability": round(flood_probability, 2),
                "severity": "High" if flood_probability > 0.7 else "Moderate" if flood_probability > 0.4 else "Low",
                "factors": {
                    "rainfall_mm": round(avg_rainfall, 1),
                    "water_level_cm": round(avg_water_level, 1)
                }
            },
            "fire": {
                "probability": round(fire_probability, 2),
                "severity": "High" if fire_probability > 0.7 else "Moderate" if fire_probability > 0.4 else "Low",
                "factors": {
                    "dry_conditions": avg_rainfall < 10
                }
            },
            "contamination": {
                "probability": round(contamination_probability, 2),
                "severity": "High" if contamination_probability > 0.7 else "Moderate" if contamination_probability > 0.4 else "Low",
                "factors": {
                    "flood_related": flood_probability > 0.6
                }
            }
        },
        "overall_risk": risk['composite_risk'] if risk else 0
    }
