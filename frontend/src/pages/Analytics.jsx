import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Minus, Activity, Users, Building, DollarSign, Clock, AlertTriangle, Shield, RefreshCw } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const Analytics = () => {
  const [kpiData, setKpiData] = useState(null);
  const [resilienceData, setResilienceData] = useState(null);
  const [economicData, setEconomicData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    loadAllData();
    
    if (autoRefresh) {
      const interval = setInterval(loadAllData, 5000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const loadAllData = async () => {
    try {
      const [kpis, resilience, economic] = await Promise.all([
        fetch('http://localhost:8001/api/analytics/kpis').then(r => r.json()),
        fetch('http://localhost:8001/api/analytics/resilience-index').then(r => r.json()),
        fetch('http://localhost:8001/api/analytics/economic-losses').then(r => r.json())
      ]);
      
      setKpiData(kpis);
      setResilienceData(resilience);
      setEconomicData(economic);
      setLoading(false);
    } catch (error) {
      console.error('Error loading analytics:', error);
      setLoading(false);
    }
  };

  const resetSimulation = async () => {
    try {
      await fetch('http://localhost:8001/api/analytics/reset-simulation', { method: 'POST' });
      loadAllData();
    } catch (error) {
      console.error('Error resetting simulation:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'good': return '#10b981';
      case 'warning': return '#f59e0b';
      case 'critical': return '#ef4444';
      default: return '#64748b';
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving': return <TrendingUp size={16} color="#10b981" />;
      case 'declining': return <TrendingDown size={16} color="#ef4444" />;
      default: return <Minus size={16} color="#64748b" />;
    }
  };

  const formatNumber = (num, decimals = 0) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(decimals)}M`;
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(decimals)}K`;
    }
    return num.toFixed(decimals);
  };

  const formatCurrency = (num) => {
    return `₹${formatNumber(num, 1)}`;
  };

  if (loading) {
    return (
      <div className="page">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
          <div style={{ textAlign: 'center' }}>
            <Activity size={48} color="#3b82f6" className="spin" />
            <div style={{ marginTop: '1rem', color: '#94a3b8' }}>Loading Analytics...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>📊 KPI Analytics Dashboard</h1>
          <p>Real-time Key Performance Indicators and Metrics</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button
            className="btn btn-secondary"
            onClick={() => setAutoRefresh(!autoRefresh)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <RefreshCw size={16} className={autoRefresh ? 'spin' : ''} />
            {autoRefresh ? 'Auto-Refresh ON' : 'Auto-Refresh OFF'}
          </button>
          <button
            className="btn btn-primary"
            onClick={resetSimulation}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <RefreshCw size={16} />
            Reset Simulation
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid-4">
        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '0.5rem',
              background: 'linear-gradient(135deg, #ef4444, #dc2626)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <AlertTriangle size={24} color="white" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                Casualties
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                {kpiData?.casualties || 0}
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '0.5rem',
              background: 'linear-gradient(135deg, #3b82f6, #2563eb)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Users size={24} color="white" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                Population Affected
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                {formatNumber(kpiData?.population_affected || 0)}
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '0.5rem',
              background: 'linear-gradient(135deg, #f59e0b, #d97706)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <DollarSign size={24} color="white" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                Economic Loss
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                {formatCurrency(kpiData?.economic_loss || 0)}
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '0.5rem',
              background: 'linear-gradient(135deg, #10b981, #059669)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Shield size={24} color="white" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                Resilience Score
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                {resilienceData?.overall_resilience?.toFixed(1) || 0}%
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* KPI Details */}
      {kpiData?.kpis && (
        <Card title="📈 Key Performance Indicators">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {Object.entries(kpiData.kpis).map(([name, kpi]) => (
              <div key={name} style={{
                padding: '1rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                borderLeft: `4px solid ${getStatusColor(kpi.status)}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                  <div>
                    <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      {name.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                    </div>
                    <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: getStatusColor(kpi.status) }}>
                      {kpi.unit === 'ratio' ? (kpi.value * 100).toFixed(1) + '%' :
                       kpi.unit === 'currency' ? formatCurrency(kpi.value) :
                       kpi.unit === 'people' ? formatNumber(kpi.value) :
                       kpi.value.toFixed(1)}
                      {kpi.unit !== 'ratio' && kpi.unit !== 'currency' && kpi.unit !== 'people' && ` ${kpi.unit}`}
                    </div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.25rem' }}>
                    <div style={{
                      padding: '0.25rem 0.5rem',
                      borderRadius: '0.25rem',
                      background: getStatusColor(kpi.status) + '20',
                      color: getStatusColor(kpi.status),
                      fontSize: '0.65rem',
                      fontWeight: 'bold'
                    }}>
                      {kpi.status.toUpperCase()}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      {getTrendIcon(kpi.trend)}
                      <span style={{ fontSize: '0.65rem', color: '#94a3b8' }}>
                        {kpi.trend}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      <div className="grid-2">
        {/* Resilience Metrics */}
        {resilienceData && (
          <Card title="🛡️ Resilience Index">
            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Overall Resilience</span>
                <span style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#10b981' }}>
                  {resilienceData.overall_resilience.toFixed(1)}%
                </span>
              </div>
              <div style={{
                height: '12px',
                background: '#0f172a',
                borderRadius: '6px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${resilienceData.overall_resilience}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #10b981, #059669)',
                  transition: 'width 0.5s'
                }} />
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {[
                { name: 'Robustness', value: resilienceData.robustness, icon: <Building size={16} /> },
                { name: 'Redundancy', value: resilienceData.redundancy, icon: <Shield size={16} /> },
                { name: 'Resourcefulness', value: resilienceData.resourcefulness, icon: <Activity size={16} /> },
                { name: 'Rapidity', value: resilienceData.rapidity, icon: <Clock size={16} /> }
              ].map((metric) => (
                <div key={metric.name}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                      {metric.icon}
                      <span>{metric.name}</span>
                    </div>
                    <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                      {metric.value.toFixed(1)}%
                    </span>
                  </div>
                  <div style={{
                    height: '6px',
                    background: '#0f172a',
                    borderRadius: '3px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${metric.value}%`,
                      height: '100%',
                      background: metric.value > 75 ? '#10b981' : metric.value > 50 ? '#f59e0b' : '#ef4444',
                      transition: 'width 0.5s'
                    }} />
                  </div>
                </div>
              ))}
            </div>

            <div style={{
              marginTop: '1rem',
              padding: '0.75rem',
              background: '#0f172a',
              borderRadius: '0.5rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Trend</span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                {resilienceData.trend === 'improving' ? 
                  <TrendingUp size={16} color="#10b981" /> : 
                  <TrendingDown size={16} color="#ef4444" />
                }
                <span style={{ 
                  fontSize: '0.875rem', 
                  fontWeight: 'bold',
                  color: resilienceData.trend === 'improving' ? '#10b981' : '#ef4444'
                }}>
                  {resilienceData.trend}
                </span>
              </div>
            </div>
          </Card>
        )}

        {/* Economic Losses */}
        {economicData && (
          <Card title="💰 Economic Impact Analysis">
            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Total Economic Loss
              </div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ef4444' }}>
                {formatCurrency(economicData.total_loss)}
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Direct Damage</span>
                  <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                    {formatCurrency(economicData.direct_damage)}
                  </span>
                </div>
                <div style={{
                  height: '8px',
                  background: '#0f172a',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${(economicData.direct_damage / economicData.total_loss) * 100}%`,
                    height: '100%',
                    background: 'linear-gradient(90deg, #ef4444, #dc2626)'
                  }} />
                </div>
              </div>

              <div style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Indirect Loss</span>
                  <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                    {formatCurrency(economicData.indirect_loss)}
                  </span>
                </div>
                <div style={{
                  height: '8px',
                  background: '#0f172a',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${(economicData.indirect_loss / economicData.total_loss) * 100}%`,
                    height: '100%',
                    background: 'linear-gradient(90deg, #f59e0b, #d97706)'
                  }} />
                </div>
              </div>

              <div style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Recovery Cost</span>
                  <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                    {formatCurrency(economicData.recovery_cost)}
                  </span>
                </div>
                <div style={{
                  height: '8px',
                  background: '#0f172a',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${(economicData.recovery_cost / economicData.total_loss) * 100}%`,
                    height: '100%',
                    background: 'linear-gradient(90deg, #3b82f6, #2563eb)'
                  }} />
                </div>
              </div>
            </div>
          </Card>
        )}
      </div>

      <style>{`
        .spin {
          animation: spin 2s linear infinite;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Analytics;
