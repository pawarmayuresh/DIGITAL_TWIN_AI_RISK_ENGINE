"""
Model Updater - Updates and maintains RL models.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class ModelUpdater:
    """Manages model updates and versioning."""
    
    def __init__(self, update_frequency: int = 100):
        self.update_frequency = update_frequency
        self.update_count = 0
        self.model_versions: List[Dict[str, Any]] = []
        self.current_version = "1.0.0"
        self.pending_updates: List[Dict[str, Any]] = []
    
    def should_update(self, training_steps: int) -> bool:
        """Check if model should be updated."""
        return training_steps % self.update_frequency == 0
    
    def queue_update(
        self,
        update_type: str,
        data: Dict[str, Any],
        priority: str = 'normal'
    ):
        """Queue a model update."""
        update = {
            'type': update_type,
            'data': data,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        self.pending_updates.append(update)
    
    def apply_updates(
        self,
        model: Any,
        max_updates: Optional[int] = None
    ) -> Dict[str, Any]:
        """Apply pending updates to model."""
        
        if not self.pending_updates:
            return {'updates_applied': 0, 'status': 'no_updates'}
        
        # Sort by priority
        priority_order = {'high': 0, 'normal': 1, 'low': 2}
        self.pending_updates.sort(key=lambda x: priority_order.get(x['priority'], 1))
        
        # Apply updates
        updates_to_apply = self.pending_updates[:max_updates] if max_updates else self.pending_updates
        applied_updates = []
        
        for update in updates_to_apply:
            try:
                self._apply_single_update(model, update)
                update['status'] = 'applied'
                applied_updates.append(update)
                self.update_count += 1
            except Exception as e:
                update['status'] = 'failed'
                update['error'] = str(e)
        
        # Remove applied updates
        self.pending_updates = [u for u in self.pending_updates if u['status'] == 'pending']
        
        # Create new version if significant updates
        if len(applied_updates) >= 10:
            self._create_new_version(applied_updates)
        
        return {
            'updates_applied': len(applied_updates),
            'updates_failed': len([u for u in applied_updates if u['status'] == 'failed']),
            'updates_pending': len(self.pending_updates),
            'current_version': self.current_version
        }
    
    def _apply_single_update(self, model: Any, update: Dict[str, Any]):
        """Apply a single update to the model."""
        update_type = update['type']
        data = update['data']
        
        if update_type == 'learning_rate':
            model.learning_rate = data['new_value']
        
        elif update_type == 'epsilon':
            model.epsilon = data['new_value']
        
        elif update_type == 'q_values':
            # Update specific Q-values
            state_key = data['state_key']
            action = data['action']
            new_value = data['new_value']
            model.q_table[state_key][action] = new_value
        
        elif update_type == 'policy_merge':
            # Merge external policy
            external_policy = data['policy']
            for state_key, actions in external_policy.items():
                if state_key not in model.q_table:
                    model.q_table[state_key] = actions
                else:
                    # Average with existing values
                    for action, value in actions.items():
                        current = model.q_table[state_key].get(action, 0)
                        model.q_table[state_key][action] = (current + value) / 2
    
    def _create_new_version(self, applied_updates: List[Dict[str, Any]]):
        """Create a new model version."""
        # Increment version
        major, minor, patch = map(int, self.current_version.split('.'))
        patch += 1
        if patch >= 10:
            minor += 1
            patch = 0
        if minor >= 10:
            major += 1
            minor = 0
        
        self.current_version = f"{major}.{minor}.{patch}"
        
        # Record version
        version_info = {
            'version': self.current_version,
            'timestamp': datetime.now().isoformat(),
            'updates_included': len(applied_updates),
            'update_types': list(set(u['type'] for u in applied_updates))
        }
        self.model_versions.append(version_info)
    
    def get_update_statistics(self) -> Dict[str, Any]:
        """Get statistics about model updates."""
        return {
            'total_updates': self.update_count,
            'pending_updates': len(self.pending_updates),
            'current_version': self.current_version,
            'version_history': len(self.model_versions),
            'update_frequency': self.update_frequency
        }
    
    def rollback_to_version(self, version: str) -> bool:
        """Rollback to a previous version (placeholder)."""
        # In a real implementation, this would restore model state
        version_exists = any(v['version'] == version for v in self.model_versions)
        if version_exists:
            self.current_version = version
            return True
        return False
    
    def export_update_log(self, filepath: str):
        """Export update log to file."""
        log_data = {
            'current_version': self.current_version,
            'total_updates': self.update_count,
            'version_history': self.model_versions,
            'pending_updates': self.pending_updates
        }
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
