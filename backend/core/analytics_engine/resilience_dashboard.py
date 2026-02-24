"""
Resilience Dashboard Metrics - Aggregates metrics for dashboard display.
"""

from typing import Dict, Any, List, Optional


class ResilienceDashboardMetrics:
    """Aggregates and formats metrics for dashboard display."""
    
    def __init__(self):
        self.dashboard_data: Dict[str, Any] = {}
    
    def generate_dashboard(
        self,
        kpis: Dict[str, Any],
        resilience_score: Dict[str, Any],
        economic_losses: Dict[str, Any],
        social_stability: Dict[str, Any],
        simulation_stats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate complete dashboard data."""
        
        dashboard = {
            'summary': self._generate_summary(kpis, resilience_score),
            'kpi_overview': self._format_kpi_overview(kpis),
            'resilience_metrics': resilience_score,
            'economic_impact': economic_losses,
            'social_metrics': social_stability,
            'simulation_performance': simulation_stats,
            'alerts': self._generate_alerts(kpis, resilience_score, social_stability),
            'recommendations': self._generate_recommendations(kpis, resilience_score)
        }
        
        self.dashboard_data = dashboard
        return dashboard
    
    def _generate_summary(self, kpis: Dict, resilience: Dict) -> Dict[str, Any]:
        """Generate executive summary."""
        kpi_summary = kpis.get('summary', {}) if isinstance(kpis, dict) else {}
        
        return {
            'overall_status': self._determine_overall_status(kpi_summary, resilience),
            'critical_issues': kpi_summary.get('critical_kpis', []),
            'resilience_level': resilience.get('overall_score', 0),
            'key_message': self._generate_key_message(kpi_summary, resilience)
        }
    
    def _format_kpi_overview(self, kpis: Dict) -> List[Dict[str, Any]]:
        """Format KPIs for display."""
        formatted = []
        
        for name, kpi in kpis.items():
            if name == 'summary':
                continue
            
            if hasattr(kpi, 'value'):
                formatted.append({
                    'name': name,
                    'value': kpi.value,
                    'unit': kpi.unit,
                    'status': kpi.status,
                    'trend': kpi.trend
                })
        
        return formatted
    
    def _generate_alerts(self, kpis: Dict, resilience: Dict, social: Dict) -> List[Dict[str, str]]:
        """Generate alerts for critical issues."""
        alerts = []
        
        # KPI alerts
        kpi_summary = kpis.get('summary', {}) if isinstance(kpis, dict) else {}
        critical_kpis = kpi_summary.get('critical_kpis', [])
        
        for kpi_name in critical_kpis:
            alerts.append({
                'severity': 'high',
                'category': 'kpi',
                'message': f"Critical KPI: {kpi_name} requires immediate attention"
            })
        
        # Resilience alerts
        resilience_score = resilience.get('overall_score', 100)
        if resilience_score < 40:
            alerts.append({
                'severity': 'high',
                'category': 'resilience',
                'message': "City resilience is critically low"
            })
        
        # Social stability alerts
        stability = social.get('overall_stability', 100)
        if stability < 50:
            alerts.append({
                'severity': 'medium',
                'category': 'social',
                'message': "Social stability is declining"
            })
        
        return alerts
    
    def _generate_recommendations(self, kpis: Dict, resilience: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        kpi_summary = kpis.get('summary', {}) if isinstance(kpis, dict) else {}
        
        if kpi_summary.get('critical_kpis'):
            recommendations.append("Address critical KPIs immediately")
        
        resilience_score = resilience.get('overall_score', 100)
        if resilience_score < 60:
            recommendations.append("Invest in infrastructure redundancy")
        
        return recommendations
    
    def _determine_overall_status(self, kpi_summary: Dict, resilience: Dict) -> str:
        """Determine overall system status."""
        critical_count = len(kpi_summary.get('critical_kpis', []))
        resilience_score = resilience.get('overall_score', 100)
        
        if critical_count > 2 or resilience_score < 40:
            return "critical"
        elif critical_count > 0 or resilience_score < 60:
            return "warning"
        else:
            return "good"
    
    def _generate_key_message(self, kpi_summary: Dict, resilience: Dict) -> str:
        """Generate key message for dashboard."""
        status = self._determine_overall_status(kpi_summary, resilience)
        
        if status == "critical":
            return "Immediate action required - multiple critical issues detected"
        elif status == "warning":
            return "Attention needed - some metrics below target"
        else:
            return "System performing well - continue monitoring"
