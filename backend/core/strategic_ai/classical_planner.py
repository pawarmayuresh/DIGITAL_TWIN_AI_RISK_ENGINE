"""
Classical Planner - STRIPS-style planning for disaster response
"""

from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ActionType(Enum):
    """Types of planning actions"""
    EVACUATE = "evacuate"
    REPAIR = "repair"
    DISTRIBUTE = "distribute"
    DEPLOY = "deploy"
    COMMUNICATE = "communicate"


@dataclass
class Action:
    """Represents a planning action (STRIPS-style)"""
    action_id: str
    action_type: ActionType
    name: str
    preconditions: Set[str] = field(default_factory=set)  # Required conditions
    add_effects: Set[str] = field(default_factory=set)    # Conditions added
    delete_effects: Set[str] = field(default_factory=set) # Conditions removed
    cost: float = 1.0
    duration: int = 1  # Time steps
    
    def is_applicable(self, state: Set[str]) -> bool:
        """Check if action can be applied in given state"""
        return self.preconditions.issubset(state)
    
    def apply(self, state: Set[str]) -> Set[str]:
        """Apply action to state, returning new state"""
        new_state = state.copy()
        new_state -= self.delete_effects
        new_state |= self.add_effects
        return new_state
    
    def to_dict(self) -> Dict:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type.value,
            "name": self.name,
            "preconditions": list(self.preconditions),
            "add_effects": list(self.add_effects),
            "delete_effects": list(self.delete_effects),
            "cost": self.cost,
            "duration": self.duration
        }


@dataclass
class PlanningProblem:
    """Defines a planning problem"""
    initial_state: Set[str]
    goal_state: Set[str]
    actions: List[Action]
    
    def is_goal(self, state: Set[str]) -> bool:
        """Check if state satisfies goal"""
        return self.goal_state.issubset(state)


