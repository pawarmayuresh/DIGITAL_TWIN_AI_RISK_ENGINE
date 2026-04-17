"""
Natural Language Processing Service
Provides conversational interface for disaster management system
"""
from typing import Dict, Any, List, Optional
import re
from datetime import datetime


class DisasterChatbot:
    """Conversational AI for disaster management queries"""
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
        self.supported_languages = ['english', 'hindi', 'marathi']
        
        # Enhanced intent patterns with more variations
        self.intent_patterns = {
            'risk_query': [
                r'what.*risk.*(?:in|at|for)\s+(\w+)',
                r'risk.*(?:level|score).*(?:in|at|for|of)\s*(\w+)',
                r'how.*(?:dangerous|risky|safe).*(?:is|in)\s+(\w+)',
                r'(\w+).*(?:risk|danger|threat)',
                r'(?:check|show|tell).*risk.*(\w+)',
                r'is\s+(\w+).*(?:safe|dangerous|risky)',
                r'(\w+).*(?:safe|dangerous)',
                r'risk\s+(?:in|at|for)\s+(\w+)',
                r'(\w+)\s+risk',
                r'danger.*(?:in|at)\s+(\w+)',
                r'threat.*(?:in|at)\s+(\w+)'
            ],
            'evacuation_query': [
                r'evacuation.*(?:route|path|way).*(?:from|in)\s+(\w+)',
                r'how.*(?:evacuate|escape|leave).*(?:from)?\s*(\w+)',
                r'safe.*(?:zone|area|place).*(?:near|from|in)\s+(\w+)',
                r'(?:escape|exit|leave).*(?:from|in)\s+(\w+)',
                r'where.*(?:go|evacuate).*(?:from)?\s*(\w+)',
                r'evacuation.*(\w+)',
                r'(?:show|find|get).*(?:route|path).*(\w+)',
                r'nearest.*(?:shelter|safe zone).*(\w+)',
                r'how.*(?:get out|leave).*(\w+)'
            ],
            'forecast_query': [
                r'forecast.*(?:for|in|at)?\s*(\w+)?',
                r'predict.*(?:for|in)?\s*(\w+)?',
                r'what.*(?:will|might).*happen.*(?:in|at)?\s*(\w+)?',
                r'future.*(?:risk|situation).*(?:in|at)?\s*(\w+)?',
                r'(?:next|coming).*(?:days|week|hours).*(\w+)?',
                r'weather.*(?:forecast|prediction).*(\w+)?',
                r'(?:7|seven).*day.*(?:forecast)?.*(\w+)?',
                r'tomorrow.*(\w+)?',
                r'upcoming.*(?:risk|weather).*(\w+)?'
            ],
            'report_query': [
                r'generate.*report.*(?:for)?\s*(\w+)?',
                r'create.*report.*(?:for)?\s*(\w+)?',
                r'(?:show|get|give).*report.*(?:for)?\s*(\w+)?',
                r'report.*(?:for|on|about)\s+(\w+)',
                r'(?:make|prepare).*report.*(\w+)?',
                r'(?:download|export).*report.*(\w+)?',
                r'assessment.*report.*(\w+)?'
            ],
            'help_query': [
                r'^help$',
                r'what.*can.*(?:you|i).*do',
                r'(?:show|list).*(?:commands|options|features)',
                r'how.*(?:use|work)',
                r'what.*(?:are|is).*(?:your|the).*(?:capabilities|features)',
                r'guide',
                r'instructions',
                r'how.*(?:to|do|can)',
                r'what.*(?:can|should).*(?:i|you)'
            ],
            'status_query': [
                r'(?:what|show).*status.*(?:of|in|at)?\s*(\w+)?',
                r'current.*(?:situation|status|condition).*(?:in|at|of)?\s*(\w+)?',
                r'what.*(?:happening|going on).*(?:in|at)?\s*(\w+)?',
                r'(?:how|what).*(?:is|are).*(\w+).*(?:doing|now)',
                r'situation.*(?:in|at)\s+(\w+)',
                r'(?:active|ongoing).*(?:incidents|emergencies).*(\w+)?',
                r'(?:latest|current).*(?:update|news).*(\w+)?',
                r'infrastructure.*(?:status)?.*(\w+)?'
            ],
            'resource_query': [
                r'(?:available|show).*(?:resources|teams|supplies).*(\w+)?',
                r'how many.*(?:teams|resources|supplies).*(\w+)?',
                r'resource.*(?:allocation|distribution).*(\w+)?',
                r'(?:emergency|rescue).*(?:teams|services).*(\w+)?'
            ],
            'shelter_query': [
                r'(?:where|show|find).*(?:shelter|refuge).*(\w+)?',
                r'(?:nearest|closest).*shelter.*(\w+)?',
                r'shelter.*(?:capacity|availability).*(\w+)?',
                r'(?:safe|emergency).*(?:shelter|location).*(\w+)?'
            ],
            'contact_query': [
                r'(?:emergency|contact).*(?:number|phone)',
                r'(?:who|how).*(?:to|do i).*(?:call|contact)',
                r'helpline',
                r'(?:phone|contact).*(?:number|info)'
            ]
        }
    
    def answer_query(self, question: str, language: str = 'english') -> Dict[str, Any]:
        """Process natural language query and return answer"""
        try:
            question_lower = question.lower().strip()
            
            # Store in conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'question': question,
                'language': language
            })
            
            # Detect intent
            intent, entities = self._detect_intent(question_lower)
            
            # Generate response based on intent
            if intent == 'risk_query':
                response = self._handle_risk_query(entities)
            elif intent == 'evacuation_query':
                response = self._handle_evacuation_query(entities)
            elif intent == 'forecast_query':
                response = self._handle_forecast_query(entities)
            elif intent == 'report_query':
                response = self._handle_report_query(entities)
            elif intent == 'status_query':
                response = self._handle_status_query(entities)
            elif intent == 'help_query':
                response = self._handle_help_query()
            elif intent == 'resource_query':
                response = self._handle_resource_query(entities)
            elif intent == 'shelter_query':
                response = self._handle_shelter_query(entities)
            elif intent == 'contact_query':
                response = self._handle_contact_query()
            else:
                response = self._handle_unknown_query(question)
            
            # Translate if needed
            if language != 'english':
                response = self._translate_response(response, language)
            
            return response
            
        except Exception as e:
            # Fallback error response
            return {
                'intent': 'error',
                'answer': "I encountered an error processing your query. Please try again or rephrase your question.",
                'data': {
                    'error': str(e),
                    'suggestions': [
                        "Try asking about risk in a specific ward",
                        "Ask for evacuation routes",
                        "Type 'help' for available commands"
                    ]
                },
                'confidence': 0.0
            }
    
    def _detect_intent(self, question: str) -> tuple:
        """Detect user intent from question"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                try:
                    match = re.search(pattern, question, re.IGNORECASE)
                    if match:
                        # Extract entities, filter out None values
                        entities = tuple(e for e in match.groups() if e is not None)
                        return intent, entities
                except Exception as e:
                    # If pattern matching fails, continue to next pattern
                    continue
        
        return 'unknown', ()
    
    def _handle_risk_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle risk-related queries"""
        ward = entities[0] if entities else 'Mumbai'
        ward = ward.title()
        
        # Simulate risk data with more realistic values
        import random
        
        # Base risk varies by ward characteristics
        base_risks = {
            'kurla': 0.72, 'bandra': 0.58, 'andheri': 0.65, 'colaba': 0.45,
            'worli': 0.52, 'dadar': 0.68, 'borivali': 0.55, 'chembur': 0.63,
            'ghatkopar': 0.61, 'mulund': 0.57, 'byculla': 0.70, 'parel': 0.66,
            'mahim': 0.59, 'santacruz': 0.54
        }
        
        base_risk = base_risks.get(ward.lower(), random.uniform(0.4, 0.8))
        risk_score = base_risk + random.uniform(-0.05, 0.05)
        risk_score = max(0.0, min(1.0, risk_score))
        
        severity = 'CRITICAL' if risk_score > 0.8 else 'HIGH' if risk_score > 0.7 else 'MODERATE' if risk_score > 0.5 else 'LOW'
        severity_color = 'red' if risk_score > 0.7 else 'orange' if risk_score > 0.5 else 'green'
        
        # Generate detailed factors
        factors = {
            'rainfall': random.uniform(20, 150),
            'water_level': random.uniform(1.5, 4.5),
            'population_density': random.randint(15000, 45000),
            'infrastructure_health': random.uniform(0.5, 0.95),
            'drainage_capacity': random.uniform(0.4, 0.9),
            'historical_incidents': random.randint(2, 15)
        }
        
        # Generate recommendations based on risk level
        recommendations = []
        if risk_score > 0.7:
            recommendations = [
                "⚠️ HIGH ALERT: Prepare for immediate evacuation",
                "Monitor official channels continuously",
                "Keep emergency kit ready",
                "Avoid low-lying areas",
                "Stay indoors if possible"
            ]
        elif risk_score > 0.5:
            recommendations = [
                "Stay alert and monitor updates",
                "Review evacuation routes",
                "Prepare emergency supplies",
                "Avoid unnecessary travel"
            ]
        else:
            recommendations = [
                "Situation is stable",
                "Continue normal activities with caution",
                "Stay informed through official channels"
            ]
        
        return {
            'intent': 'risk_query',
            'answer': f"The current risk level in {ward} is {severity} with a risk score of {risk_score:.1%}. {recommendations[0] if recommendations else ''}",
            'data': {
                'ward': ward,
                'risk_score': risk_score,
                'severity': severity,
                'severity_color': severity_color,
                'factors': factors,
                'trend': random.choice(['increasing', 'stable', 'decreasing']),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'suggestions': recommendations[1:] if len(recommendations) > 1 else [
                f"Check evacuation routes from {ward}",
                "View 7-day forecast",
                "Get detailed report"
            ],
            'confidence': 0.85 + random.uniform(0, 0.1)
        }
    
    def _handle_evacuation_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle evacuation-related queries"""
        location = entities[0] if entities else 'your location'
        
        return {
            'intent': 'evacuation_query',
            'answer': f"For evacuation from {location.title()}, follow these routes:",
            'data': {
                'location': location,
                'safe_zones': [
                    {'name': 'Safe Zone A', 'distance': '2.5 km', 'capacity': 5000},
                    {'name': 'Safe Zone B', 'distance': '3.8 km', 'capacity': 3000},
                    {'name': 'Safe Zone C', 'distance': '5.2 km', 'capacity': 7000}
                ],
                'recommended_route': 'Safe Zone A (closest and highest capacity)',
                'estimated_time': '15-20 minutes',
                'transportation': ['Walking', 'Emergency vehicles available']
            },
            'suggestions': [
                "Carry essential documents and supplies",
                "Follow official evacuation orders",
                "Stay with your group",
                "Avoid flooded areas"
            ],
            'emergency_contacts': [
                {'service': 'Emergency', 'number': '108'},
                {'service': 'Police', 'number': '100'},
                {'service': 'Fire', 'number': '101'}
            ],
            'confidence': 0.90
        }
    
    def _handle_forecast_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle forecast-related queries"""
        ward = entities[0] if entities else 'Mumbai'
        ward = ward.title()
        
        # Generate 7-day forecast
        import random
        from datetime import timedelta
        
        forecast = []
        base_risk = random.uniform(0.45, 0.75)
        
        weather_conditions = ['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Moderate Rain', 'Heavy Rain', 'Thunderstorm']
        
        for i in range(7):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = (datetime.now() + timedelta(days=i)).strftime('%A')
            
            # Add some variation
            risk = max(0.2, min(0.95, base_risk + random.uniform(-0.15, 0.15)))
            weather = random.choice(weather_conditions)
            rainfall = random.uniform(0, 150) if 'Rain' in weather else random.uniform(0, 20)
            
            severity = 'High' if risk > 0.7 else 'Moderate' if risk > 0.5 else 'Low'
            
            forecast.append({
                'date': date,
                'day': day_name,
                'risk_score': risk,
                'severity': severity,
                'weather': weather,
                'rainfall_mm': round(rainfall, 1),
                'temperature': random.randint(25, 35),
                'humidity': random.randint(60, 95),
                'wind_speed': random.randint(10, 40),
                'recommendation': 'Stay alert' if risk > 0.7 else 'Exercise caution' if risk > 0.5 else 'Normal operations'
            })
        
        # Calculate trend
        trend = 'increasing' if forecast[-1]['risk_score'] > forecast[0]['risk_score'] + 0.1 else \
                'decreasing' if forecast[-1]['risk_score'] < forecast[0]['risk_score'] - 0.1 else 'stable'
        
        # Peak risk day
        peak_day = max(forecast, key=lambda x: x['risk_score'])
        
        return {
            'intent': 'forecast_query',
            'answer': f"7-day disaster risk forecast for {ward}. Overall trend: {trend}. Peak risk expected on {peak_day['day']} ({peak_day['date']}) with {peak_day['severity']} risk.",
            'data': {
                'ward': ward,
                'forecast': forecast,
                'trend': trend,
                'peak_risk_day': peak_day,
                'average_risk': sum(f['risk_score'] for f in forecast) / len(forecast),
                'high_risk_days': sum(1 for f in forecast if f['risk_score'] > 0.7),
                'generated_at': datetime.now().isoformat()
            },
            'suggestions': [
                "Monitor daily updates",
                f"Prepare for {peak_day['day']} (highest risk)",
                "Review evacuation plans",
                "Stock emergency supplies"
            ],
            'confidence': 0.78
        }
    
    def _handle_report_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle report generation queries"""
        ward = entities[0] if entities else 'all wards'
        
        return {
            'intent': 'report_query',
            'answer': f"Generating comprehensive disaster management report for {ward.title()}...",
            'data': {
                'report_type': 'Comprehensive Disaster Assessment',
                'ward': ward,
                'generated_at': datetime.now().isoformat(),
                'sections': [
                    'Executive Summary',
                    'Current Risk Assessment',
                    'Infrastructure Status',
                    'Population Impact Analysis',
                    'Evacuation Readiness',
                    'Resource Allocation',
                    'Recommendations'
                ],
                'download_url': f'/api/reports/generate/{ward}',
                'format': 'PDF'
            },
            'suggestions': [
                "Review executive summary first",
                "Share with stakeholders",
                "Update emergency plans based on findings"
            ],
            'confidence': 0.95
        }
    
    def _handle_status_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle status queries"""
        ward = entities[0] if entities else 'Mumbai'
        
        import random
        
        return {
            'intent': 'status_query',
            'answer': f"Current situation in {ward.title()}:",
            'data': {
                'ward': ward,
                'overall_status': random.choice(['Normal', 'Alert', 'Warning', 'Emergency']),
                'active_incidents': random.randint(0, 5),
                'evacuation_in_progress': random.choice([True, False]),
                'infrastructure': {
                    'power': random.choice(['Operational', 'Partial', 'Down']),
                    'water': random.choice(['Operational', 'Partial', 'Down']),
                    'roads': random.choice(['Clear', 'Congested', 'Blocked']),
                    'communication': random.choice(['Operational', 'Degraded'])
                },
                'emergency_services': {
                    'available': random.randint(10, 50),
                    'deployed': random.randint(5, 30),
                    'response_time': f"{random.randint(5, 20)} minutes"
                }
            },
            'suggestions': [
                "Stay informed through official channels",
                "Follow local authority instructions",
                "Keep emergency contacts handy"
            ],
            'confidence': 0.88
        }
    
    def _handle_help_query(self) -> Dict[str, Any]:
        """Handle help queries"""
        return {
            'intent': 'help_query',
            'answer': "I can help you with disaster management queries. Here's what I can do:",
            'data': {
                'capabilities': [
                    {
                        'category': 'Risk Assessment',
                        'examples': [
                            "What's the risk in Kurla?",
                            "How dangerous is Bandra today?",
                            "Show me risk scores for Colaba"
                        ]
                    },
                    {
                        'category': 'Evacuation Planning',
                        'examples': [
                            "Show evacuation routes from Andheri",
                            "Where are safe zones near Byculla?",
                            "How do I evacuate from Chembur?"
                        ]
                    },
                    {
                        'category': 'Forecasting',
                        'examples': [
                            "Forecast for Kurla",
                            "What will happen in Borivali tomorrow?",
                            "Predict risk for next week"
                        ]
                    },
                    {
                        'category': 'Reports',
                        'examples': [
                            "Generate report for Ghatkopar",
                            "Create disaster assessment report",
                            "Show me the latest report"
                        ]
                    },
                    {
                        'category': 'Status Updates',
                        'examples': [
                            "What's the current situation in Kurla?",
                            "Status of Colaba",
                            "Show me active incidents"
                        ]
                    }
                ],
                'supported_languages': self.supported_languages
            },
            'suggestions': [
                "Try asking about risk in a specific ward",
                "Ask for evacuation routes",
                "Request a forecast"
            ],
            'confidence': 1.0
        }
    
    def _handle_unknown_query(self, question: str) -> Dict[str, Any]:
        """Handle unknown queries with better suggestions"""
        # Try to extract ward names even if intent is unclear
        mumbai_wards = ['kurla', 'bandra', 'andheri', 'colaba', 'worli', 'dadar', 'borivali', 
                        'chembur', 'ghatkopar', 'mulund', 'byculla', 'parel', 'mahim', 'santacruz']
        
        found_ward = None
        for ward in mumbai_wards:
            if ward in question.lower():
                found_ward = ward
                break
        
        if found_ward:
            # If we found a ward, assume it's a risk query
            return self._handle_risk_query((found_ward,))
        
        # Check for keywords to provide better suggestions
        keywords_suggestions = {
            'weather': "Try asking: 'What's the forecast for Mumbai?' or 'Show weather prediction'",
            'team': "Try asking: 'Show available resources' or 'How many rescue teams?'",
            'emergency': "Try asking: 'Show emergency contacts' or 'What's the emergency number?'",
            'map': "Try asking: 'Show risk map' or 'Display evacuation routes'",
            'alert': "Try asking: 'What's the current status?' or 'Show active alerts'"
        }
        
        suggestion = None
        for keyword, sug in keywords_suggestions.items():
            if keyword in question.lower():
                suggestion = sug
                break
        
        return {
            'intent': 'unknown',
            'answer': "I'm not sure I understand that question. " + (suggestion if suggestion else "Could you rephrase it or try one of these examples?"),
            'data': {
                'original_question': question,
                'detected_keywords': [k for k in keywords_suggestions.keys() if k in question.lower()],
                'suggestions': [
                    "What's the risk in Kurla?",
                    "Show evacuation routes from Bandra",
                    "Forecast for next 7 days",
                    "What's the current situation?",
                    "Show emergency contacts",
                    "Type 'help' to see all commands"
                ]
            },
            'confidence': 0.0
        }
    
    def _handle_resource_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle resource availability queries"""
        ward = entities[0] if entities else 'Mumbai'
        
        import random
        
        return {
            'intent': 'resource_query',
            'answer': f"Resource availability in {ward.title()}:",
            'data': {
                'ward': ward,
                'rescue_teams': {
                    'total': random.randint(20, 50),
                    'available': random.randint(10, 30),
                    'deployed': random.randint(5, 20),
                    'types': ['Fire Brigade', 'Medical', 'Search & Rescue', 'Police']
                },
                'equipment': {
                    'boats': random.randint(5, 15),
                    'ambulances': random.randint(10, 25),
                    'fire_trucks': random.randint(5, 12),
                    'helicopters': random.randint(1, 3)
                },
                'supplies': {
                    'food_packets': random.randint(1000, 5000),
                    'water_bottles': random.randint(2000, 10000),
                    'medical_kits': random.randint(100, 500),
                    'blankets': random.randint(500, 2000)
                },
                'shelters': {
                    'total': random.randint(10, 25),
                    'capacity': random.randint(5000, 15000),
                    'occupied': random.randint(1000, 8000)
                }
            },
            'suggestions': [
                "Request additional resources if needed",
                "Check resource distribution",
                "Monitor supply levels"
            ],
            'confidence': 0.87
        }
    
    def _handle_shelter_query(self, entities: tuple) -> Dict[str, Any]:
        """Handle shelter-related queries"""
        location = entities[0] if entities else 'your location'
        
        import random
        
        shelters = []
        for i in range(1, 4):
            shelters.append({
                'name': f'Emergency Shelter {chr(64+i)}',
                'distance': f'{random.uniform(1, 8):.1f} km',
                'capacity': random.randint(1000, 5000),
                'occupied': random.randint(100, 3000),
                'facilities': random.sample(['Medical', 'Food', 'Water', 'Sanitation', 'Power', 'Communication'], 4),
                'status': random.choice(['Open', 'Nearly Full', 'Available'])
            })
        
        return {
            'intent': 'shelter_query',
            'answer': f"Nearest emergency shelters from {location.title()}:",
            'data': {
                'location': location,
                'shelters': shelters,
                'total_capacity': sum(s['capacity'] for s in shelters),
                'total_occupied': sum(s['occupied'] for s in shelters),
                'recommendation': shelters[0]['name'] + ' (closest with good availability)'
            },
            'suggestions': [
                "Bring essential documents and supplies",
                "Register at shelter upon arrival",
                "Follow shelter guidelines",
                "Keep emergency contacts handy"
            ],
            'confidence': 0.89
        }
    
    def _handle_contact_query(self) -> Dict[str, Any]:
        """Handle emergency contact queries"""
        return {
            'intent': 'contact_query',
            'answer': "Emergency contact numbers for Mumbai:",
            'data': {
                'emergency_services': [
                    {'service': 'Emergency (Ambulance)', 'number': '108', 'available': '24/7'},
                    {'service': 'Police', 'number': '100', 'available': '24/7'},
                    {'service': 'Fire Brigade', 'number': '101', 'available': '24/7'},
                    {'service': 'Disaster Management', 'number': '1916', 'available': '24/7'},
                    {'service': 'Women Helpline', 'number': '1091', 'available': '24/7'}
                ],
                'municipal_services': [
                    {'service': 'BMC Control Room', 'number': '1916', 'available': '24/7'},
                    {'service': 'Mumbai Traffic Police', 'number': '103', 'available': '24/7'},
                    {'service': 'Railway Helpline', 'number': '139', 'available': '24/7'}
                ],
                'important_info': [
                    'Save these numbers in your phone',
                    'Keep phone charged during emergencies',
                    'Provide clear location when calling',
                    'Stay calm and speak clearly'
                ]
            },
            'suggestions': [
                "Save all emergency numbers",
                "Share with family members",
                "Keep a printed copy"
            ],
            'confidence': 1.0
        }
    
    def _translate_response(self, response: Dict, language: str) -> Dict:
        """Translate response to requested language"""
        # Simplified translation (in production, use proper translation API)
        translations = {
            'hindi': {
                'The current risk level': 'वर्तमान जोखिम स्तर',
                'HIGH': 'उच्च',
                'MODERATE': 'मध्यम',
                'LOW': 'कम',
                'For evacuation from': 'से निकासी के लिए',
                'Safe Zone': 'सुरक्षित क्षेत्र'
            },
            'marathi': {
                'The current risk level': 'सध्याचा धोका पातळी',
                'HIGH': 'उच्च',
                'MODERATE': 'मध्यम',
                'LOW': 'कम',
                'For evacuation from': 'पासून बाहेर काढण्यासाठी',
                'Safe Zone': 'सुरक्षित क्षेत्र'
            }
        }
        
        if language in translations:
            # Simple word replacement (in production, use proper NLP translation)
            answer = response['answer']
            for eng, trans in translations[language].items():
                answer = answer.replace(eng, trans)
            response['answer'] = answer
            response['translated'] = True
            response['language'] = language
        
        return response
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.context = {}
