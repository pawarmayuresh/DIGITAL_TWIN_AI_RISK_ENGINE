"""
CSP (Constraint Satisfaction Problem) API Routes
Exposes all CSP types for disaster management visualization
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from backend.core.csp.csp_solver import (
    solve_all_csp_types,
    DisasterResourceAllocationCSP,
    EvacuationSchedulingCSP,
    ShelterAssignmentCSP,
    RouteSelectionCSP
)

router = APIRouter(prefix="/api/csp", tags=["csp"])


class CSPScenarioRequest(BaseModel):
    scenario: str = "flood"
    num_teams: int = 8
    num_zones: int = 3


@router.get("/solve-all")
async def solve_all_csp(scenario: str = "flood"):
    """
    Solve all CSP types for a disaster scenario
    Returns solutions for:
    1. Resource Allocation CSP
    2. Evacuation Scheduling CSP
    3. Shelter Assignment CSP
    4. Route Selection CSP
    """
    try:
        results = solve_all_csp_types(scenario)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource-allocation")
async def solve_resource_allocation(
    num_teams: int = 8
):
    """
    Solve Resource Allocation CSP
    Allocate rescue teams to disaster zones
    """
    try:
        zones = [
            {'id': 'Z1', 'priority': 5, 'severity': 0.9, 'people': 150},
            {'id': 'Z2', 'priority': 3, 'severity': 0.6, 'people': 80},
            {'id': 'Z3', 'priority': 4, 'severity': 0.7, 'people': 120}
        ]
        
        csp = DisasterResourceAllocationCSP(num_teams, zones)
        result = csp.solve()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evacuation-scheduling")
async def solve_evacuation_scheduling():
    """
    Solve Evacuation Scheduling CSP
    Schedule evacuation times for different areas
    """
    try:
        areas = [
            {'id': 'A1', 'risk': 0.8, 'x': 0, 'y': 0, 'population': 500},
            {'id': 'A2', 'risk': 0.6, 'x': 1, 'y': 0, 'population': 300},
            {'id': 'A3', 'risk': 0.9, 'x': 0, 'y': 1, 'population': 600},
            {'id': 'A4', 'risk': 0.4, 'x': 2, 'y': 2, 'population': 200}
        ]
        
        time_slots = ['T0_immediate', 'T1_1hour', 'T2_2hours', 'T3_3hours']
        
        csp = EvacuationSchedulingCSP(areas, time_slots)
        result = csp.solve()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/shelter-assignment")
async def solve_shelter_assignment():
    """
    Solve Shelter Assignment CSP
    Assign evacuees to shelters
    """
    try:
        evacuee_groups = [
            {'id': 'G1', 'size': 200, 'special_needs': False, 'location': 'A1'},
            {'id': 'G2', 'size': 150, 'special_needs': True, 'location': 'A2'},
            {'id': 'G3', 'size': 180, 'special_needs': False, 'location': 'A3'},
            {'id': 'G4', 'size': 100, 'special_needs': False, 'location': 'A4'}
        ]
        
        shelters = [
            {'id': 'S1', 'capacity': 300, 'medical_facility': True},
            {'id': 'S2', 'capacity': 250, 'medical_facility': False},
            {'id': 'S3', 'capacity': 200, 'medical_facility': True}
        ]
        
        csp = ShelterAssignmentCSP(evacuee_groups, shelters)
        result = csp.solve()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/route-selection")
async def solve_route_selection():
    """
    Solve Route Selection CSP
    Select evacuation routes for different areas
    """
    try:
        areas = ['A1', 'A2', 'A3', 'A4']
        
        routes = [
            {'id': 'R1', 'risk': 0.3, 'capacity': 2, 'distance': 5},
            {'id': 'R2', 'risk': 0.4, 'capacity': 3, 'distance': 7},
            {'id': 'R3', 'risk': 0.2, 'capacity': 2, 'distance': 6}
        ]
        
        csp = RouteSelectionCSP(areas, routes)
        result = csp.solve()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_csp_info():
    """
    Get information about CSP formulation in the system
    """
    return {
        "csp_formulation": {
            "description": "Constraint Satisfaction Problem (CSP) formulation for disaster management",
            "components": {
                "variables": "Decision variables (X₁, X₂, ..., Xₙ) representing choices to be made",
                "domains": "Possible values each variable can take (D₁, D₂, ..., Dₙ)",
                "constraints": "Rules that must be satisfied (hard) or optimized (soft)"
            }
        },
        "csp_types": [
            {
                "name": "Resource Allocation CSP",
                "description": "Allocate rescue teams to disaster zones",
                "variables": "team_i → zone_j assignments",
                "constraints": [
                    "Each zone must have at least 1 team (hard)",
                    "High priority zones need ≥2 teams (hard)",
                    "Minimize total distance (soft)"
                ]
            },
            {
                "name": "Evacuation Scheduling CSP",
                "description": "Schedule evacuation times for different areas",
                "variables": "area_i → time_slot_j assignments",
                "constraints": [
                    "High risk areas evacuate first (hard)",
                    "Adjacent areas can't evacuate simultaneously (hard)",
                    "Minimize total evacuation time (soft)"
                ]
            },
            {
                "name": "Shelter Assignment CSP",
                "description": "Assign evacuees to shelters",
                "variables": "group_i → shelter_j assignments",
                "constraints": [
                    "Shelter capacity limits (hard)",
                    "Special needs groups to equipped shelters (hard)",
                    "Minimize distance (soft)"
                ]
            },
            {
                "name": "Route Selection CSP",
                "description": "Select evacuation routes for areas",
                "variables": "area_i → route_j assignments",
                "constraints": [
                    "Route safety requirements (hard)",
                    "Route capacity limits (hard)",
                    "Minimize total distance (soft)"
                ]
            }
        ],
        "solving_algorithm": {
            "name": "Backtracking Search with MRV Heuristic",
            "description": "Systematic search with Minimum Remaining Values heuristic",
            "features": [
                "Forward checking for constraint propagation",
                "MRV (Minimum Remaining Values) variable ordering",
                "Backtracking when constraints violated",
                "Soft constraint optimization"
            ]
        }
    }
