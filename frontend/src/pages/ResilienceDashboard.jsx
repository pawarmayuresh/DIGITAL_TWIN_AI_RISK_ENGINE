import { useState, useEffect, useRef } from 'react';
import { Shield, TrendingUp, Network, AlertTriangle, Activity, RefreshCw, Play, Pause } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import './Pages.css';

const ResilienceDashboard = () => {
  const { selectedWard } = useWard();
  const [networkState, setNetworkState] = useState(null);
  const [filteredNodes, setFilteredNodes] = useState([]);
  const [vulnerabilityAnalysis, setVulnerabilityAnalysis] = useState(null);
  const [cascadeEvents, setCascadeEvents] = useState([]);
  const [resilienceMetrics, setResilienceMetrics] = useState({
    overall: 0,
    robustness: 0,
    infrastructure: 0,
    recovery: 0
  });
  const [autoUpdate, setAutoUpdate] = useState(true);  // Changed to true by default
  const [loading, setLoading] = useState(true);
  const [timestep, setTimestep] = useState(0);
  const intervalRef = useRef(null);
  const [lastUpdate, setLastUpdate] = useState(Date.now());

  useEffect(() => {
    loadAllData();
    
    // Start auto-update immediately
    if (autoUpdate) {
      intervalRef.current = setInterval(() => {
        loadResilienceMetrics();
      }, 2000);  // Update every 2 seconds
    }
    
    // Listen for ward selection events
    const handleWardSelected = (event) => {
      console.log('Ward selected in Resilience Dashboard:', event.detail.ward);
      loadAllData();
    };
    
    // Listen for evacuation simulation events
    const handleEvacuationSimulation = (event) => {
      console.log('Evacuation simulation detected, updating infrastructure:', event.detail);
      // Trigger infrastructure update with evacuation data
      if (event.detail.ward) {
        updateNetworkWithEvacuationData(event.detail);
      }
    };
    
    window.addEventListener('wardSelected', handleWardSelected);
    window.addEventListener('evacuationSimulated', handleEvacuationSimulation);
    
    return () => {
      window.removeEventListener('wardSelected', handleWardSelected);
      window.removeEventListener('evacuationSimulated', handleEvacuationSimulation);
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [selectedWard]);

  useEffect(() => {
    if (autoUpdate) {
      intervalRef.current = setInterval(() => {
        loadResilienceMetrics();
      }, 2000);  // Update every 2 seconds
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [autoUpdate, selectedWard]);

  const loadResilienceMetrics = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/analytics/resilience-index');
      const data = await response.json();
      
      setResilienceMetrics({
        overall: data.overall_resilience || 0,
        robustness: data.robustness || 0,
        infrastructure: data.redundancy || 0,
        recovery: data.resourcefulness || 0
      });
      
      setTimestep(data.timestep || 0);
      setLastUpdate(Date.now());
    } catch (error) {
      console.error('Failed to load resilience metrics:', error);
    }
  };

  const loadAllData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        loadNetworkState(),
        loadVulnerabilityAnalysis(),
        loadCascadeEvents()
      ]);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadNetworkState = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/infrastructure/network/status');
      const data = await response.json();
      setNetworkState(data);
      setTimestep(data.timestep || 0);
      
      // Filter nodes by ward if selected
      let nodes = data.nodes || [];
      if (selectedWard) {
        const wardId = selectedWard.ward_id || selectedWard.ward_name;
        nodes = nodes.filter(node => {
          // Match exact ward_id or check if node.ward contains the ward_id
          return node.ward === wardId || 
                 node.ward === selectedWard.ward_name ||
                 node.ward?.includes(wardId);
        });
        console.log(`Filtered ${nodes.length} nodes for ward ${wardId}`, nodes);
      }
      setFilteredNodes(nodes);
      
      // Calculate resilience metrics - use all nodes if no ward selected
      const metricsNodes = nodes.length > 0 ? nodes : (data.nodes || []);
      if (metricsNodes.length > 0) {
        const avgHealth = metricsNodes.reduce((sum, n) => sum + n.health_score, 0) / metricsNodes.length;
        const avgRisk = metricsNodes.reduce((sum, n) => sum + n.risk_score, 0) / metricsNodes.length;
        const healthyCount = metricsNodes.filter(n => n.most_likely_state === 'Healthy').length;
        const robustness = (healthyCount / metricsNodes.length) * 100;
        
        setResilienceMetrics({
          overall: avgHealth,
          robustness: robustness,
          infrastructure: avgHealth,
          recovery: Math.max(0, 100 - avgRisk)
        });
      } else if (data.average_health !== undefined) {
        // Use network-wide metrics if no nodes available
        setResilienceMetrics({
          overall: data.average_health,
          robustness: data.average_health,
          infrastructure: data.average_health,
          recovery: Math.max(0, 100 - data.average_risk)
        });
      }
    } catch (error) {
      console.error('Failed to load network state:', error);
    }
  };

  const loadVulnerabilityAnalysis = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/infrastructure/cascade/analysis');
      const data = await response.json();
      setVulnerabilityAnalysis(data.vulnerability_analysis);
    } catch (error) {
      console.error('Failed to load vulnerability analysis:', error);
    }
  };

  const loadCascadeEvents = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/infrastructure/cascade/analysis');
      const data = await response.json();
      setCascadeEvents(data.cascade_history || []);
    } catch (error) {
      console.error('Failed to load cascade events:', error);
    }
  };

  const updateNetworkWithEvidence = async () => {
    try {
      // Call the update endpoint which applies new evidence and triggers cascades
      const response = await fetch('http://localhost:8001/api/infrastructure/network/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      
      if (data.success) {
        // Update network state
        setNetworkState(data.network_state);
        setTimestep(data.timestep || 0);
        
        // Filter nodes by ward if selected
        let nodes = data.network_state.nodes || [];
        if (selectedWard) {
          const wardId = selectedWard.ward_id || selectedWard.ward_name;
          nodes = nodes.filter(node => {
            return node.ward === wardId || 
                   node.ward === selectedWard.ward_name ||
                   node.ward?.includes(wardId);
          });
        }
        setFilteredNodes(nodes);
        
        // Update resilience metrics - use all nodes if no ward selected
        const metricsNodes = nodes.length > 0 ? nodes : (data.network_state.nodes || []);
        if (metricsNodes.length > 0) {
          const avgHealth = metricsNodes.reduce((sum, n) => sum + n.health_score, 0) / metricsNodes.length;
          const avgRisk = metricsNodes.reduce((sum, n) => sum + n.risk_score, 0) / metricsNodes.length;
          const healthyCount = metricsNodes.filter(n => n.most_likely_state === 'Healthy').length;
          const robustness = (healthyCount / metricsNodes.length) * 100;
          
          setResilienceMetrics({
            overall: avgHealth,
            robustness: robustness,
            infrastructure: avgHealth,
            recovery: Math.max(0, 100 - avgRisk)
          });
        } else if (data.network_state.average_health !== undefined) {
          setResilienceMetrics({
            overall: data.network_state.average_health,
            robustness: data.network_state.average_health,
            infrastructure: data.network_state.average_health,
            recovery: Math.max(0, 100 - data.network_state.average_risk)
          });
        }
        
        // Update cascade events if cascade detected
        if (data.cascade && data.cascade.cascade_detected) {
          setCascadeEvents(prev => [...prev, data.cascade]);
        }
        
        // Reload vulnerability analysis
        await loadVulnerabilityAnalysis();
      }
    } catch (error) {
      console.error('Failed to update network:', error);
    }
  };

  const updateNetworkWithEvacuationData = async (evacuationData) => {
    try {
      // Convert evacuation simulation data to infrastructure evidence
      const evidence = {
        RainIntensity: evacuationData.rainfall || 0.5,
        FloodLevel: evacuationData.waterLevel || 0.3,
        CyberAttack: 0,
        PowerStress: evacuationData.riskLevel > 0.7 ? 0.8 : 0.3,
        WaterStress: evacuationData.waterLevel || 0.4
      };
      
      console.log('Applying evacuation evidence to infrastructure:', evidence);
      
      // Call the update endpoint with evacuation-derived evidence
      const response = await fetch('http://localhost:8001/api/infrastructure/network/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(evidence)
      });
      const data = await response.json();
      
      if (data.success) {
        // Update network state
        setNetworkState(data.network_state);
        setTimestep(data.timestep || 0);
        
        // Filter nodes by ward if selected
        let nodes = data.network_state.nodes || [];
        if (selectedWard) {
          const wardId = selectedWard.ward_id || selectedWard.ward_name;
          nodes = nodes.filter(node => {
            return node.ward === wardId || 
                   node.ward === selectedWard.ward_name ||
                   node.ward?.includes(wardId);
          });
        }
        setFilteredNodes(nodes);
        
        // Update resilience metrics
        const metricsNodes = nodes.length > 0 ? nodes : (data.network_state.nodes || []);
        if (metricsNodes.length > 0) {
          const avgHealth = metricsNodes.reduce((sum, n) => sum + n.health_score, 0) / metricsNodes.length;
          const avgRisk = metricsNodes.reduce((sum, n) => sum + n.risk_score, 0) / metricsNodes.length;
          const healthyCount = metricsNodes.filter(n => n.most_likely_state === 'Healthy').length;
          const robustness = (healthyCount / metricsNodes.length) * 100;
          
          setResilienceMetrics({
            overall: avgHealth,
            robustness: robustness,
            infrastructure: avgHealth,
            recovery: Math.max(0, 100 - avgRisk)
          });
        }
        
        // Update cascade events if cascade detected
        if (data.cascade && data.cascade.cascade_detected) {
          setCascadeEvents(prev => [...prev, data.cascade]);
        }
        
        // Reload vulnerability analysis
        await loadVulnerabilityAnalysis();
      }
    } catch (error) {
      console.error('Failed to update network with evacuation data:', error);
    }
  };

  const toggleAutoUpdate = () => {
    if (!autoUpdate) {
      // Starting auto-update, trigger first update immediately
      updateNetworkWithEvidence();
    }
    setAutoUpdate(!autoUpdate);
  };

  const getNodeColor = (node) => {
    const health = node.health_score;
    if (health > 80) return '#10b981';
    if (health > 60) return '#3b82f6';
    if (health > 40) return '#f59e0b';
    return '#ef4444';
  };

  const getNodeIcon = (type) => {
    switch (type) {
      case 'Utility': return '⚡';
      case 'Healthcare': return '🏥';
      case 'IT': return '💻';
      case 'Emergency': return '🚨';
      default: return '🏢';
    }
  };

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-icon" style={{ color }}>
        <Icon size={24} />
      </div>
      <div className="stat-content">
        <div className="stat-label">{label}</div>
        <div className="stat-value">{value.toFixed(0)}/100</div>
      </div>
    </div>
  );

  if (loading && !networkState) {
    return (
      <div className="page">
        <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
          Loading resilience data...
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🛡️ Resilience Dashboard</h1>
          <p>Real-time infrastructure resilience and vulnerability analysis</p>
        </div>
        {selectedWard && (
          <div style={{ 
            padding: '0.75rem 1rem', 
            background: '#1e293b', 
            borderRadius: '0.5rem',
            borderLeft: '3px solid #10b981'
          }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Analyzing Ward</div>
            <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white' }}>
              {selectedWard.ward_name || selectedWard.ward_id}
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <button
          className={autoUpdate ? "btn btn-secondary" : "btn btn-primary"}
          onClick={toggleAutoUpdate}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          {autoUpdate ? <Pause size={16} /> : <Play size={16} />}
          {autoUpdate ? 'Pause Auto-Update' : 'Start Auto-Update'}
        </button>
        <button
          className="btn btn-secondary"
          onClick={updateNetworkWithEvidence}
          disabled={loading}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <RefreshCw size={16} />
          Update Network
        </button>
        {autoUpdate && (
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.5rem',
            fontSize: '0.875rem',
            color: '#94a3b8'
          }}>
            <div style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              background: '#10b981',
              animation: 'pulse 2s infinite'
            }} />
            Live Updates • Timestep: <span style={{ color: 'white', fontWeight: 'bold' }}>{timestep}</span>
          </div>
        )}
      </div>

      <div className="stats-grid">
        <StatCard
          icon={Shield}
          label="Overall Resilience"
          value={resilienceMetrics.overall}
          color="#10b981"
        />
        <StatCard
          icon={TrendingUp}
          label="Robustness"
          value={resilienceMetrics.robustness}
          color="#3b82f6"
        />
        <StatCard
          icon={Network}
          label="Infrastructure Health"
          value={resilienceMetrics.infrastructure}
          color="#8b5cf6"
        />
        <StatCard
          icon={Activity}
          label="Recovery Capacity"
          value={resilienceMetrics.recovery}
          color="#f59e0b"
        />
      </div>

      {/* Real-time Update Indicator */}
      {autoUpdate && (
        <div style={{
          padding: '0.75rem 1rem',
          background: 'linear-gradient(135deg, #065f46 0%, #047857 100%)',
          borderRadius: '0.5rem',
          borderLeft: '4px solid #10b981',
          marginBottom: '1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <Activity size={20} color="#10b981" style={{ animation: 'pulse 2s infinite' }} />
          <div>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
              Real-Time Simulation Active
            </div>
            <div style={{ fontSize: '0.75rem', color: '#6ee7b7' }}>
              Network updating every 3 seconds with new evidence • Timestep: {timestep}
            </div>
          </div>
        </div>
      )}

      <div className="grid-2">
        {/* Infrastructure Network Graph */}
        <Card title={selectedWard ? `Infrastructure Network - ${selectedWard.ward_name}` : "Infrastructure Network - All Wards"}>
          {(selectedWard && filteredNodes.length === 0) ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              No infrastructure nodes in this ward
            </div>
          ) : (
            <div>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))',
                gap: '0.75rem',
                marginBottom: '1rem',
                maxHeight: '400px',
                overflowY: 'auto'
              }}>
                {(selectedWard ? filteredNodes : (networkState?.nodes || [])).map((node) => (
                  <div
                    key={node.node_id}
                    style={{
                      padding: '0.75rem',
                      background: '#1e293b',
                      borderRadius: '0.5rem',
                      border: `2px solid ${getNodeColor(node)}`,
                      position: 'relative',
                      overflow: 'hidden'
                    }}
                  >
                    {node.risk_score > 50 && (
                      <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: `${getNodeColor(node)}22`,
                        animation: 'pulse 2s infinite'
                      }} />
                    )}
                    
                    <div style={{ position: 'relative', zIndex: 1 }}>
                      <div style={{ fontSize: '1.5rem', textAlign: 'center', marginBottom: '0.25rem' }}>
                        {getNodeIcon(node.type)}
                      </div>
                      <div style={{ fontSize: '0.625rem', color: '#94a3b8', textAlign: 'center', marginBottom: '0.25rem' }}>
                        {node.node_id}
                      </div>
                      <div style={{ fontSize: '0.875rem', fontWeight: 'bold', textAlign: 'center', color: getNodeColor(node) }}>
                        {node.health_score?.toFixed(0)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div style={{ 
                padding: '0.75rem',
                background: '#0f172a',
                borderRadius: '0.5rem',
                fontSize: '0.75rem',
                color: '#94a3b8'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span>Total Nodes:</span>
                  <span style={{ color: 'white', fontWeight: 'bold' }}>
                    {selectedWard ? filteredNodes.length : (networkState?.nodes?.length || 0)}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span>Avg Health:</span>
                  <span style={{ color: '#10b981', fontWeight: 'bold' }}>
                    {(() => {
                      const nodes = selectedWard ? filteredNodes : (networkState?.nodes || []);
                      return nodes.length > 0 
                        ? (nodes.reduce((sum, n) => sum + n.health_score, 0) / nodes.length).toFixed(0)
                        : '0';
                    })()}%
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>At Risk:</span>
                  <span style={{ color: '#ef4444', fontWeight: 'bold' }}>
                    {(() => {
                      const nodes = selectedWard ? filteredNodes : (networkState?.nodes || []);
                      return nodes.filter(n => n.risk_score > 50).length;
                    })()}
                  </span>
                </div>
              </div>
            </div>
          )}
        </Card>

        {/* Vulnerability Analysis */}
        <Card title="⚠️ Vulnerability Analysis">
          {vulnerabilityAnalysis ? (
            <div>
              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                  Network Resilience Score
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
                  <div style={{ 
                    fontSize: '2.5rem', 
                    fontWeight: 'bold',
                    color: vulnerabilityAnalysis.network_resilience > 0.7 ? '#10b981' : 
                           vulnerabilityAnalysis.network_resilience > 0.5 ? '#f59e0b' : '#ef4444'
                  }}>
                    {(vulnerabilityAnalysis.network_resilience * 100).toFixed(0)}%
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
                    {vulnerabilityAnalysis.network_resilience > 0.7 ? 'Strong' : 
                     vulnerabilityAnalysis.network_resilience > 0.5 ? 'Moderate' : 'Weak'}
                  </div>
                </div>
              </div>

              <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Most Vulnerable Nodes
              </div>
              {vulnerabilityAnalysis.most_vulnerable?.slice(0, 5).map(([nodeId, data], idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid ${
                    data.risk_level === 'HIGH' ? '#ef4444' : 
                    data.risk_level === 'MEDIUM' ? '#f59e0b' : '#10b981'
                  }`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ color: 'white', fontWeight: 'bold', fontSize: '0.875rem' }}>
                      {nodeId}
                    </span>
                    <span style={{ 
                      padding: '0.125rem 0.5rem',
                      borderRadius: '0.25rem',
                      fontSize: '0.625rem',
                      fontWeight: 'bold',
                      background: data.risk_level === 'HIGH' ? '#7f1d1d' : 
                                 data.risk_level === 'MEDIUM' ? '#78350f' : '#14532d',
                      color: data.risk_level === 'HIGH' ? '#ef4444' : 
                             data.risk_level === 'MEDIUM' ? '#f59e0b' : '#10b981'
                    }}>
                      {data.risk_level}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                    Vulnerability: {(data.score * 100).toFixed(0)}% • 
                    Failure Risk: {(data.failure_prob * 100).toFixed(0)}%
                  </div>
                  {data.dependent_nodes > 0 && (
                    <div style={{ fontSize: '0.625rem', color: '#94a3b8', marginTop: '0.25rem' }}>
                      {data.dependent_nodes} dependent nodes at risk
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Loading vulnerability analysis...
            </div>
          )}
        </Card>
      </div>

      {/* Resilience Graph */}
      <Card title="📊 Resilience Trends">
        <div>
          <svg width="100%" height="300" viewBox="0 0 800 300">
            {/* Grid lines */}
            {[0, 1, 2, 3, 4].map(i => (
              <line
                key={`grid-${i}`}
                x1="50"
                y1={50 + i * 50}
                x2="750"
                y2={50 + i * 50}
                stroke="#1e293b"
                strokeWidth="1"
              />
            ))}
            
            {/* Y-axis labels */}
            {[100, 75, 50, 25, 0].map((val, i) => (
              <text
                key={`label-${i}`}
                x="30"
                y={55 + i * 50}
                fontSize="12"
                fill="#64748b"
              >
                {val}
              </text>
            ))}

            {/* Resilience bars */}
            {Object.entries(resilienceMetrics).map(([key, value], idx) => {
              const x = 100 + idx * 150;
              const height = (value / 100) * 200;
              const y = 250 - height;
              const colors = {
                overall: '#10b981',
                robustness: '#3b82f6',
                infrastructure: '#8b5cf6',
                recovery: '#f59e0b'
              };
              
              return (
                <g key={key}>
                  <rect
                    x={x}
                    y={y}
                    width="80"
                    height={height}
                    fill={colors[key]}
                    opacity="0.8"
                    rx="4"
                  />
                  <text
                    x={x + 40}
                    y={y - 10}
                    fontSize="14"
                    fill="white"
                    textAnchor="middle"
                    fontWeight="bold"
                  >
                    {value.toFixed(0)}%
                  </text>
                  <text
                    x={x + 40}
                    y={270}
                    fontSize="11"
                    fill="#94a3b8"
                    textAnchor="middle"
                  >
                    {key.charAt(0).toUpperCase() + key.slice(1)}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>
      </Card>

      {/* Cascade Events */}
      <Card title="⚡ Recent Cascade Events">
        {cascadeEvents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
            No cascade events detected
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '0.75rem' }}>
            {cascadeEvents.slice(-10).reverse().map((event, idx) => (
              <div key={idx} style={{
                padding: '1rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                borderLeft: `4px solid ${
                  event.severity === 'CRITICAL' ? '#ef4444' : 
                  event.severity === 'HIGH' ? '#f59e0b' : 
                  event.severity === 'MEDIUM' ? '#3b82f6' : '#10b981'
                }`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <AlertTriangle size={16} color={
                      event.severity === 'CRITICAL' ? '#ef4444' : 
                      event.severity === 'HIGH' ? '#f59e0b' : '#3b82f6'
                    } />
                    <span style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
                      {event.cascade_detected ? 'Cascade Detected' : 'No Cascade'}
                    </span>
                  </div>
                  <span style={{ 
                    padding: '0.125rem 0.5rem',
                    borderRadius: '0.25rem',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                    background: event.severity === 'CRITICAL' ? '#7f1d1d' : 
                               event.severity === 'HIGH' ? '#78350f' : 
                               event.severity === 'MEDIUM' ? '#1e3a8a' : '#14532d',
                    color: event.severity === 'CRITICAL' ? '#ef4444' : 
                           event.severity === 'HIGH' ? '#f59e0b' : 
                           event.severity === 'MEDIUM' ? '#3b82f6' : '#10b981'
                  }}>
                    {event.severity}
                  </span>
                </div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                  {event.num_events} failure events • {event.affected_nodes?.length || 0} nodes affected
                </div>
                {event.affected_nodes && event.affected_nodes.length > 0 && (
                  <div style={{ 
                    marginTop: '0.5rem', 
                    fontSize: '0.625rem', 
                    color: '#64748b',
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '0.25rem'
                  }}>
                    {event.affected_nodes.slice(0, 5).map((node, i) => (
                      <span key={i} style={{
                        padding: '0.125rem 0.375rem',
                        background: '#0f172a',
                        borderRadius: '0.25rem'
                      }}>
                        {node}
                      </span>
                    ))}
                    {event.affected_nodes.length > 5 && (
                      <span style={{ color: '#64748b' }}>
                        +{event.affected_nodes.length - 5} more
                      </span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </Card>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
};

export default ResilienceDashboard;
