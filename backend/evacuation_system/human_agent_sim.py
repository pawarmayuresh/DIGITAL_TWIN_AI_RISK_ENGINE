"""
Human Agent Simulator - Simulates people evacuating across grid
Each agent moves step-by-step following evacuation path
"""
import uuid
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from .grid_engine import GridZone
from .pathfinder import EvacuationPathfinder

class AgentStatus(Enum):
    WAITING = "WAITING"
    EVACUATING = "EVACUATING"
    SAFE = "SAFE"
    STUCK = "STUCK"

@dataclass
class HumanAgent:
    """Represents a person evacuating"""
    id: str
    name: str
    current_grid: GridZone
    destination_grid: Optional[GridZone] = None
    path: List[Dict] = field(default_factory=list)
    path_index: int = 0
    status: AgentStatus = AgentStatus.WAITING
    speed: float = 1.0  # grids per step
    health: int = 100  # 0-100
    age_group: str = "adult"  # child, adult, elderly
    steps_taken: int = 0
    
    def get_position(self) -> Dict:
        """Get current position"""
        return {
            "grid_id": self.current_grid.id,
            "grid_name": self.current_grid.name,
            "row": self.current_grid.row,
            "col": self.current_grid.col,
            "latitude": self.current_grid.latitude,
            "longitude": self.current_grid.longitude
        }
    
    def move_to_next_grid(self, next_grid: GridZone):
        """Move agent to next grid in path"""
        self.current_grid = next_grid
        self.path_index += 1
        self.steps_taken += 1
        
        # Health decreases in risky areas
        if next_grid.risk_score > 0.6:
            self.health -= int(next_grid.risk_score * 5)
        
        # Check if reached destination
        if self.destination_grid and next_grid.id == self.destination_grid.id:
            self.status = AgentStatus.SAFE
    
    def to_dict(self) -> Dict:
        """Export agent data"""
        # Handle path - can be list of GridZone objects or dicts
        path_ids = []
        if self.path:
            for item in self.path:
                if isinstance(item, dict):
                    path_ids.append(item.get('grid_id', ''))
                elif hasattr(item, 'id'):
                    path_ids.append(item.id)
        
        return {
            "id": self.id,
            "name": self.name,
            "position": self.get_position(),
            "destination": {
                "grid_id": self.destination_grid.id,
                "name": self.destination_grid.name
            } if self.destination_grid else None,
            "status": self.status.value,
            "health": self.health,
            "age_group": self.age_group,
            "steps_taken": self.steps_taken,
            "progress": (self.path_index / len(self.path) * 100) if self.path else 0,
            "path": path_ids
        }


