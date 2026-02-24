"""
Infrastructure-Evacuation Integration - BATCH 6
Connects infrastructure health to evacuation decisions
"""
from typing import Dict, List, Optional
from backend.core.infrastructure.bayesian_network import InfrastructureBayesianNetwork


class InfrastructureEvacuationIntegrator:
    """Integrates infrastructure state with evacuation system"""
    
    def __init__(self, network: InfrastructureBayesianNetwork):
        self.network = network
    
    def get_ward_infrastructure_impact(self, ward_id: str) -> Dict:
        """Get infrastructure impact on evacuation for a ward"""
        ward_nodes = self.network.get_nodes_by_ward(ward_id)
        
        if not ward_nodes:
            return {
                "ward_id": ward_id,
                "infrastructure_available": False,
                "evacuation_priority": "NORMAL",
                "risk_multiplier": 1.0,
                "affected_services": []
            }
        
        # Calculate aggregate health
        avg_health = sum(n.get_health_score() for n in ward_nodes) / len(ward_nodes)
        avg_risk = sum(n.get_risk_score() for n in ward_nodes) / len(ward_nodes)
        
        # Identify critical failures
        critical_services = []
        hospital_failed = False
        emergency_failed = False
        power_failed = False
        
        for node in ward_nodes:
            if node.get_risk_score() > 50:
                critical_services.append({
                    "service": node.node_id,
                    "type": node.node_type,
                    "risk": node.get_risk_score()
                })
                
                if node.node_type == "Healthcare":
                    hospital_failed = True
                elif node.node_type == "Emergency":
                    emergency_failed = True
                elif node.node_type == "Utility" and "Power" in node.node_id:
                    power_failed = True
        
        # Determine evacuation priority
        if hospital_failed or emergency_failed:
            priority = "CRITICAL"
            risk_multiplier = 1.5
        elif power_failed or avg_risk > 60:
            priority = "HIGH"
            risk_multiplier = 1.3
        elif avg_risk > 40:
            priority = "ELEVATED"
            risk_multiplier = 1.1
        else:
            priority = "NORMAL"
            risk_multiplier = 1.0
        
        # Generate recommendations
        recommendations = []
        if hospital_failed:
            recommendations.append("⚠️ Hospital at risk - prioritize medical evacuations")
        if emergency_failed:
            recommendations.append("🚨 Emergency services compromised - dispatch more rescue vehicles")
        if power_failed:
            recommendations.append("⚡ Power grid failure - evacuation routes may be dark")
        if avg_health < 50:
            recommendations.append("🏗️ Critical infrastructure failure - increase evacuation urgency")
        
        return {
            "ward_id": ward_id,
            "infrastructure_available": True,
            "avg_health": avg_health,
            "avg_risk": avg_risk,
            "evacuation_priority": priority,
            "risk_multiplier": risk_multiplier,
            "critical_services": critical_services,
            "hospital_operational": not hospital_failed,
            "emergency_services_operational": not emergency_failed,
            "power_available": not power_failed,
            "recommendations": recommendations,
            "total_nodes": len(ward_nodes)
        }
    
    def get_evacuation_route_safety(self, grid_ids: List[str]) -> Dict:
        """Assess safety of evacuation route based on infrastructure"""
        # Map grid IDs to wards (simplified - in production use proper mapping)
        route_safety = {
            "overall_safety": 1.0,
            "hazards": [],
            "safe_segments": 0,
            "risky_segments": 0
        }
        
        # Check if route passes through areas with failed infrastructure
        for grid_id in grid_ids:
            # Extract ward from grid (simplified)
            # In production, use proper grid-to-ward mapping
            pass
        
        return route_safety
    
    def should_increase_evacuation_resources(self, ward_id: str) -> Dict:
        """Determine if more evacuation resources needed based on infrastructure"""
        impact = self.get_ward_infrastructure_impact(ward_id)
        
        additional_cars = 0
        additional_agents = 0
        
        if impact["evacuation_priority"] == "CRITICAL":
            additional_cars = 3
            additional_agents = 10
        elif impact["evacuation_priority"] == "HIGH":
            additional_cars = 2
            additional_agents = 5
        elif impact["evacuation_priority"] == "ELEVATED":
            additional_cars = 1
            additional_agents = 3
        
        return {
            "ward_id": ward_id,
            "needs_additional_resources": additional_cars > 0 or additional_agents > 0,
            "additional_cars": additional_cars,
            "additional_agents": additional_agents,
            "reason": f"Infrastructure priority: {impact['evacuation_priority']}",
            "infrastructure_impact": impact
        }
    
    def get_safe_evacuation_zones(self) -> List[str]:
        """Get list of wards with operational infrastructure suitable for evacuation"""
        safe_zones = []
        
        # Group nodes by ward
        ward_health = {}
        for node in self.network.nodes.values():
            if node.ward not in ward_health:
                ward_health[node.ward] = []
            ward_health[node.ward].append(node.get_health_score())
        
        # Identify safe wards
        for ward, health_scores in ward_health.items():
            avg_health = sum(health_scores) / len(health_scores)
            if avg_health > 70:  # 70% threshold for safe zone
                safe_zones.append(ward)
        
        return safe_zones
    
    def get_infrastructure_status_for_grid(self, grid_id: str) -> Dict:
        """Get infrastructure status affecting a specific grid"""
        # Simplified - in production, implement proper grid-to-infrastructure mapping
        return {
            "grid_id": grid_id,
            "power_available": True,
            "water_available": True,
            "emergency_services_nearby": True,
            "hospital_accessible": True,
            "infrastructure_risk": 0.2
        }
