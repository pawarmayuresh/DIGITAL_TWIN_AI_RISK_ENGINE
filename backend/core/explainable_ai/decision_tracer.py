"""
Decision Tracer - Logs and traces AI decision-making processes.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
from enum import Enum


class DecisionType(Enum):
    """Types of decisions that can be traced."""
    RESOURCE_ALLOCATION = "resource_allocation"
    EVACUATION = "evacuation"
    INFRASTRUCTURE_REPAIR = "infrastructure_repair"
    COALITION_FORMATION = "coalition_formation"
    POLICY_SELECTION = "policy_selection"
    RISK_ASSESSMENT = "risk_assessment"


@dataclass
class DecisionStep:
    """Single step in a decision process."""
    step_id: str
    timestamp: str
    component: str
    action: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    reasoning: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionTrace:
    """Complete trace of a decision."""
    trace_id: str
    decision_type: str
    timestamp: str
    context: Dict[str, Any]
    steps: List[DecisionStep]
    final_decision: Dict[str, Any]
    total_confidence: float
    execution_time_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'trace_id': self.trace_id,
            'decision_type': self.decision_type,
            'timestamp': self.timestamp,
            'context': self.context,
            'steps': [asdict(step) for step in self.steps],
            'final_decision': self.final_decision,
            'total_confidence': self.total_confidence,
            'execution_time_ms': self.execution_time_ms
        }


class DecisionTracer:
    """Traces and logs AI decision-making processes."""
    
    def __init__(self, max_traces: int = 1000):
        self.max_traces = max_traces
        self.traces: List[DecisionTrace] = []
        self.active_traces: Dict[str, Dict[str, Any]] = {}
        self.trace_counter = 0
    
    def start_trace(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any]
    ) -> str:
        """Start tracing a new decision."""
        self.trace_counter += 1
        trace_id = f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.trace_counter}"
        
        self.active_traces[trace_id] = {
            'trace_id': trace_id,
            'decision_type': decision_type.value,
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'steps': [],
            'start_time': datetime.now()
        }
        
        return trace_id
    
    def log_step(
        self,
        trace_id: str,
        component: str,
        action: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        reasoning: str,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a step in the decision process."""
        if trace_id not in self.active_traces:
            return
        
        step_id = f"{trace_id}_step_{len(self.active_traces[trace_id]['steps']) + 1}"
        
        step = DecisionStep(
            step_id=step_id,
            timestamp=datetime.now().isoformat(),
            component=component,
            action=action,
            inputs=inputs,
            outputs=outputs,
            reasoning=reasoning,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        self.active_traces[trace_id]['steps'].append(step)
    
    def end_trace(
        self,
        trace_id: str,
        final_decision: Dict[str, Any],
        total_confidence: Optional[float] = None
    ) -> DecisionTrace:
        """End tracing and create final trace."""
        if trace_id not in self.active_traces:
            raise ValueError(f"Trace {trace_id} not found")
        
        trace_data = self.active_traces[trace_id]
        
        # Calculate execution time
        execution_time = (datetime.now() - trace_data['start_time']).total_seconds() * 1000
        
        # Calculate total confidence if not provided
        if total_confidence is None:
            if trace_data['steps']:
                total_confidence = sum(s.confidence for s in trace_data['steps']) / len(trace_data['steps'])
            else:
                total_confidence = 0.0
        
        # Create trace
        trace = DecisionTrace(
            trace_id=trace_data['trace_id'],
            decision_type=trace_data['decision_type'],
            timestamp=trace_data['timestamp'],
            context=trace_data['context'],
            steps=trace_data['steps'],
            final_decision=final_decision,
            total_confidence=total_confidence,
            execution_time_ms=execution_time
        )
        
        # Store trace
        self.traces.append(trace)
        
        # Maintain max traces
        if len(self.traces) > self.max_traces:
            self.traces.pop(0)
        
        # Remove from active
        del self.active_traces[trace_id]
        
        return trace
    
    def get_trace(self, trace_id: str) -> Optional[DecisionTrace]:
        """Get a specific trace."""
        for trace in self.traces:
            if trace.trace_id == trace_id:
                return trace
        return None
    
    def get_traces_by_type(self, decision_type: DecisionType) -> List[DecisionTrace]:
        """Get all traces of a specific type."""
        return [t for t in self.traces if t.decision_type == decision_type.value]
    
    def get_recent_traces(self, n: int = 10) -> List[DecisionTrace]:
        """Get the n most recent traces."""
        return self.traces[-n:]
    
    def get_trace_summary(self, trace_id: str) -> Dict[str, Any]:
        """Get a summary of a trace."""
        trace = self.get_trace(trace_id)
        if not trace:
            return {}
        
        return {
            'trace_id': trace.trace_id,
            'decision_type': trace.decision_type,
            'timestamp': trace.timestamp,
            'num_steps': len(trace.steps),
            'total_confidence': trace.total_confidence,
            'execution_time_ms': trace.execution_time_ms,
            'final_decision': trace.final_decision
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about traced decisions."""
        if not self.traces:
            return {'total_traces': 0}
        
        decision_types = {}
        for trace in self.traces:
            decision_types[trace.decision_type] = decision_types.get(trace.decision_type, 0) + 1
        
        avg_confidence = sum(t.total_confidence for t in self.traces) / len(self.traces)
        avg_execution_time = sum(t.execution_time_ms for t in self.traces) / len(self.traces)
        avg_steps = sum(len(t.steps) for t in self.traces) / len(self.traces)
        
        return {
            'total_traces': len(self.traces),
            'decision_types': decision_types,
            'avg_confidence': avg_confidence,
            'avg_execution_time_ms': avg_execution_time,
            'avg_steps_per_decision': avg_steps
        }
    
    def export_trace(self, trace_id: str, filepath: str):
        """Export a trace to JSON file."""
        trace = self.get_trace(trace_id)
        if not trace:
            raise ValueError(f"Trace {trace_id} not found")
        
        with open(filepath, 'w') as f:
            json.dump(trace.to_dict(), f, indent=2)
    
    def export_all_traces(self, filepath: str):
        """Export all traces to JSON file."""
        data = {
            'traces': [t.to_dict() for t in self.traces],
            'statistics': self.get_statistics()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
