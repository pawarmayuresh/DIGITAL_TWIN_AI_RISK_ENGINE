"""
Advanced Inference Engine with Multiple Reasoning Strategies
Implements: Abductive, Analogical, Case-Based, Fuzzy, Probabilistic, and Temporal Reasoning
"""
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import random


@dataclass
class Case:
    """Represents a case for case-based reasoning"""
    id: str
    features: Dict[str, float]
    solution: str
    outcome: str
    similarity_score: float = 0.0


@dataclass
class TemporalFact:
    """Fact with temporal information"""
    fact: str
    timestamp: datetime
    duration: Optional[int] = None  # Duration in minutes
    confidence: float = 1.0


class AdvancedInferenceEngine:
    """
    Advanced inference engine with multiple reasoning strategies
    """
    
    def __init__(self):
        self.case_base = []
        self.temporal_facts = []
        self.fuzzy_rules = []
        self.probabilistic_network = {}
        self.reasoning_history = []
        self.current_strategy = "forward_chaining"
        
    # ============================================================================
    # 1. ABDUCTIVE REASONING - Find best explanation for observations
    # ============================================================================
    
    def abductive_reasoning(self, observations: List[str], hypotheses: List[Dict]) -> Dict:
        """
        Abductive Reasoning: Given observations, find the best explanation
        
        Example: 
        Observations: ["high_water_level", "heavy_rainfall", "flooded_streets"]
        Hypotheses: [
            {"name": "monsoon_flood", "explains": [...], "prior": 0.6},
            {"name": "dam_breach", "explains": [...], "prior": 0.2}
        ]
        """
        self.reasoning_history.append({
            "strategy": "abductive",
            "timestamp": datetime.now().isoformat()
        })
        
        scored_hypotheses = []
        
        for hypothesis in hypotheses:
            # Calculate how well hypothesis explains observations
            explained = set(hypothesis.get("explains", []))
            observed = set(observations)
            
            # Coverage: How many observations are explained
            coverage = len(explained.intersection(observed)) / len(observed) if observed else 0
            
            # Parsimony: Prefer simpler explanations (fewer assumptions)
            parsimony = 1.0 / (1.0 + len(hypothesis.get("assumptions", [])))
            
            # Prior probability
            prior = hypothesis.get("prior", 0.5)
            
            # Combined score
            score = (coverage * 0.5) + (parsimony * 0.2) + (prior * 0.3)
            
            scored_hypotheses.append({
                "hypothesis": hypothesis["name"],
                "score": score,
                "coverage": coverage,
                "parsimony": parsimony,
                "prior": prior,
                "explanation": hypothesis.get("description", ""),
                "confidence": score
            })
        
        # Sort by score
        scored_hypotheses.sort(key=lambda x: x["score"], reverse=True)
        
        best_hypothesis = scored_hypotheses[0] if scored_hypotheses else None
        
        return {
            "reasoning_type": "abductive",
            "observations": observations,
            "best_explanation": best_hypothesis,
            "all_hypotheses": scored_hypotheses,
            "reasoning": f"Best explanation for {len(observations)} observations"
        }
    
    # ============================================================================
    # 2. ANALOGICAL REASONING - Reason by similarity to past cases
    # ============================================================================
    
    def analogical_reasoning(self, current_situation: Dict, past_cases: List[Dict]) -> Dict:
        """
        Analogical Reasoning: Find similar past cases and apply their solutions
        
        Example:
        Current: {"rainfall": 80, "water_level": 2.5, "ward": "Kurla"}
        Past cases: [{"rainfall": 75, "water_level": 2.3, "solution": "evacuate"}]
        """
        self.reasoning_history.append({
            "strategy": "analogical",
            "timestamp": datetime.now().isoformat()
        })
        
        if not past_cases:
            return {
                "reasoning_type": "analogical",
                "similar_cases": [],
                "recommended_solution": "No similar cases found"
            }
        
        # Calculate similarity for each past case
        similar_cases = []
        
        for case in past_cases:
            similarity = self._calculate_similarity(current_situation, case)
            
            similar_cases.append({
                "case_id": case.get("id", "unknown"),
                "similarity": similarity,
                "features": case.get("features", {}),
                "solution": case.get("solution", ""),
                "outcome": case.get("outcome", ""),
                "confidence": similarity
            })
        
        # Sort by similarity
        similar_cases.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Get top 3 most similar cases
        top_cases = similar_cases[:3]
        
        # Recommend solution from most similar case
        recommended_solution = top_cases[0]["solution"] if top_cases else "No recommendation"
        
        return {
            "reasoning_type": "analogical",
            "current_situation": current_situation,
            "most_similar_case": top_cases[0] if top_cases else None,
            "top_similar_cases": top_cases,
            "recommended_solution": recommended_solution,
            "reasoning": f"Based on {len(top_cases)} similar past cases"
        }
    
    def _calculate_similarity(self, case1: Dict, case2: Dict) -> float:
        """Calculate similarity between two cases using weighted Euclidean distance"""
        features1 = case1.get("features", case1)
        features2 = case2.get("features", case2)
        
        common_keys = set(features1.keys()).intersection(set(features2.keys()))
        
        if not common_keys:
            return 0.0
        
        # Calculate normalized distance
        distances = []
        for key in common_keys:
            v1 = features1[key]
            v2 = features2[key]
            
            # Normalize by max value
            max_val = max(abs(v1), abs(v2), 1.0)
            dist = abs(v1 - v2) / max_val
            distances.append(dist)
        
        # Average distance
        avg_distance = sum(distances) / len(distances)
        
        # Convert to similarity (1 - distance)
        similarity = 1.0 - avg_distance
        
        return max(0.0, min(1.0, similarity))
    
    # ============================================================================
    # 3. FUZZY REASONING - Handle imprecise/vague information
    # ============================================================================
    
    def fuzzy_reasoning(self, crisp_values: Dict[str, float]) -> Dict:
        """
        Fuzzy Reasoning: Handle vague concepts like "high", "medium", "low"
        
        Example:
        Input: {"rainfall": 65, "water_level": 2.3}
        Output: Fuzzy memberships and defuzzified risk score
        """
        self.reasoning_history.append({
            "strategy": "fuzzy",
            "timestamp": datetime.now().isoformat()
        })
        
        fuzzy_sets = {}
        
        # Fuzzify each input
        for variable, value in crisp_values.items():
            if variable == "rainfall":
                fuzzy_sets["rainfall"] = self._fuzzify_rainfall(value)
            elif variable == "water_level":
                fuzzy_sets["water_level"] = self._fuzzify_water_level(value)
            elif variable == "traffic_density":
                fuzzy_sets["traffic_density"] = self._fuzzify_traffic(value)
            elif variable == "temperature":
                fuzzy_sets["temperature"] = self._fuzzify_temperature(value)
        
        # Apply fuzzy rules
        fuzzy_risk = self._apply_fuzzy_rules(fuzzy_sets)
        
        # Defuzzify to get crisp risk score
        crisp_risk = self._defuzzify_risk(fuzzy_risk)
        
        return {
            "reasoning_type": "fuzzy",
            "crisp_inputs": crisp_values,
            "fuzzy_memberships": fuzzy_sets,
            "fuzzy_risk": fuzzy_risk,
            "crisp_risk_score": crisp_risk,
            "risk_level": self._risk_level_from_score(crisp_risk),
            "reasoning": "Fuzzy logic handles imprecise measurements"
        }
    
    def _fuzzify_rainfall(self, value: float) -> Dict[str, float]:
        """Convert rainfall to fuzzy memberships"""
        return {
            "low": max(0, min(1, (30 - value) / 30)) if value < 30 else 0,
            "medium": max(0, min((value - 20) / 30, (80 - value) / 30)) if 20 <= value <= 80 else 0,
            "high": max(0, min((value - 50) / 50, 1)) if value > 50 else 0,
            "extreme": max(0, min((value - 100) / 50, 1)) if value > 100 else 0
        }
    
    def _fuzzify_water_level(self, value: float) -> Dict[str, float]:
        """Convert water level to fuzzy memberships"""
        return {
            "low": max(0, min(1, (1.0 - value) / 1.0)) if value < 1.0 else 0,
            "medium": max(0, min((value - 0.5) / 1.0, (2.0 - value) / 1.0)) if 0.5 <= value <= 2.0 else 0,
            "high": max(0, min((value - 1.5) / 1.0, (3.5 - value) / 1.0)) if 1.5 <= value <= 3.5 else 0,
            "critical": max(0, min((value - 3.0) / 1.0, 1)) if value > 3.0 else 0
        }
    
    def _fuzzify_traffic(self, value: float) -> Dict[str, float]:
        """Convert traffic density to fuzzy memberships"""
        return {
            "light": max(0, min(1, (0.3 - value) / 0.3)) if value < 0.3 else 0,
            "moderate": max(0, min((value - 0.2) / 0.3, (0.7 - value) / 0.3)) if 0.2 <= value <= 0.7 else 0,
            "heavy": max(0, min((value - 0.5) / 0.3, 1)) if value > 0.5 else 0
        }
    
    def _fuzzify_temperature(self, value: float) -> Dict[str, float]:
        """Convert temperature to fuzzy memberships"""
        return {
            "cold": max(0, min(1, (20 - value) / 10)) if value < 20 else 0,
            "normal": max(0, min((value - 15) / 10, (35 - value) / 10)) if 15 <= value <= 35 else 0,
            "hot": max(0, min((value - 30) / 10, (45 - value) / 10)) if 30 <= value <= 45 else 0,
            "extreme": max(0, min((value - 40) / 10, 1)) if value > 40 else 0
        }
    
    def _apply_fuzzy_rules(self, fuzzy_sets: Dict) -> Dict[str, float]:
        """Apply fuzzy inference rules"""
        risk_levels = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        # Rule 1: IF rainfall is high AND water_level is high THEN risk is high
        if "rainfall" in fuzzy_sets and "water_level" in fuzzy_sets:
            activation = min(
                fuzzy_sets["rainfall"].get("high", 0),
                fuzzy_sets["water_level"].get("high", 0)
            )
            risk_levels["high"] = max(risk_levels["high"], activation)
        
        # Rule 2: IF rainfall is extreme OR water_level is critical THEN risk is critical
        if "rainfall" in fuzzy_sets and "water_level" in fuzzy_sets:
            activation = max(
                fuzzy_sets["rainfall"].get("extreme", 0),
                fuzzy_sets["water_level"].get("critical", 0)
            )
            risk_levels["critical"] = max(risk_levels["critical"], activation)
        
        # Rule 3: IF rainfall is medium AND water_level is medium THEN risk is medium
        if "rainfall" in fuzzy_sets and "water_level" in fuzzy_sets:
            activation = min(
                fuzzy_sets["rainfall"].get("medium", 0),
                fuzzy_sets["water_level"].get("medium", 0)
            )
            risk_levels["medium"] = max(risk_levels["medium"], activation)
        
        # Rule 4: IF traffic is heavy AND risk is high THEN risk is critical
        if "traffic_density" in fuzzy_sets:
            traffic_heavy = fuzzy_sets["traffic_density"].get("heavy", 0)
            if traffic_heavy > 0.5 and risk_levels["high"] > 0.5:
                risk_levels["critical"] = max(risk_levels["critical"], 0.8)
        
        # Rule 5: IF temperature is extreme THEN risk is high
        if "temperature" in fuzzy_sets:
            temp_extreme = fuzzy_sets["temperature"].get("extreme", 0)
            risk_levels["high"] = max(risk_levels["high"], temp_extreme)
        
        return risk_levels
    
    def _defuzzify_risk(self, fuzzy_risk: Dict[str, float]) -> float:
        """Convert fuzzy risk to crisp value using centroid method"""
        # Define centroids for each risk level
        centroids = {"low": 0.2, "medium": 0.5, "high": 0.75, "critical": 0.95}
        
        numerator = sum(fuzzy_risk[level] * centroids[level] for level in fuzzy_risk)
        denominator = sum(fuzzy_risk.values())
        
        if denominator == 0:
            return 0.2  # Default low risk
        
        return numerator / denominator
    
    def _risk_level_from_score(self, score: float) -> str:
        """Convert risk score to level"""
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    # ============================================================================
    # 4. PROBABILISTIC REASONING - Bayesian inference
    # ============================================================================
    
    def probabilistic_reasoning(self, evidence: Dict[str, bool], network: Dict) -> Dict:
        """
        Probabilistic Reasoning: Bayesian inference
        
        Example:
        Evidence: {"heavy_rain": True, "high_tide": True}
        Network: Bayesian network structure with conditional probabilities
        """
        self.reasoning_history.append({
            "strategy": "probabilistic",
            "timestamp": datetime.now().isoformat()
        })
        
        # Simple Bayesian inference (simplified for demonstration)
        # P(Flood | Evidence) = P(Evidence | Flood) * P(Flood) / P(Evidence)
        
        # Prior probabilities
        p_flood = network.get("prior_flood", 0.3)
        p_fire = network.get("prior_fire", 0.1)
        p_contamination = network.get("prior_contamination", 0.05)
        
        # Likelihood of evidence given each disaster
        p_evidence_given_flood = 1.0
        p_evidence_given_fire = 1.0
        p_evidence_given_contamination = 1.0
        p_evidence_given_none = 1.0
        
        for key, value in evidence.items():
            if key == "heavy_rain" and value:
                p_evidence_given_flood *= 0.9
                p_evidence_given_fire *= 0.2
                p_evidence_given_contamination *= 0.3
                p_evidence_given_none *= 0.1
            elif key == "high_temperature" and value:
                p_evidence_given_flood *= 0.2
                p_evidence_given_fire *= 0.9
                p_evidence_given_contamination *= 0.3
                p_evidence_given_none *= 0.3
            elif key == "chemical_smell" and value:
                p_evidence_given_flood *= 0.1
                p_evidence_given_fire *= 0.3
                p_evidence_given_contamination *= 0.9
                p_evidence_given_none *= 0.05
        
        # Calculate posterior probabilities (unnormalized)
        p_flood_given_evidence = p_evidence_given_flood * p_flood
        p_fire_given_evidence = p_evidence_given_fire * p_fire
        p_contamination_given_evidence = p_evidence_given_contamination * p_contamination
        p_none_given_evidence = p_evidence_given_none * (1 - p_flood - p_fire - p_contamination)
        
        # Normalize
        total = p_flood_given_evidence + p_fire_given_evidence + p_contamination_given_evidence + p_none_given_evidence
        
        if total > 0:
            p_flood_given_evidence /= total
            p_fire_given_evidence /= total
            p_contamination_given_evidence /= total
            p_none_given_evidence /= total
        
        # Determine most likely disaster
        probabilities = {
            "flood": p_flood_given_evidence,
            "fire": p_fire_given_evidence,
            "contamination": p_contamination_given_evidence,
            "none": p_none_given_evidence
        }
        
        most_likely = max(probabilities.items(), key=lambda x: x[1])
        
        return {
            "reasoning_type": "probabilistic",
            "evidence": evidence,
            "posterior_probabilities": probabilities,
            "most_likely_disaster": most_likely[0],
            "confidence": most_likely[1],
            "reasoning": "Bayesian inference from observed evidence"
        }
    
    # ============================================================================
    # 5. TEMPORAL REASONING - Reason about time and sequences
    # ============================================================================
    
    def temporal_reasoning(self, events: List[Dict]) -> Dict:
        """
        Temporal Reasoning: Analyze sequences and time-based patterns
        
        Example:
        Events: [
            {"event": "rainfall_started", "time": "10:00", "duration": 120},
            {"event": "water_rising", "time": "11:30", "duration": 60}
        ]
        """
        self.reasoning_history.append({
            "strategy": "temporal",
            "timestamp": datetime.now().isoformat()
        })
        
        if not events:
            return {
                "reasoning_type": "temporal",
                "patterns": [],
                "predictions": []
            }
        
        # Sort events by time
        sorted_events = sorted(events, key=lambda x: x.get("time", ""))
        
        # Detect patterns
        patterns = []
        
        # Pattern 1: Cause-effect sequences
        for i in range(len(sorted_events) - 1):
            event1 = sorted_events[i]
            event2 = sorted_events[i + 1]
            
            # Check if event2 follows event1 within reasonable time
            time_diff = self._calculate_time_diff(event1.get("time"), event2.get("time"))
            
            if time_diff < 120:  # Within 2 hours
                patterns.append({
                    "type": "causal_sequence",
                    "cause": event1.get("event"),
                    "effect": event2.get("event"),
                    "time_gap_minutes": time_diff,
                    "confidence": 0.8
                })
        
        # Pattern 2: Concurrent events
        concurrent = []
        for i in range(len(sorted_events)):
            for j in range(i + 1, len(sorted_events)):
                event1 = sorted_events[i]
                event2 = sorted_events[j]
                
                time_diff = self._calculate_time_diff(event1.get("time"), event2.get("time"))
                
                if time_diff < 15:  # Within 15 minutes
                    concurrent.append({
                        "events": [event1.get("event"), event2.get("event")],
                        "time_gap_minutes": time_diff
                    })
        
        if concurrent:
            patterns.append({
                "type": "concurrent_events",
                "events": concurrent,
                "confidence": 0.9
            })
        
        # Make predictions based on patterns
        predictions = []
        
        if patterns:
            last_event = sorted_events[-1]
            
            # Predict next event based on causal patterns
            for pattern in patterns:
                if pattern.get("type") == "causal_sequence":
                    if pattern["cause"] == last_event.get("event"):
                        predictions.append({
                            "predicted_event": pattern["effect"],
                            "expected_time_minutes": pattern["time_gap_minutes"],
                            "confidence": pattern["confidence"]
                        })
        
        return {
            "reasoning_type": "temporal",
            "events_analyzed": len(events),
            "temporal_patterns": patterns,
            "predictions": predictions,
            "reasoning": f"Analyzed {len(events)} events for temporal patterns"
        }
    
    def _calculate_time_diff(self, time1: str, time2: str) -> int:
        """Calculate time difference in minutes"""
        try:
            # Simple HH:MM format
            h1, m1 = map(int, time1.split(":"))
            h2, m2 = map(int, time2.split(":"))
            
            minutes1 = h1 * 60 + m1
            minutes2 = h2 * 60 + m2
            
            return abs(minutes2 - minutes1)
        except:
            return 0
    
    # ============================================================================
    # 6. META-REASONING - Reason about reasoning strategies
    # ============================================================================
    
    def meta_reasoning(self, problem_characteristics: Dict) -> Dict:
        """
        Meta-Reasoning: Choose the best reasoning strategy for the problem
        
        Example:
        Characteristics: {
            "has_past_cases": True,
            "has_uncertainty": True,
            "has_temporal_data": False
        }
        """
        self.reasoning_history.append({
            "strategy": "meta",
            "timestamp": datetime.now().isoformat()
        })
        
        strategy_scores = {
            "abductive": 0.0,
            "analogical": 0.0,
            "fuzzy": 0.0,
            "probabilistic": 0.0,
            "temporal": 0.0
        }
        
        # Score each strategy based on problem characteristics
        if problem_characteristics.get("has_past_cases"):
            strategy_scores["analogical"] += 0.8
        
        if problem_characteristics.get("has_uncertainty"):
            strategy_scores["fuzzy"] += 0.7
            strategy_scores["probabilistic"] += 0.6
        
        if problem_characteristics.get("has_temporal_data"):
            strategy_scores["temporal"] += 0.9
        
        if problem_characteristics.get("needs_explanation"):
            strategy_scores["abductive"] += 0.8
        
        if problem_characteristics.get("has_vague_concepts"):
            strategy_scores["fuzzy"] += 0.9
        
        if problem_characteristics.get("has_probabilities"):
            strategy_scores["probabilistic"] += 0.9
        
        # Recommend top strategies
        sorted_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommended = sorted_strategies[0] if sorted_strategies else ("forward_chaining", 0.5)
        
        return {
            "reasoning_type": "meta",
            "problem_characteristics": problem_characteristics,
            "strategy_scores": strategy_scores,
            "recommended_strategy": recommended[0],
            "confidence": recommended[1],
            "all_strategies": sorted_strategies,
            "reasoning": f"Recommended {recommended[0]} based on problem characteristics"
        }
    
    # ============================================================================
    # 7. HYBRID REASONING - Combine multiple strategies
    # ============================================================================
    
    def hybrid_reasoning(self, data: Dict, strategies: List[str] = None) -> Dict:
        """
        Hybrid Reasoning: Combine multiple reasoning strategies
        
        Automatically selects and combines appropriate strategies
        """
        if strategies is None:
            # Auto-select strategies based on data
            strategies = self._auto_select_strategies(data)
        
        self.reasoning_history.append({
            "strategy": "hybrid",
            "sub_strategies": strategies,
            "timestamp": datetime.now().isoformat()
        })
        
        results = {}
        
        # Apply each strategy
        for strategy in strategies:
            if strategy == "fuzzy" and any(k in data for k in ["rainfall", "water_level", "traffic_density"]):
                results["fuzzy"] = self.fuzzy_reasoning(data)
            
            elif strategy == "probabilistic":
                # Convert data to evidence
                evidence = {
                    "heavy_rain": data.get("rainfall", 0) > 50,
                    "high_temperature": data.get("temperature", 25) > 35,
                    "chemical_smell": data.get("chemical_level", 0) > 0.5
                }
                results["probabilistic"] = self.probabilistic_reasoning(evidence, {})
            
            elif strategy == "temporal" and "events" in data:
                results["temporal"] = self.temporal_reasoning(data["events"])
        
        # Combine results
        combined_risk = self._combine_risk_scores(results)
        
        return {
            "reasoning_type": "hybrid",
            "strategies_used": strategies,
            "individual_results": results,
            "combined_risk_score": combined_risk,
            "risk_level": self._risk_level_from_score(combined_risk),
            "reasoning": f"Combined {len(strategies)} reasoning strategies"
        }
    
    def _auto_select_strategies(self, data: Dict) -> List[str]:
        """Automatically select appropriate strategies based on data"""
        strategies = []
        
        if any(k in data for k in ["rainfall", "water_level", "traffic_density", "temperature"]):
            strategies.append("fuzzy")
        
        if any(k in data for k in ["rainfall", "temperature", "chemical_level"]):
            strategies.append("probabilistic")
        
        if "events" in data:
            strategies.append("temporal")
        
        return strategies if strategies else ["fuzzy"]
    
    def _combine_risk_scores(self, results: Dict) -> float:
        """Combine risk scores from multiple strategies"""
        scores = []
        weights = []
        
        if "fuzzy" in results:
            scores.append(results["fuzzy"].get("crisp_risk_score", 0.5))
            weights.append(0.4)
        
        if "probabilistic" in results:
            # Use max probability as risk indicator
            probs = results["probabilistic"].get("posterior_probabilities", {})
            max_prob = max(probs.values()) if probs else 0.5
            scores.append(max_prob)
            weights.append(0.3)
        
        if "temporal" in results:
            # Use number of predictions as risk indicator
            predictions = results["temporal"].get("predictions", [])
            temporal_risk = min(len(predictions) * 0.2, 0.9)
            scores.append(temporal_risk)
            weights.append(0.3)
        
        if not scores:
            return 0.5
        
        # Weighted average
        total_weight = sum(weights)
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def get_reasoning_history(self) -> List[Dict]:
        """Get history of reasoning strategies used"""
        return self.reasoning_history
    
    def clear_history(self):
        """Clear reasoning history"""
        self.reasoning_history = []
    
    def get_strategy_statistics(self) -> Dict:
        """Get statistics on strategy usage"""
        strategy_counts = {}
        
        for entry in self.reasoning_history:
            strategy = entry.get("strategy", "unknown")
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return {
            "total_inferences": len(self.reasoning_history),
            "strategy_counts": strategy_counts,
            "most_used_strategy": max(strategy_counts.items(), key=lambda x: x[1])[0] if strategy_counts else None
        }
