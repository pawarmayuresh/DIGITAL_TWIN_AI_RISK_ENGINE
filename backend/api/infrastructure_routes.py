"""
Infrastructure API Routes - Probabilistic Bayesian Network
Implements all 6 batches
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
import pandas as pd
import os

from backend.core.infrastructure.probabilistic_node import ProbabilisticNode
from backend.core.infrastructure.bayesian_network import InfrastructureBayesianNetwork
from backend.core.infrastructure.cascading_failure import CascadingFailureEngine
from backend.core.infrastructure.temporal_model import DynamicBayesianNetwork
from backend.core.infrastructure.evacuation_integration import InfrastructureEvacuationIntegrator

router = APIRouter(prefix="/api/infrastructure", tags=["infrastructure"])

# Global instances
network: Optional[InfrastructureBayesianNetwork] = None
cascade_engine: Optional[CascadingFailureEngine] = None
temporal_model: Optional[DynamicBayesianNetwork] = None
integrator: Optional[InfrastructureEvacuationIntegrator] = None
evidence_data: Optional[pd.DataFrame] = None
current_evidence_index = 0


def initialize_network():
    """Initialize the Bayesian network from CSV data"""
    global network, cascade_engine, temporal_model, integrator, evidence_data
    
    if network is not None:
        return  # Already initialized
    
    network = InfrastructureBayesianNetwork()
    
    # Load nodes
    nodes_file = "data/mumbai/static/infrastructure_nodes_probabilistic.csv"
    if os.path.exists(nodes_file):
        df = pd.read_csv(nodes_file)
        for _, row in df.iterrows():
            node = ProbabilisticNode(
                node_id=row['Node'],
                node_type=row['Type'],
                p_healthy=row['Initial_Healthy'],
                p_degraded=row['Initial_Degraded'],
                p_failed=row['Initial_Failed'],
                latitude=row.get('Latitude', 0.0),
                longitude=row.get('Longitude', 0.0),
                ward=row.get('Ward', '')
            )
            network.add_node(node)
    
    # Load dependencies
    deps_file = "data/mumbai/static/infrastructure_dependencies.csv"
    if os.path.exists(deps_file):
        df = pd.read_csv(deps_file)
        for _, row in df.iterrows():
            network.add_dependency(row['Parent'], row['Child'], row['Influence_Weight'])
    
    # Initialize CPTs
    for node_id in network.nodes.keys():
        network.initialize_cpt(node_id)
    
    # Initialize cascade engine
    cascade_engine = CascadingFailureEngine(network, failure_threshold=0.6)
    
    # Initialize temporal model
    temporal_model = DynamicBayesianNetwork(network)
    
    # Initialize evacuation integrator
    integrator = InfrastructureEvacuationIntegrator(network)
    
    # Load evidence data
    evidence_file = "data/mumbai/realtime/infrastructure_evidence.csv"
    if os.path.exists(evidence_file):
        evidence_data = pd.read_csv(evidence_file)
    
    print(f"✅ Infrastructure network initialized: {len(network.nodes)} nodes, {sum(len(n.parents) for n in network.nodes.values())} dependencies")


@router.get("/network/status")
async def get_network_status():
    """Get current state of infrastructure network"""
    initialize_network()
    return network.get_network_state()


@router.get("/network/nodes")
async def get_all_nodes():
    """Get all infrastructure nodes"""
    initialize_network()
    return {
        "nodes": [node.to_dict() for node in network.nodes.values()],
        "total": len(network.nodes)
    }


@router.get("/network/node/{node_id}")
async def get_node_details(node_id: str):
    """Get detailed information about a specific node"""
    initialize_network()
    node = network.get_node_by_id(node_id)
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Get dependencies
    parents = [{"node_id": p.node_id, "weight": w} for p, w in node.parents]
    children = [{"node_id": c.node_id, "weight": w} for c, w in node.children]
    
    return {
        **node.to_dict(),
        "parents": parents,
        "children": children,
        "state_history": [s.value for s in node.state_history[-10:]]  # Last 10 states
    }


@router.get("/network/ward/{ward_id}")
async def get_ward_infrastructure(ward_id: str):
    """Get all infrastructure nodes in a ward"""
    initialize_network()
    nodes = network.get_nodes_by_ward(ward_id)
    
    return {
        "ward_id": ward_id,
        "nodes": [node.to_dict() for node in nodes],
        "total_nodes": len(nodes),
        "avg_health": sum(n.get_health_score() for n in nodes) / len(nodes) if nodes else 0,
        "avg_risk": sum(n.get_risk_score() for n in nodes) / len(nodes) if nodes else 0
    }


@router.post("/network/update")
async def update_network(evidence: Optional[Dict[str, float]] = None):
    """Update network with new evidence - BATCH 3"""
    initialize_network()
    
    # If no evidence provided, use next from time series
    global current_evidence_index
    if evidence is None and evidence_data is not None:
        if current_evidence_index < len(evidence_data):
            row = evidence_data.iloc[current_evidence_index]
            evidence = {
                "RainIntensity": row['RainIntensity'],
                "FloodLevel": row['FloodLevel'],
                "CyberAttack": row['CyberAttack'],
                "PowerStress": row.get('PowerStress', 0.0),
                "WaterStress": row.get('WaterStress', 0.0)
            }
            current_evidence_index = (current_evidence_index + 1) % len(evidence_data)
    
    # Update network
    network.update_network(evidence)
    
    # Check for cascading failures - BATCH 4
    cascade_result = cascade_engine.check_and_propagate_failures()
    
    return {
        "success": True,
        "timestep": network.timestep,
        "evidence": evidence,
        "network_state": network.get_network_state(),
        "cascade": cascade_result
    }


@router.get("/cascade/analysis")
async def get_cascade_analysis():
    """Get cascading failure analysis - BATCH 4"""
    initialize_network()
    
    vulnerability = cascade_engine.get_vulnerability_analysis()
    
    return {
        "vulnerability_analysis": vulnerability,
        "cascade_history": cascade_engine.cascade_history[-10:],  # Last 10 cascades
        "current_cascade": cascade_engine.current_cascade
    }


@router.post("/cascade/simulate/{node_id}")
async def simulate_node_failure(node_id: str):
    """Simulate failure of a specific node - BATCH 4"""
    initialize_network()
    
    result = cascade_engine.simulate_node_failure(node_id)
    
    return result


@router.get("/cascade/path/{node_id}")
async def get_cascade_path(node_id: str):
    """Get potential cascade path from a node"""
    initialize_network()
    
    path = cascade_engine.get_cascade_path(node_id)
    
    return {
        "start_node": node_id,
        "cascade_path": path,
        "path_length": len(path)
    }


@router.get("/prediction/node/{node_id}")
async def predict_node_future(node_id: str, steps: int = 5):
    """Predict future state of a node - BATCH 5"""
    initialize_network()
    
    predictions = temporal_model.predict_node_future(node_id, steps)
    
    return {
        "node_id": node_id,
        "current_timestep": network.timestep,
        "predictions": predictions
    }


@router.get("/prediction/network")
async def predict_network_future(steps: int = 5):
    """Predict future state of entire network - BATCH 5"""
    initialize_network()
    
    predictions = temporal_model.predict_network_future(steps)
    
    return predictions


@router.get("/prediction/collapse-risk")
async def get_collapse_risk():
    """Detect if network is heading towards collapse - BATCH 5"""
    initialize_network()
    
    risk_analysis = temporal_model.detect_collapse_risk()
    
    return risk_analysis


@router.post("/network/reset")
async def reset_network():
    """Reset network to initial state"""
    global network, cascade_engine, temporal_model, integrator, current_evidence_index
    
    network = None
    cascade_engine = None
    temporal_model = None
    integrator = None
    current_evidence_index = 0
    
    initialize_network()
    
    return {
        "success": True,
        "message": "Network reset to initial state"
    }


# ==================== EVACUATION INTEGRATION ENDPOINTS (BATCH 6) ====================

@router.get("/evacuation/ward-impact/{ward_id}")
async def get_ward_evacuation_impact(ward_id: str):
    """Get infrastructure impact on evacuation for a ward - BATCH 6"""
    initialize_network()
    
    impact = integrator.get_ward_infrastructure_impact(ward_id)
    
    return {
        "success": True,
        "ward_impact": impact
    }


@router.get("/evacuation/resource-needs/{ward_id}")
async def get_evacuation_resource_needs(ward_id: str):
    """Determine if additional evacuation resources needed - BATCH 6"""
    initialize_network()
    
    needs = integrator.should_increase_evacuation_resources(ward_id)
    
    return {
        "success": True,
        "resource_needs": needs
    }


@router.get("/evacuation/safe-zones")
async def get_safe_evacuation_zones():
    """Get wards with operational infrastructure suitable for evacuation - BATCH 6"""
    initialize_network()
    
    safe_zones = integrator.get_safe_evacuation_zones()
    
    # Get details for each safe zone
    zone_details = []
    for ward in safe_zones:
        nodes = network.get_nodes_by_ward(ward)
        if nodes:
            avg_health = sum(n.get_health_score() for n in nodes) / len(nodes)
            zone_details.append({
                "ward_id": ward,
                "avg_health": avg_health,
                "num_nodes": len(nodes),
                "status": "SAFE"
            })
    
    return {
        "success": True,
        "safe_zones": safe_zones,
        "zone_details": zone_details,
        "total_safe_zones": len(safe_zones)
    }


@router.get("/evacuation/grid-status/{grid_id}")
async def get_grid_infrastructure_status(grid_id: str):
    """Get infrastructure status for a specific grid - BATCH 6"""
    initialize_network()
    
    status = integrator.get_infrastructure_status_for_grid(grid_id)
    
    return {
        "success": True,
        "grid_status": status
    }


@router.get("/network/statistics")
async def get_network_statistics():
    """Get comprehensive network statistics"""
    initialize_network()
    
    # Node type distribution
    type_counts = {}
    type_health = {}
    
    for node in network.nodes.values():
        node_type = node.node_type
        if node_type not in type_counts:
            type_counts[node_type] = 0
            type_health[node_type] = []
        type_counts[node_type] += 1
        type_health[node_type].append(node.get_health_score())
    
    type_stats = {
        node_type: {
            "count": type_counts[node_type],
            "avg_health": sum(type_health[node_type]) / len(type_health[node_type])
        }
        for node_type in type_counts
    }
    
    return {
        "total_nodes": len(network.nodes),
        "total_dependencies": sum(len(n.parents) for n in network.nodes.values()),
        "timestep": network.timestep,
        "type_statistics": type_stats,
        "network_health": network.get_network_state()["average_health"],
        "network_risk": network.get_network_state()["average_risk"],
        "critical_nodes": network.get_network_state()["critical_nodes"]
    }
