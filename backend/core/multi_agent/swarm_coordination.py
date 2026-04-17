"""
Swarm Intelligence for Rescue Team Coordination
Uses particle swarm optimization and collective intelligence
"""
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RescueTeam:
    """Rescue team agent"""
    team_id: str
    position: Tuple[float, float]  # (x, y) coordinates
    capacity: int
    current_load: int
    velocity: Tuple[float, float]
    best_position: Tuple[float, float]
    best_score: float
    status: str  # 'idle', 'moving', 'rescuing', 'returning'


@dataclass
class DisasterZone:
    """Disaster zone requiring rescue"""
    zone_id: str
    position: Tuple[float, float]
    severity: float
    people_count: int
    priority: int


class SwarmRescueCoordinator:
    """Coordinates rescue teams using swarm intelligence"""
    
    def __init__(self, num_teams: int = 10):
        self.num_teams = num_teams
        self.teams: List[RescueTeam] = []
        self.disaster_zones: List[DisasterZone] = []
        self.global_best_position = (0.0, 0.0)
        self.global_best_score = float('inf')
        
        # PSO parameters
        self.w = 0.7  # Inertia weight
        self.c1 = 1.5  # Cognitive parameter
        self.c2 = 1.5  # Social parameter
        
        self.iteration = 0
        self.assignments = {}
    
    def initialize_teams(self, base_positions: List[Tuple[float, float]]):
        """Initialize rescue teams at base positions"""
        self.teams = []
        
        for i in range(self.num_teams):
            if i < len(base_positions):
                pos = base_positions[i]
            else:
                pos = (np.random.uniform(0, 100), np.random.uniform(0, 100))
            
            team = RescueTeam(
                team_id=f"TEAM-{i+1}",
                position=pos,
                capacity=50,
                current_load=0,
                velocity=(0.0, 0.0),
                best_position=pos,
                best_score=float('inf'),
                status='idle'
            )
            self.teams.append(team)
    
    def add_disaster_zone(self, zone: DisasterZone):
        """Add a disaster zone requiring rescue"""
        self.disaster_zones.append(zone)
    
    def optimize_team_deployment(self, max_iterations: int = 50) -> Dict[str, Any]:
        """Optimize rescue team deployment using PSO"""
        if not self.teams or not self.disaster_zones:
            return {'error': 'No teams or disaster zones defined'}
        
        convergence_history = []
        
        for iteration in range(max_iterations):
            self.iteration = iteration
            
            # Update each team
            for team in self.teams:
                # Calculate fitness (total rescue time + priority)
                fitness = self._calculate_fitness(team)
                
                # Update personal best
                if fitness < team.best_score:
                    team.best_score = fitness
                    team.best_position = team.position
                
                # Update global best
                if fitness < self.global_best_score:
                    self.global_best_score = fitness
                    self.global_best_position = team.position
                
                # Update velocity
                team.velocity = self._update_velocity(team)
                
                # Update position
                team.position = self._update_position(team)
            
            convergence_history.append(self.global_best_score)
            
            # Check convergence
            if iteration > 10 and abs(convergence_history[-1] - convergence_history[-5]) < 0.01:
                break
        
        # Generate final assignments
        self.assignments = self._generate_assignments()
        
        return {
            'status': 'optimized',
            'iterations': iteration + 1,
            'global_best_score': self.global_best_score,
            'convergence_history': convergence_history,
            'team_assignments': self.assignments,
            'total_teams': len(self.teams),
            'total_zones': len(self.disaster_zones),
            'estimated_completion_time': self._estimate_completion_time()
        }
    
    def coordinate_dynamic_response(self, new_zones: List[DisasterZone]) -> Dict[str, Any]:
        """Dynamically coordinate response to new disaster zones"""
        # Add new zones
        for zone in new_zones:
            self.add_disaster_zone(zone)
        
        # Reassign idle teams
        idle_teams = [t for t in self.teams if t.status == 'idle']
        
        reassignments = []
        for team in idle_teams:
            # Find nearest high-priority zone
            best_zone = self._find_best_zone_for_team(team)
            
            if best_zone:
                reassignments.append({
                    'team_id': team.team_id,
                    'assigned_zone': best_zone.zone_id,
                    'distance': self._calculate_distance(team.position, best_zone.position),
                    'eta_minutes': self._calculate_eta(team.position, best_zone.position)
                })
                
                team.status = 'moving'
        
        return {
            'new_zones_added': len(new_zones),
            'teams_reassigned': len(reassignments),
            'reassignments': reassignments,
            'remaining_idle_teams': len([t for t in self.teams if t.status == 'idle']),
            'timestamp': datetime.now().isoformat()
        }
    
    def simulate_swarm_behavior(self, steps: int = 10) -> List[Dict]:
        """Simulate swarm behavior over time"""
        simulation_steps = []
        
        for step in range(steps):
            step_data = {
                'step': step,
                'timestamp': datetime.now().isoformat(),
                'team_positions': [],
                'zone_coverage': [],
                'efficiency_score': 0.0
            }
            
            # Update each team
            for team in self.teams:
                # Move towards assigned zone
                if team.team_id in self.assignments:
                    target_zone = self._get_zone_by_id(self.assignments[team.team_id])
                    if target_zone:
                        # Move towards target
                        direction = self._get_direction(team.position, target_zone.position)
                        team.position = (
                            team.position[0] + direction[0] * 2,
                            team.position[1] + direction[1] * 2
                        )
                        
                        # Check if reached
                        distance = self._calculate_distance(team.position, target_zone.position)
                        if distance < 5:
                            team.status = 'rescuing'
                
                step_data['team_positions'].append({
                    'team_id': team.team_id,
                    'position': team.position,
                    'status': team.status
                })
            
            # Calculate zone coverage
            for zone in self.disaster_zones:
                nearby_teams = self._count_nearby_teams(zone.position, radius=10)
                step_data['zone_coverage'].append({
                    'zone_id': zone.zone_id,
                    'teams_assigned': nearby_teams,
                    'coverage_adequate': nearby_teams >= (zone.severity * 3)
                })
            
            # Calculate efficiency
            step_data['efficiency_score'] = self._calculate_swarm_efficiency()
            
            simulation_steps.append(step_data)
        
        return simulation_steps
    
    def _calculate_fitness(self, team: RescueTeam) -> float:
        """Calculate fitness score for team position"""
        if not self.disaster_zones:
            return float('inf')
        
        total_cost = 0.0
        
        for zone in self.disaster_zones:
            distance = self._calculate_distance(team.position, zone.position)
            priority_weight = zone.priority * 10
            severity_weight = zone.severity * 5
            
            cost = distance + priority_weight + severity_weight
            total_cost += cost
        
        return total_cost
    
    def _update_velocity(self, team: RescueTeam) -> Tuple[float, float]:
        """Update team velocity using PSO formula"""
        r1, r2 = np.random.random(), np.random.random()
        
        # Cognitive component (personal best)
        cognitive = (
            self.c1 * r1 * (team.best_position[0] - team.position[0]),
            self.c1 * r1 * (team.best_position[1] - team.position[1])
        )
        
        # Social component (global best)
        social = (
            self.c2 * r2 * (self.global_best_position[0] - team.position[0]),
            self.c2 * r2 * (self.global_best_position[1] - team.position[1])
        )
        
        # New velocity
        new_velocity = (
            self.w * team.velocity[0] + cognitive[0] + social[0],
            self.w * team.velocity[1] + cognitive[1] + social[1]
        )
        
        # Limit velocity
        max_velocity = 5.0
        new_velocity = (
            np.clip(new_velocity[0], -max_velocity, max_velocity),
            np.clip(new_velocity[1], -max_velocity, max_velocity)
        )
        
        return new_velocity
    
    def _update_position(self, team: RescueTeam) -> Tuple[float, float]:
        """Update team position"""
        new_position = (
            team.position[0] + team.velocity[0],
            team.position[1] + team.velocity[1]
        )
        
        # Keep within bounds
        new_position = (
            np.clip(new_position[0], 0, 100),
            np.clip(new_position[1], 0, 100)
        )
        
        return new_position
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance"""
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _generate_assignments(self) -> Dict[str, str]:
        """Generate team-to-zone assignments"""
        assignments = {}
        assigned_zones = set()
        
        # Sort zones by priority
        sorted_zones = sorted(self.disaster_zones, key=lambda z: z.priority, reverse=True)
        
        for zone in sorted_zones:
            if zone.zone_id in assigned_zones:
                continue
            
            # Find nearest available team
            best_team = None
            best_distance = float('inf')
            
            for team in self.teams:
                if team.team_id in assignments:
                    continue
                
                distance = self._calculate_distance(team.position, zone.position)
                if distance < best_distance:
                    best_distance = distance
                    best_team = team
            
            if best_team:
                assignments[best_team.team_id] = zone.zone_id
                assigned_zones.add(zone.zone_id)
        
        return assignments
    
    def _find_best_zone_for_team(self, team: RescueTeam) -> Optional[DisasterZone]:
        """Find best zone for a team"""
        best_zone = None
        best_score = float('inf')
        
        for zone in self.disaster_zones:
            distance = self._calculate_distance(team.position, zone.position)
            score = distance / (zone.priority + 1)
            
            if score < best_score:
                best_score = score
                best_zone = zone
        
        return best_zone
    
    def _get_zone_by_id(self, zone_id: str) -> Optional[DisasterZone]:
        """Get zone by ID"""
        for zone in self.disaster_zones:
            if zone.zone_id == zone_id:
                return zone
        return None
    
    def _get_direction(self, from_pos: Tuple[float, float], to_pos: Tuple[float, float]) -> Tuple[float, float]:
        """Get normalized direction vector"""
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return (0.0, 0.0)
        
        return (dx / distance, dy / distance)
    
    def _count_nearby_teams(self, position: Tuple[float, float], radius: float) -> int:
        """Count teams within radius of position"""
        count = 0
        for team in self.teams:
            if self._calculate_distance(team.position, position) <= radius:
                count += 1
        return count
    
    def _calculate_eta(self, from_pos: Tuple[float, float], to_pos: Tuple[float, float]) -> float:
        """Calculate estimated time of arrival in minutes"""
        distance = self._calculate_distance(from_pos, to_pos)
        speed_kmh = 40  # Average speed
        return (distance / speed_kmh) * 60
    
    def _estimate_completion_time(self) -> float:
        """Estimate total completion time"""
        max_time = 0.0
        
        for team_id, zone_id in self.assignments.items():
            team = next((t for t in self.teams if t.team_id == team_id), None)
            zone = self._get_zone_by_id(zone_id)
            
            if team and zone:
                eta = self._calculate_eta(team.position, zone.position)
                rescue_time = zone.people_count / team.capacity * 10  # 10 min per capacity unit
                total_time = eta + rescue_time
                
                if total_time > max_time:
                    max_time = total_time
        
        return max_time
    
    def _calculate_swarm_efficiency(self) -> float:
        """Calculate overall swarm efficiency"""
        if not self.disaster_zones:
            return 1.0
        
        covered_zones = 0
        for zone in self.disaster_zones:
            if self._count_nearby_teams(zone.position, radius=10) > 0:
                covered_zones += 1
        
        return covered_zones / len(self.disaster_zones)
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination status"""
        return {
            'total_teams': len(self.teams),
            'total_zones': len(self.disaster_zones),
            'active_assignments': len(self.assignments),
            'team_status': {
                'idle': len([t for t in self.teams if t.status == 'idle']),
                'moving': len([t for t in self.teams if t.status == 'moving']),
                'rescuing': len([t for t in self.teams if t.status == 'rescuing']),
                'returning': len([t for t in self.teams if t.status == 'returning'])
            },
            'swarm_efficiency': self._calculate_swarm_efficiency(),
            'iteration': self.iteration,
            'timestamp': datetime.now().isoformat()
        }
