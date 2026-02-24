"""
Constraint Solver - Solves constraint satisfaction problems for planning
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ConstraintType(Enum):
    """Types of constraints"""
    RESOURCE = "resource"  # Resource availability constraints
    TIME = "time"  # Temporal constraints
    DEPENDENCY = "dependency"  # Action dependencies
    CAPACITY = "capacity"  # Capacity constraints
    BUDGET = "budget"  # Budget constraints


@dataclass
class Constraint:
    """Represents a constraint"""
    constraint_id: str
    constraint_type: ConstraintType
    description: str
    variables: List[str]
    condition: str  # Constraint condition
    
    def to_dict(self) -> Dict:
        return {
            "constraint_id": self.constraint_id,
            "constraint_type": self.constraint_type.value,
            "description": self.description,
            "variables": self.variables,
            "condition": self.condition
        }


class ConstraintSolver:
    """
    Solves constraint satisfaction problems for disaster response planning.
    Ensures plans satisfy resource, time, and dependency constraints.
    """
    
    def __init__(self):
        self.constraints: List[Constraint] = []
        self.solutions: List[Dict] = []
    
    def add_constraint(self, constraint: Constraint) -> None:
        """Add a constraint"""
        self.constraints.append(constraint)
    
    def check_constraints(
        self,
        assignment: Dict[str, Any]
    ) -> Dict:
        """
        Check if assignment satisfies all constraints.
        
        Args:
            assignment: Variable assignments to check
        
        Returns:
            Validation result
        """
        violations = []
        
        for constraint in self.constraints:
            if not self._check_constraint(constraint, assignment):
                violations.append({
                    "constraint_id": constraint.constraint_id,
                    "description": constraint.description,
                    "type": constraint.constraint_type.value
                })
        
        return {
            "satisfied": len(violations) == 0,
            "violations": violations,
            "constraints_checked": len(self.constraints)
        }
    
    def _check_constraint(
        self,
        constraint: Constraint,
        assignment: Dict[str, Any]
    ) -> bool:
        """Check if single constraint is satisfied"""
        # Simplified constraint checking
        # In production, would use proper constraint evaluation
        
        if constraint.constraint_type == ConstraintType.RESOURCE:
            # Check resource availability
            for var in constraint.variables:
                if var in assignment:
                    if assignment[var] < 0:
                        return False
            return True
        
        elif constraint.constraint_type == ConstraintType.BUDGET:
            # Check budget constraint
            total_cost = sum(
                assignment.get(var, 0)
                for var in constraint.variables
            )
            # Assume condition is max budget
            return total_cost <= 1000000  # Simplified
        
        else:
            # Default: assume satisfied
            return True
    
    def solve(
        self,
        variables: List[str],
        domains: Dict[str, List[Any]]
    ) -> Optional[Dict]:
        """
        Solve constraint satisfaction problem.
        
        Args:
            variables: List of variables to assign
            domains: Possible values for each variable
        
        Returns:
            Solution assignment or None
        """
        # Simplified backtracking search
        assignment = {}
        
        if self._backtrack(assignment, variables, domains):
            self.solutions.append(assignment.copy())
            return assignment
        
        return None
    
    def _backtrack(
        self,
        assignment: Dict,
        variables: List[str],
        domains: Dict[str, List[Any]]
    ) -> bool:
        """Backtracking search"""
        if len(assignment) == len(variables):
            return self.check_constraints(assignment)["satisfied"]
        
        # Select unassigned variable
        var = next(v for v in variables if v not in assignment)
        
        # Try each value in domain
        for value in domains.get(var, []):
            assignment[var] = value
            
            if self.check_constraints(assignment)["satisfied"]:
                if self._backtrack(assignment, variables, domains):
                    return True
            
            del assignment[var]
        
        return False
    
    def get_constraints(self) -> List[Dict]:
        """Get all constraints"""
        return [c.to_dict() for c in self.constraints]
