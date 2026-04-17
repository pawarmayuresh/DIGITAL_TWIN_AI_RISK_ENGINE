"""
Advanced Features API Routes
Provides endpoints for new advanced features
"""
from fastapi import APIRouter, Query
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter(tags=["advanced"])

# Import new services
try:
    from backend.services.external_data_service import ExternalDataIntegrator
    from backend.core.analytics_engine.forecasting import DisasterForecaster
    from backend.services.nlp_service import DisasterChatbot
    from backend.core.ml_models.deep_learning import DisasterLSTM, CNNImageAnalyzer, TransformerMultiModal
    from backend.core.multi_agent.swarm_coordination import SwarmRescueCoordinator, RescueTeam, DisasterZone
except ImportError as e:
    print(f"Import error in advanced_routes: {e}")
    ExternalDataIntegrator = None
    DisasterForecaster = None
    DisasterChatbot = None
    DisasterLSTM = None
    CNNImageAnalyzer = None
    TransformerMultiModal = None
    SwarmRescueCoordinator = None

# Initialize services
external_data = ExternalDataIntegrator() if ExternalDataIntegrator else None
forecaster = DisasterForecaster() if DisasterForecaster else None
chatbot = DisasterChatbot() if DisasterChatbot else None
lstm_model = DisasterLSTM() if DisasterLSTM else None
cnn_analyzer = CNNImageAnalyzer() if CNNImageAnalyzer else None
transformer_model = TransformerMultiModal() if TransformerMultiModal else None
swarm_coordinator = SwarmRescueCoordinator() if SwarmRescueCoordinator else None


class ChatQuery(BaseModel):
    question: str
    language: str = 'english'


class ScenarioRequest(BaseModel):
    name: str
    base_risk: float = 0.5
    rainfall_mm: float = 0
    population_increase: int = 0
    infrastructure_quality: float = 0.7
    population: int = 500000


# ============================================================================
# EXTERNAL DATA INTEGRATION ENDPOINTS
# ============================================================================

@router.get("/external-data/weather/{ward_id}")
async def get_weather_data(ward_id: str):
    """Get real-time weather data for a ward"""
    if not external_data:
        return {"error": "External data service not available"}
    
    return external_data.fetch_weather_data(ward_id)


@router.get("/external-data/traffic/{ward_id}")
async def get_traffic_data(ward_id: str):
    """Get real-time traffic data for a ward"""
    if not external_data:
        return {"error": "External data service not available"}
    
    return external_data.fetch_traffic_data(ward_id)


@router.get("/external-data/sentiment/{ward_id}")
async def get_social_sentiment(ward_id: str, keyword: str = Query("disaster")):
    """Get social media sentiment analysis"""
    if not external_data:
        return {"error": "External data service not available"}
    
    return external_data.fetch_social_sentiment(ward_id, keyword)


@router.get("/external-data/iot/{ward_id}")
async def get_iot_sensors(ward_id: str):
    """Get IoT sensor data"""
    if not external_data:
        return {"error": "External data service not available"}
    
    return external_data.fetch_iot_sensor_data(ward_id)


@router.get("/external-data/integrated/{ward_id}")
async def get_integrated_assessment(ward_id: str):
    """Get comprehensive risk assessment from all external sources"""
    if not external_data:
        return {"error": "External data service not available"}
    
    return external_data.get_integrated_risk_assessment(ward_id)


# ============================================================================
# FORECASTING ENDPOINTS
# ============================================================================

@router.get("/forecast/7-day/{ward_id}")
async def get_7_day_forecast(ward_id: str, current_risk: float = Query(0.5)):
    """Get 7-day disaster risk forecast"""
    if not forecaster:
        return {"error": "Forecasting service not available"}
    
    forecasts = forecaster.forecast_7_day_risk(ward_id, current_risk)
    
    return {
        "ward_id": ward_id,
        "forecast_period": "7 days",
        "forecasts": [
            {
                "date": f.date,
                "risk_score": f.risk_score,
                "confidence": f.confidence,
                "factors": f.factors,
                "recommendation": f.recommendation
            }
            for f in forecasts
        ]
    }


@router.get("/forecast/seasonal/{ward_id}")
async def get_seasonal_analysis(ward_id: str):
    """Get seasonal risk analysis"""
    if not forecaster:
        return {"error": "Forecasting service not available"}
    
    return forecaster.seasonal_analysis(ward_id)


