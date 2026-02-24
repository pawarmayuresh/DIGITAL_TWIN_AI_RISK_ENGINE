import { useState, useEffect } from 'react';
import { Zap, Network, Activity, AlertTriangle, Play, Pause } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import './Pages.css';

const KnowledgeEngine = () => {
  const { selectedWard, disasterType } = useWard();
  const [realtimeAnalysis, setRealtimeAnalysis] = useState(null);
  const [wardAnalysis, setWardAnalysis] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    loadRealtimeAnalysis();
  }, [disasterType]); // Reload when disaster type changes

  useEffect(() => {
    if (selectedWard) {
      loadWardAnalysis(selectedWard.ward_id);
    }
  }, [selectedWard]);

  useEffect(() => {
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        loadRealtimeAnalysis();
        if (selectedWard) {
          loadWardAnalysis(selectedWard.ward_id);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [autoRefresh, selectedWard]);

  const loadRealtimeAnalysis = async () => {
    try {
      const disaster = disasterType || 'flood';
      const response = await fetch(`http://localhost:8001/api/knowledge/realtime/quick?disaster_type=${disaster}`);
      const data = await response.json();
      setRealtimeAnalysis(data);
    } catch (error) {
      console.error('Error loading analysis:', error);
    }
  };

  const loadWardAnalysis = async (wardId) => {
    try {
      const disaster = disasterType || 'flood';
      const response = await fetch(`http://localhost:8001/api/knowledge/realtime/ward-quick/${encodeURIComponent(wardId)}?disaster_type=${disaster}`);
      const data = await response.json();
      setWardAnalysis(data);
    } catch (error) {
      console.error('Error loading ward analysis:', error);
    }
  };

  const getStatusColor = (value, threshold) => {
    if (value > threshold) return '#ef4444';
    if (value > threshold * 0.7) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🧠 Knowledge Representation Engine</h1>
          <p>Real-time AI reasoning with SymPy, Experta, and Logic Programming</p>
          {realtimeAnalysis?.disaster_type && (
            <div style={{ 
              marginTop: '0.5rem',
              padding: '0.5rem 1rem',
              background: realtimeAnalysis.disaster_type === 'fire' ? '#7f1d1d' :
                         realtimeAnalysis.disaster_type === 'contamination' ? '#581c87' : '#1e3a8a',
              borderRadius: '0.5rem',
              display: 'inline-block',
              fontSize: '0.875rem',
              fontWeight: 'bold',
              color: 'white'
            }}>
              {realtimeAnalysis.disaster_type === 'fire' ? '🔥 FIRE' :
               realtimeAnalysis.disaster_type === 'contamination' ? '☢️ CONTAMINATION' : '🌊 FLOOD'} Analysis Mode
            </div>
          )}
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            className={autoRefresh ? "btn btn-secondary" : "btn btn-primary"}
            onClick={() => setAutoRefresh(!autoRefresh)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            {autoRefresh ? <Pause size={16} /> : <Play size={16} />}
            {autoRefresh ? 'Pause' : 'Start'} Auto-Refresh
          </button>
          {selectedWard && (
            <div style={{ 
              padding: '0.75rem 1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '3px solid #3b82f6'
            }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Analyzing Ward</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                {selectedWard.ward_name}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Real-time Data Sources */}
      {realtimeAnalysis && (
        <div className="stats-grid">
          <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
            <div className="stat-icon" style={{ color: '#3b82f6' }}>
              <Activity size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Rainfall Sensors</div>
              <div className="stat-value">{realtimeAnalysis.data_sources?.rainfall_sensors || 0}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
            <div className="stat-icon" style={{ color: '#10b981' }}>
              <Network size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Water Sensors</div>
              <div className="stat-value">{realtimeAnalysis.data_sources?.water_sensors || 0}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
            <div className="stat-icon" style={{ color: '#f59e0b' }}>
              <Zap size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Infrastructure Nodes</div>
              <div className="stat-value">{realtimeAnalysis.data_sources?.infrastructure_nodes || 0}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#ef4444' }}>
            <div className="stat-icon" style={{ color: '#ef4444' }}>
              <AlertTriangle size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Failed Infrastructure</div>
              <div className="stat-value">{realtimeAnalysis.metrics?.failed_infrastructure || 0}</div>
            </div>
          </div>
        </div>
      )}

      <div className="grid-2">
        {/* Expert System - Production Rules */}
        <Card title="🤖 Expert System - Production Rules (Experta)">
          {realtimeAnalysis?.expert_system ? (
            <div>
              <div style={{ 
                padding: '1rem', 
                background: realtimeAnalysis.expert_system.risk_level === 'CRITICAL' ? '#7f1d1d' :
                           realtimeAnalysis.expert_system.risk_level === 'EXTREME' ? '#991b1b' :
                           realtimeAnalysis.expert_system.risk_level === 'HIGH' ? '#92400e' : '#14532d',
                borderRadius: '0.5rem',
                borderLeft: `4px solid ${
                  realtimeAnalysis.expert_system.risk_level === 'CRITICAL' ? '#ef4444' :
                  realtimeAnalysis.expert_system.risk_level === 'EXTREME' ? '#dc2626' :
                  realtimeAnalysis.expert_system.risk_level === 'HIGH' ? '#f59e0b' : '#10b981'
                }`,
                marginBottom: '1rem'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginBottom: '0.25rem' }}>
                  Risk Assessment
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                  {realtimeAnalysis.expert_system.risk_level}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginTop: '0.25rem' }}>
                  {realtimeAnalysis.expert_system.total_rules_fired} rules fired
                </div>
              </div>
              
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Rules Fired (Forward Chaining)
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1rem', maxHeight: '200px', overflowY: 'auto' }}>
                {realtimeAnalysis.expert_system.rules.map((rule, idx) => (
                  <div key={idx} style={{
                    padding: '0.5rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    borderLeft: '3px solid #f59e0b',
                    fontSize: '0.75rem',
                    color: '#f59e0b',
                    fontFamily: 'monospace'
                  }}>
                    {rule}
                  </div>
                ))}
              </div>
              
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Automated Decisions
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '200px', overflowY: 'auto' }}>
                {realtimeAnalysis.expert_system.decisions.map((decision, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    fontSize: '0.875rem',
                    color: 'white'
                  }}>
                    {decision}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading expert system...
            </div>
          )}
        </Card>

        {/* Symbolic Logic - Consistency Checking */}
        <Card title="🔬 Symbolic Logic - Consistency (SymPy)">
          {realtimeAnalysis?.symbolic_logic ? (
            <div>
              <div style={{ 
                padding: '1rem', 
                background: realtimeAnalysis.symbolic_logic.consistent ? '#14532d' : '#7f1d1d',
                borderRadius: '0.5rem',
                borderLeft: `4px solid ${realtimeAnalysis.symbolic_logic.consistent ? '#10b981' : '#ef4444'}`,
                marginBottom: '1rem'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginBottom: '0.25rem' }}>
                  Logical Consistency
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                  {realtimeAnalysis.symbolic_logic.consistent ? '✓ CONSISTENT' : '✗ INCONSISTENT'}
                </div>
              </div>
              
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Proposition Truth Values
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {Object.entries(realtimeAnalysis.symbolic_logic.propositions).map(([prop, value]) => (
                  <div key={prop} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <span style={{ fontSize: '0.875rem', color: '#94a3b8', fontFamily: 'monospace' }}>
                      {prop}
                    </span>
                    <span style={{ 
                      fontSize: '0.875rem', 
                      fontWeight: 'bold',
                      color: value ? '#10b981' : '#64748b'
                    }}>
                      {value ? 'TRUE' : 'FALSE'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading symbolic logic...
            </div>
          )}
        </Card>
      </div>

      <div className="grid-2">
        {/* Real-time Sensor Metrics */}
        <Card title="⚡ Real-time Sensor Metrics">
          {realtimeAnalysis?.metrics ? (
            <div>
              {realtimeAnalysis.disaster_type === 'fire' ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Temperature</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.temperature_celsius, 40)
                    }}>
                      {realtimeAnalysis.metrics.temperature_celsius}°C
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Wind Speed</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.wind_speed_kmh, 35)
                    }}>
                      {realtimeAnalysis.metrics.wind_speed_kmh} km/h
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Humidity</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: realtimeAnalysis.metrics.humidity_percent < 30 ? '#ef4444' : '#10b981'
                    }}>
                      {realtimeAnalysis.metrics.humidity_percent}%
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Failed Infrastructure</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.failed_infrastructure, 3)
                    }}>
                      {realtimeAnalysis.metrics.failed_infrastructure}
                    </div>
                  </div>
                </div>
              ) : realtimeAnalysis.disaster_type === 'contamination' ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Air Quality Index</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.air_quality_index, 200)
                    }}>
                      {realtimeAnalysis.metrics.air_quality_index}
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Water Contamination</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.water_contamination_level, 0.5)
                    }}>
                      {(realtimeAnalysis.metrics.water_contamination_level * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Chemical Level</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.chemical_level, 0.5)
                    }}>
                      {(realtimeAnalysis.metrics.chemical_level * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Failed Infrastructure</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.failed_infrastructure, 3)
                    }}>
                      {realtimeAnalysis.metrics.failed_infrastructure}
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Avg Rainfall</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.avg_rainfall_mm, 50)
                    }}>
                      {realtimeAnalysis.metrics.avg_rainfall_mm} mm
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Avg Water Level</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.avg_water_level_m, 2.0)
                    }}>
                      {realtimeAnalysis.metrics.avg_water_level_m} m
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Avg Traffic</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.avg_traffic_density, 0.7)
                    }}>
                      {(realtimeAnalysis.metrics.avg_traffic_density * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Failed Infrastructure</div>
                    <div style={{ 
                      fontSize: '1.5rem', 
                      fontWeight: 'bold',
                      color: getStatusColor(realtimeAnalysis.metrics.failed_infrastructure, 3)
                    }}>
                      {realtimeAnalysis.metrics.failed_infrastructure}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading metrics...
            </div>
          )}
        </Card>

        {/* Logic Programming - Ward Dependencies */}
        <Card title="🌐 Logic Programming - FOL Queries">
          {wardAnalysis?.logic_programming ? (
            <div>
              <div style={{ 
                padding: '1rem', 
                background: wardAnalysis.logic_programming.risk_detected ? '#7f1d1d' : '#14532d',
                borderRadius: '0.5rem',
                borderLeft: `4px solid ${wardAnalysis.logic_programming.risk_detected ? '#ef4444' : '#10b981'}`,
                marginBottom: '1rem'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginBottom: '0.25rem' }}>
                  FOL Query Result
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'white' }}>
                  {wardAnalysis.logic_programming.risk_detected ? 
                    (wardAnalysis.disaster_type === 'fire' ? '🔥 Fire Risk Detected' :
                     wardAnalysis.disaster_type === 'contamination' ? '☢️ Contamination Risk Detected' :
                     '⚠️ Flood Risk Detected') :
                    (wardAnalysis.disaster_type === 'fire' ? '✓ No Fire Risk' :
                     wardAnalysis.disaster_type === 'contamination' ? '✓ No Contamination Risk' :
                     '✓ No Flood Risk')}
                </div>
              </div>
              
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Asserted Facts
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {Object.entries(wardAnalysis.logic_programming.facts).map(([predicate, args]) => (
                  args.length > 0 && (
                    <div key={predicate} style={{
                      padding: '0.5rem',
                      background: '#1e293b',
                      borderRadius: '0.5rem',
                      borderLeft: '3px solid #3b82f6',
                      fontSize: '0.75rem',
                      color: '#3b82f6',
                      fontFamily: 'monospace'
                    }}>
                      {predicate}({args.map(a => JSON.stringify(a)).join(', ')})
                    </div>
                  )
                ))}
                {Object.values(wardAnalysis.logic_programming.facts).every(v => v.length === 0) && (
                  <div style={{ 
                    padding: '1rem', 
                    textAlign: 'center', 
                    color: '#64748b',
                    fontSize: '0.875rem'
                  }}>
                    No facts asserted - conditions below thresholds
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              {selectedWard ? 'Loading logic programming...' : 'Select a ward to see FOL analysis'}
            </div>
          )}
        </Card>
      </div>

      {/* Ward-Specific Expert System Analysis */}
      {wardAnalysis?.expert_system && (
        <Card title={`🎯 Ward Expert System Analysis - ${wardAnalysis.ward_id}`}>
          <div className="grid-2">
            <div>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Real-time Sensor Data
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {wardAnalysis.disaster_type === 'fire' ? (
                  <>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Temperature</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.temperature, 40)
                      }}>
                        {wardAnalysis.sensor_data.temperature}°C
                      </div>
                    </div>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Wind Speed</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.wind_speed, 35)
                      }}>
                        {wardAnalysis.sensor_data.wind_speed} km/h
                      </div>
                    </div>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Humidity</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: wardAnalysis.sensor_data.humidity < 30 ? '#ef4444' : '#10b981'
                      }}>
                        {wardAnalysis.sensor_data.humidity}%
                      </div>
                    </div>
                  </>
                ) : wardAnalysis.disaster_type === 'contamination' ? (
                  <>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Air Quality Index</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.air_quality_index, 200)
                      }}>
                        {wardAnalysis.sensor_data.air_quality_index}
                      </div>
                    </div>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Water Contamination</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.water_contamination, 0.5)
                      }}>
                        {(wardAnalysis.sensor_data.water_contamination * 100).toFixed(0)}%
                      </div>
                    </div>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Chemical Level</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.chemical_level, 0.5)
                      }}>
                        {(wardAnalysis.sensor_data.chemical_level * 100).toFixed(0)}%
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Rainfall</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.rainfall_mm, 50)
                      }}>
                        {wardAnalysis.sensor_data.rainfall_mm} mm
                      </div>
                    </div>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Water Level</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.water_level_m, 2.0)
                      }}>
                        {wardAnalysis.sensor_data.water_level_m} m
                      </div>
                    </div>
                    <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Traffic Density</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getStatusColor(wardAnalysis.sensor_data.traffic_density, 0.7)
                      }}>
                        {(wardAnalysis.sensor_data.traffic_density * 100).toFixed(0)}%
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
            
            <div>
              <div style={{ 
                padding: '1rem', 
                background: wardAnalysis.expert_system.risk_level === 'CRITICAL' ? '#7f1d1d' :
                           wardAnalysis.expert_system.risk_level === 'EXTREME' ? '#991b1b' :
                           wardAnalysis.expert_system.risk_level === 'HIGH' ? '#92400e' : '#14532d',
                borderRadius: '0.5rem',
                borderLeft: `4px solid ${
                  wardAnalysis.expert_system.risk_level === 'CRITICAL' ? '#ef4444' :
                  wardAnalysis.expert_system.risk_level === 'EXTREME' ? '#dc2626' :
                  wardAnalysis.expert_system.risk_level === 'HIGH' ? '#f59e0b' : '#10b981'
                }`,
                marginBottom: '1rem'
              }}>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white', marginBottom: '0.5rem' }}>
                  {wardAnalysis.expert_system.risk_level}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
                  {wardAnalysis.expert_system.rules_fired.length} rules fired
                </div>
              </div>
              
              <h4 style={{ fontSize: '0.75rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Decisions
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '200px', overflowY: 'auto' }}>
                {wardAnalysis.expert_system.decisions.map((decision, idx) => (
                  <div key={idx} style={{
                    padding: '0.5rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    fontSize: '0.75rem',
                    color: 'white'
                  }}>
                    {decision}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

export default KnowledgeEngine;
