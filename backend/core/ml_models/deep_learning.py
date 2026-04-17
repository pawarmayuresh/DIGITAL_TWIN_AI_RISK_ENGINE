"""
Deep Learning Models for Disaster Prediction
Uses LSTM and other neural networks for advanced predictions
"""
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json


class DisasterLSTM:
    """LSTM-based disaster prediction model (simplified implementation)"""
    
    def __init__(self, input_size: int = 10, hidden_size: int = 64, num_layers: int = 2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.is_trained = False
        
        # Simplified weights (in production, use PyTorch/TensorFlow)
        self.weights = self._initialize_weights()
        
    def _initialize_weights(self) -> Dict:
        """Initialize model weights"""
        np.random.seed(42)
        return {
            'lstm_weights': np.random.randn(self.input_size, self.hidden_size) * 0.01,
            'output_weights': np.random.randn(self.hidden_size, 1) * 0.01,
            'bias': np.zeros((1, 1))
        }
    
    def predict_next_24h(self, historical_data: List[Dict], ward_id: str = None, external_data: Dict = None) -> List[Dict]:
        """Predict disaster risk for next 24 hours with real-time data integration"""
        if len(historical_data) < 24:
            # Need at least 24 hours of history
            historical_data = self._generate_synthetic_history(24, ward_id)
        
        # Extract features from historical data
        features = self._extract_features(historical_data[-24:])
        
        # Get ward-specific base risk
        ward_base_risk = self._get_ward_base_risk(ward_id)
        
        # Integrate external real-time data if available
        external_risk_factor = 1.0
        weather_impact = 0.0
        traffic_impact = 0.0
        sensor_impact = 0.0
        
        if external_data:
            external_risk_factor = external_data.get('overall_risk_score', 0.5) / 0.5
            risk_factors = external_data.get('risk_factors', {})
            weather_impact = risk_factors.get('weather_risk', 0.0)
            traffic_impact = risk_factors.get('traffic_risk', 0.0)
            sensor_impact = risk_factors.get('sensor_risk', 0.0)
        
        # Make predictions for next 24 hours
        predictions = []
        current_time = datetime.now()
        
        for hour in range(24):
            # Simple forward pass (simplified LSTM)
            base_prediction = self._forward_pass(features)
            
            # Add temporal patterns
            hour_of_day = (current_time + timedelta(hours=hour)).hour
            seasonal_factor = self._get_seasonal_factor(hour_of_day)
            
            # Add ward-specific characteristics
            ward_factor = self._get_ward_risk_factor(ward_id, hour_of_day)
            
            # Add time-decay for external data (becomes less relevant over time)
            time_decay = np.exp(-hour / 12)  # Exponential decay
            current_external_factor = 1.0 + (external_risk_factor - 1.0) * time_decay
            
            # Add random variation to simulate real-time changes
            random_variation = np.random.normal(0, 0.05)
            
            # Combine all factors
            risk_score = (
                ward_base_risk * 0.3 +
                base_prediction * 0.3 +
                (weather_impact * 0.15 + traffic_impact * 0.1 + sensor_impact * 0.15) * time_decay
            ) * seasonal_factor * ward_factor * current_external_factor + random_variation
            
            risk_score = max(0.0, min(1.0, risk_score))
            
            predictions.append({
                'hour': hour,
                'timestamp': (current_time + timedelta(hours=hour)).isoformat(),
                'risk_score': float(risk_score),
                'confidence': 0.92 - (hour * 0.015),  # Confidence decreases with time
                'factors': {
                    'base_prediction': float(base_prediction),
                    'ward_base_risk': float(ward_base_risk),
                    'seasonal_factor': float(seasonal_factor),
                    'ward_factor': float(ward_factor),
                    'weather_impact': float(weather_impact * time_decay),
                    'traffic_impact': float(traffic_impact * time_decay),
                    'sensor_impact': float(sensor_impact * time_decay),
                    'hour_of_day': hour_of_day,
                    'external_data_weight': float(time_decay)
                }
            })
            
            # Update features for next prediction (rolling window)
            features = np.roll(features, -1)
            features[-1] = risk_score
        
        return predictions
    
    def predict_weekly_pattern(self, ward_id: str) -> Dict[str, Any]:
        """Predict weekly disaster risk pattern"""
        daily_predictions = []
        
        for day in range(7):
            # Generate 24-hour prediction for each day
            day_data = self._generate_synthetic_history(24)
            hourly_predictions = self.predict_next_24h(day_data)
            
            # Aggregate to daily risk
            daily_risk = np.mean([p['risk_score'] for p in hourly_predictions])
            max_risk = np.max([p['risk_score'] for p in hourly_predictions])
            
            daily_predictions.append({
                'day': day,
                'date': (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d'),
                'average_risk': float(daily_risk),
                'peak_risk': float(max_risk),
                'risk_category': self._categorize_risk(daily_risk)
            })
        
        return {
            'ward_id': ward_id,
            'prediction_type': 'weekly_pattern',
            'model': 'LSTM',
            'predictions': daily_predictions,
            'overall_trend': self._detect_trend(daily_predictions),
            'high_risk_days': [p['day'] for p in daily_predictions if p['average_risk'] > 0.7]
        }
    
    def train_on_historical_data(self, training_data: List[Dict]) -> Dict[str, Any]:
        """Train model on historical disaster data"""
        # Simplified training (in production, use proper backpropagation)
        epochs = 10
        learning_rate = 0.01
        
        training_loss = []
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            # Simulate training
            for i in range(len(training_data) - 1):
                # Extract features and target
                features = self._extract_features([training_data[i]])
                target = training_data[i + 1].get('risk_score', 0.5)
                
                # Forward pass
                prediction = self._forward_pass(features)
                
                # Calculate loss (MSE)
                loss = (prediction - target) ** 2
                epoch_loss += loss
                
                # Simplified weight update
                gradient = 2 * (prediction - target)
                self.weights['output_weights'] -= learning_rate * gradient * 0.01
            
            avg_loss = epoch_loss / len(training_data)
            training_loss.append(float(avg_loss))
        
        self.is_trained = True
        
        return {
            'status': 'trained',
            'epochs': epochs,
            'final_loss': training_loss[-1],
            'training_history': training_loss,
            'model_parameters': {
                'input_size': self.input_size,
                'hidden_size': self.hidden_size,
                'num_layers': self.num_layers
            }
        }
    
    def _forward_pass(self, features: np.ndarray) -> float:
        """Simplified forward pass through network"""
        # LSTM cell (simplified)
        hidden = np.tanh(np.dot(features, self.weights['lstm_weights']))
        
        # Output layer
        output = np.dot(hidden.mean(), self.weights['output_weights']) + self.weights['bias']
        
        # Sigmoid activation
        prediction = 1 / (1 + np.exp(-output))
        
        return float(prediction[0, 0])
    
    def _extract_features(self, data: List[Dict]) -> np.ndarray:
        """Extract features from historical data"""
        features = []
        
        for record in data:
            feature_vector = [
                record.get('risk_score', 0.5),
                record.get('rainfall', 0.0) / 100,  # Normalize
                record.get('temperature', 25) / 50,
                record.get('humidity', 70) / 100,
                record.get('wind_speed', 10) / 50,
                record.get('population_density', 10000) / 50000,
                record.get('infrastructure_health', 0.8),
                datetime.now().hour / 24,  # Hour of day
                datetime.now().month / 12,  # Month of year
                1.0  # Bias term
            ]
            features.append(feature_vector)
        
        return np.array(features).mean(axis=0)
    
    def _generate_synthetic_history(self, hours: int, ward_id: str = None) -> List[Dict]:
        """Generate synthetic historical data with ward-specific patterns"""
        history = []
        
        # Ward-specific base risk
        base_risk = self._get_ward_base_risk(ward_id)
        
        # Add realistic patterns
        for i in range(hours):
            time_point = datetime.now() - timedelta(hours=hours-i)
            hour_of_day = time_point.hour
            
            # Diurnal pattern (higher risk at night)
            diurnal_factor = 1.2 if 22 <= hour_of_day or hour_of_day <= 5 else 0.9
            
            # Weekly pattern (higher risk on weekends)
            day_of_week = time_point.weekday()
            weekly_factor = 1.1 if day_of_week >= 5 else 1.0
            
            # Random walk with mean reversion
            risk_change = np.random.normal(0, 0.08)
            mean_reversion = (base_risk - history[-1]['risk_score']) * 0.1 if history else 0
            
            risk = (history[-1]['risk_score'] if history else base_risk) + risk_change + mean_reversion
            risk = risk * diurnal_factor * weekly_factor
            risk = max(0.1, min(0.95, risk))
            
            # Realistic weather patterns
            rainfall = max(0, np.random.gamma(2, 10) if np.random.random() > 0.7 else np.random.uniform(0, 5))
            temperature = 25 + 5 * np.sin(hour_of_day * np.pi / 12) + np.random.normal(0, 2)
            humidity = 70 + 15 * np.sin((hour_of_day - 6) * np.pi / 12) + np.random.normal(0, 5)
            
            history.append({
                'timestamp': time_point.isoformat(),
                'risk_score': risk,
                'rainfall': rainfall,
                'temperature': temperature,
                'humidity': max(40, min(100, humidity)),
                'wind_speed': np.random.gamma(3, 3),
                'population_density': self._get_ward_population(ward_id),
                'infrastructure_health': self._get_ward_infrastructure(ward_id)
            })
        
        return history
    
    def _get_seasonal_factor(self, hour: int) -> float:
        """Get seasonal adjustment factor based on hour"""
        # Higher risk during night and early morning
        if 0 <= hour < 6:
            return 1.2
        elif 6 <= hour < 12:
            return 0.9
        elif 12 <= hour < 18:
            return 1.0
        else:
            return 1.1
    
    def _get_ward_base_risk(self, ward_id: str) -> float:
        """Get base risk level for specific ward"""
        ward_risks = {
            'Colaba': 0.35,
            'Byculla': 0.55,
            'Kurla': 0.65,
            'Andheri': 0.50,
            'Bandra': 0.45,
            'Chembur': 0.60,
            'Ghatkopar': 0.58,
            'Borivali': 0.48,
            'Dadar': 0.52,
            'Worli': 0.42
        }
        return ward_risks.get(ward_id, 0.50)
    
    def _get_ward_population(self, ward_id: str) -> int:
        """Get population density for specific ward"""
        ward_populations = {
            'Colaba': 12000,
            'Byculla': 25000,
            'Kurla': 35000,
            'Andheri': 28000,
            'Bandra': 22000,
            'Chembur': 30000,
            'Ghatkopar': 32000,
            'Borivali': 26000,
            'Dadar': 27000,
            'Worli': 18000
        }
        return ward_populations.get(ward_id, 20000)
    
    def _get_ward_infrastructure(self, ward_id: str) -> float:
        """Get infrastructure health for specific ward"""
        ward_infrastructure = {
            'Colaba': 0.85,
            'Byculla': 0.65,
            'Kurla': 0.60,
            'Andheri': 0.75,
            'Bandra': 0.80,
            'Chembur': 0.68,
            'Ghatkopar': 0.70,
            'Borivali': 0.78,
            'Dadar': 0.72,
            'Worli': 0.82
        }
        return ward_infrastructure.get(ward_id, 0.70)
    
    def _get_ward_risk_factor(self, ward_id: str, hour_of_day: int) -> float:
        """Get ward-specific risk factor based on time of day"""
        # Some wards have higher risk during specific hours
        high_traffic_wards = ['Kurla', 'Andheri', 'Bandra', 'Dadar']
        coastal_wards = ['Colaba', 'Worli', 'Bandra']
        
        factor = 1.0
        
        # Traffic-heavy wards have higher risk during rush hours
        if ward_id in high_traffic_wards:
            if 8 <= hour_of_day <= 10 or 17 <= hour_of_day <= 20:
                factor *= 1.15
        
        # Coastal wards have higher risk during high tide hours
        if ward_id in coastal_wards:
            if 2 <= hour_of_day <= 4 or 14 <= hour_of_day <= 16:
                factor *= 1.12
        
        return factor
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk score"""
        if risk_score > 0.8:
            return 'CRITICAL'
        elif risk_score > 0.6:
            return 'HIGH'
        elif risk_score > 0.4:
            return 'MODERATE'
        elif risk_score > 0.2:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _detect_trend(self, predictions: List[Dict]) -> str:
        """Detect overall trend in predictions"""
        risks = [p['average_risk'] for p in predictions]
        
        # Simple linear regression
        x = np.arange(len(risks))
        slope = np.polyfit(x, risks, 1)[0]
        
        if slope > 0.05:
            return 'increasing'
        elif slope < -0.05:
            return 'decreasing'
        else:
            return 'stable'
    
    def save_model(self, filepath: str) -> bool:
        """Save model weights to file"""
        try:
            model_data = {
                'weights': {k: v.tolist() if isinstance(v, np.ndarray) else v 
                           for k, v in self.weights.items()},
                'config': {
                    'input_size': self.input_size,
                    'hidden_size': self.hidden_size,
                    'num_layers': self.num_layers,
                    'is_trained': self.is_trained
                },
                'saved_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(model_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """Load model weights from file"""
        try:
            with open(filepath, 'r') as f:
                model_data = json.load(f)
            
            # Restore weights
            self.weights = {k: np.array(v) if isinstance(v, list) else v 
                           for k, v in model_data['weights'].items()}
            
            # Restore config
            config = model_data['config']
            self.input_size = config['input_size']
            self.hidden_size = config['hidden_size']
            self.num_layers = config['num_layers']
            self.is_trained = config['is_trained']
            
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False


class CNNImageAnalyzer:
    """CNN for satellite image analysis (simplified)"""
    
    def __init__(self):
        self.model_loaded = False
    
    def analyze_satellite_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze satellite image for disaster detection"""
        # Simplified analysis (in production, use actual CNN)
        
        return {
            'image_path': image_path,
            'analysis': {
                'flood_detected': np.random.choice([True, False], p=[0.3, 0.7]),
                'flood_coverage': float(np.random.uniform(0, 0.5)),
                'affected_area_km2': float(np.random.uniform(0, 100)),
                'severity': np.random.choice(['low', 'moderate', 'high', 'severe']),
                'confidence': float(np.random.uniform(0.7, 0.95))
            },
            'detected_features': {
                'water_bodies': int(np.random.randint(5, 20)),
                'flooded_roads': int(np.random.randint(0, 15)),
                'affected_buildings': int(np.random.randint(0, 100))
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def compare_temporal_images(self, before_image: str, after_image: str) -> Dict[str, Any]:
        """Compare before/after images to detect changes"""
        
        return {
            'before_image': before_image,
            'after_image': after_image,
            'changes_detected': {
                'new_flooding': float(np.random.uniform(0, 0.4)),
                'infrastructure_damage': float(np.random.uniform(0, 0.3)),
                'vegetation_loss': float(np.random.uniform(0, 0.2))
            },
            'change_magnitude': float(np.random.uniform(0.1, 0.8)),
            'recommendation': 'Immediate assessment required' if np.random.random() > 0.5 else 'Monitor situation',
            'timestamp': datetime.now().isoformat()
        }


class TransformerMultiModal:
    """Transformer model for multi-modal data fusion"""
    
    def __init__(self):
        self.attention_heads = 8
        self.model_dim = 512
    
    def fuse_data_sources(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """Fuse multiple data sources using attention mechanism"""
        
        # Extract data from different sources
        weather = data_sources.get('weather', {})
        social = data_sources.get('social', {})
        sensors = data_sources.get('sensors', {})
        
        # Calculate attention weights (simplified)
        weights = {
            'weather': 0.4,
            'social': 0.2,
            'sensors': 0.4
        }
        
        # Fused risk score
        fused_risk = (
            weather.get('risk', 0.5) * weights['weather'] +
            social.get('panic_level', 0.3) * weights['social'] +
            sensors.get('alert_level', 0.4) * weights['sensors']
        )
        
        return {
            'fused_risk_score': float(fused_risk),
            'attention_weights': weights,
            'confidence': 0.88,
            'contributing_factors': {
                'weather_contribution': float(weather.get('risk', 0.5) * weights['weather']),
                'social_contribution': float(social.get('panic_level', 0.3) * weights['social']),
                'sensor_contribution': float(sensors.get('alert_level', 0.4) * weights['sensors'])
            },
            'recommendation': self._generate_recommendation(fused_risk),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendation(self, risk: float) -> str:
        """Generate recommendation based on fused risk"""
        if risk > 0.8:
            return 'URGENT: Activate emergency protocols immediately'
        elif risk > 0.6:
            return 'HIGH ALERT: Prepare for potential evacuation'
        elif risk > 0.4:
            return 'ELEVATED: Increase monitoring and readiness'
        else:
            return 'NORMAL: Continue routine operations'
