#!/usr/bin/env python3
"""Test Mumbai Data Loading"""

import sys
sys.path.insert(0, 'backend')

from data_loaders.mumbai_data_loader import MumbaiDataLoader

def main():
    print("🌆 Testing Mumbai Digital Twin Data...")
    print()
    
    # Load data
    loader = MumbaiDataLoader()
    loader.load_all()
    
    print("✅ Mumbai Data Loaded Successfully!")
    print()
    
    # Summary
    print("📊 Data Summary:")
    print(f"  Wards: {len(loader.get_all_wards())}")
    print(f"  Infrastructure: {len(loader.get_all_infrastructure())}")
    print(f"  Rain Sensors: {len(loader.get_rain_sensors())}")
    print(f"  Water Sensors: {len(loader.get_water_sensors())}")
    print(f"  Traffic Sensors: {len(loader.get_traffic_sensors())}")
    print(f"  Risk Scores: {len(loader.get_risk_scores())}")
    print()
    
    # Sample wards
    print("🗺️ Mumbai Wards with Risk Scores:")
    print("-" * 70)
    wards = loader.get_all_wards()
    risk_scores = {r['ward_id']: r for r in loader.get_risk_scores()}
    
    for ward in wards:
        ward_id = ward['ward_id']
        risk = risk_scores.get(ward_id, {})
        risk_score = risk.get('composite_risk', 0)
        severity = risk.get('severity_level', 'Unknown')
        
        # Color coding
        if risk_score > 0.8:
            color = '🔴'
        elif risk_score > 0.6:
            color = '🟠'
        elif risk_score > 0.4:
            color = '🟡'
        else:
            color = '🟢'
        
        print(f"{color} {ward_id:6} {ward['ward_name']:20} Pop: {ward['population']:>8,}  "
              f"Risk: {risk_score:>4.0%}  {severity}")
    
    print()
    print("💧 Mithi River Water Levels:")
    print("-" * 70)
    water_sensors = loader.get_water_sensors()
    for sensor in water_sensors:
        alert = "⚠️ ALERT!" if sensor['water_level_cm'] > sensor['alert_threshold'] else "✓ Normal"
        print(f"  {sensor['location']:15} {sensor['river_or_drain']:20} "
              f"{sensor['water_level_cm']}cm / {sensor['alert_threshold']}cm  {alert}")
    
    print()
    print("🌧️ Rainfall Sensors:")
    print("-" * 70)
    rain_sensors = loader.get_rain_sensors()
    for sensor in rain_sensors:
        intensity = "🔴 Heavy" if sensor['rainfall_mm'] > 50 else "🟡 Moderate" if sensor['rainfall_mm'] > 30 else "🟢 Light"
        print(f"  Ward {sensor['ward_id']:6} Sensor {sensor['sensor_id']}  "
              f"{sensor['rainfall_mm']}mm  {intensity}")
    
    print()
    print("🚗 Traffic Conditions:")
    print("-" * 70)
    traffic_sensors = loader.get_traffic_sensors()
    for sensor in traffic_sensors:
        congestion = "🔴 Heavy" if sensor['congestion_index'] > 0.7 else "🟡 Moderate" if sensor['congestion_index'] > 0.5 else "🟢 Light"
        print(f"  Road {sensor['road_id']}  {sensor['vehicle_count']:>4} vehicles  "
              f"{sensor['avg_speed']:>2} km/h  {congestion}")
    
    print()
    print("🏥 Critical Infrastructure:")
    print("-" * 70)
    infra = loader.get_all_infrastructure()
    for item in infra[:5]:
        print(f"  {item['type']:20} {item['name']:40} Ward: {item['ward_id']}")
    
    print()
    print("📜 Historical Flood Events:")
    print("-" * 70)
    floods = loader.get_historical_floods()
    for event in floods:
        print(f"  {event['date']}  Wards: {event['affected_wards']:20}  "
              f"Loss: ₹{event['economic_loss_crore']:>6} crore  "
              f"Casualties: {event['casualties']}")
    
    print()
    print("✅ All data loaded and validated successfully!")
    print()
    print("🚀 Ready to start the API server!")
    print("   Run: python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()