class EvacuationSimulator:
    """Manages multiple human agents during evacuation"""
    
    def __init__(self, grid_engine, pathfinder: EvacuationPathfinder):
        self.grid_engine = grid_engine
        self.pathfinder = pathfinder
        self.agents: Dict[str, HumanAgent] = {}
        self.simulation_step = 0
        self.evacuation_stats = {
            "total_agents": 0,
            "evacuating": 0,
            "safe": 0,
            "stuck": 0,
            "average_health": 100
        }
    
    def create_agents_in_dangerous_zones(self, agents_per_zone: int = 5) -> List[HumanAgent]:
        """Create agents in dangerous zones that need evacuation"""
        dangerous_zones = self.grid_engine.get_dangerous_zones()
        agents_created = []
        
        for zone in dangerous_zones:
            for i in range(agents_per_zone):
                agent_id = str(uuid.uuid4())[:8]
                
                # Vary agent characteristics
                age_groups = ["child", "adult", "elderly"]
                age_group = age_groups[i % 3]
                
                speed = 1.0
                if age_group == "child":
                    speed = 0.8
                elif age_group == "elderly":
                    speed = 0.6
                
                agent = HumanAgent(
                    id=agent_id,
                    name=f"Person-{agent_id}",
                    current_grid=zone,
                    speed=speed,
                    age_group=age_group
                )
                
                self.agents[agent_id] = agent
                agents_created.append(agent)
        
        self.evacuation_stats["total_agents"] = len(self.agents)
        return agents_created
    
    def assign_evacuation_paths(self):
        """Assign evacuation paths to all agents"""
        for agent in self.agents.values():
            if agent.status == AgentStatus.WAITING:
                # Find nearest safe zone
                safe_zone = self.pathfinder.find_nearest_safe_zone(agent.current_grid)
                
                if safe_zone:
                    # Find path
                    path_result = self.pathfinder.find_path(agent.current_grid, safe_zone)
                    
                    if path_result["success"]:
                        agent.path = path_result["path"]
                        agent.destination_grid = safe_zone
                        agent.status = AgentStatus.EVACUATING
                    else:
                        agent.status = AgentStatus.STUCK
                else:
                    agent.status = AgentStatus.STUCK
    
    def simulate_step(self) -> Dict:
        """Simulate one time step of evacuation"""
        self.simulation_step += 1
        movements = []
        
        for agent in self.agents.values():
            if agent.status == AgentStatus.EVACUATING:
                # Check if agent can move
                if agent.path_index < len(agent.path) - 1:
                    next_grid_data = agent.path[agent.path_index + 1]
                    next_grid = self.grid_engine.get_grid(next_grid_data["grid_id"])
                    
                    if next_grid and next_grid.is_passable():
                        old_pos = agent.get_position()
                        agent.move_to_next_grid(next_grid)
                        new_pos = agent.get_position()
                        
                        movements.append({
                            "agent_id": agent.id,
                            "from": old_pos,
                            "to": new_pos,
                            "health": agent.health,
                            "status": agent.status.value
                        })
                    else:
                        # Path blocked, need rerouting
                        agent.status = AgentStatus.STUCK
        
        # Update stats
        self._update_stats()
        
        return {
            "step": self.simulation_step,
            "movements": movements,
            "stats": self.evacuation_stats,
            "agents": [agent.to_dict() for agent in self.agents.values()]
        }
    
    def _update_stats(self):
        """Update evacuation statistics"""
        evacuating = sum(1 for a in self.agents.values() if a.status == AgentStatus.EVACUATING)
        safe = sum(1 for a in self.agents.values() if a.status == AgentStatus.SAFE)
        stuck = sum(1 for a in self.agents.values() if a.status == AgentStatus.STUCK)
        
        total_health = sum(a.health for a in self.agents.values())
        avg_health = total_health / len(self.agents) if self.agents else 100
        
        self.evacuation_stats = {
            "total_agents": len(self.agents),
            "evacuating": evacuating,
            "safe": safe,
            "stuck": stuck,
            "average_health": round(avg_health, 1),
            "completion_rate": round((safe / len(self.agents) * 100) if self.agents else 0, 1)
        }
    
    def get_all_paths(self) -> List[Dict]:
        """Get all evacuation paths for visualization"""
        # Group agents by their paths
        path_groups = {}
        
        for agent in self.agents.values():
            if agent.path and len(agent.path) > 0:
                # Handle path items - can be dicts or GridZone objects
                def get_grid_id(item):
                    if isinstance(item, dict):
                        return item.get('grid_id', '')
                    elif hasattr(item, 'id'):
                        return item.id
                    return ''
                
                def get_risk_score(item):
                    if isinstance(item, dict):
                        return item.get('risk_score', 0)
                    elif hasattr(item, 'risk_score'):
                        return item.risk_score
                    return 0
                
                # Create path key from start and end
                start_id = get_grid_id(agent.path[0])
                end_id = get_grid_id(agent.path[-1])
                path_key = f"{start_id}_{end_id}"
                
                if path_key not in path_groups:
                    # Calculate path statistics
                    total_risk = sum(get_risk_score(item) for item in agent.path)
                    avg_risk = total_risk / len(agent.path)
                    
                    # Get path IDs
                    path_ids = [get_grid_id(item) for item in agent.path]
                    
                    path_groups[path_key] = {
                        "start_grid": start_id,
                        "goal_grid": end_id,
                        "path_ids": path_ids,
                        "path_length": len(agent.path),
                        "average_risk": avg_risk,
                        "grids_avoided": 0,  # Simplified - avoid complex neighbor checking
                        "agents_using": 1
                    }
                else:
                    path_groups[path_key]["agents_using"] += 1
        
        return list(path_groups.values())
    
    def is_complete(self) -> bool:
        """Check if evacuation is complete"""
        return all(a.status in [AgentStatus.SAFE, AgentStatus.STUCK] 
                  for a in self.agents.values())
