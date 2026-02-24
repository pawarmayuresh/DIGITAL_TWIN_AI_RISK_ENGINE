"""
Checkpoint Manager - Saves and loads training checkpoints.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import os
from pathlib import Path


class CheckpointManager:
    """Manages training checkpoints for RL models."""
    
    def __init__(self, checkpoint_dir: str = "checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints: List[Dict[str, Any]] = []
        self._load_checkpoint_index()
    
    def save_checkpoint(
        self,
        agent: Any,
        experience_store: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a training checkpoint."""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_id = f"checkpoint_{timestamp}"
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        checkpoint_path.mkdir(exist_ok=True)
        
        # Save agent policy
        agent_file = checkpoint_path / "agent_policy.json"
        agent.save_policy(str(agent_file))
        
        # Save experience store
        experience_file = checkpoint_path / "experiences.json"
        experience_store.save_to_file(str(experience_file))
        
        # Save metadata
        checkpoint_metadata = {
            'checkpoint_id': checkpoint_id,
            'timestamp': datetime.now().isoformat(),
            'agent_stats': agent.get_statistics(),
            'experience_stats': experience_store.get_statistics(),
            'custom_metadata': metadata or {}
        }
        
        metadata_file = checkpoint_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(checkpoint_metadata, f, indent=2)
        
        # Update checkpoint index
        self.checkpoints.append(checkpoint_metadata)
        self._save_checkpoint_index()
        
        return checkpoint_id
    
    def load_checkpoint(
        self,
        checkpoint_id: str,
        agent: Any,
        experience_store: Any
    ) -> bool:
        """Load a training checkpoint."""
        
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        
        if not checkpoint_path.exists():
            return False
        
        try:
            # Load agent policy
            agent_file = checkpoint_path / "agent_policy.json"
            if agent_file.exists():
                agent.load_policy(str(agent_file))
            
            # Load experience store
            experience_file = checkpoint_path / "experiences.json"
            if experience_file.exists():
                experience_store.load_from_file(str(experience_file))
            
            return True
        
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return False
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints."""
        return sorted(self.checkpoints, key=lambda x: x['timestamp'], reverse=True)
    
    def get_latest_checkpoint(self) -> Optional[str]:
        """Get the ID of the most recent checkpoint."""
        if not self.checkpoints:
            return None
        latest = max(self.checkpoints, key=lambda x: x['timestamp'])
        return latest['checkpoint_id']
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint."""
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        
        if not checkpoint_path.exists():
            return False
        
        try:
            # Remove files
            for file in checkpoint_path.iterdir():
                file.unlink()
            checkpoint_path.rmdir()
            
            # Update index
            self.checkpoints = [c for c in self.checkpoints if c['checkpoint_id'] != checkpoint_id]
            self._save_checkpoint_index()
            
            return True
        
        except Exception as e:
            print(f"Error deleting checkpoint: {e}")
            return False
    
    def cleanup_old_checkpoints(self, keep_last_n: int = 5):
        """Keep only the N most recent checkpoints."""
        if len(self.checkpoints) <= keep_last_n:
            return
        
        sorted_checkpoints = sorted(self.checkpoints, key=lambda x: x['timestamp'], reverse=True)
        to_delete = sorted_checkpoints[keep_last_n:]
        
        for checkpoint in to_delete:
            self.delete_checkpoint(checkpoint['checkpoint_id'])
    
    def _save_checkpoint_index(self):
        """Save checkpoint index to disk."""
        index_file = self.checkpoint_dir / "checkpoint_index.json"
        with open(index_file, 'w') as f:
            json.dump(self.checkpoints, f, indent=2)
    
    def _load_checkpoint_index(self):
        """Load checkpoint index from disk."""
        index_file = self.checkpoint_dir / "checkpoint_index.json"
        if index_file.exists():
            with open(index_file, 'r') as f:
                self.checkpoints = json.load(f)
    
    def get_checkpoint_info(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific checkpoint."""
        for checkpoint in self.checkpoints:
            if checkpoint['checkpoint_id'] == checkpoint_id:
                return checkpoint
        return None
    
    def export_checkpoint(self, checkpoint_id: str, export_path: str) -> bool:
        """Export a checkpoint to a different location."""
        import shutil
        
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        if not checkpoint_path.exists():
            return False
        
        try:
            shutil.copytree(checkpoint_path, export_path)
            return True
        except Exception as e:
            print(f"Error exporting checkpoint: {e}")
            return False
