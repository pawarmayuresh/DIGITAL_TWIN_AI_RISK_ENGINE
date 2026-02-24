"""
Audit Log Interpreter - Interprets and analyzes audit logs for compliance.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict


class AuditLogInterpreter:
    """Interprets audit logs and generates compliance reports."""
    
    def __init__(self):
        self.audit_logs: List[Dict[str, Any]] = []
        self.interpretations: List[Dict[str, Any]] = []
    
    def log_decision(
        self,
        decision_id: str,
        decision_type: str,
        user_id: Optional[str],
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        confidence: float,
        explanation: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a decision for audit purposes."""
        log_entry = {
            'log_id': f"log_{len(self.audit_logs) + 1}",
            'decision_id': decision_id,
            'decision_type': decision_type,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'inputs': inputs,
            'outputs': outputs,
            'confidence': confidence,
            'explanation': explanation,
            'metadata': metadata or {}
        }
        
        self.audit_logs.append(log_entry)
    
    def interpret_logs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        decision_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Interpret audit logs and generate insights."""
        
        # Filter logs
        filtered_logs = self._filter_logs(start_date, end_date, decision_type)
        
        if not filtered_logs:
            return {'status': 'no_logs', 'message': 'No logs found for criteria'}
        
        interpretation = {
            'interpretation_id': f"interp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'num_logs_analyzed': len(filtered_logs),
            'time_range': {
                'start': filtered_logs[0]['timestamp'],
                'end': filtered_logs[-1]['timestamp']
            },
            'decision_statistics': self._analyze_decision_statistics(filtered_logs),
            'confidence_analysis': self._analyze_confidence(filtered_logs),
            'user_activity': self._analyze_user_activity(filtered_logs),
            'anomalies': self._detect_anomalies(filtered_logs),
            'compliance_status': self._assess_compliance(filtered_logs)
        }
        
        self.interpretations.append(interpretation)
        return interpretation
    
    def _filter_logs(
        self,
        start_date: Optional[str],
        end_date: Optional[str],
        decision_type: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Filter logs by criteria."""
        filtered = self.audit_logs
        
        if decision_type:
            filtered = [log for log in filtered if log['decision_type'] == decision_type]
        
        if start_date:
            filtered = [log for log in filtered if log['timestamp'] >= start_date]
        
        if end_date:
            filtered = [log for log in filtered if log['timestamp'] <= end_date]
        
        return filtered
    
    def _analyze_decision_statistics(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze decision statistics."""
        decision_types = defaultdict(int)
        for log in logs:
            decision_types[log['decision_type']] += 1
        
        return {
            'total_decisions': len(logs),
            'decisions_by_type': dict(decision_types),
            'most_common_type': max(decision_types.items(), key=lambda x: x[1])[0] if decision_types else None
        }
    
    def _analyze_confidence(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze confidence levels."""
        confidences = [log['confidence'] for log in logs]
        
        if not confidences:
            return {}
        
        avg_confidence = sum(confidences) / len(confidences)
        low_confidence_count = sum(1 for c in confidences if c < 0.6)
        
        return {
            'avg_confidence': avg_confidence,
            'min_confidence': min(confidences),
            'max_confidence': max(confidences),
            'low_confidence_decisions': low_confidence_count,
            'low_confidence_percentage': (low_confidence_count / len(confidences)) * 100
        }
    
    def _analyze_user_activity(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user activity."""
        user_decisions = defaultdict(int)
        for log in logs:
            user_id = log.get('user_id', 'system')
            user_decisions[user_id] += 1
        
        return {
            'unique_users': len(user_decisions),
            'decisions_by_user': dict(user_decisions),
            'most_active_user': max(user_decisions.items(), key=lambda x: x[1])[0] if user_decisions else None
        }
    
    def _detect_anomalies(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in logs."""
        anomalies = []
        
        # Check for very low confidence decisions
        for log in logs:
            if log['confidence'] < 0.3:
                anomalies.append({
                    'type': 'low_confidence',
                    'log_id': log['log_id'],
                    'decision_id': log['decision_id'],
                    'confidence': log['confidence'],
                    'severity': 'high'
                })
        
        # Check for rapid decision sequences (potential automation issues)
        for i in range(len(logs) - 1):
            time1 = datetime.fromisoformat(logs[i]['timestamp'])
            time2 = datetime.fromisoformat(logs[i+1]['timestamp'])
            time_diff = (time2 - time1).total_seconds()
            
            if time_diff < 0.1:  # Less than 100ms between decisions
                anomalies.append({
                    'type': 'rapid_sequence',
                    'log_ids': [logs[i]['log_id'], logs[i+1]['log_id']],
                    'time_diff_seconds': time_diff,
                    'severity': 'medium'
                })
        
        return anomalies
    
    def _assess_compliance(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess compliance with transparency requirements."""
        compliance_checks = {
            'all_decisions_logged': len(logs) > 0,
            'explanations_provided': all('explanation' in log and log['explanation'] for log in logs),
            'confidence_tracked': all('confidence' in log for log in logs),
            'user_attribution': all('user_id' in log for log in logs),
            'timestamps_present': all('timestamp' in log for log in logs)
        }
        
        compliance_score = sum(compliance_checks.values()) / len(compliance_checks)
        
        return {
            'compliance_score': compliance_score,
            'compliance_percentage': compliance_score * 100,
            'checks': compliance_checks,
            'status': 'compliant' if compliance_score >= 0.8 else 'non_compliant',
            'missing_requirements': [k for k, v in compliance_checks.items() if not v]
        }
    
    def generate_audit_report(
        self,
        interpretation_id: str
    ) -> Dict[str, Any]:
        """Generate a comprehensive audit report."""
        interpretation = next(
            (i for i in self.interpretations if i['interpretation_id'] == interpretation_id),
            None
        )
        
        if not interpretation:
            return {'error': 'Interpretation not found'}
        
        report = {
            'report_id': f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'interpretation': interpretation,
            'summary': self._generate_audit_summary(interpretation),
            'recommendations': self._generate_audit_recommendations(interpretation)
        }
        
        return report
    
    def _generate_audit_summary(self, interpretation: Dict[str, Any]) -> str:
        """Generate audit summary text."""
        stats = interpretation['decision_statistics']
        confidence = interpretation['confidence_analysis']
        compliance = interpretation['compliance_status']
        
        summary = f"Analyzed {stats['total_decisions']} decisions. "
        summary += f"Average confidence: {confidence.get('avg_confidence', 0):.2f}. "
        summary += f"Compliance score: {compliance['compliance_percentage']:.1f}%. "
        
        if interpretation['anomalies']:
            summary += f"Found {len(interpretation['anomalies'])} anomalies requiring attention."
        else:
            summary += "No anomalies detected."
        
        return summary
    
    def _generate_audit_recommendations(self, interpretation: Dict[str, Any]) -> List[str]:
        """Generate audit recommendations."""
        recommendations = []
        
        # Confidence recommendations
        confidence = interpretation['confidence_analysis']
        if confidence.get('low_confidence_percentage', 0) > 20:
            recommendations.append(
                "⚠️ High percentage of low-confidence decisions. Review model performance."
            )
        
        # Compliance recommendations
        compliance = interpretation['compliance_status']
        if compliance['status'] == 'non_compliant':
            missing = compliance['missing_requirements']
            recommendations.append(
                f"⚠️ Compliance issues detected: {', '.join(missing)}"
            )
        
        # Anomaly recommendations
        if interpretation['anomalies']:
            high_severity = [a for a in interpretation['anomalies'] if a.get('severity') == 'high']
            if high_severity:
                recommendations.append(
                    f"🚨 {len(high_severity)} high-severity anomalies require immediate attention"
                )
        
        if not recommendations:
            recommendations.append("✓ Audit looks good. No immediate actions required.")
        
        return recommendations
    
    def export_audit_logs(self, filepath: str, format: str = 'json'):
        """Export audit logs to file."""
        import json
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump({
                    'logs': self.audit_logs,
                    'total_logs': len(self.audit_logs)
                }, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_decision_audit_trail(self, decision_id: str) -> List[Dict[str, Any]]:
        """Get complete audit trail for a specific decision."""
        return [log for log in self.audit_logs if log['decision_id'] == decision_id]
