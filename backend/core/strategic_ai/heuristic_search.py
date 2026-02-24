"""
Heuristic Search - A* search for optimal planning
"""

from typing import Dict, List, Optional, Callable, Set, Tuple
from dataclasses import dataclass, field
import heapq
from enum import Enum


class Heuristic(Enum):
    """Heuristic functions for search"""
    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"
    GOAL_COUNT = "goal_count"
    COST_BASED = "cost_based"


@dataclass(order=True)
class SearchNode:
    """Node in search tree"""
    f_score: float  # f(n) = g(n) + h(n)
    state: Set[str] = field(compare=False)
    g_score: float = field(compare=False)  # Cost from start
    h_score: float = field(compare=False)  # Heuristic to goal
    parent: Optional['SearchNode'] = field(default=None, compare=False)
    action: Optional[str] = field(default=None, compare=False)
    
    def __hash__(self):
        return hash(frozenset(self.state))


class HeuristicSearch:
    """
    A* search algorithm for optimal planning.
    Uses heuristics to guide search toward goal.
    """
    
    def __init__(self, heuristic_type: Heuristic = Heuristic.GOAL_COUNT):
        self.heuristic_type = heuristic_type
        self.nodes_expanded = 0
        self.search_history: List[Dict] = []
    
    def heuristic(self, state: Set[str], goal: Set[str]) -> float:
        """
        Calculate heuristic value for state.
        
        Args:
            state: Current state
            goal: Goal state
        
        Returns:
            Heuristic estimate of cost to goal
        """
        if self.heuristic_type == Heuristic.GOAL_COUNT:
            # Count unsatisfied goals
            return len(goal - state)
        
        elif self.heuristic_type == Heuristic.COST_BASED:
            # Estimate based on missing goals
            missing = goal - state
            return len(missing) * 10.0  # Assume average cost of 10 per goal
        
        else:
            # Default: goal count
            return len(goal - state)
    
    def a_star_search(
        self,
        initial_state: Set[str],
        goal_state: Set[str],
        actions: List,
        max_iterations: int = 1000
    ) -> Optional[List]:
        """
        A* search algorithm.
        
        Args:
            initial_state: Starting state
            goal_state: Goal to achieve
            actions: Available actions
            max_iterations: Maximum search iterations
        
        Returns:
            List of actions forming optimal plan, or None
        """
        self.nodes_expanded = 0
        
        # Priority queue: (f_score, node)
        start_node = SearchNode(
            f_score=self.heuristic(initial_state, goal_state),
            state=initial_state,
            g_score=0.0,
            h_score=self.heuristic(initial_state, goal_state)
        )
        
        open_set = [start_node]
        closed_set: Set[frozenset] = set()
        
        while open_set and self.nodes_expanded < max_iterations:
            current = heapq.heappop(open_set)
            self.nodes_expanded += 1
            
            # Check if goal reached
            if goal_state.issubset(current.state):
                return self._reconstruct_path(current)
            
            state_key = frozenset(current.state)
            if state_key in closed_set:
                continue
            
            closed_set.add(state_key)
            
            # Expand node
            for action in actions:
                if action.is_applicable(current.state):
                    new_state = action.apply(current.state)
                    new_g = current.g_score + action.cost
                    new_h = self.heuristic(new_state, goal_state)
                    new_f = new_g + new_h
                    
                    neighbor = SearchNode(
                        f_score=new_f,
                        state=new_state,
                        g_score=new_g,
                        h_score=new_h,
                        parent=current,
                        action=action.action_id
                    )
                    
                    heapq.heappush(open_set, neighbor)
        
        return None  # No solution found
    
    def _reconstruct_path(self, node: SearchNode) -> List:
        """Reconstruct action sequence from goal node"""
        path = []
        current = node
        
        while current.parent is not None:
            if current.action:
                path.append(current.action)
            current = current.parent
        
        return list(reversed(path))
    
    def search(
        self,
        initial_conditions: List[str],
        goals: List[str],
        actions: List,
        max_iterations: int = 1000
    ) -> Dict:
        """
        Perform heuristic search.
        
        Args:
            initial_conditions: Initial state
            goals: Goal conditions
            actions: Available actions
            max_iterations: Max search iterations
        
        Returns:
            Search result with optimal plan
        """
        initial_state = set(initial_conditions)
        goal_state = set(goals)
        
        plan = self.a_star_search(initial_state, goal_state, actions, max_iterations)
        
        if plan:
            return {
                "success": True,
                "plan": plan,
                "plan_length": len(plan),
                "nodes_expanded": self.nodes_expanded,
                "heuristic_used": self.heuristic_type.value
            }
        else:
            return {
                "success": False,
                "error": "No plan found",
                "nodes_expanded": self.nodes_expanded
            }
