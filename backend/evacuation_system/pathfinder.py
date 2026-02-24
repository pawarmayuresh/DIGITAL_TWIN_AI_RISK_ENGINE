"""
Pathfinder - A* Algorithm for Optimal Evacuation Routes
Finds shortest + safest path avoiding dangerous zones
"""
import heapq
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from .grid_engine import GridZone, MumbaiGridEngine

@dataclass
class PathNode:
    """Node in the pathfinding algorithm"""
    grid: GridZone
    g_cost: float  # Cost from start
    h_cost: float  # Heuristic cost to goal
    f_cost: float  # Total cost (g + h)
    parent: Optional['PathNode'] = None
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class EvacuationPathfinder:
    """A* pathfinding for evacuation routes"""
    
    def __init__(self, grid_engine: MumbaiGridEngine):
        self.grid_engine = grid_engine
        self.explanation_log = []
    
    def heuristic(self, grid1: GridZone, grid2: GridZone) -> float:
        """Manhattan distance + safety penalty"""
        # Manhattan distance
        distance = abs(grid1.row - grid2.row) + abs(grid1.col - grid2.col)
        
        # Safety penalty (prefer safer routes)
        safety_penalty = grid1.risk_score * 5
        
        return distance + safety_penalty
    
    def get_movement_cost(self, from_grid: GridZone, to_grid: GridZone) -> float:
        """Calculate cost of moving between grids"""
        base_cost = 1.0
        
        # Risk penalty
        risk_penalty = to_grid.risk_score * 10
        
        # Water level penalty
        water_penalty = to_grid.water_level * 3
        
        # Infrastructure penalty
        infra_penalty = 0
        if to_grid.infrastructure_status == "damaged":
            infra_penalty = 2
        elif to_grid.infrastructure_status == "blocked":
            return float('inf')  # Cannot pass
        
        total_cost = base_cost + risk_penalty + water_penalty + infra_penalty
        
        return total_cost
    
    def find_path(self, start_grid: GridZone, goal_grid: GridZone) -> Optional[Dict]:
        """
        Find optimal evacuation path using A* algorithm
        Returns path with explanation
        """
        self.explanation_log = []
        
        # Initialize
        open_set = []
        closed_set = set()
        
        start_node = PathNode(
            grid=start_grid,
            g_cost=0,
            h_cost=self.heuristic(start_grid, goal_grid),
            f_cost=self.heuristic(start_grid, goal_grid)
        )
        
        heapq.heappush(open_set, start_node)
        
        nodes_explored = 0
        grids_avoided = []
        
        while open_set:
            current_node = heapq.heappop(open_set)
            nodes_explored += 1
            
            # Goal reached
            if current_node.grid.id == goal_grid.id:
                path = self._reconstruct_path(current_node)
                
                # Generate explanation
                explanation = self._generate_explanation(
                    path, start_grid, goal_grid, nodes_explored, grids_avoided
                )
                
                return {
                    "success": True,
                    "path": path,
                    "path_length": len(path),
                    "total_cost": current_node.g_cost,
                    "nodes_explored": nodes_explored,
                    "explanation": explanation,
                    "avoided_grids": grids_avoided
                }
            
            closed_set.add(current_node.grid.id)
            
            # Explore neighbors
            for neighbor in self.grid_engine.get_neighbors(current_node.grid):
                if neighbor.id in closed_set:
                    continue
                
                # Check if grid should be avoided
                if neighbor.safety_level.value == "DANGEROUS":
                    grids_avoided.append({
                        "id": neighbor.id,
                        "name": neighbor.name,
                        "reason": "Dangerous zone",
                        "risk_score": neighbor.risk_score
                    })
                    continue
                
                if neighbor.water_level > 1.5:
                    grids_avoided.append({
                        "id": neighbor.id,
                        "name": neighbor.name,
                        "reason": "High water level",
                        "water_level": neighbor.water_level
                    })
                    continue
                
                # Calculate costs
                movement_cost = self.get_movement_cost(current_node.grid, neighbor)
                if movement_cost == float('inf'):
                    grids_avoided.append({
                        "id": neighbor.id,
                        "name": neighbor.name,
                        "reason": "Blocked infrastructure",
                        "status": neighbor.infrastructure_status
                    })
                    continue
                
                tentative_g_cost = current_node.g_cost + movement_cost
                h_cost = self.heuristic(neighbor, goal_grid)
                f_cost = tentative_g_cost + h_cost
                
                # Check if this path is better
                neighbor_node = PathNode(
                    grid=neighbor,
                    g_cost=tentative_g_cost,
                    h_cost=h_cost,
                    f_cost=f_cost,
                    parent=current_node
                )
                
                heapq.heappush(open_set, neighbor_node)
        
        # No path found
        return {
            "success": False,
            "path": [],
            "message": "No safe path found",
            "nodes_explored": nodes_explored,
            "avoided_grids": grids_avoided
        }
    
    def _reconstruct_path(self, node: PathNode) -> List[Dict]:
        """Reconstruct path from goal to start"""
        path = []
        current = node
        
        while current:
            path.append({
                "grid_id": current.grid.id,
                "name": current.grid.name,
                "row": current.grid.row,
                "col": current.grid.col,
                "latitude": current.grid.latitude,
                "longitude": current.grid.longitude,
                "risk_score": current.grid.risk_score,
                "safety_level": current.grid.safety_level.value,
                "cost": current.g_cost
            })
            current = current.parent
        
        path.reverse()
        return path
    
    def _generate_explanation(self, path: List[Dict], start: GridZone, 
                            goal: GridZone, nodes_explored: int, 
                            avoided_grids: List[Dict]) -> Dict:
        """Generate explainable AI output"""
        # Calculate path statistics
        total_risk = sum(p["risk_score"] for p in path)
        avg_risk = total_risk / len(path) if path else 0
        
        # Safety comparison
        alternative_direct_risk = self._calculate_direct_path_risk(start, goal)
        
        # Generate reasons
        reasons = []
        
        reasons.append(f"Selected path has {len(path)} steps with average risk score of {avg_risk:.2f}")
        
        if avoided_grids:
            reasons.append(f"Avoided {len(avoided_grids)} dangerous/blocked grids")
            dangerous_count = sum(1 for g in avoided_grids if g.get("reason") == "Dangerous zone")
            if dangerous_count:
                reasons.append(f"Bypassed {dangerous_count} high-risk zones")
        
        if avg_risk < alternative_direct_risk:
            reasons.append(f"Chosen path is {((alternative_direct_risk - avg_risk) / alternative_direct_risk * 100):.1f}% safer than direct route")
        
        reasons.append(f"Explored {nodes_explored} possible routes to find optimal path")
        
        # Path segments analysis
        segments = []
        for i in range(len(path) - 1):
            current = path[i]
            next_grid = path[i + 1]
            segments.append({
                "from": current["grid_id"],
                "to": next_grid["grid_id"],
                "risk": next_grid["risk_score"],
                "safety": next_grid["safety_level"]
            })
        
        return {
            "path_length": len(path),
            "average_risk": avg_risk,
            "total_risk": total_risk,
            "nodes_explored": nodes_explored,
            "grids_avoided": len(avoided_grids),
            "reasons": reasons,
            "segments": segments,
            "safety_comparison": {
                "chosen_path_risk": avg_risk,
                "direct_path_risk": alternative_direct_risk,
                "improvement": alternative_direct_risk - avg_risk
            }
        }
    
    def _calculate_direct_path_risk(self, start: GridZone, goal: GridZone) -> float:
        """Calculate risk of direct path (for comparison)"""
        # Simple estimation
        row_diff = abs(goal.row - start.row)
        col_diff = abs(goal.col - start.col)
        steps = row_diff + col_diff
        
        # Assume average risk of 0.5 for direct path
        return 0.5 * steps if steps > 0 else 0
    
    def find_nearest_safe_zone(self, start_grid: GridZone) -> Optional[GridZone]:
        """Find nearest safe evacuation point"""
        evacuation_points = self.grid_engine.get_evacuation_points()
        
        if not evacuation_points:
            # Fallback to any safe zone
            evacuation_points = self.grid_engine.get_safe_zones()
        
        if not evacuation_points:
            return None
        
        # Find closest by Manhattan distance
        min_distance = float('inf')
        nearest = None
        
        for evac_point in evacuation_points:
            distance = abs(evac_point.row - start_grid.row) + abs(evac_point.col - start_grid.col)
            if distance < min_distance:
                min_distance = distance
                nearest = evac_point
        
        return nearest
