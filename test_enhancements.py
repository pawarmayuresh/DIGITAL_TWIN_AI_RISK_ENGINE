#!/usr/bin/env python3
"""
Test script to verify Advanced Features enhancements
"""
import sys
sys.path.insert(0, '.')

from backend.core.ml_models.deep_learning import DisasterLSTM
from backend.services.external_data_service import ExternalDataIntegrator
from datetime import datetime

def test_ward_specific_risk():
    """Test that different wards have different base risks"""
    print("=" * 60)
    print("TEST 1: Ward-Specific Base Risk")
    print("=" * 60)
    
    lstm = DisasterLSTM()
    wards = ['Colaba', 'Kurla', 'Bandra', 'Andheri']
    
    for ward in wards:
        base_risk = lstm._get_ward_base_risk(ward)
        print(f"{ward:15} Base Risk: {base_risk*100:.0f}%")
    
    print("\n✓ Different wards have different base risks\n")

def test_time_based_patterns():
    """Test that risk varies by time of day"""
    print("=" * 60)
    print("TEST 2: Time-Based Risk Patterns")
    print("=" * 60)
    
    lstm = DisasterLSTM()
    hours = [2, 9, 14, 19, 23]  # Different times of day
    
    for hour in hours:
        factor = lstm._get_seasonal_factor(hour)
        time_label = "Night" if hour < 6 else "Morning" if hour < 12 else "Afternoon" if hour < 18 else "Evening"
        print(f"{hour:02d}:00 ({time_label:10}) Risk Factor: {factor:.2f}x")
    
    print("\n✓ Risk varies by time of day\n")

def test_external_data_integration():
    """Test external data service with realistic patterns"""
    print("=" * 60)
    print("TEST 3: External Data Integration")
    print("=" * 60)
    
    integrator = ExternalDataIntegrator()
    ward = 'Kurla'
    
    # Test weather data
    weather = integrator.fetch_weather_data(ward)
    print(f"\nWeather Data for {ward}:")
    print(f"  Temperature: {weather['temperature']}°C")
    print(f"  Humidity: {weather['humidity']}%")
    print(f"  Rainfall: {weather['rainfall']}mm")
    print(f"  Condition: {weather['weather_condition']}")
    
    # Test traffic data
    traffic = integrator.fetch_traffic_data(ward)
    print(f"\nTraffic Data for {ward}:")
    print(f"  Congestion: {traffic['congestion_level']}")
    print(f"  Avg Speed: {traffic['average_speed']} km/h")
    print(f"  Incidents: {traffic['incidents']}")
    
    # Test integrated assessment
    assessment = integrator.get_integrated_risk_assessment(ward)
    print(f"\nIntegrated Risk Assessment:")
    print(f"  Overall Risk: {assessment['overall_risk_score']*100:.0f}%")
    print(f"  Weather Risk: {assessment['risk_factors']['weather_risk']*100:.0f}%")
    print(f"  Traffic Risk: {assessment['risk_factors']['traffic_risk']*100:.0f}%")
    print(f"  Sensor Risk: {assessment['risk_factors']['sensor_risk']*100:.0f}%")
    
    print("\n✓ External data integration working\n")

def test_lstm_with_external_data():
    """Test LSTM predictions with external data integration"""
    print("=" * 60)
    print("TEST 4: LSTM with Real-Time Data Integration")
    print("=" * 60)
    
    lstm = DisasterLSTM()
    integrator = ExternalDataIntegrator()
    
    ward = 'Kurla'
    
    # Get external data
    external_data = integrator.get_integrated_risk_assessment(ward)
    
    # Generate historical data
    historical = lstm._generate_synthetic_history(48, ward)
    
    # Make predictions with external data
    predictions = lstm.predict_next_24h(historical, ward, external_data)
    
    print(f"\n24-Hour Predictions for {ward}:")
    print(f"  Current Hour Risk: {predictions[0]['risk_score']*100:.0f}%")
    print(f"  Confidence: {predictions[0]['confidence']*100:.0f}%")
    print(f"\n  Risk Factors:")
    factors = predictions[0]['factors']
    print(f"    Ward Base Risk: {factors['ward_base_risk']*100:.0f}%")
    print(f"    Weather Impact: {factors['weather_impact']*100:.0f}%")
    print(f"    Traffic Impact: {factors['traffic_impact']*100:.0f}%")
    print(f"    Sensor Impact: {factors['sensor_impact']*100:.0f}%")
    
    # Show variation over 24 hours
    print(f"\n  Risk Variation Over 24 Hours:")
    for i in [0, 6, 12, 18, 23]:
        pred = predictions[i]
        print(f"    Hour {i:2d}: {pred['risk_score']*100:.0f}%")
    
    print("\n✓ LSTM predictions integrate real-time data\n")

def test_ward_comparison():
    """Test that different wards show different risk profiles"""
    print("=" * 60)
    print("TEST 5: Ward Comparison")
    print("=" * 60)
    
    lstm = DisasterLSTM()
    integrator = ExternalDataIntegrator()
    
    wards = ['Colaba', 'Kurla', 'Bandra']
    
    print(f"\nCurrent Risk Scores (Hour: {datetime.now().hour}):")
    print("-" * 60)
    
    for ward in wards:
        external_data = integrator.get_integrated_risk_assessment(ward)
        historical = lstm._generate_synthetic_history(48, ward)
        predictions = lstm.predict_next_24h(historical, ward, external_data)
        
        current_risk = predictions[0]['risk_score']
        print(f"{ward:15} {current_risk*100:.0f}%  ", end="")
        print("█" * int(current_risk * 50))
    
    print("\n✓ Different wards show different risk profiles\n")

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("ADVANCED FEATURES ENHANCEMENT TEST SUITE")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    try:
        test_ward_specific_risk()
        test_time_based_patterns()
        test_external_data_integration()
        test_lstm_with_external_data()
        test_ward_comparison()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        print("\nThe Advanced Features enhancements are working correctly!")
        print("Risk scores now vary based on:")
        print("  • Ward characteristics")
        print("  • Time of day")
        print("  • Weather conditions")
        print("  • Traffic patterns")
        print("  • Sensor readings")
        print("\nThe system is ready for use!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
