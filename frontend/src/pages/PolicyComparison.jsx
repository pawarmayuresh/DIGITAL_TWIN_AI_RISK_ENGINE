import { useState } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const PolicyComparison = () => {
  const [selectedMetric, setSelectedMetric] = useState('casualties');

  const policies = [
    {
      id: 1,
      name: 'Aggressive Response',
      description: 'Immediate evacuation and maximum resource deployment',
      metrics: {
        casualties: 50,
        cost: 5000000,
        response_time: 15,
        public_satisfaction: 85
      }
    },
    {
      id: 2,
      name: 'Balanced Approach',
      description: 'Measured response with resource optimization',
      metrics: {
        casualties: 75,
        cost: 3000000,
        response_time: 30,
        public_satisfaction: 75
      }
    },
    {
      id: 3,
      name: 'Conservative Strategy',
      description: 'Minimal intervention, monitor and respond',
      metrics: {
        casualties: 120,
        cost: 1500000,
        response_time: 45,
        public_satisfaction: 60
      }
    }
  ];

  const metrics = [
    { id: 'casualties', name: 'Casualties', unit: 'people', lowerIsBetter: true },
    { id: 'cost', name: 'Cost', unit: '$', lowerIsBetter: true },
    { id: 'response_time', name: 'Response Time', unit: 'min', lowerIsBetter: true },
    { id: 'public_satisfaction', name: 'Public Satisfaction', unit: '%', lowerIsBetter: false }
  ];

  const getBestPolicy = (metricId) => {
    const metric = metrics.find(m => m.id === metricId);
    if (!metric) return null;
    
    return policies.reduce((best, policy) => {
      const value = policy.metrics[metricId];
      const bestValue = best.metrics[metricId];
      
      if (metric.lowerIsBetter) {
        return value < bestValue ? policy : best;
      } else {
        return value > bestValue ? policy : best;
      }
    });
  };

  const getTrend = (policy, metricId) => {
    const bestPolicy = getBestPolicy(metricId);
    if (!bestPolicy) return 'neutral';
    
    if (bestPolicy.id === policy.id) return 'best';
    
    const metric = metrics.find(m => m.id === metricId);
    const value = policy.metrics[metricId];
    const bestValue = bestPolicy.metrics[metricId];
    const diff = Math.abs(value - bestValue) / bestValue;
    
    if (diff < 0.2) return 'good';
    if (diff < 0.5) return 'neutral';
    return 'poor';
  };

  const formatValue = (value, unit) => {
    if (unit === '$') return `$${(value / 1000000).toFixed(1)}M`;
    return `${value}${unit}`;
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Policy Comparison</h1>
        <p>Compare different response strategies</p>
      </div>

      <Card title="Policy Metrics">
        <div className="form-group">
          <label className="form-label">Compare by Metric</label>
          <select 
            className="form-select"
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value)}
          >
            {metrics.map(m => (
              <option key={m.id} value={m.id}>{m.name}</option>
            ))}
          </select>
        </div>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1rem',
          marginTop: '1.5rem'
        }}>
          {policies.map(policy => {
            const trend = getTrend(policy, selectedMetric);
            const metric = metrics.find(m => m.id === selectedMetric);
            const value = policy.metrics[selectedMetric];
            
            return (
              <div 
                key={policy.id}
                style={{
                  background: '#0f172a',
                  border: `2px solid ${trend === 'best' ? '#10b981' : '#334155'}`,
                  borderRadius: '0.5rem',
                  padding: '1.5rem'
                }}
              >
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between',
                  marginBottom: '0.5rem'
                }}>
                  <h4 style={{ color: '#f1f5f9', fontSize: '1.125rem' }}>
                    {policy.name}
                  </h4>
                  {trend === 'best' && (
                    <span className="status-badge status-good">Best</span>
                  )}
                </div>
                
                <p style={{ color: '#94a3b8', fontSize: '0.875rem', marginBottom: '1rem' }}>
                  {policy.description}
                </p>

                <div style={{ 
                  background: '#1e293b', 
                  padding: '1rem', 
                  borderRadius: '0.375rem',
                  marginBottom: '1rem'
                }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.25rem' }}>
                    {metric.name}
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#f1f5f9' }}>
                    {formatValue(value, metric.unit)}
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {metrics.filter(m => m.id !== selectedMetric).map(m => (
                    <div key={m.id} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                      <span style={{ color: '#94a3b8' }}>{m.name}</span>
                      <span style={{ color: '#cbd5e1' }}>
                        {formatValue(policy.metrics[m.id], m.unit)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      <Card title="Metric Comparison Chart">
        <div style={{ padding: '1rem' }}>
          {metrics.map(metric => {
            const maxValue = Math.max(...policies.map(p => p.metrics[metric.id]));
            
            return (
              <div key={metric.id} style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                  {metric.name}
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  {policies.map(policy => {
                    const value = policy.metrics[metric.id];
                    const percentage = (value / maxValue) * 100;
                    const trend = getTrend(policy, metric.id);
                    
                    return (
                      <div key={policy.id} style={{ flex: 1 }}>
                        <div style={{
                          height: '40px',
                          background: trend === 'best' ? '#10b981' : 
                                    trend === 'good' ? '#3b82f6' : 
                                    trend === 'neutral' ? '#f59e0b' : '#ef4444',
                          borderRadius: '0.25rem',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontSize: '0.75rem',
                          fontWeight: '600',
                          opacity: 0.9
                        }}>
                          {formatValue(value, metric.unit)}
                        </div>
                        <div style={{ 
                          fontSize: '0.75rem', 
                          color: '#64748b', 
                          textAlign: 'center',
                          marginTop: '0.25rem'
                        }}>
                          {policy.name.split(' ')[0]}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};

export default PolicyComparison;
