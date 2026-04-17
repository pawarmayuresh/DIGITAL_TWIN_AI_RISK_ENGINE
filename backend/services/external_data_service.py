"""
External Data Integration Service
Fetches real-time data from external APIs
"""
import os
import requests
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import json


class ExternalDataIntegrator:
    """Integrates external data sources for real-time disaster monitoring"""
    
    def __init__(self):
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        self.weather_base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def fetch_weather_data(self, ward_id: str, lat: float = 19.0760, lon: float = 72.8777) -> Dict[str, Any]:
        """Fetch real-time weather data for Mumbai ward"""
        cache_key = f"weather_{ward_id}"
        
        # Check cache
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            # Try real API call
            url = f"{self.weather_base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'rainfall': data.get('rain', {}).get('1h', 0),
                    'weather_condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'timestamp': datetime.now().isoformat(),
                    'source': 'OpenWeatherMap'
                }
                
                self._cache_data(cache_key, weather_data)
                return weather_data
        except Exception as e:
            print(f"Weather API error: {e}")
        
        # Fallback to simulated data
        return self._generate_simulated_weather(ward_id)
    
    def fetch_traffic_data(self, ward_id: str) -> Dict[str, Any]:
        """Fetch real-time traffic data"""
        cache_key = f"traffic_{ward_id}"
        
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        # Simulated traffic data with realistic time-based patterns
        import random
        
        hour = datetime.now().hour
        day_of_week = datetime.now().weekday()
        high_traffic_wards = ['Kurla', 'Andheri', 'Bandra', 'Dadar']
        
        # Base congestion by time of day
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            base_congestion = 'high'
            speed_factor = 0.4
        elif 11 <= hour <= 16:
            base_congestion = 'moderate'
            speed_factor = 0.6
        elif 21 <= hour <= 23:
            base_congestion = 'moderate'
            speed_factor = 0.7
        else:
            base_congestion = 'low'
            speed_factor = 0.9
        
        # Weekend adjustment
        if day_of_week >= 5:
            if base_congestion == 'high':
                base_congestion = 'moderate'
            speed_factor += 0.1
        
        # Ward-specific adjustment
        if ward_id in high_traffic_wards:
            congestion_levels = ['moderate', 'high', 'severe']
            base_congestion = random.choice(congestion_levels) if base_congestion != 'low' else 'moderate'
            speed_factor *= 0.8
        
        avg_speed = 50 * speed_factor + random.uniform(-5, 5)
        incidents = random.randint(0, 3) if base_congestion in ['high', 'severe'] else random.randint(0, 1)
        
        traffic_data = {
            'congestion_level': base_congestion,
            'average_speed': round(max(5, avg_speed), 1),
            'incidents': incidents,
            'road_closures': random.randint(0, 1) if base_congestion == 'severe' else 0,
            'estimated_delay': round(random.uniform(5, 30) if base_congestion in ['high', 'severe'] else random.uniform(0, 10), 1),
            'timestamp': datetime.now().isoformat(),
            'source': 'Simulated'
        }
        
        self._cache_data(cache_key, traffic_data)
        return traffic_data
    
    def fetch_social_sentiment(self, ward_id: str, keyword: str = "disaster") -> Dict[str, Any]:
        """Fetch social media sentiment analysis"""
        cache_key = f"sentiment_{ward_id}_{keyword}"
        
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        # Simulated sentiment data (can be replaced with Twitter API)
        import random
        
        sentiment_data = {
            'panic_level': random.uniform(0, 1),
            'positive_mentions': random.randint(10, 100),
            'negative_mentions': random.randint(5, 80),
            'neutral_mentions': random.randint(20, 150),
            'trending_topics': ['flood', 'evacuation', 'safety', 'rescue'],
            'sentiment_score': random.uniform(-1, 1),  # -1 (negative) to 1 (positive)
            'timestamp': datetime.now().isoformat(),
            'source': 'Simulated'
        }
        
        self._cache_data(cache_key, sentiment_data)
        return sentiment_data
    
    def fetch_iot_sensor_data(self, ward_id: str) -> Dict[str, Any]:
        """Fetch IoT sensor data"""
        cache_key = f"iot_{ward_id}"
        
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        import random
        
        sensor_data = {
            'water_level_sensors': [
                {
                    'sensor_id': f'WL_{i}',
                    'location': f'Location_{i}',
                    'water_level_cm': random.uniform(0, 200),
                    'status': random.choice(['normal', 'warning', 'critical'])
                }
                for i in range(3)
            ],
            'rain_gauges': [
                {
                    'sensor_id': f'RG_{i}',
                    'location': f'Location_{i}',
                    'rainfall_mm': random.uniform(0, 50),
                    'intensity': random.choice(['light', 'moderate', 'heavy'])
                }
                for i in range(3)
            ],
            'seismic_sensors': [
                {
                    'sensor_id': f'SS_{i}',
                    'location': f'Location_{i}',
                    'magnitude': random.uniform(0, 3),
                    'status': 'normal'
                }
                for i in range(2)
            ],
            'timestamp': datetime.now().isoformat(),
            'source': 'Simulated IoT Network'
        }
        
        self._cache_data(cache_key, sensor_data)
        return sensor_data
    
    def get_integrated_risk_assessment(self, ward_id: str) -> Dict[str, Any]:
        """Combine all external data sources for comprehensive risk assessment"""
        weather = self.fetch_weather_data(ward_id)
        traffic = self.fetch_traffic_data(ward_id)
        sentiment = self.fetch_social_sentiment(ward_id)
        iot = self.fetch_iot_sensor_data(ward_id)
        
        # Calculate integrated risk score
        risk_factors = {
            'weather_risk': self._calculate_weather_risk(weather),
            'traffic_risk': self._calculate_traffic_risk(traffic),
            'social_risk': sentiment['panic_level'],
            'sensor_risk': self._calculate_sensor_risk(iot)
        }
        
        overall_risk = sum(risk_factors.values()) / len(risk_factors)
        
        return {
            'ward_id': ward_id,
            'overall_risk_score': overall_risk,
            'risk_factors': risk_factors,
            'weather': weather,
            'traffic': traffic,
            'sentiment': sentiment,
            'iot_sensors': iot,
            'timestamp': datetime.now().isoformat(),
            'recommendation': self._generate_recommendation(overall_risk)
        }
    
    def _calculate_weather_risk(self, weather: Dict) -> float:
        """Calculate risk from weather data"""
        risk = 0.0
        
        # High rainfall increases risk
        if weather['rainfall'] > 50:
            risk += 0.8
        elif weather['rainfall'] > 20:
            risk += 0.5
        elif weather['rainfall'] > 10:
            risk += 0.3
        
        # High wind speed increases risk
        if weather['wind_speed'] > 50:
            risk += 0.3
        elif weather['wind_speed'] > 30:
            risk += 0.2
        
        return min(risk, 1.0)
    
    def _calculate_traffic_risk(self, traffic: Dict) -> float:
        """Calculate risk from traffic data"""
        congestion_map = {
            'low': 0.1,
            'moderate': 0.3,
            'high': 0.6,
            'severe': 0.9
        }
        
        base_risk = congestion_map.get(traffic['congestion_level'], 0.5)
        incident_risk = min(traffic['incidents'] * 0.1, 0.3)
        
        return min(base_risk + incident_risk, 1.0)
    
    def _calculate_sensor_risk(self, iot: Dict) -> float:
        """Calculate risk from IoT sensor data"""
        risk = 0.0
        
        # Check water level sensors
        critical_water = sum(1 for s in iot['water_level_sensors'] if s['status'] == 'critical')
        risk += critical_water * 0.3
        
        # Check rain gauges
        heavy_rain = sum(1 for s in iot['rain_gauges'] if s['intensity'] == 'heavy')
        risk += heavy_rain * 0.2
        
        return min(risk, 1.0)
    
    def _generate_recommendation(self, risk_score: float) -> str:
        """Generate recommendation based on risk score"""
        if risk_score > 0.8:
            return "CRITICAL: Immediate evacuation recommended"
        elif risk_score > 0.6:
            return "HIGH: Prepare for evacuation, monitor situation"
        elif risk_score > 0.4:
            return "MODERATE: Stay alert, avoid unnecessary travel"
        elif risk_score > 0.2:
            return "LOW: Normal precautions advised"
        else:
            return "MINIMAL: No immediate action required"
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is in cache and still valid"""
        if key not in self.cache:
            return False
        
        cache_time = self.cache[key]['timestamp']
        age = (datetime.now() - cache_time).total_seconds()
        
        return age < self.cache_duration
    
    def _cache_data(self, key: str, data: Dict):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def _generate_simulated_weather(self, ward_id: str) -> Dict[str, Any]:
        """Generate simulated weather data as fallback"""
        import random
        import numpy as np
        
        # Ward-specific and time-based patterns
        coastal_wards = ['Colaba', 'Worli', 'Bandra']
        hour = datetime.now().hour
        is_monsoon = datetime.now().month in [6, 7, 8, 9]
        
        # Temperature varies by time of day
        base_temp = 25 + 5 * np.sin((hour - 6) * np.pi / 12)
        temp_variation = -2 if ward_id in coastal_wards else random.uniform(-2, 3)
        temperature = base_temp + temp_variation
        
        # Humidity patterns
        humidity = 70 + 10 * np.sin((hour - 6) * np.pi / 12)
        humidity += 10 if ward_id in coastal_wards else 0
        humidity += random.uniform(-5, 10)
        
        # Rainfall with realistic patterns
        if is_monsoon:
            rainfall = random.gamma(2, 10) if random.random() > 0.5 else random.uniform(0, 5)
        else:
            rainfall = random.uniform(0, 15) if random.random() > 0.85 else 0
        
        # Wind speed
        wind_speed = (15 if ward_id in coastal_wards else 10) + random.uniform(-5, 8)
        
        # Determine condition
        if rainfall > 50:
            condition = 'Thunderstorm'
        elif rainfall > 20:
            condition = 'Rain'
        elif rainfall > 5:
            condition = 'Drizzle'
        elif humidity > 85:
            condition = 'Clouds'
        else:
            condition = 'Clear'
        
        return {
            'temperature': round(temperature, 1),
            'humidity': round(min(100, max(40, humidity)), 1),
            'pressure': round(1013 + random.uniform(-5, 5), 1),
            'wind_speed': round(max(0, wind_speed), 1),
            'rainfall': round(rainfall, 1),
            'weather_condition': condition,
            'description': f'Simulated {condition.lower()} conditions',
            'timestamp': datetime.now().isoformat(),
            'source': 'Simulated'
        }
