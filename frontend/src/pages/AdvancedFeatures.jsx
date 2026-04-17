import { useState, useEffect } from 'react';
import { Brain, Zap, Users, TrendingUp, Activity, RefreshCw } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const AdvancedFeatures = () => {
  const [lstmPrediction, setLstmPrediction] = useState(null);
  const [weeklyPattern, setWeeklyPattern] = useState(null);
  const [swarmStatus, setSwarmStatus] = useState(null);
  const [externalData, setExternalData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedWard, setSelectedWard] = useState('Kurla');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [dataQuality, setDataQuality] = useState({ weather: 0, traffic: 0, sensors: 0 });

  const wards = ['Colaba', 'Byculla', 'Kurla', 'Andheri', 'Bandra', 'Chembur', 'Ghatkopar', 'Borivali'];

  useEffect(() => {
    loadAllData();
  }, [selectedWard]);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(() => {
      loadAllData();
    }, 30000);
    
    return () => clearInterval(interval);
  }, [autoRefresh, selectedWard]);

  const loadAllData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        loadLSTMPrediction(),
        loadWeeklyPattern(),
        loadSwarmStatus(),
        loadExternalData()
      ]);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadLSTMPrediction = async () => {
    try {
      const response = await fetch(`http://localhost:8001/api/advanced/ml/lstm/predict-24h/${selectedWard}`);
      if (!response.ok) {
        console.error('LSTM API error:', response.status);
        return;
      }
      const data = await response.json();
      if (data && data.predictions) {
        setLstmPrediction(data);
      }
    } catch (error) {
      console.error('Error loading LSTM prediction:', error);
    }
  };

  const loadWeeklyPattern = async () => {
    try {
      const response = await fetch(`http://localhost:8001/api/advanced/ml/lstm/weekly-pattern/${selectedWard}`);
      if (!response.ok) {
        console.error('Weekly pattern API error:', response.status);
        return;
      }
      const data = await response.json();
      if (data && data.predictions) {
        setWeeklyPattern(data);
      }
    } catch (error) {
      console.error('Error loading weekly pattern:', error);
    }
  };

  const loadSwarmStatus = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/advanced/swarm/status');
      if (!response.ok) {
        console.error('Swarm API error:', response.status);
        return;
      }
      const data = await response.json();
      if (data && !data.error) {
        setSwarmStatus(data);
      }
    } catch (error) {
      console.error('Error loading swarm status:', error);
    }
  };

  const loadExternalData = async () => {
    try {
      const response = await fetch(`http://localhost:8001/api/advanced/external-data/integrated/${selectedWard}`);
      if (!response.ok) {
        console.error('External data API error:', response.status);
        return;
      }
      const data = await response.json();
      if (data && !data.error) {
        setExternalData(data);
        
        // Update data quality indicators
        if (data.risk_factors) {
          setDataQuality({
            weather: data.risk_factors.weather_risk || 0,
            traffic: data.risk_factors.traffic_risk || 0,
            sensors: data.risk_factors.sensor_risk || 0
          });
        }
      }
    } catch (error) {
      console.error('Error loading external data:', error);
    }
  };

  const getTimeSinceUpdate = () => {
    if (!lastUpdate) return 'Never';
    const seconds = Math.floor((new Date() - lastUpdate) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m ago`;
  };

  const initializeSwarm = async () => {
    try {
      await fetch('http://localhost:8001/api/advanced/swarm/initialize?num_teams=10', {
        method: 'POST'
      });
      
      // Add some disaster zones
      const zones = [
        { zone_id: 'Z1', x: 20, y: 30, severity: 0.8, people_count: 100, priority: 5 },
        { zone_id: 'Z2', x: 60, y: 70, severity: 0.6, people_count: 50, priority: 3 },
        { zone_id: 'Z3', x: 80, y: 20, severity: 0.9, people_count: 150, priority: 5 }
      ];
      
      for (const zone of zones) {
        await fetch(`http://localhost:8001/api/advanced/swarm/add-disaster-zone?zone_id=${zone.zone_id}&x=${zone.x}&y=${zone.y}&severity=${zone.severity}&people_count=${zone.people_count}&priority=${zone.priority}`, {
          method: 'POST'
        });
      }
      
      // Optimize
      await fetch('http://localhost:8001/api/advanced/swarm/optimize?max_iterations=50', {
        method: 'POST'
      });
      
      await loadSwarmStatus();
    } catch (error) {
      console.error('Error initializing swarm:', error);
    }
  };

  const getRiskColor = (risk) => {
    if (risk > 0.8) return '#ef4444';
    if (risk > 0.6) return '#f59e0b';
    if (risk > 0.4) return '#3b82f6';
    return '#10b981';
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🚀 Advanced Features</h1>
          <p>Deep Learning, Swarm Intelligence & Real-Time Data Integration</p>
          {lastUpdate && (
            <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
              Last updated: {getTimeSinceUpdate()}
              {autoRefresh && <span style={{ color: '#10b981', marginLeft: '0.5rem' }}>● Live</span>}
            </div>
          )}
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <select
            value={selectedWard}
            onChange={(e) => setSelectedWard(e.target.value)}
            style={{
              padding: '0.5rem 1rem',
              background: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              color: 'white',
              fontSize: '0.875rem'
            }}
          >
            {wards.map(ward => (
              <option key={ward} value={ward}>{ward}</option>
            ))}
          </select>
          <button
            className="btn"
            onClick={() => setAutoRefresh(!autoRefresh)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: autoRefresh ? '#10b981' : '#334155',
              border: 'none'
            }}
          >
            <Activity size={16} />
            {autoRefresh ? 'Live' : 'Paused'}
          </button>
          <button
            className="btn btn-primary"
            onClick={loadAllData}
            disabled={loading}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <RefreshCw size={16} className={loading ? 'spin' : ''} />
            Refresh
          </button>
        </div>
      </div>

      {/* Feature Status */}
      <div style={{
        padding: '1rem',
        background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
        borderRadius: '0.75rem',
        marginBottom: '1.5rem',
        display: 'flex',
        justifyContent: 'space-around',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Brain size={24} color="#10b981" />
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>LSTM Model</div>
          <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
            {lstmPrediction ? 'Active' : 'Loading...'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <Users size={24} color="#10b981" />
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>Swarm AI</div>
          <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
            {swarmStatus ? 'Ready' : 'Standby'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <Activity size={24} color={autoRefresh ? '#10b981' : '#64748b'} />
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>Real-Time Data</div>
          <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
            {autoRefresh ? 'Streaming' : 'Paused'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <Zap size={24} color="#10b981" />
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>Data Quality</div>
          <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
            {externalData ? `${((dataQuality.weather + dataQuality.traffic + dataQuality.sensors) / 3 * 100).toFixed(0)}%` : '--'}
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* LSTM 24-Hour Prediction */}
        <Card title="🧠 LSTM: 24-Hour Prediction">
          {lstmPrediction && lstmPrediction.predictions ? (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Next Hour Risk
                  </div>
                  {lstmPrediction.external_data_integrated && (
                    <div style={{
                      fontSize: '0.65rem',
                      padding: '0.25rem 0.5rem',
                      background: '#10b981',
                      color: 'white',
                      borderRadius: '0.25rem',
                      fontWeight: 'bold'
                    }}>
                      LIVE DATA
                    </div>
                  )}
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
                  <div style={{
                    fontSize: '2.5rem',
                    fontWeight: 'bold',
                    color: getRiskColor(lstmPrediction.predictions[0]?.risk_score || 0)
                  }}>
                    {((lstmPrediction.predictions[0]?.risk_score || 0) * 100).toFixed(0)}%
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
                    Confidence: {((lstmPrediction.predictions[0]?.confidence || 0) * 100).toFixed(0)}%
                  </div>
                </div>
                {lstmPrediction.predictions[0]?.factors && (
                  <div style={{
                    marginTop: '0.5rem',
                    padding: '0.5rem',
                    background: '#0f172a',
                    borderRadius: '0.375rem',
                    fontSize: '0.7rem',
                    color: '#94a3b8'
                  }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.25rem' }}>
                      <div>Weather: {(lstmPrediction.predictions[0].factors.weather_impact * 100).toFixed(0)}%</div>
                      <div>Traffic: {(lstmPrediction.predictions[0].factors.traffic_impact * 100).toFixed(0)}%</div>
                      <div>Sensors: {(lstmPrediction.predictions[0].factors.sensor_impact * 100).toFixed(0)}%</div>
                      <div>Ward Base: {(lstmPrediction.predictions[0].factors.ward_base_risk * 100).toFixed(0)}%</div>
                    </div>
                  </div>
                )}
              </div>

              {/* 24-hour chart */}
              <svg width="100%" height="200" viewBox="0 0 600 200">
                {/* Grid */}
                {[0, 1, 2, 3, 4].map(i => (
                  <line
                    key={`grid-${i}`}
                    x1="40"
                    y1={40 + i * 40}
                    x2="560"
                    y2={40 + i * 40}
                    stroke="#1e293b"
                    strokeWidth="1"
                  />
                ))}

                {/* Line chart */}
                {lstmPrediction.predictions.slice(0, 24).map((pred, i) => {
                  if (i === 0) return null;
                  const prev = lstmPrediction.predictions[i - 1];
                  const x1 = 40 + ((i - 1) / 23) * 520;
                  const x2 = 40 + (i / 23) * 520;
                  const y1 = 180 - (prev.risk_score * 140);
                  const y2 = 180 - (pred.risk_score * 140);
                  
                  return (
                    <line
                      key={i}
                      x1={x1}
                      y1={y1}
                      x2={x2}
                      y2={y2}
                      stroke="#3b82f6"
                      strokeWidth="2"
                    />
                  );
                })}

                {/* Points */}
                {lstmPrediction.predictions.slice(0, 24).filter((_, i) => i % 4 === 0).map((pred, i) => {
                  const actualIndex = i * 4;
                  const x = 40 + (actualIndex / 23) * 520;
                  const y = 180 - (pred.risk_score * 140);
                  
                  return (
                    <g key={actualIndex}>
                      <circle
                        cx={x}
                        cy={y}
                        r="4"
                        fill={getRiskColor(pred.risk_score)}
                      />
                      <text
                        x={x}
                        y="195"
                        fontSize="10"
                        fill="#94a3b8"
                        textAnchor="middle"
                      >
                        {pred.hour}h
                      </text>
                    </g>
                  );
                })}
              </svg>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading LSTM predictions...
            </div>
          )}
        </Card>

        {/* Weekly Pattern */}
        <Card title="📊 Weekly Risk Pattern">
          {weeklyPattern && weeklyPattern.predictions ? (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                  Trend: <span style={{ color: 'white', fontWeight: 'bold' }}>
                    {weeklyPattern.overall_trend}
                  </span>
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {weeklyPattern.predictions.map((day, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <div>
                      <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
                        Day {day.day + 1}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                        {day.date}
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Avg Risk</div>
                        <div style={{
                          fontSize: '1.25rem',
                          fontWeight: 'bold',
                          color: getRiskColor(day.average_risk)
                        }}>
                          {(day.average_risk * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div style={{
                        padding: '0.25rem 0.75rem',
                        borderRadius: '0.25rem',
                        fontSize: '0.75rem',
                        fontWeight: 'bold',
                        background: day.risk_category === 'CRITICAL' ? '#7f1d1d' :
                                   day.risk_category === 'HIGH' ? '#78350f' :
                                   day.risk_category === 'MODERATE' ? '#1e3a8a' : '#14532d',
                        color: day.risk_category === 'CRITICAL' ? '#ef4444' :
                               day.risk_category === 'HIGH' ? '#f59e0b' :
                               day.risk_category === 'MODERATE' ? '#3b82f6' : '#10b981'
                      }}>
                        {day.risk_category}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading weekly pattern...
            </div>
          )}
        </Card>
      </div>

      <div className="grid-2">
        {/* External Data Integration */}
        <Card title="🌐 Real-Time Data Integration">
          {externalData ? (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Integrated Risk Score
                  </div>
                  <div style={{
                    fontSize: '0.65rem',
                    padding: '0.25rem 0.5rem',
                    background: autoRefresh ? '#10b981' : '#64748b',
                    color: 'white',
                    borderRadius: '0.25rem',
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem'
                  }}>
                    {autoRefresh && <span className="pulse">●</span>}
                    {autoRefresh ? 'LIVE' : 'STATIC'}
                  </div>
                </div>
                <div style={{
                  fontSize: '2rem',
                  fontWeight: 'bold',
                  color: getRiskColor(externalData.overall_risk_score || 0)
                }}>
                  {((externalData.overall_risk_score || 0) * 100).toFixed(0)}%
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1rem' }}>
                {externalData.risk_factors && Object.entries(externalData.risk_factors).map(([key, value]) => (
                  <div key={key} style={{
                    padding: '0.75rem',
                    background: '#0f172a',
                    borderRadius: '0.5rem',
                    position: 'relative',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      height: '100%',
                      width: `${value * 100}%`,
                      background: `linear-gradient(90deg, ${getRiskColor(value)}22, transparent)`,
                      transition: 'width 0.5s ease'
                    }} />
                    <div style={{ position: 'relative', zIndex: 1 }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                        {key.replace('_', ' ').toUpperCase()}
                      </div>
                      <div style={{
                        fontSize: '1.25rem',
                        fontWeight: 'bold',
                        color: getRiskColor(value)
                      }}>
                        {(value * 100).toFixed(0)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {externalData.recommendation && (
                <div style={{
                  padding: '0.75rem',
                  background: '#0f172a',
                  borderRadius: '0.5rem',
                  borderLeft: '3px solid #3b82f6'
                }}>
                  <div style={{ fontSize: '0.75rem', color: '#3b82f6', fontWeight: 'bold' }}>
                    Recommendation
                  </div>
                  <div style={{ fontSize: '0.875rem', color: 'white', marginTop: '0.25rem' }}>
                    {externalData.recommendation}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading external data...
            </div>
          )}
        </Card>

        {/* Swarm Coordination */}
        <Card title="🐝 Swarm Intelligence">
          {swarmStatus ? (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1rem' }}>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Total Teams</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                    {swarmStatus.total_teams}
                  </div>
                </div>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Disaster Zones</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                    {swarmStatus.total_zones}
                  </div>
                </div>
              </div>

              {swarmStatus.team_status && (
                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                    Team Status
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.5rem' }}>
                    {Object.entries(swarmStatus.team_status).map(([status, count]) => (
                      <div key={status} style={{
                        padding: '0.5rem',
                        background: '#0f172a',
                        borderRadius: '0.375rem',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#10b981' }}>
                          {count}
                        </div>
                        <div style={{ fontSize: '0.65rem', color: '#64748b', textTransform: 'capitalize' }}>
                          {status}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                marginBottom: '1rem'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                  Swarm Efficiency
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{
                    flex: 1,
                    height: '8px',
                    background: '#0f172a',
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${(swarmStatus.swarm_efficiency || 0) * 100}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, #10b981, #3b82f6)',
                      transition: 'width 0.3s'
                    }} />
                  </div>
                  <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                    {((swarmStatus.swarm_efficiency || 0) * 100).toFixed(0)}%
                  </div>
                </div>
              </div>

              <button
                className="btn btn-primary"
                onClick={initializeSwarm}
                style={{ width: '100%' }}
              >
                Initialize & Optimize Swarm
              </button>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading swarm status...
            </div>
          )}
        </Card>
      </div>

      <style>{`
        .spin {
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        .pulse {
          animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
};

export default AdvancedFeatures;