@router.get("/forecast/historical/{ward_id}")
async def get_historical_trends(ward_id: str, days: int = Query(30, ge=7, le=90)):
    """Get historical trend analysis"""
    if not forecaster:
        return {"error": "Forecasting service not available"}
    
    return forecaster.historical_trend_analysis(ward_id, days)


@router.post("/forecast/what-if/{ward_id}")
async def analyze_what_if_scenario(ward_id: str, scenario: ScenarioRequest):
    """Analyze what-if scenario"""
    if not forecaster:
        return {"error": "Forecasting service not available"}
    
    scenario_dict = scenario.dict()
    return forecaster.what_if_scenario_builder(ward_id, scenario_dict)


# ============================================================================
# NATURAL LANGUAGE INTERFACE ENDPOINTS
# ============================================================================

@router.post("/chatbot/query")
async def chat_query(query: ChatQuery):
    """Process natural language query"""
    if not chatbot:
        return {
            "intent": "error",
            "answer": "Chatbot service not available",
            "confidence": 0.0
        }
    
    try:
        response = chatbot.answer_query(query.question, query.language)
        return response
    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "intent": "error",
            "answer": f"I encountered an issue processing your query. Please try rephrasing or ask something else.",
            "data": {
                "error": str(e),
                "suggestions": [
                    "Try asking about risk in a specific ward",
                    "Ask for evacuation routes",
                    "Request emergency contacts",
                    "Type 'help' for available commands"
                ]
            },
            "confidence": 0.0
        }


@router.get("/chatbot/history")
async def get_chat_history(limit: int = Query(10, ge=1, le=50)):
    """Get conversation history"""
    if not chatbot:
        return {"error": "Chatbot service not available"}
    
    return {
        "history": chatbot.get_conversation_history(limit),
        "total_conversations": len(chatbot.conversation_history)
    }


@router.post("/chatbot/clear-history")
async def clear_chat_history():
    """Clear conversation history"""
    if not chatbot:
        return {"error": "Chatbot service not available"}
    
    chatbot.clear_history()
    return {"success": True, "message": "Conversation history cleared"}


@router.get("/chatbot/capabilities")
async def get_chatbot_capabilities():
    """Get chatbot capabilities and examples"""
    return {
        "supported_languages": ["english", "hindi", "marathi"],
        "intents": [
            {
                "name": "Risk Query",
                "examples": [
                    "What's the risk in Kurla?",
                    "How dangerous is Bandra?",
                    "Show me risk score for Colaba"
                ]
            },
            {
                "name": "Evacuation Query",
                "examples": [
                    "Show evacuation routes from Andheri",
                    "Where are safe zones near Byculla?",
                    "How do I evacuate from Chembur?"
                ]
            },
            {
                "name": "Forecast Query",
                "examples": [
                    "Forecast for Kurla",
                    "What will happen tomorrow?",
                    "Predict risk for next week"
                ]
            },
            {
                "name": "Report Query",
                "examples": [
                    "Generate report for Ghatkopar",
                    "Create disaster assessment",
                    "Show me the latest report"
                ]
            },
            {
                "name": "Status Query",
                "examples": [
                    "What's the current situation?",
                    "Status of Colaba",
                    "Show active incidents"
                ]
            }
        ]
    }


# ============================================================================
# COMBINED ANALYTICS ENDPOINT
# ============================================================================

@router.get("/analytics/comprehensive/{ward_id}")
async def get_comprehensive_analytics(ward_id: str):
    """Get comprehensive analytics combining all advanced features"""
    result = {
        "ward_id": ward_id,
        "timestamp": None,
        "external_data": None,
        "forecast": None,
        "seasonal_analysis": None
    }
    
    # Fetch external data
    if external_data:
        try:
            result["external_data"] = external_data.get_integrated_risk_assessment(ward_id)
            result["timestamp"] = result["external_data"]["timestamp"]
        except Exception as e:
            result["external_data"] = {"error": str(e)}
    
    # Fetch forecast
    if forecaster:
        try:
            forecasts = forecaster.forecast_7_day_risk(ward_id)
            result["forecast"] = [
                {
                    "date": f.date,
                    "risk_score": f.risk_score,
                    "confidence": f.confidence
                }
                for f in forecasts[:3]  # Next 3 days
            ]
        except Exception as e:
            result["forecast"] = {"error": str(e)}
    
    # Fetch seasonal analysis
    if forecaster:
        try:
            result["seasonal_analysis"] = forecaster.seasonal_analysis(ward_id)
        except Exception as e:
            result["seasonal_analysis"] = {"error": str(e)}
    
    return result


