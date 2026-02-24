"""
Natural Language Explainer - Converts structured explanations to natural language
"""
from typing import Dict, Any, List


class NaturalLanguageExplainer:
    """Generates natural language explanations from structured XAI data"""
    
    def _detect_disaster_type(self, features: Dict[str, float]) -> str:
        """Detect disaster type from features"""
        feature_keys = set(features.keys())
        
        # Check for specific disaster indicators
        if 'fire_intensity' in feature_keys or 'temperature' in feature_keys:
            return 'fire'
        elif 'wind_speed' in feature_keys or 'cyclone_category' in feature_keys:
            return 'cyclone'
        elif 'contamination_level' in feature_keys or 'toxicity' in feature_keys:
            return 'contamination'
        elif 'policy_effectiveness' in feature_keys or 'compliance_rate' in feature_keys:
            return 'policy'
        elif 'water_level' in feature_keys or 'rainfall' in feature_keys:
            return 'flood'
        else:
            return 'general'
    
    def explain_risk_decision(
        self,
        ward_id: str,
        risk_score: float,
        features: Dict[str, float],
        feature_contributions: Dict[str, float],
        action: str
    ) -> str:
        """Generate natural language explanation for risk decision"""
        
        # Detect disaster type
        disaster_type = self._detect_disaster_type(features)
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "HIGH"
            urgency = "immediate"
        elif risk_score >= 0.4:
            risk_level = "MEDIUM"
            urgency = "elevated"
        else:
            risk_level = "LOW"
            urgency = "minimal"
        
        # Find top contributors
        sorted_contributions = sorted(
            feature_contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        top_factors = sorted_contributions[:3]
        
        # Build explanation
        explanation_parts = []
        
        # Opening statement with disaster-specific language
        disaster_labels = {
            'flood': 'flood risk',
            'fire': 'fire hazard',
            'cyclone': 'cyclone threat',
            'contamination': 'contamination risk',
            'policy': 'policy compliance risk',
            'general': 'risk level'
        }
        
        explanation_parts.append(
            f"Ward {ward_id} has a {risk_level} {disaster_labels.get(disaster_type, 'risk')} "
            f"(score: {risk_score:.2f}) requiring {urgency} attention."
        )
        
        # Primary factors
        if top_factors:
            factor_texts = []
            for feature, contribution in top_factors:
                feature_value = features.get(feature, 0)
                factor_texts.append(self._explain_feature(feature, feature_value, contribution))
            
            explanation_parts.append(
                f"This assessment is primarily driven by {', '.join(factor_texts)}."
            )
        
        # Recommended action with disaster-specific guidance
        action_guidance = {
            'flood': {
                'EVACUATION_REQUIRED': "Evacuation is recommended because flood probability exceeds safe thresholds.",
                'MONITOR_CLOSELY': "Continuous monitoring is advised as water levels may rise.",
                'default': "Current flood conditions are within acceptable parameters."
            },
            'fire': {
                'EVACUATION_REQUIRED': "Immediate evacuation required due to fire spread risk.",
                'MONITOR_CLOSELY': "Fire watch protocols should be activated.",
                'default': "Fire risk is currently manageable with standard precautions."
            },
            'cyclone': {
                'EVACUATION_REQUIRED': "Evacuation to cyclone shelters is strongly advised.",
                'MONITOR_CLOSELY': "Cyclone tracking and preparation measures should be intensified.",
                'default': "Cyclone threat is minimal; maintain standard preparedness."
            },
            'contamination': {
                'EVACUATION_REQUIRED': "Area evacuation needed due to hazardous contamination levels.",
                'MONITOR_CLOSELY': "Contamination monitoring and containment protocols active.",
                'default': "Contamination levels are within safe limits."
            },
            'policy': {
                'EVACUATION_REQUIRED': "Critical policy violations require immediate intervention.",
                'MONITOR_CLOSELY': "Policy compliance requires enhanced oversight.",
                'default': "Policy implementation is proceeding as expected."
            },
            'general': {
                'EVACUATION_REQUIRED': "Evacuation recommended due to elevated risk levels.",
                'MONITOR_CLOSELY': "Continuous monitoring is advised as conditions may deteriorate.",
                'default': "Current conditions are within acceptable parameters."
            }
        }
        
        disaster_actions = action_guidance.get(disaster_type, action_guidance['general'])
        explanation_parts.append(disaster_actions.get(action, disaster_actions['default']))
        
        return " ".join(explanation_parts)
    
    def _explain_feature(
        self,
        feature_name: str,
        value: float,
        contribution: float
    ) -> str:
        """Explain a single feature's contribution"""
        
        feature_descriptions = {
            # Flood features
            "water_level": f"water level of {value:.2f}m",
            "rainfall": f"rainfall intensity of {value:.1f}mm/hr",
            
            # Fire features
            "fire_intensity": f"fire intensity level {value:.1f}",
            "temperature": f"temperature of {value:.1f}°C",
            "humidity": f"humidity at {value:.1f}%",
            "wind_speed": f"wind speed of {value:.1f} km/h",
            
            # Cyclone features
            "cyclone_category": f"cyclone category {int(value)}",
            "wind_velocity": f"wind velocity {value:.1f} km/h",
            "storm_surge": f"storm surge of {value:.2f}m",
            
            # Contamination features
            "contamination_level": f"contamination level {value:.2f}",
            "toxicity": f"toxicity index {value:.2f}",
            "air_quality_index": f"AQI of {value:.0f}",
            
            # Policy features
            "policy_effectiveness": f"policy effectiveness {value:.1%}",
            "compliance_rate": f"compliance rate {value:.1%}",
            "implementation_score": f"implementation score {value:.2f}",
            
            # Common features
            "population_density": f"population density of {int(value)} people",
            "risk_score": f"baseline risk of {value:.2f}",
            "infrastructure": "infrastructure condition",
            "vulnerability_index": f"vulnerability index {value:.2f}"
        }
        
        description = feature_descriptions.get(feature_name, feature_name)
        
        if contribution > 0.3:
            impact = "significantly elevated"
        elif contribution > 0.15:
            impact = "moderately elevated"
        else:
            impact = "slightly elevated"
        
        return f"{description} ({impact} risk)"
    
    def explain_counterfactual(
        self,
        counterfactual_data: Dict[str, Any]
    ) -> str:
        """Generate natural language explanation for counterfactual"""
        
        if not counterfactual_data.get("success"):
            return "No viable counterfactual scenario could be identified with the given constraints."
        
        changes = counterfactual_data["changes"]
        original_risk = counterfactual_data["original_output"].get("risk_score", 0)
        new_risk = counterfactual_data["counterfactual_output"].get("risk_score", 0)
        risk_reduction = original_risk - new_risk
        
        explanation_parts = []
        
        # Opening
        explanation_parts.append(
            f"To reduce risk from {original_risk:.2f} to {new_risk:.2f} "
            f"(a {risk_reduction:.2f} reduction), the following changes would be needed:"
        )
        
        # List changes with disaster-specific interventions
        for feature, change_info in changes.items():
            original = change_info["original"]
            modified = change_info["modified"]
            
            # Flood interventions
            if feature == "water_level":
                explanation_parts.append(
                    f"• Reduce water level from {original:.2f}m to {modified:.2f}m "
                    f"(achievable through improved drainage or pumping)"
                )
            elif feature == "rainfall":
                explanation_parts.append(
                    f"• If rainfall decreases from {original:.1f}mm/hr to {modified:.1f}mm/hr "
                    f"(natural weather variation)"
                )
            
            # Fire interventions
            elif feature == "fire_intensity":
                explanation_parts.append(
                    f"• Reduce fire intensity from {original:.1f} to {modified:.1f} "
                    f"(through firefighting operations and containment)"
                )
            elif feature == "temperature":
                explanation_parts.append(
                    f"• Lower temperature from {original:.1f}°C to {modified:.1f}°C "
                    f"(cooling measures and fire suppression)"
                )
            
            # Cyclone interventions
            elif feature == "wind_speed" or feature == "wind_velocity":
                explanation_parts.append(
                    f"• If wind speed reduces from {original:.1f} to {modified:.1f} km/h "
                    f"(natural cyclone weakening)"
                )
            elif feature == "storm_surge":
                explanation_parts.append(
                    f"• Reduce storm surge from {original:.2f}m to {modified:.2f}m "
                    f"(through coastal barriers)"
                )
            
            # Contamination interventions
            elif feature == "contamination_level":
                explanation_parts.append(
                    f"• Reduce contamination from {original:.2f} to {modified:.2f} "
                    f"(through decontamination and cleanup operations)"
                )
            elif feature == "toxicity":
                explanation_parts.append(
                    f"• Lower toxicity from {original:.2f} to {modified:.2f} "
                    f"(neutralization and remediation)"
                )
            
            # Policy interventions
            elif feature == "policy_effectiveness":
                explanation_parts.append(
                    f"• Improve policy effectiveness from {original:.1%} to {modified:.1%} "
                    f"(through better implementation and enforcement)"
                )
            elif feature == "compliance_rate":
                explanation_parts.append(
                    f"• Increase compliance from {original:.1%} to {modified:.1%} "
                    f"(through education and incentives)"
                )
            
            # Common interventions
            elif feature == "population_density":
                people_to_evacuate = int(abs(original - modified))
                explanation_parts.append(
                    f"• Evacuate approximately {people_to_evacuate} people "
                    f"to reduce population density"
                )
            else:
                # Generic change description
                explanation_parts.append(
                    f"• Adjust {feature} from {original:.2f} to {modified:.2f}"
                )
        
        # Conclusion
        explanation_parts.append(
            "These interventions would bring the area to a safer risk level."
        )
        
        return "\n".join(explanation_parts)
    
    def explain_path_selection(
        self,
        path_data: Dict[str, Any]
    ) -> str:
        """Generate natural language explanation for path selection"""
        
        path_length = path_data.get("path_length", 0)
        safety_score = path_data.get("safety_score", 0)
        high_risk_avoided = path_data.get("high_risk_avoided", 0)
        
        explanation_parts = []
        
        # Path characteristics
        explanation_parts.append(
            f"The selected evacuation route spans {path_length} grid zones "
            f"with an overall safety score of {safety_score:.2f}."
        )
        
        # Safety features
        if high_risk_avoided > 0:
            explanation_parts.append(
                f"This path successfully avoids {high_risk_avoided} high-risk flood zones, "
                f"prioritizing evacuee safety over route length."
            )
        
        # Recommendation
        if safety_score > 0.8:
            explanation_parts.append(
                "This is a highly safe evacuation route with minimal flood exposure."
            )
        elif safety_score > 0.6:
            explanation_parts.append(
                "This route provides adequate safety while maintaining reasonable travel distance."
            )
        else:
            explanation_parts.append(
                "This route has some risk exposure; alternative paths should be considered if available."
            )
        
        return " ".join(explanation_parts)
    
    def explain_uncertainty(
        self,
        uncertainty_data: Dict[str, Any]
    ) -> str:
        """Generate natural language explanation for uncertainty analysis"""
        
        mean_pred = uncertainty_data.get("mean_prediction", 0)
        confidence = uncertainty_data.get("confidence_score", 0)
        ci = uncertainty_data.get("confidence_interval_95", {})
        
        explanation_parts = []
        
        # Main prediction
        explanation_parts.append(
            f"The predicted risk level is {mean_pred:.2f} with "
            f"{confidence*100:.0f}% confidence."
        )
        
        # Confidence interval
        if ci:
            explanation_parts.append(
                f"Based on {uncertainty_data.get('num_simulations', 0)} simulations, "
                f"we are 95% confident the true risk lies between "
                f"{ci.get('lower', 0):.2f} and {ci.get('upper', 0):.2f}."
            )
        
        # Interpretation
        interpretation = uncertainty_data.get("interpretation", "")
        if interpretation:
            explanation_parts.append(interpretation)
        
        return " ".join(explanation_parts)
    
    def generate_summary_report(
        self,
        ward_id: str,
        risk_data: Dict[str, Any],
        counterfactual: Dict[str, Any] = None,
        uncertainty: Dict[str, Any] = None,
        disaster_type: str = None  # Add explicit disaster_type parameter
    ) -> str:
        """Generate comprehensive summary report"""
        
        report_sections = []
        
        # Use explicit disaster type if provided, otherwise detect from features
        features = risk_data.get("features", {})
        if disaster_type is None:
            disaster_type = features.get('_disaster_type') or self._detect_disaster_type(features)
        
        disaster_titles = {
            'flood': 'FLOOD RISK ANALYSIS',
            'fire': 'FIRE HAZARD ASSESSMENT',
            'cyclone': 'CYCLONE THREAT ANALYSIS',
            'contamination': 'CONTAMINATION RISK REPORT',
            'policy': 'POLICY COMPLIANCE ANALYSIS',
            'general': 'RISK ASSESSMENT'
        }
        
        # Title
        report_sections.append(
            f"=== {disaster_titles.get(disaster_type, 'RISK ANALYSIS')} REPORT: Ward {ward_id} ===\n"
        )
        
        # Risk assessment
        report_sections.append("RISK ASSESSMENT:")
        report_sections.append(self.explain_risk_decision(
            ward_id=ward_id,
            risk_score=risk_data.get("risk_score", 0),
            features=risk_data.get("features", {}),
            feature_contributions=risk_data.get("feature_contributions", {}),
            action=risk_data.get("action", "MONITOR")
        ))
        report_sections.append("")
        
        # Counterfactual
        if counterfactual:
            report_sections.append("MITIGATION STRATEGIES:")
            report_sections.append(self.explain_counterfactual(counterfactual))
            report_sections.append("")
        
        # Uncertainty
        if uncertainty:
            report_sections.append("CONFIDENCE ASSESSMENT:")
            report_sections.append(self.explain_uncertainty(uncertainty))
            report_sections.append("")
        
        return "\n".join(report_sections)


# Global instance
nl_explainer = NaturalLanguageExplainer()
