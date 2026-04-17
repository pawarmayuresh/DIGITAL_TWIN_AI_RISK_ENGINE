"""
Constraint Satisfaction Problem (CSP) Solver
Demonstrates different types of CSP in disaster management
"""
import numpy as np
from typing import Dict, List, Any, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
import random


@dataclass
class Variable:
    """CSP Variable"""
    name: str
    domain: List[Any]
    value: Any = None


@dataclass
class Constraint:
    """CSP Constraint"""
    name: str
    variables: List[str]
    constraint_type: str  # 'hard' or 'soft'
    check_function: Any
    weight: float = 1.0


class CSPSolver:
    """Base CSP Solver"""
    
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.constraints: List[Constraint] = []
        self.solution: Dict[str, Any] = {}
        self.iterations = 0
        self.backtracks = 0
        
    def add_variable(self, name: str, domain: List[Any]):
        """Add a variable to the CSP"""
        self.variables[name] = Variable(name, domain)
    
    def add_constraint(self, name: str, variables: List[str], 
                      constraint_type: str, check_function, weight: float = 1.0):
        """Add a constraint to the CSP"""
        self.constraints.append(Constraint(
            name, variables, constraint_type, check_function, weight
        ))
    
    def is_consistent(self, assignment: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Check if assignment satisfies all hard constraints"""
        violated = []
        
        for constraint in self.constraints:
            if constraint.constraint_type == 'hard':
                # Check if all variables in constraint are assigned
                if all(var in assignment for var in constraint.variables):
                    values = [assignment[var] for var in constraint.variables]
                    if not constraint.check_function(*values):
                        violated.append(constraint.name)
        
        return len(violated) == 0, violated
    
    def calculate_soft_constraint_score(self, assignment: Dict[str, Any]) -> float:
        """Calculate score for soft constraints (higher is better)"""
        score = 0.0
        
        for constraint in self.constraints:
            if constraint.constraint_type == 'soft':
                if all(var in assignment for var in constraint.variables):
                    values = [assignment[var] for var in constraint.variables]
                    if constraint.check_function(*values):
                        score += constraint.weight
        
        return score
    
    def backtracking_search(self) -> Dict[str, Any]:
        """Solve CSP using backtracking"""
        self.iterations = 0
        self.backtracks = 0
        return self._backtrack({})
    
    def _backtrack(self, assignment: Dict[str, Any]) -> Dict[str, Any]:
        """Recursive backtracking"""
        self.iterations += 1
        
        # Check if assignment is complete
        if len(assignment) == len(self.variables):
            return assignment
        
        # Select unassigned variable
        var = self._select_unassigned_variable(assignment)
        
        # Try each value in domain
        for value in self._order_domain_values(var, assignment):
            assignment[var] = value
            
            # Check consistency
            is_consistent, _ = self.is_consistent(assignment)
            
            if is_consistent:
                result = self._backtrack(assignment)
                if result is not None:
                    return result
            
            # Backtrack
            del assignment[var]
            self.backtracks += 1
        
        return None
    
    def _select_unassigned_variable(self, assignment: Dict[str, Any]) -> str:
        """Select next variable to assign (MRV heuristic)"""
        unassigned = [v for v in self.variables if v not in assignment]
        
        if not unassigned:
            return None
        
        # Minimum Remaining Values heuristic
        return min(unassigned, key=lambda v: len(self.variables[v].domain))
    
    def _order_domain_values(self, var: str, assignment: Dict[str, Any]) -> List[Any]:
        """Order domain values (Least Constraining Value heuristic)"""
        return self.variables[var].domain


class DisasterResourceAllocationCSP(CSPSolver):
    """
    CSP Type 1: Resource Allocation Problem
    Allocate rescue teams to disaster zones
    """
    
    def __init__(self, num_teams: int, zones: List[Dict]):
        super().__init__()
        self.num_teams = num_teams
        self.zones = zones
        self._setup_problem()
    
    def _setup_problem(self):
        """Setup resource allocation CSP"""
        # Variables: team_i → zone_j
        for i in range(self.num_teams):
            zone_ids = [z['id'] for z in self.zones]
            self.add_variable(f'team_{i}', zone_ids)
        
        # Hard Constraint 1: Each zone must have at least 1 team
        for zone in self.zones:
            self.add_constraint(
                f'zone_{zone["id"]}_coverage',
                [f'team_{i}' for i in range(self.num_teams)],
                'hard',
                lambda *assignments, zid=zone['id']: zid in assignments,
                weight=1.0
            )
        
        # Hard Constraint 2: High priority zones need more teams
        for zone in self.zones:
            if zone['priority'] >= 4:
                self.add_constraint(
                    f'zone_{zone["id"]}_priority',
                    [f'team_{i}' for i in range(self.num_teams)],
                    'hard',
                    lambda *assignments, zid=zone['id']: assignments.count(zid) >= 2,
                    weight=1.0
                )
        
        # Soft Constraint: Minimize total distance
        self.add_constraint(
            'minimize_distance',
            [f'team_{i}' for i in range(self.num_teams)],
            'soft',
            lambda *assignments: sum(1 for _ in assignments) > 0,  # Placeholder
            weight=0.5
        )
    
    def solve(self) -> Dict[str, Any]:
        """Solve resource allocation CSP"""
        solution = self.backtracking_search()
        
        if solution:
            # Calculate statistics
            zone_coverage = {}
            for zone in self.zones:
                zone_coverage[zone['id']] = sum(
                    1 for team, assigned_zone in solution.items() 
                    if assigned_zone == zone['id']
                )
            
            return {
                'type': 'Resource Allocation CSP',
                'status': 'solved',
                'solution': solution,
                'zone_coverage': zone_coverage,
                'iterations': self.iterations,
                'backtracks': self.backtracks,
                'constraints_satisfied': len(self.constraints)
            }
        
        return {
            'type': 'Resource Allocation CSP',
            'status': 'no_solution',
            'iterations': self.iterations,
            'backtracks': self.backtracks
        }


class EvacuationSchedulingCSP(CSPSolver):
    """
    CSP Type 2: Scheduling Problem
    Schedule evacuation times for different areas
    """
    
    def __init__(self, areas: List[Dict], time_slots: List[str]):
        super().__init__()
        self.areas = areas
        self.time_slots = time_slots
        self._setup_problem()
    
    def _setup_problem(self):
        """Setup scheduling CSP"""
        # Variables: area_i → time_slot_j
        for area in self.areas:
            self.add_variable(f'area_{area["id"]}', self.time_slots)
        
        # Hard Constraint 1: High risk areas must evacuate first
        high_risk_areas = [a for a in self.areas if a['risk'] > 0.7]
        for area in high_risk_areas:
            self.add_constraint(
                f'area_{area["id"]}_urgent',
                [f'area_{area["id"]}'],
                'hard',
                lambda time: time in self.time_slots[:2],  # First 2 slots
                weight=1.0
            )
        
        # Hard Constraint 2: Adjacent areas can't evacuate simultaneously
        for i, area1 in enumerate(self.areas):
            for area2 in self.areas[i+1:]:
                if self._are_adjacent(area1, area2):
                    self.add_constraint(
                        f'adjacent_{area1["id"]}_{area2["id"]}',
                        [f'area_{area1["id"]}', f'area_{area2["id"]}'],
                        'hard',
                        lambda t1, t2: t1 != t2,
                        weight=1.0
                    )
        
        # Soft Constraint: Minimize total evacuation time
        self.add_constraint(
            'minimize_time',
            [f'area_{a["id"]}' for a in self.areas],
            'soft',
            lambda *times: all(t in self.time_slots[:3] for t in times),
            weight=0.8
        )
    
    def _are_adjacent(self, area1: Dict, area2: Dict) -> bool:
        """Check if two areas are adjacent"""
        # Simple distance check
        return abs(area1.get('x', 0) - area2.get('x', 0)) <= 1 and \
               abs(area1.get('y', 0) - area2.get('y', 0)) <= 1
    
    def solve(self) -> Dict[str, Any]:
        """Solve scheduling CSP"""
        solution = self.backtracking_search()
        
        if solution:
            # Group by time slot
            schedule = {}
            for time_slot in self.time_slots:
                schedule[time_slot] = [
                    area.replace('area_', '') 
                    for area, time in solution.items() 
                    if time == time_slot
                ]
            
            return {
                'type': 'Evacuation Scheduling CSP',
                'status': 'solved',
                'solution': solution,
                'schedule': schedule,
                'iterations': self.iterations,
                'backtracks': self.backtracks
            }
        
        return {
            'type': 'Evacuation Scheduling CSP',
            'status': 'no_solution',
            'iterations': self.iterations,
            'backtracks': self.backtracks
        }


class ShelterAssignmentCSP(CSPSolver):
    """
    CSP Type 3: Assignment Problem
    Assign evacuees to shelters
    """
    
    def __init__(self, evacuee_groups: List[Dict], shelters: List[Dict]):
        super().__init__()
        self.evacuee_groups = evacuee_groups
        self.shelters = shelters
        self._setup_problem()
    
    def _setup_problem(self):
        """Setup assignment CSP"""
        # Variables: group_i → shelter_j
        for group in self.evacuee_groups:
            shelter_ids = [s['id'] for s in self.shelters]
            self.add_variable(f'group_{group["id"]}', shelter_ids)
        
        # Hard Constraint 1: Shelter capacity
        for shelter in self.shelters:
            self.add_constraint(
                f'shelter_{shelter["id"]}_capacity',
                [f'group_{g["id"]}' for g in self.evacuee_groups],
                'hard',
                lambda *assignments, sid=shelter['id'], cap=shelter['capacity']: 
                    sum(g['size'] for g, a in zip(self.evacuee_groups, assignments) if a == sid) <= cap,
                weight=1.0
            )
        
        # Hard Constraint 2: Special needs groups to equipped shelters
        for group in self.evacuee_groups:
            if group.get('special_needs', False):
                equipped_shelters = [s['id'] for s in self.shelters if s.get('medical_facility', False)]
                self.add_constraint(
                    f'group_{group["id"]}_special_needs',
                    [f'group_{group["id"]}'],
                    'hard',
                    lambda shelter, eq=equipped_shelters: shelter in eq,
                    weight=1.0
                )
        
        # Soft Constraint: Minimize distance
        self.add_constraint(
            'minimize_distance',
            [f'group_{g["id"]}' for g in self.evacuee_groups],
            'soft',
            lambda *assignments: len(set(assignments)) <= len(self.shelters),
            weight=0.6
        )
    
    def solve(self) -> Dict[str, Any]:
        """Solve assignment CSP"""
        solution = self.backtracking_search()
        
        if solution:
            # Calculate shelter utilization
            utilization = {}
            for shelter in self.shelters:
                assigned = sum(
                    g['size'] for g in self.evacuee_groups
                    if solution.get(f'group_{g["id"]}') == shelter['id']
                )
                utilization[shelter['id']] = {
                    'assigned': assigned,
                    'capacity': shelter['capacity'],
                    'percentage': (assigned / shelter['capacity'] * 100) if shelter['capacity'] > 0 else 0
                }
            
            return {
                'type': 'Shelter Assignment CSP',
                'status': 'solved',
                'solution': solution,
                'utilization': utilization,
                'iterations': self.iterations,
                'backtracks': self.backtracks
            }
        
        return {
            'type': 'Shelter Assignment CSP',
            'status': 'no_solution',
            'iterations': self.iterations,
            'backtracks': self.backtracks
        }


class RouteSelectionCSP(CSPSolver):
    """
    CSP Type 4: Path Selection Problem
    Select evacuation routes for different areas
    """
    
    def __init__(self, areas: List[str], routes: List[Dict]):
        super().__init__()
        self.areas = areas
        self.routes = routes
        self._setup_problem()
    
    def _setup_problem(self):
        """Setup route selection CSP"""
        # Variables: area_i → route_j
        for area in self.areas:
            route_ids = [r['id'] for r in self.routes]
            self.add_variable(f'area_{area}', route_ids)
        
        # Hard Constraint 1: Route safety
        for area in self.areas:
            safe_routes = [r['id'] for r in self.routes if r['risk'] < 0.5]
            self.add_constraint(
                f'area_{area}_safety',
                [f'area_{area}'],
                'hard',
                lambda route, safe=safe_routes: route in safe,
                weight=1.0
            )
        
        # Hard Constraint 2: Route capacity
        for route in self.routes:
            self.add_constraint(
                f'route_{route["id"]}_capacity',
                [f'area_{a}' for a in self.areas],
                'hard',
                lambda *assignments, rid=route['id'], cap=route['capacity']: 
                    assignments.count(rid) <= cap,
                weight=1.0
            )
        
        # Soft Constraint: Minimize total distance
        self.add_constraint(
            'minimize_distance',
            [f'area_{a}' for a in self.areas],
            'soft',
            lambda *assignments: len(set(assignments)) >= 2,  # Use multiple routes
            weight=0.7
        )
    
    def solve(self) -> Dict[str, Any]:
        """Solve route selection CSP"""
        solution = self.backtracking_search()
        
        if solution:
            # Calculate route usage
            route_usage = {}
            for route in self.routes:
                areas_using = [
                    area.replace('area_', '') 
                    for area, assigned_route in solution.items() 
                    if assigned_route == route['id']
                ]
                route_usage[route['id']] = {
                    'areas': areas_using,
                    'count': len(areas_using),
                    'capacity': route['capacity'],
                    'risk': route['risk']
                }
            
            return {
                'type': 'Route Selection CSP',
                'status': 'solved',
                'solution': solution,
                'route_usage': route_usage,
                'iterations': self.iterations,
                'backtracks': self.backtracks
            }
        
        return {
            'type': 'Route Selection CSP',
            'status': 'no_solution',
            'iterations': self.iterations,
            'backtracks': self.backtracks
        }


def solve_all_csp_types(scenario: str = 'flood') -> Dict[str, Any]:
    """
    Solve all CSP types for a disaster scenario
    """
    results = {
        'scenario': scenario,
        'timestamp': datetime.now().isoformat(),
        'csp_problems': []
    }
    
    # 1. Resource Allocation CSP
    zones = [
        {'id': 'Z1', 'priority': 5, 'severity': 0.9, 'people': 150},
        {'id': 'Z2', 'priority': 3, 'severity': 0.6, 'people': 80},
        {'id': 'Z3', 'priority': 4, 'severity': 0.7, 'people': 120}
    ]
    resource_csp = DisasterResourceAllocationCSP(num_teams=8, zones=zones)
    results['csp_problems'].append(resource_csp.solve())
    
    # 2. Evacuation Scheduling CSP
    areas = [
        {'id': 'A1', 'risk': 0.8, 'x': 0, 'y': 0, 'population': 500},
        {'id': 'A2', 'risk': 0.6, 'x': 1, 'y': 0, 'population': 300},
        {'id': 'A3', 'risk': 0.9, 'x': 0, 'y': 1, 'population': 600},
        {'id': 'A4', 'risk': 0.4, 'x': 2, 'y': 2, 'population': 200}
    ]
    time_slots = ['T0_immediate', 'T1_1hour', 'T2_2hours', 'T3_3hours']
    scheduling_csp = EvacuationSchedulingCSP(areas, time_slots)
    results['csp_problems'].append(scheduling_csp.solve())
    
    # 3. Shelter Assignment CSP
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
    assignment_csp = ShelterAssignmentCSP(evacuee_groups, shelters)
    results['csp_problems'].append(assignment_csp.solve())
    
    # 4. Route Selection CSP
    areas_list = ['A1', 'A2', 'A3', 'A4']
    routes = [
        {'id': 'R1', 'risk': 0.3, 'capacity': 2, 'distance': 5},
        {'id': 'R2', 'risk': 0.4, 'capacity': 3, 'distance': 7},
        {'id': 'R3', 'risk': 0.2, 'capacity': 2, 'distance': 6}
    ]
    route_csp = RouteSelectionCSP(areas_list, routes)
    results['csp_problems'].append(route_csp.solve())
    
    # Summary statistics
    results['summary'] = {
        'total_problems': len(results['csp_problems']),
        'solved': sum(1 for p in results['csp_problems'] if p['status'] == 'solved'),
        'total_iterations': sum(p.get('iterations', 0) for p in results['csp_problems']),
        'total_backtracks': sum(p.get('backtracks', 0) for p in results['csp_problems'])
    }
    
    return results
