"""
Mumbai Data Loader
Loads all CSV files for Mumbai Digital Twin
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional

class MumbaiDataLoader:
    """Load and manage Mumbai city data from CSV files"""
    
    def __init__(self, data_dir='data/mumbai'):
        self.data_dir = Path(data_dir)
        self.wards = None
        self.infrastructure = None
        self.road_nodes = None
        self.road_edges = None
        self.rainfall_history = None
        self.flood_events = None
        self.cyclone_history = None
        self.rain_sensors = None
        self.water_sensors = None
        self.traffic_sensors = None
        self.power_load = None
        self.alert_sensors = None
        self.risk_scores = None
        self.explainability = None
        self.recommendations = None
    
    def load_all(self):
        """Load all Mumbai datasets"""
        try:
            # Static data
            self.wards = pd.read_csv(self.data_dir / 'static/mumbai_wards.csv')
            self.infrastructure = pd.read_csv(self.data_dir / 'static/infrastructure_nodes.csv')
            self.road_nodes = pd.read_csv(self.data_dir / 'static/road_nodes.csv')
            self.road_edges = pd.read_csv(self.data_dir / 'static/road_network_edges.csv')
            
            # Historical data
            self.rainfall_history = pd.read_csv(self.data_dir / 'historical/rainfall_history.csv')
            self.flood_events = pd.read_csv(self.data_dir / 'historical/flood_events.csv')
            self.cyclone_history = pd.read_csv(self.data_dir / 'historical/mumbai_cyclone_history.csv')
            
            # Real-time data
            self.rain_sensors = pd.read_csv(self.data_dir / 'realtime/rain_sensors.csv')
            self.water_sensors = pd.read_csv(self.data_dir / 'realtime/water_level_sensors.csv')
            self.traffic_sensors = pd.read_csv(self.data_dir / 'realtime/traffic_density.csv')
            self.power_load = pd.read_csv(self.data_dir / 'realtime/power_load.csv')
            self.alert_sensors = pd.read_csv(self.data_dir / 'realtime/alert_sound_sensors.csv')
            
            # Output data
            self.risk_scores = pd.read_csv(self.data_dir / 'outputs/ward_risk_scores.csv')
            self.explainability = pd.read_csv(self.data_dir / 'outputs/explainability_log.csv')
            self.recommendations = pd.read_csv(self.data_dir / 'outputs/ai_recommendations.csv')
            
            print("✅ All Mumbai data loaded successfully")
            return self
        except Exception as e:
            print(f"❌ Error loading Mumbai data: {e}")
            raise
    
    def get_ward(self, ward_id: str) -> Optional[Dict]:
        """Get specific ward data"""
        if self.wards is None:
            return None
        ward_data = self.wards[self.wards['ward_id'] == ward_id]
        if ward_data.empty:
            return None
        return ward_data.iloc[0].to_dict()
    
    def get_all_wards(self) -> List[Dict]:
        """Get all wards"""
        if self.wards is None:
            return []
        return self.wards.to_dict('records')
    
    def get_infrastructure_by_ward(self, ward_id: str) -> List[Dict]:
        """Get all infrastructure in a ward"""
        if self.infrastructure is None:
            return []
        infra = self.infrastructure[self.infrastructure['ward_id'] == ward_id]
        return infra.to_dict('records')
    
    def get_all_infrastructure(self) -> List[Dict]:
        """Get all infrastructure nodes"""
        if self.infrastructure is None:
            return []
        return self.infrastructure.to_dict('records')
    
    def get_risk_scores(self) -> List[Dict]:
        """Get current risk scores for all wards"""
        if self.risk_scores is None:
            return []
        return self.risk_scores.to_dict('records')
    
    def get_ward_risk(self, ward_id: str) -> Optional[Dict]:
        """Get risk score for specific ward"""
        if self.risk_scores is None:
            return None
        risk = self.risk_scores[self.risk_scores['ward_id'] == ward_id]
        if risk.empty:
            return None
        return risk.iloc[0].to_dict()
    
    def get_recommendations(self, ward_id: Optional[str] = None) -> List[Dict]:
        """Get AI recommendations"""
        if self.recommendations is None:
            return []
        if ward_id:
            recs = self.recommendations[self.recommendations['ward_id'] == ward_id]
            return recs.to_dict('records')
        return self.recommendations.to_dict('records')
    
    def get_explainability(self, ward_id: str) -> List[Dict]:
        """Get feature importance for ward"""
        if self.explainability is None:
            return []
        explain = self.explainability[self.explainability['ward_id'] == ward_id]
        return explain.to_dict('records')
    
    def get_rain_sensors(self) -> List[Dict]:
        """Get rain sensor data"""
        if self.rain_sensors is None:
            return []
        return self.rain_sensors.to_dict('records')
    
    def get_water_sensors(self) -> List[Dict]:
        """Get water level sensor data"""
        if self.water_sensors is None:
            return []
        return self.water_sensors.to_dict('records')
    
    def get_traffic_sensors(self) -> List[Dict]:
        """Get traffic density data"""
        if self.traffic_sensors is None:
            return []
        return self.traffic_sensors.to_dict('records')
    
    def get_power_load(self) -> List[Dict]:
        """Get power grid data"""
        if self.power_load is None:
            return []
        return self.power_load.to_dict('records')
    
    def get_alert_sensors(self) -> List[Dict]:
        """Get crowd panic sensor data"""
        if self.alert_sensors is None:
            return []
        return self.alert_sensors.to_dict('records')
    
    def get_historical_floods(self) -> List[Dict]:
        """Get historical flood events"""
        if self.flood_events is None:
            return []
        return self.flood_events.to_dict('records')
    
    def get_cyclone_history(self) -> List[Dict]:
        """Get cyclone history"""
        if self.cyclone_history is None:
            return []
        return self.cyclone_history.to_dict('records')
    
    def get_rainfall_history(self, ward_id: Optional[str] = None) -> List[Dict]:
        """Get rainfall history"""
        if self.rainfall_history is None:
            return []
        if ward_id:
            history = self.rainfall_history[self.rainfall_history['ward_id'] == ward_id]
            return history.to_dict('records')
        return self.rainfall_history.to_dict('records')


# Global instance
_loader = None

def get_mumbai_data_loader() -> MumbaiDataLoader:
    """Get singleton instance of data loader"""
    global _loader
    if _loader is None:
        _loader = MumbaiDataLoader().load_all()
    return _loader
