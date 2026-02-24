"""
Transparency Report Builder - Generates comprehensive transparency reports.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class TransparencyReportBuilder:
    """Builds comprehensive transparency reports for AI decisions."""
    
    def __init__(self):
        self.reports: List[Dict[str, Any]] = []
    
    def build_report(
        self,
        decision_trace: Any,
        causal_graph: Dict[str, Any],
        shap_explanation: Dict[str, Any],
        counterfactual: Dict[str, Any],
        confidence: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build a comprehensive transparency report."""
        
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        report = {
            'report_id': report_id,
            'timestamp': datetime.now().isoformat(),
            'decision_summary': self._build_decision_summary(decision_trace),
            'confidence_assessment': self._build_confidence_section(confidence),
            'causal_analysis': self._build_causal_section(causal_graph),
            'feature_importance': self._build_feature_importance_section(shap_explanation),
            'counterfactual_analysis': self._build_counterfactual_section(counterfactual),
            'decision_trace': self._build_trace_section(decision_trace),
            'recommendations': self._generate_recommendations(confidence, counterfactual),
            'metadata': additional_context or {}
        }
        
        self.reports.append(report)
        return report
    
    def _build_decision_summary(self, trace: Any) -> Dict[str, Any]:
        """Build decision summary section."""
        if hasattr(trace, 'to_dict'):
            trace_dict = trace.to_dict()
        else:
            trace_dict = trace if isinstance(trace, dict) else {}
        
        return {
            'decision_type': trace_dict.get('decision_type', 'unknown'),
            'timestamp': trace_dict.get('timestamp', ''),
            'final_decision': trace_dict.get('final_decision', {}),
            'execution_time_ms': trace_dict.get('execution_time_ms', 0),
            'num_steps': len(trace_dict.get('steps', []))
        }
    
    def _build_confidence_section(self, confidence: Dict[str, Any]) -> Dict[str, Any]:
        """Build confidence assessment section."""
        return {
            'overall_confidence': confidence.get('overall_confidence', 0),
            'confidence_level': confidence.get('confidence_level', 'unknown'),
            'key_factors': confidence.get('confidence_factors', {}),
            'explanation': confidence.get('explanation', ''),
            'low_confidence_factors': [
                k for k, v in confidence.get('confidence_factors', {}).items()
                if v < 0.6
            ]
        }
    
    def _build_causal_section(self, causal_graph: Dict[str, Any]) -> Dict[str, Any]:
        """Build causal analysis section."""
        return {
            'num_nodes': len(causal_graph.get('nodes', [])),
            'num_edges': len(causal_graph.get('edges', [])),
            'critical_path': self._extract_critical_path(causal_graph),
            'key_relationships': self._extract_key_relationships(causal_graph)
        }
    
    def _build_feature_importance_section(
        self,
        shap_explanation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build feature importance section."""
        return {
            'top_features': shap_explanation.get('top_features', []),
            'feature_contributions': shap_explanation.get('feature_contributions', {}),
            'explanation': self._summarize_feature_importance(shap_explanation)
        }
    
    def _build_counterfactual_section(
        self,
        counterfactual: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build counterfactual analysis section."""
        if not counterfactual.get('success'):
            return {
                'available': False,
                'message': 'Counterfactual analysis not available'
            }
        
        return {
            'available': True,
            'minimal_changes': counterfactual.get('num_changes', 0),
            'changes_required': list(counterfactual.get('changes', {}).keys()),
            'explanation': counterfactual.get('explanation', '')
        }
    
    def _build_trace_section(self, trace: Any) -> Dict[str, Any]:
        """Build decision trace section."""
        if hasattr(trace, 'to_dict'):
            trace_dict = trace.to_dict()
        else:
            trace_dict = trace if isinstance(trace, dict) else {}
        
        steps = trace_dict.get('steps', [])
        
        return {
            'num_steps': len(steps),
            'step_summary': [
                {
                    'component': step.get('component', 'unknown'),
                    'action': step.get('action', 'unknown'),
                    'confidence': step.get('confidence', 0)
                }
                for step in steps[:5]  # First 5 steps
            ],
            'avg_step_confidence': sum(s.get('confidence', 0) for s in steps) / len(steps) if steps else 0
        }
    
    def _extract_critical_path(self, causal_graph: Dict[str, Any]) -> List[str]:
        """Extract critical path from causal graph."""
        nodes = causal_graph.get('nodes', [])
        # Sort by importance
        sorted_nodes = sorted(nodes, key=lambda n: n.get('importance', 0), reverse=True)
        return [n['label'] for n in sorted_nodes[:5]]
    
    def _extract_key_relationships(self, causal_graph: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract key relationships from causal graph."""
        edges = causal_graph.get('edges', [])
        nodes = causal_graph.get('nodes', [])
        
        # Get strongest edges
        sorted_edges = sorted(edges, key=lambda e: e.get('strength', 0), reverse=True)
        
        relationships = []
        for edge in sorted_edges[:5]:
            source = next((n for n in nodes if n['node_id'] == edge['source_id']), None)
            target = next((n for n in nodes if n['node_id'] == edge['target_id']), None)
            
            if source and target:
                relationships.append({
                    'from': source['label'],
                    'to': target['label'],
                    'type': edge.get('relation_type', 'unknown'),
                    'explanation': edge.get('explanation', '')
                })
        
        return relationships
    
    def _summarize_feature_importance(self, shap_explanation: Dict[str, Any]) -> str:
        """Summarize feature importance."""
        top_features = shap_explanation.get('top_features', [])
        if not top_features:
            return "No feature importance data available"
        
        top_3 = top_features[:3]
        return f"The most important features are: {', '.join(top_3)}"
    
    def _generate_recommendations(
        self,
        confidence: Dict[str, Any],
        counterfactual: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Confidence-based recommendations
        conf_level = confidence.get('confidence_level', 'unknown')
        if conf_level in ['low', 'very_low']:
            recommendations.append(
                "⚠️ Low confidence detected. Consider gathering more data or reviewing model parameters."
            )
        
        # Counterfactual-based recommendations
        if counterfactual.get('success'):
            num_changes = counterfactual.get('num_changes', 0)
            if num_changes == 1:
                recommendations.append(
                    "✓ Decision is sensitive to a single factor. Monitor this factor closely."
                )
            elif num_changes > 3:
                recommendations.append(
                    "⚠️ Decision requires multiple factors to change. Consider if this is appropriate."
                )
        
        # General recommendations
        if not recommendations:
            recommendations.append("✓ Decision appears well-supported and transparent.")
        
        return recommendations
    
    def generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML version of report."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Transparency Report - {report['report_id']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
                .section {{ margin: 20px 0; }}
                .confidence-high {{ color: green; }}
                .confidence-medium {{ color: orange; }}
                .confidence-low {{ color: red; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>AI Decision Transparency Report</h1>
            <p><strong>Report ID:</strong> {report['report_id']}</p>
            <p><strong>Generated:</strong> {report['timestamp']}</p>
            
            <div class="section">
                <h2>Decision Summary</h2>
                <p><strong>Type:</strong> {report['decision_summary']['decision_type']}</p>
                <p><strong>Execution Time:</strong> {report['decision_summary']['execution_time_ms']:.2f} ms</p>
                <p><strong>Steps:</strong> {report['decision_summary']['num_steps']}</p>
            </div>
            
            <div class="section">
                <h2>Confidence Assessment</h2>
                <p class="confidence-{report['confidence_assessment']['confidence_level']}">
                    <strong>Confidence Level:</strong> {report['confidence_assessment']['confidence_level']} 
                    ({report['confidence_assessment']['overall_confidence']:.2f})
                </p>
                <p>{report['confidence_assessment']['explanation']}</p>
            </div>
            
            <div class="section">
                <h2>Feature Importance</h2>
                <p>{report['feature_importance']['explanation']}</p>
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                <ul>
                    {''.join(f'<li>{rec}</li>' for rec in report['recommendations'])}
                </ul>
            </div>
        </body>
        </html>
        """
        return html
    
    def export_report(self, report_id: str, filepath: str, format: str = 'json'):
        """Export report to file."""
        report = next((r for r in self.reports if r['report_id'] == report_id), None)
        if not report:
            raise ValueError(f"Report {report_id} not found")
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
        elif format == 'html':
            html = self.generate_html_report(report)
            with open(filepath, 'w') as f:
                f.write(html)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific report."""
        return next((r for r in self.reports if r['report_id'] == report_id), None)
    
    def list_reports(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent reports."""
        return self.reports[-limit:]