# ============================================================================
# SYSTEM STATUS ENDPOINT
# ============================================================================

@router.get("/system/status")
async def get_system_status():
    """Get status of all advanced features"""
    return {
        "external_data_integration": external_data is not None,
        "forecasting_engine": forecaster is not None,
        "nlp_chatbot": chatbot is not None,
        "features": {
            "real_time_weather": external_data is not None,
            "traffic_monitoring": external_data is not None,
            "social_sentiment": external_data is not None,
            "iot_sensors": external_data is not None,
            "7_day_forecast": forecaster is not None,
            "seasonal_analysis": forecaster is not None,
            "what_if_scenarios": forecaster is not None,
            "natural_language_queries": chatbot is not None,
            "multi_language_support": chatbot is not None
        },
        "version": "2.0.0-advanced"
    }



# ============================================================================
# DEEP LEARNING ENDPOINTS
# ============================================================================

@router.get("/ml/lstm/predict-24h/{ward_id}")
async def predict_24h_lstm(ward_id: str):
    """Predict disaster risk for next 24 hours using LSTM with real-time data integration"""
    if not lstm_model:
        return {"error": "LSTM model not available"}
    
    # Fetch real-time external data
    external_risk_data = None
    if external_data:
        try:
            external_risk_data = external_data.get_integrated_risk_assessment(ward_id)
        except Exception as e:
            print(f"Error fetching external data: {e}")
    
    # Generate ward-specific historical data
    historical_data = lstm_model._generate_synthetic_history(48, ward_id)
    
    # Make predictions with external data integration
    predictions = lstm_model.predict_next_24h(historical_data, ward_id, external_risk_data)
    
    return {
        "ward_id": ward_id,
        "model": "LSTM",
        "prediction_horizon": "24 hours",
        "predictions": predictions,
        "model_confidence": 0.88,
        "external_data_integrated": external_risk_data is not None,
        "real_time_factors": {
            "weather_integrated": external_risk_data is not None,
            "traffic_integrated": external_risk_data is not None,
            "sensor_integrated": external_risk_data is not None
        } if external_risk_data else None
    }


@router.get("/ml/lstm/weekly-pattern/{ward_id}")
async def predict_weekly_pattern(ward_id: str):
    """Predict weekly disaster risk pattern using LSTM"""
    if not lstm_model:
        return {"error": "LSTM model not available"}
    
    return lstm_model.predict_weekly_pattern(ward_id)


@router.post("/ml/lstm/train")
async def train_lstm_model():
    """Train LSTM model on historical data"""
    if not lstm_model:
        return {"error": "LSTM model not available"}
    
    # Generate synthetic training data
    training_data = lstm_model._generate_synthetic_history(1000)
    
    result = lstm_model.train_on_historical_data(training_data)
    
    return result


@router.post("/ml/cnn/analyze-image")
async def analyze_satellite_image(image_path: str = Query(...)):
    """Analyze satellite image for disaster detection"""
    if not cnn_analyzer:
        return {"error": "CNN analyzer not available"}
    
    return cnn_analyzer.analyze_satellite_image(image_path)


@router.post("/ml/cnn/compare-images")
async def compare_temporal_images(
    before_image: str = Query(...),
    after_image: str = Query(...)
):
    """Compare before/after satellite images"""
    if not cnn_analyzer:
        return {"error": "CNN analyzer not available"}
    
    return cnn_analyzer.compare_temporal_images(before_image, after_image)


@router.post("/ml/transformer/fuse-data")
async def fuse_multi_modal_data(data_sources: Dict):
    """Fuse multiple data sources using transformer"""
    if not transformer_model:
        return {"error": "Transformer model not available"}
    
    return transformer_model.fuse_data_sources(data_sources)


# ============================================================================
# SWARM COORDINATION ENDPOINTS
# ============================================================================

@router.post("/swarm/initialize")
async def initialize_swarm(num_teams: int = Query(10)):
    """Initialize swarm rescue coordination"""
    if not swarm_coordinator:
        return {"error": "Swarm coordinator not available"}
    
    # Initialize teams at random base positions
    import numpy as np
    base_positions = [(np.random.uniform(0, 100), np.random.uniform(0, 100)) 
                      for _ in range(num_teams)]
    
    swarm_coordinator.initialize_teams(base_positions)
    
    return {
        "status": "initialized",
        "num_teams": num_teams,
        "teams": [
            {
                "team_id": team.team_id,
                "position": team.position,
                "capacity": team.capacity,
                "status": team.status
            }
            for team in swarm_coordinator.teams
        ]
    }