class ClassicalPlanner:
    """
    Classical AI planner using forward search.
    Finds sequence of actions to achieve disaster response goals.
    """
    
    def __init__(self):
        self.actions: List[Action] = []
        self.plans: Dict[str, List[Action]] = {}
        
        # Initialize default actions
        self._initialize_default_actions()
    
    def _initialize_default_actions(self) -> None:
        """Initialize standard disaster response actions"""
        
        # Evacuate action
        self.register_action(Action(
            action_id="evacuate_zone",
            action_type=ActionType.EVACUATE,
            name="Evacuate High-Risk Zone",
            preconditions={"disaster_detected", "evacuation_routes_clear"},
            add_effects={"population_evacuated", "zone_empty"},
            delete_effects={"population_at_risk"},
            cost=100.0,
            duration=2
        ))
        
        # Repair infrastructure
        self.register_action(Action(
            action_id="repair_power",
            action_type=ActionType.REPAIR,
            name="Repair Power Grid",
            preconditions={"disaster_passed", "repair_crews_available"},
            add_effects={"power_restored", "infrastructure_operational"},
            delete_effects={"power_outage"},
            cost=200.0,
            duration=5
        ))
        
        # Distribute resources
        self.register_action(Action(
            action_id="distribute_supplies",
            action_type=ActionType.DISTRIBUTE,
            name="Distribute Emergency Supplies",
            preconditions={"supplies_available", "distribution_points_setup"},
            add_effects={"population_supplied", "basic_needs_met"},
            delete_effects={"resource_shortage"},
            cost=50.0,
            duration=1
        ))
        
        # Deploy medical teams
        self.register_action(Action(
            action_id="deploy_medical",
            action_type=ActionType.DEPLOY,
            name="Deploy Medical Teams",
            preconditions={"medical_teams_ready", "access_routes_clear"},
            add_effects={"medical_care_available", "casualties_treated"},
            delete_effects={"medical_emergency"},
            cost=150.0,
            duration=3
        ))
        
        # Communicate warnings
        self.register_action(Action(
            action_id="issue_warning",
            action_type=ActionType.COMMUNICATE,
            name="Issue Emergency Warning",
            preconditions={"communication_system_operational"},
            add_effects={"population_warned", "awareness_high"},
            delete_effects={"population_unaware"},
            cost=10.0,
            duration=1
        ))
        
        # Setup distribution points
        self.register_action(Action(
            action_id="setup_distribution",
            action_type=ActionType.DEPLOY,
            name="Setup Distribution Points",
            preconditions={"locations_identified", "staff_available"},
            add_effects={"distribution_points_setup"},
            delete_effects={},
            cost=30.0,
            duration=2
        ))
        
        # Clear evacuation routes
        self.register_action(Action(
            action_id="clear_routes",
            action_type=ActionType.REPAIR,
            name="Clear Evacuation Routes",
            preconditions={"disaster_detected"},
            add_effects={"evacuation_routes_clear", "access_routes_clear"},
            delete_effects={"routes_blocked"},
            cost=80.0,
            duration=2
        ))
    
    def register_action(self, action: Action) -> None:
        """Register a new action"""
        self.actions.append(action)
    
    def create_problem(
        self,
        initial_state: Set[str],
        goal_state: Set[str]
    ) -> PlanningProblem:
        """Create a planning problem"""
        return PlanningProblem(
            initial_state=initial_state,
            goal_state=goal_state,
            actions=self.actions
        )
    
    def forward_search(
        self,
        problem: PlanningProblem,
        max_depth: int = 10
    ) -> Optional[List[Action]]:
        """
        Forward search planning algorithm.
        
        Args:
            problem: Planning problem to solve
            max_depth: Maximum search depth
        
        Returns:
            List of actions forming a plan, or None if no plan found
        """
        # Breadth-first search
        from collections import deque
        
        queue = deque([(problem.initial_state, [], 0)])  # (state, plan, depth)
        visited = {frozenset(problem.initial_state)}
        
        while queue:
            current_state, current_plan, depth = queue.popleft()
            
            # Check if goal reached
            if problem.is_goal(current_state):
                self.plans["last_plan"] = current_plan
                return current_plan
            
            # Check depth limit
            if depth >= max_depth:
                continue
            
            # Try all applicable actions
            for action in problem.actions:
                if action.is_applicable(current_state):
                    new_state = action.apply(current_state)
                    state_key = frozenset(new_state)
                    
                    if state_key not in visited:
                        visited.add(state_key)
                        new_plan = current_plan + [action]
                        queue.append((new_state, new_plan, depth + 1))
        
        return None  # No plan found
    
    def plan(
        self,
        initial_conditions: List[str],
        goals: List[str],
        max_depth: int = 10
    ) -> Dict:
        """
        Create a plan to achieve goals from initial conditions.
        
        Args:
            initial_conditions: List of initial state conditions
            goals: List of goal conditions to achieve
            max_depth: Maximum planning depth
        
        Returns:
            Planning result with action sequence
        """
        # Create problem
        problem = self.create_problem(
            initial_state=set(initial_conditions),
            goal_state=set(goals)
        )
        
        # Find plan
        plan = self.forward_search(problem, max_depth)
        
        if plan:
            total_cost = sum(action.cost for action in plan)
            total_duration = sum(action.duration for action in plan)
            
            return {
                "success": True,
                "plan": [action.to_dict() for action in plan],
                "plan_length": len(plan),
                "total_cost": total_cost,
                "total_duration": total_duration,
                "actions": [action.name for action in plan]
            }
        else:
            return {
                "success": False,
                "error": "No plan found",
                "initial_state": list(initial_conditions),
                "goal_state": list(goals)
            }
    
    def get_applicable_actions(self, current_state: List[str]) -> List[Dict]:
        """Get all actions applicable in current state"""
        state_set = set(current_state)
        applicable = [
            action.to_dict()
            for action in self.actions
            if action.is_applicable(state_set)
        ]
        return applicable
    
    def validate_plan(
        self,
        plan: List[str],
        initial_state: List[str]
    ) -> Dict:
        """
        Validate that a plan is executable.
        
        Args:
            plan: List of action IDs
            initial_state: Initial state conditions
        
        Returns:
            Validation result
        """
        # Find actions by ID
        action_map = {action.action_id: action for action in self.actions}
        
        current_state = set(initial_state)
        valid = True
        errors = []
        
        for i, action_id in enumerate(plan):
            if action_id not in action_map:
                valid = False
                errors.append(f"Step {i}: Unknown action '{action_id}'")
                continue
            
            action = action_map[action_id]
            
            if not action.is_applicable(current_state):
                valid = False
                missing = action.preconditions - current_state
                errors.append(
                    f"Step {i}: Action '{action.name}' not applicable. "
                    f"Missing: {missing}"
                )
            else:
                current_state = action.apply(current_state)
        
        return {
            "valid": valid,
            "errors": errors,
            "final_state": list(current_state)
        }
    
    def get_all_actions(self) -> List[Dict]:
        """Get all registered actions"""
        return [action.to_dict() for action in self.actions]
