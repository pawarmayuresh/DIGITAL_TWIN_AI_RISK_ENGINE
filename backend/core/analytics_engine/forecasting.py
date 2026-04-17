"""
Disaster Forecasting Engine
Provides predictive analytics for disaster risk
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass


@dataclass
class ForecastPoint:
    """Single forecast data point"""
    date: str
    risk_score: float
    confidence: float
    factors: Dict[str, float]
    recommendation: str


class DisasterForecaster:
    """Forecasts disaster risk using historical patterns and trends"""
    
    def __init__(self):
        self.historical_data = {}
        self.seasonal_patterns = self._initialize_seasonal_patterns()
    
    def forecast_7_day_risk(self, ward_id: str, current_risk: float = 0.5) -> List[ForecastPoint]:
        """Generate 7-day disaster risk forecast"""
        forecasts = []
        base_date = datetime.now()
        
        for day in range(7):
            forecast_date = base_date + timedelta(days=day)
            
            # Apply seasonal patterns
            seasonal_factor = self._get_seasonal_factor(forecast_date)
            
            # Apply trend (slight random walk)
            trend = np.random.uniform(-0.05, 0.05)
            
            # Calculate risk score
            risk_score = current_risk * seasonal_factor + trend
            risk_score = max(0.0, min(1.0, risk_score))
            
            # Calculate confidence (decreases with time)
            confidence = 0.95 - (day * 0.1)
            
            # Identify risk factors
            factors = self._identify_risk_factors(risk_score, forecast_date)
            
            # Generate recommendation
            recommendation = self._generate_forecast_recommendation(risk_score, day)
            
            forecasts.append(ForecastPoint(
                date=forecast_date.strftime('%Y-%m-%d'),
                risk_score=risk_score,
                confidence=confidence,
                factors=factors,
                recommendation=recommendation
            ))
            
            # Update current risk for next iteration
            current_risk = risk_score
        
        return forecasts
    
    def seasonal_analysis(self, ward_id: str) -> Dict[str, Any]:
        """Analyze seasonal risk patterns"""
        current_month = datetime.now().month
        
        # Monsoon season (June-September) has higher flood risk
        is_monsoon = 6 <= current_month <= 9
        
        # Winter (December-February) has lower disaster risk
        is_winter = current_month in [12, 1, 2]
        
        # Summer (March-May) has heat wave risk
        is_summer = 3 <= current_month <= 5
        
        seasonal_risks = {
            'monsoon': {
                'active': is_monsoon,
                'flood_risk': 0.8 if is_monsoon else 0.2,
                'landslide_risk': 0.6 if is_monsoon else 0.1,
                'description': 'High rainfall and flooding expected' if is_monsoon else 'Low monsoon risk'
            },
            'winter': {
                'active': is_winter,
                'cold_wave_risk': 0.3 if is_winter else 0.0,
                'fog_risk': 0.4 if is_winter else 0.1,
                'description': 'Stable weather conditions' if is_winter else 'Not winter season'
            },
            'summer': {
                'active': is_summer,
                'heat_wave_risk': 0.7 if is_summer else 0.2,
                'drought_risk': 0.5 if is_summer else 0.1,
                'description': 'High temperatures expected' if is_summer else 'Not summer season'
            }
        }
        
        # Calculate overall seasonal risk
        active_season = 'monsoon' if is_monsoon else 'winter' if is_winter else 'summer' if is_summer else 'transition'
        
        return {
            'current_season': active_season,
            'current_month': datetime.now().strftime('%B'),
            'seasonal_risks': seasonal_risks,
            'overall_seasonal_risk': self._calculate_overall_seasonal_risk(seasonal_risks),
            'historical_comparison': self._get_historical_comparison(current_month),
            'recommendations': self._get_seasonal_recommendations(active_season)
        }
    
    def historical_trend_analysis(self, ward_id: str, days: int = 30) -> Dict[str, Any]:
        """Analyze historical disaster trends"""
        # Simulate historical data
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days, 0, -1)]
        
        # Generate synthetic historical risk scores with trend
        base_risk = 0.5
        trend_slope = np.random.uniform(-0.01, 0.01)
        noise = np.random.normal(0, 0.05, days)
        
        risk_scores = [max(0, min(1, base_risk + (i * trend_slope) + noise[i])) for i in range(days)]
        
        # Calculate statistics
        avg_risk = np.mean(risk_scores)
        max_risk = np.max(risk_scores)
        min_risk = np.min(risk_scores)
        std_dev = np.std(risk_scores)
        
        # Detect trend
        if trend_slope > 0.005:
            trend = 'increasing'
        elif trend_slope < -0.005:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        # Identify peaks
        peaks = self._identify_peaks(risk_scores, dates)
        
        return {
            'period': f'Last {days} days',
            'average_risk': avg_risk,
            'maximum_risk': max_risk,
            'minimum_risk': min_risk,
            'volatility': std_dev,
            'trend': trend,
            'trend_slope': trend_slope,
            'risk_peaks': peaks,
            'historical_data': [
                {'date': dates[i], 'risk_score': risk_scores[i]}
                for i in range(days)
            ]
        }
    
    def what_if_scenario_builder(self, ward_id: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Build and analyze what-if scenarios"""
        base_risk = scenario.get('base_risk', 0.5)
        
        # Apply scenario modifications
        rainfall_factor = scenario.get('rainfall_mm', 0) / 100  # 100mm = +1.0 risk
        population_factor = scenario.get('population_increase', 0) / 100000  # Per 100k people
        infrastructure_factor = 1 - scenario.get('infrastructure_quality', 0.7)
        
        # Calculate scenario risk
        scenario_risk = base_risk + rainfall_factor + population_factor + infrastructure_factor
        scenario_risk = max(0.0, min(1.0, scenario_risk))
        
        # Calculate impact
        impact = self._calculate_scenario_impact(scenario_risk, scenario)
        
        # Generate mitigation strategies
        mitigations = self._generate_mitigation_strategies(scenario_risk, scenario)
        
        return {
            'scenario_name': scenario.get('name', 'Custom Scenario'),
            'base_risk': base_risk,
            'scenario_risk': scenario_risk,
            'risk_increase': scenario_risk - base_risk,
            'risk_factors': {
                'rainfall': rainfall_factor,
                'population': population_factor,
                'infrastructure': infrastructure_factor
            },
            'estimated_impact': impact,
            'mitigation_strategies': mitigations,
            'confidence': 0.75
        }
    
    def _initialize_seasonal_patterns(self) -> Dict[str, float]:
        """Initialize seasonal risk patterns for Mumbai"""
        return {
            1: 0.3,   # January - Low risk
            2: 0.3,   # February - Low risk
            3: 0.4,   # March - Moderate risk
            4: 0.5,   # April - Moderate risk
            5: 0.6,   # May - Pre-monsoon
            6: 0.9,   # June - Monsoon peak
            7: 1.0,   # July - Monsoon peak
            8: 0.95,  # August - Monsoon
            9: 0.8,   # September - Late monsoon
            10: 0.6,  # October - Post-monsoon
            11: 0.4,  # November - Moderate risk
            12: 0.3   # December - Low risk
        }
    
    def _get_seasonal_factor(self, date: datetime) -> float:
        """Get seasonal risk factor for a date"""
        return self.seasonal_patterns.get(date.month, 0.5)
    
    def _identify_risk_factors(self, risk_score: float, date: datetime) -> Dict[str, float]:
        """Identify contributing risk factors"""
        factors = {}
        
        # Seasonal factor
        factors['seasonal'] = self._get_seasonal_factor(date)
        
        # Weather factor (simulated)
        factors['weather'] = np.random.uniform(0.2, 0.8)
        
        # Infrastructure factor
        factors['infrastructure'] = np.random.uniform(0.3, 0.7)
        
        # Population density factor
        factors['population'] = np.random.uniform(0.4, 0.9)
        
        return factors
    
    def _generate_forecast_recommendation(self, risk_score: float, days_ahead: int) -> str:
        """Generate recommendation for forecast"""
        if risk_score > 0.8:
            return f"HIGH RISK in {days_ahead} days: Prepare evacuation plans"
        elif risk_score > 0.6:
            return f"ELEVATED RISK in {days_ahead} days: Monitor situation closely"
        elif risk_score > 0.4:
            return f"MODERATE RISK in {days_ahead} days: Stay informed"
        else:
            return f"LOW RISK in {days_ahead} days: Normal operations"
    
    def _calculate_overall_seasonal_risk(self, seasonal_risks: Dict) -> float:
        """Calculate overall seasonal risk score"""
        total_risk = 0.0
        count = 0
        
        for season_data in seasonal_risks.values():
            if season_data['active']:
                # Sum all risk types for active season
                for key, value in season_data.items():
                    if key.endswith('_risk'):
                        total_risk += value
                        count += 1
        
        return total_risk / count if count > 0 else 0.3
    
    def _get_historical_comparison(self, current_month: int) -> Dict[str, Any]:
        """Compare current conditions to historical averages"""
        historical_avg = self.seasonal_patterns.get(current_month, 0.5)
        
        return {
            'historical_average_risk': historical_avg,
            'comparison': 'Above average' if historical_avg > 0.6 else 'Below average',
            'percentile': int(historical_avg * 100)
        }
    
    def _get_seasonal_recommendations(self, season: str) -> List[str]:
        """Get recommendations based on season"""
        recommendations = {
            'monsoon': [
                'Ensure drainage systems are clear',
                'Stock emergency supplies',
                'Prepare evacuation routes',
                'Monitor weather forecasts daily'
            ],
            'winter': [
                'Maintain infrastructure',
                'Plan for fog-related delays',
                'Review emergency protocols'
            ],
            'summer': [
                'Prepare for heat waves',
                'Ensure water supply adequacy',
                'Monitor fire risk in dry areas'
            ],
            'transition': [
                'Conduct routine maintenance',
                'Update emergency plans',
                'Train response teams'
            ]
        }
        
        return recommendations.get(season, recommendations['transition'])
    
    def _identify_peaks(self, risk_scores: List[float], dates: List[str]) -> List[Dict]:
        """Identify risk peaks in historical data"""
        peaks = []
        
        for i in range(1, len(risk_scores) - 1):
            if risk_scores[i] > risk_scores[i-1] and risk_scores[i] > risk_scores[i+1]:
                if risk_scores[i] > 0.7:  # Only significant peaks
                    peaks.append({
                        'date': dates[i],
                        'risk_score': risk_scores[i],
                        'severity': 'high' if risk_scores[i] > 0.8 else 'moderate'
                    })
        
        return peaks[-5:]  # Return last 5 peaks
    
    def _calculate_scenario_impact(self, risk_score: float, scenario: Dict) -> Dict[str, Any]:
        """Calculate estimated impact of scenario"""
        population = scenario.get('population', 500000)
        
        # Estimate casualties
        casualty_rate = risk_score * 0.001  # 0.1% at max risk
        estimated_casualties = int(population * casualty_rate)
        
        # Estimate economic loss
        gdp_per_capita = 200000  # INR
        economic_loss = int(population * gdp_per_capita * risk_score * 0.1)
        
        # Estimate affected population
        affected_rate = risk_score * 0.3  # 30% at max risk
        affected_population = int(population * affected_rate)
        
        return {
            'estimated_casualties': estimated_casualties,
            'economic_loss_inr': economic_loss,
            'affected_population': affected_population,
            'infrastructure_damage': f"{int(risk_score * 100)}%"
        }
    
    def _generate_mitigation_strategies(self, risk_score: float, scenario: Dict) -> List[str]:
        """Generate mitigation strategies for scenario"""
        strategies = []
        
        if risk_score > 0.7:
            strategies.append("Implement immediate evacuation protocols")
            strategies.append("Deploy emergency response teams")
            strategies.append("Activate disaster management centers")
        
        if scenario.get('rainfall_mm', 0) > 50:
            strategies.append("Clear drainage systems urgently")
            strategies.append("Set up temporary flood barriers")
        
        if scenario.get('population_increase', 0) > 50000:
            strategies.append("Increase emergency shelter capacity")
            strategies.append("Enhance communication systems")
        
        if scenario.get('infrastructure_quality', 1.0) < 0.5:
            strategies.append("Prioritize infrastructure repairs")
            strategies.append("Conduct structural assessments")
        
        if not strategies:
            strategies.append("Maintain current preparedness levels")
            strategies.append("Continue routine monitoring")
        
        return strategies
