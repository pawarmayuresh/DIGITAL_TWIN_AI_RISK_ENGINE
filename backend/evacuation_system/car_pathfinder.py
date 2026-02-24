"""
A* Pathfinder for Car Agent
Finds optimal path avoiding danger zones (except pickup location)
"""
import heapq
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class PathNode:
    grid_id: str
    g_cost: float  # Actual cost from start
    h_cost: float  # Heuristic to goal
    f_cost: float  # Total cost
    parent: Optional['PathNode'] = None
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class CarPathfinder:
    """A* pathfinding for car evacuation"""
    
    def __init__(self, grid_engine, penalty_weight: float = 10.0):
        self.grid_engine = grid_engine
        self.penalty_weight = penalty_weight
    
    def manhattan_distance(self, grid1_id: str, grid2_id: str) -> int:
        """Calculate Manhattan distance between two grids"""
        grid1 = self.grid_engine.get_grid(grid1_id)
        grid2 = self.grid_engine.get_grid(grid2_id)
        
        if not grid1 or not grid2:
            return 999
        
        return abs(grid1.row - grid2.row) + abs(grid1.col - grid2.col)
    
    def get_movement_cost(self, from_id: str, to_id: str, allow_danger: bool = False) -> float:
        """Calculate cost of moving between grids"""
        to_grid = self.grid_engine.get_grid(to_id)
        
        if not to_grid:
            return float('inf')
        
        # Base cost
        base_cost = 1.0
        
        # Risk penalty
        risk_penalty = to_grid.risk_score * self.penalty_weight
        
        # Danger zone penalty (unless allowed)
        if to_grid.safety_level.value == "DANGEROUS" and not allow_danger:
            return float('inf')  # Cannot pass through danger
        
        # Infrastructure penalty
        if to_grid.infrastructure_status == "blocked":
            return float('inf')
        elif to_grid.infrastructure_status == "damaged":
            risk_penalty += 5
        
        return base_cost + risk_penalty
    
    def find_path(self, start_id: str, goal_id: str, allow_danger_at_goal: bool = False) -> Optional[Dict]:
        """
        Find optimal path using A* algorithm
        
        Args:
            start_id: Starting grid ID
            goal_id: Goal grid ID
            allow_danger_at_goal: If True, allows entering danger zone at goal (for pickup)
        
        Returns:
            Dict with path, cost, and explanation
        """
        start_grid = self.grid_engine.get_grid(start_id)
        goal_grid = self.grid_engine.get_grid(goal_id)
        
        if not start_grid or not goal_grid:
            return None
        
        open_set = []
        closed_set = set()
        
        start_node = PathNode(
            grid_id=start_id,
            g_cost=0,
            h_cost=self.manhattan_distance(start_id, goal_id),
            f_cost=self.manhattan_distance(start_id, goal_id)
        )
        
        heapq.heappush(open_set, start_node)
        
        nodes_explored = 0
        grids_avoided = []
        
        while open_set:
            current = heapq.heappop(open_set)
            nodes_explored += 1
            
            # Goal reached
            if current.grid_id == goal_id:
                path = self._reconstruct_path(current)
                explanation = self._generate_explanation(
                    path, start_grid, goal_grid, nodes_explored, grids_avoided
                )
                
                return {
                    "success": True,
                    "path": path,
                    "path_ids": [p["grid_id"] for p in path],
                    "total_cost": current.g_cost,
                    "distance": len(path),
                    "explanation": explanation
                }
            
            closed_set.add(current.grid_id)
            
            # Explore neighbors
            current_grid = self.grid_engine.get_grid(current.grid_id)
            neighbors = self.grid_engine.get_all_neighbors(current_grid)  # Get ALL neighbors including dangerous
            
            for neighbor in neighbors:
                if neighbor.id in closed_set:
                    continue
                
                # Check if we can move to this neighbor
                is_goal = (neighbor.id == goal_id)
                allow_danger = is_goal and allow_danger_at_goal
                
                movement_cost = self.get_movement_cost(current.grid_id, neighbor.id, allow_danger)
                
                if movement_cost == float('inf'):
                    grids_avoided.append({
                        "id": neighbor.id,
                        "name": neighbor.name,
                        "reason": "Dangerous zone" if neighbor.safety_level.value == "DANGEROUS" else "Blocked",
                        "risk_score": neighbor.risk_score
                    })
                    continue
                
                tentative_g = current.g_cost + movement_cost
                h_cost = self.manhattan_distance(neighbor.id, goal_id)
                f_cost = tentative_g + h_cost
                
                neighbor_node = PathNode(
                    grid_id=neighbor.id,
                    g_cost=tentative_g,
                    h_cost=h_cost,
                    f_cost=f_cost,
                    parent=current
                )
                
                heapq.heappush(open_set, neighbor_node)
        
        # No path found
        return {
            "success": False,
            "message": "No safe path found",
            "nodes_explored": nodes_explored,
            "grids_avoided": grids_avoided
        }
    
    def _reconstruct_path(self, node: PathNode) -> List[Dict]:
        """Reconstruct path from goal to start"""
        path = []
        current = node
        
        while current:
            grid = self.grid_engine.get_grid(current.grid_id)
            path.append({
                "grid_id": grid.id,
                "name": grid.name,
                "row": grid.row,
                "col": grid.col,
                "risk_score": grid.risk_score,
                "safety_level": grid.safety_level.value
            })
            current = current.parent
        
        path.reverse()
        return path
    
    def _generate_explanation(self, path: List[Dict], start, goal, nodes_explored: int, avoided: List[Dict]) -> Dict:
        """Generate XAI explanation for path"""
        total_risk = sum(p["risk_score"] for p in path)
        avg_risk = total_risk / len(path) if path else 0
        
        reasons = []
        reasons.append(f"Path length: {len(path)} grids, Average risk: {avg_risk:.2f}")
        reasons.append(f"Avoided {len(avoided)} dangerous/blocked grids")
        reasons.append(f"Explored {nodes_explored} possible routes")
        
        # Calculate direct distance
        direct_distance = abs(goal.row - start.row) + abs(goal.col - start.col)
        detour = len(path) - direct_distance
        
        if detour > 0:
            reasons.append(f"Took {detour} extra steps to avoid danger zones")
        else:
            reasons.append("Direct path was safest option")
        
        return {
            "path_length": len(path),
            "total_risk": round(total_risk, 2),
            "average_risk": round(avg_risk, 2),
            "grids_avoided": len(avoided),
            "avoided_details": avoided,
            "nodes_explored": nodes_explored,
            "reasons": reasons,
            "direct_distance": direct_distance,
            "actual_distance": len(path),
            "detour_steps": detour
        }