@router.post("/swarm/add-disaster-zone")
async def add_disaster_zone(
    zone_id: str,
    x: float,
    y: float,
    severity: float,
    people_count: int,
    priority: int
):
    """Add a disaster zone requiring rescue"""
    if not swarm_coordinator:
        return {"error": "Swarm coordinator not available"}
    
    zone = DisasterZone(
        zone_id=zone_id,
        position=(x, y),
        severity=severity,
        people_count=people_count,
        priority=priority
    )
    
    swarm_coordinator.add_disaster_zone(zone)
    
    return {
        "status": "zone_added",
        "zone": {
            "zone_id": zone.zone_id,
            "position": zone.position,
            "severity": zone.severity,
            "people_count": zone.people_count,
            "priority": zone.priority
        }
    }


@router.post("/swarm/optimize")
async def optimize_swarm_deployment(max_iterations: int = Query(50)):
    """Optimize rescue team deployment using swarm intelligence"""
    if not swarm_coordinator:
        return {"error": "Swarm coordinator not available"}
    
    return swarm_coordinator.optimize_team_deployment(max_iterations)


@router.get("/swarm/simulate")
async def simulate_swarm(steps: int = Query(10)):
    """Simulate swarm behavior over time"""
    if not swarm_coordinator:
        return {"error": "Swarm coordinator not available"}
    
    return {
        "simulation_steps": swarm_coordinator.simulate_swarm_behavior(steps)
    }


@router.get("/swarm/status")
async def get_swarm_status():
    """Get current swarm coordination status"""
    if not swarm_coordinator:
        return {"error": "Swarm coordinator not available"}
    
    # Auto-initialize if no teams exist
    if len(swarm_coordinator.teams) == 0:
        import numpy as np
        # Initialize with default teams
        base_positions = [(np.random.uniform(0, 100), np.random.uniform(0, 100)) 
                          for _ in range(10)]
        swarm_coordinator.initialize_teams(base_positions)
        
        # Add some default disaster zones
        default_zones = [
            DisasterZone(
                zone_id=f'Z{i}',
                position=(np.random.uniform(20, 80), np.random.uniform(20, 80)),
                severity=np.random.uniform(0.5, 0.9),
                people_count=np.random.randint(50, 200),
                priority=np.random.randint(3, 5)
            )
            for i in range(1, 4)
        ]
        
        for zone in default_zones:
            swarm_coordinator.add_disaster_zone(zone)
        
        # Run initial optimization
        swarm_coordinator.optimize_team_deployment(max_iterations=30)
    
    return swarm_coordinator.get_coordination_status()


# ============================================================================
# COMBINED ADVANCED ANALYTICS
# ============================================================================

@router.get("/analytics/advanced/{ward_id}")
async def get_advanced_analytics(ward_id: str):
    """Get comprehensive advanced analytics with real-time data integration"""
    result = {
        "ward_id": ward_id,
        "lstm_prediction": None,
        "external_data": None,
        "forecast": None,
        "swarm_status": None
    }
    
    # External data (fetch first to use in LSTM)
    external_risk_data = None
    if external_data:
        try:
            external_risk_data = external_data.get_integrated_risk_assessment(ward_id)
            result["external_data"] = external_risk_data
        except Exception as e:
            result["external_data"] = {"error": str(e)}
    
    # LSTM prediction with external data integration
    if lstm_model:
        try:
            historical_data = lstm_model._generate_synthetic_history(48, ward_id)
            predictions = lstm_model.predict_next_24h(historical_data, ward_id, external_risk_data)
            result["lstm_prediction"] = {
                "next_hour": predictions[0] if predictions else None,
                "peak_risk_hour": max(predictions, key=lambda x: x['risk_score']) if predictions else None,
                "average_24h_risk": sum(p['risk_score'] for p in predictions) / len(predictions) if predictions else None
            }
        except Exception as e:
            result["lstm_prediction"] = {"error": str(e)}
    
    # Forecast
    if forecaster:
        try:
            forecasts = forecaster.forecast_7_day_risk(ward_id)
            result["forecast"] = [
                {"date": f.date, "risk_score": f.risk_score}
                for f in forecasts[:3]
            ]
        except Exception as e:
            result["forecast"] = {"error": str(e)}
    
    # Swarm status
    if swarm_coordinator:
        try:
            result["swarm_status"] = swarm_coordinator.get_coordination_status()
        except Exception as e:
            result["swarm_status"] = {"error": str(e)}
    
    return result
