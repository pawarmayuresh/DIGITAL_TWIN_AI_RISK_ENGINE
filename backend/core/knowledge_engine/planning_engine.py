"""
Planning Engine - Classical, Heuristic, and Hierarchical Planning
"""
import heapq
from typing import Set, List, Dict, Optional


class Action:
    """Action in STRIPS-style planning"""
    
    def __init__(self, name: str, preconditions: List[str], effects: List[str], cost: int = 1):
        self.name = name
        self.preconditions = set(preconditions)
        self.effects = set(effects)
        self.cost = cost
    
    def is_applicable(self, state: Set[str]) -> bool:
        """Check if action can be applied in current state"""
        return self.preconditions.issubset(state)
    
    def apply(self, state: Set[str]) -> Set[str]:
        """Apply action to state"""
        new_state = state.copy()
        new_state.update(self.effects)
        return new_state
    
    def __repr__(self):
        return f"Action({self.name})"


class Planner:
    """Classical STRIPS-style Planner"""
    
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.plan_trace = []
    
    def plan(self, initial_state: Set[str], goal: str, max_steps: int = 20) -> Optional[List[str]]:
        """
        Classical Planning - Find sequence of actions to achieve goal
        """
        self.plan_trace = []
        self.plan_trace.append(f"Initial State: {initial_state}")
        self.plan_trace.append(f"Goal: {goal}")
        
        plan = []
        current_state = set(initial_state)
        steps = 0
        
        while goal not in current_state and steps < max_steps:
            steps += 1
            action_applied = False
            
            # Find applicable action
            for action in self.actions:
                if action.is_applicable(current_state):
                    self.plan_trace.append(f"Step {steps}: Applying {action.name}")
                    current_state = action.apply(current_state)
                    plan.append(action.name)
                    action_applied = True
                    break
            
            if not action_applied:
                self.plan_trace.append("No valid action found - Planning failed")
                return None
        
        if goal in current_state:
            self.plan_trace.append(f"Goal achieved in {steps} steps!")
            return plan
        else:
            self.plan_trace.append(f"Goal not achieved within {max_steps} steps")
            return None


class HeuristicPlanner:
    """Heuristic-based Planner using A* search"""
    
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.plan_trace = []
    
    def heuristic(self, state: Set[str], goal: str) -> int:
        """
        Heuristic function - estimate cost to goal
        Lower is better
        """
        # Simple heuristic: count missing goal conditions
        if goal in state:
            return 0
        
        # Count how many preconditions are missing for actions that lead to goal
        min_distance = float('inf')
        for action in self.actions:
            if goal in action.effects:
                missing = len(action.preconditions - state)
                min_distance = min(min_distance, missing + 1)
        
        return min_distance if min_distance != float('inf') else 10
    
    def plan(self, initial_state: Set[str], goal: str) -> Optional[List[str]]:
        """
        Heuristic Planning using A* search
        """
        self.plan_trace = []
        self.plan_trace.append(f"Heuristic Planning - Initial State: {initial_state}")
        self.plan_trace.append(f"Goal: {goal}")
        
        # Priority queue: (f_score, g_score, state, plan)
        initial_h = self.heuristic(initial_state, goal)
        frontier = [(initial_h, 0, frozenset(initial_state), [])]
        visited = set()
        
        while frontier:
            f_score, g_score, state_frozen, plan = heapq.heappop(frontier)
            state = set(state_frozen)
            
            # Goal check
            if goal in state:
                self.plan_trace.append(f"Goal achieved with cost {g_score}!")
                self.plan_trace.append(f"Plan: {' → '.join(plan)}")
                return plan
            
            # Skip if already visited
            if state_frozen in visited:
                continue
            visited.add(state_frozen)
            
            # Expand actions
            for action in self.actions:
                if action.is_applicable(state):
                    new_state = action.apply(state)
                    new_plan = plan + [action.name]
                    new_g = g_score + action.cost
                    new_h = self.heuristic(new_state, goal)
                    new_f = new_g + new_h
                    
                    heapq.heappush(frontier, (new_f, new_g, frozenset(new_state), new_plan))
        
        self.plan_trace.append("No plan found")
        return None


class HierarchicalTask:
    """Task in Hierarchical Task Network (HTN)"""
    
    def __init__(self, name: str, level: str, subtasks: List[str] = None):
        self.name = name
        self.level = level  # "national", "state", "district"
        self.subtasks = subtasks or []
    
    def __repr__(self):
        return f"Task({self.name}, {self.level})"


class HierarchicalPlanner:
    """Hierarchical Task Network (HTN) Planner"""
    
    def __init__(self):
        self.tasks = {}
        self.plan_trace = []
    
    def add_task(self, task: HierarchicalTask):
        """Add a hierarchical task"""
        self.tasks[task.name] = task
    
    def decompose(self, task_name: str, depth: int = 0) -> List[str]:
        """
        Decompose high-level task into primitive actions
        """
        indent = "  " * depth
        
        if task_name not in self.tasks:
            # Primitive action
            self.plan_trace.append(f"{indent}→ Primitive Action: {task_name}")
            return [task_name]
        
        task = self.tasks[task_name]
        self.plan_trace.append(f"{indent}→ Decomposing {task.level.upper()} task: {task.name}")
        
        plan = []
        for subtask in task.subtasks:
            plan.extend(self.decompose(subtask, depth + 1))
        
        return plan
    
    def plan(self, high_level_goal: str) -> List[str]:
        """
        Create hierarchical plan
        """
        self.plan_trace = []
        self.plan_trace.append(f"Hierarchical Planning for: {high_level_goal}")
        
        plan = self.decompose(high_level_goal)
        
        self.plan_trace.append(f"\nFinal Plan ({len(plan)} actions):")
        for i, action in enumerate(plan, 1):
            self.plan_trace.append(f"  {i}. {action}")
        
        return plan
