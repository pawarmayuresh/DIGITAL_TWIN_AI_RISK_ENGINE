import { useState, useEffect, useRef } from 'react';
import { Activity, Zap, AlertTriangle, TrendingUp, Play, Pause, RotateCcw, Network, Brain } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import './Pages.css';

const InfrastructureDashboard = () => {
  const { selectedWard } = useWard();
  const [networkState, setNetworkState] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [cascadeAnalysis, setCascadeAnalysis] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [collapseRisk, setCollapseRisk] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [timestep, setTimestep] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    loadNetworkState();
    loadCascadeAnalysis();
    
    // Listen for evacuation simulation events
    const handleEvacuationSimulation = (event) => {
      console.log('Evacuation simulation detected in Infrastructure Dashboard:', event.detail);
      // Trigger infrastructure update with evacuation data
      if (event.detail.ward) {
        updateNetworkWithEvacuationData(event.detail);
      }
    };
    
    window.addEventListener('evacuationSimulated', handleEvacuationSimulation);
    
    return () => {
      window.removeEventListener('evacuationSimulated', handleEvacuationSimulation);
    };
  }, [selectedWard]);

  useEffect(() => {
    if (isSimulating) {
      intervalRef.current = setInterval(() => {
        updateNetwork();
      }, 2000); // Update every 2 seconds
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
  }, [isSimulating]);

  const loadNetworkState = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/infrastructure/network/status');
      const data = await response.json();
      setNetworkState(data);
      setNodes(data.nodes || []);
      setTimestep(data.timestep || 0);
      
      // Auto-select first node
      if (data.nodes && data.nodes.length > 0 && !selectedNode) {
        setSelectedNode(data.nodes[0]);
      }
    } catch (error) {
      console.error('Failed to load network state:', error);
    }
  };

  const loadCascadeAnalysis = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/infrastructure/cascade/analysis');
      const data = await response.json();
      setCascadeAnalysis(data);
    } catch (error) {
      console.error('Failed to load cascade analysis:', error);
    }
  };

  const loadPredictions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/infrastructure/prediction/network?steps=5');
      const data = await response.json();
      setPredictions(data);
    } catch (error) {
      console.error('Failed to load predictions:', error);
    }
  };

  const loadCollapseRisk = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/infrastructure/prediction/collapse-risk');
      const data = await response.json();
      setCollapseRisk(data);
    } catch (error) {
      console.error('Failed to load collapse risk:', error);
    }
  };

  const updateNetwork = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/infrastructure/network/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      
      if (data.success) {
        setNetworkState(data.network_state);
        setNodes(data.network_state.nodes || []);
        setTimestep(data.timestep);
        
        // Update cascade analysis
        if (data.cascade && data.cascade.cascade_detected) {
          setCascadeAnalysis(prev => ({
            ...prev,
            cascade_history: [...(prev?.cascade_history || []), data.cascade]
          }));
        }
        
        // Reload predictions
        loadPredictions();
        loadCollapseRisk();
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
      const response = await fetch('http://localhost:8000/api/infrastructure/network/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(evidence)
      });
      const data = await response.json();
      
      if (data.success) {
        setNetworkState(data.network_state);
        setNodes(data.network_state.nodes || []);
        setTimestep(data.timestep);
        
        // Update cascade analysis
        if (data.cascade && data.cascade.cascade_detected) {
          setCascadeAnalysis(prev => ({
            ...prev,
            cascade_history: [...(prev?.cascade_history || []), data.cascade]
          }));
        }
        
        // Reload predictions
        loadPredictions();
        loadCollapseRisk();
      }
    } catch (error) {
      console.error('Failed to update network with evacuation data:', error);
    }
  };

  const startSimulation = () => {
    setIsSimulating(true);
    loadPredictions();
    loadCollapseRisk();
  };

  const stopSimulation = () => {
    setIsSimulating(false);
  };

  const resetNetwork = async () => {
    try {
      await fetch('http://localhost:8000/api/infrastructure/network/reset', {
        method: 'POST'
      });
      setIsSimulating(false);
      setTimestep(0);
      await loadNetworkState();
      await loadCascadeAnalysis();
      setPredictions(null);
      setCollapseRisk(null);
    } catch (error) {
      console.error('Failed to reset network:', error);
    }
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

  if (!networkState) {
    return <div className="page"><div style={{ padding: '2rem', textAlign: 'center' }}>Loading infrastructure network...</div></div>;
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🏗️ Probabilistic Infrastructure Network</h1>
          <p>Bayesian network with cascading failures and temporal prediction</p>
        </div>
        {selectedWard && (
          <div style={{ 
            padding: '0.75rem 1rem', 
            background: '#1e293b', 
            borderRadius: '0.5rem',
            borderLeft: '3px solid #3b82f6'
          }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Analyzing Ward</div>
            <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white' }}>
              {selectedWard.ward_name || selectedWard.ward_id}
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      <Card title="Simulation Controls">
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <button
            className="btn btn-primary"
            onClick={startSimulation}
            disabled={isSimulating}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Play size={16} />
            Start Real-Time Simulation
          </button>
          <button
            className="btn btn-secondary"
            onClick={stopSimulation}
            disabled={!isSimulating}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Pause size={16} />
            Pause
          </button>
          <button
            className="btn btn-secondary"
            onClick={resetNetwork}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <RotateCcw size={16} />
            Reset
          </button>
          
          {isSimulating && (
            <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                Timestep: <span style={{ color: 'white', fontWeight: 'bold' }}>{timestep}</span>
              </div>
              <div style={{ 
                width: '12px', 
                height: '12px', 
                borderRadius: '50%', 
                background: '#10b981',
                animation: 'pulse 2s infinite'
              }} />
            </div>
          )}
        </div>
      </Card>

      {/* Statistics */}
      <div className="stats-grid">
        <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
          <div className="stat-icon" style={{ color: '#3b82f6' }}>
            <Network size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Total Nodes</div>
            <div className="stat-value">{networkState.total_nodes}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
          <div className="stat-icon" style={{ color: '#10b981' }}>
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Avg Health</div>
            <div className="stat-value">{networkState.average_health?.toFixed(0)}%</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#ef4444' }}>
          <div className="stat-icon" style={{ color: '#ef4444' }}>
            <AlertTriangle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">At Risk</div>
            <div className="stat-value">{networkState.critical_nodes?.length || 0}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#8b5cf6' }}>
          <div className="stat-icon" style={{ color: '#8b5cf6' }}>
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Dependencies</div>
            <div className="stat-value">{networkState.total_dependencies}</div>
          </div>
        </div>
      </div>

      {/* Collapse Risk Warning */}
      {collapseRisk && collapseRisk.collapse_risk_detected && (
        <div style={{
          padding: '1rem',
          background: 'linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)',
          borderRadius: '0.5rem',
          borderLeft: '4px solid #ef4444',
          marginBottom: '1rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <AlertTriangle size={32} color="#ef4444" />
            <div>
              <div style={{ fontSize: '1.125rem', fontWeight: 'bold', color: 'white', marginBottom: '0.25rem' }}>
                🚨 NETWORK COLLAPSE RISK DETECTED
              </div>
              <div style={{ fontSize: '0.875rem', color: '#fca5a5' }}>
                Predicted collapse in {collapseRisk.steps_until_collapse} timesteps • 
                Peak risk: {collapseRisk.peak_predicted_risk?.toFixed(1)}%
              </div>
              {collapseRisk.recommendations && collapseRisk.recommendations.length > 0 && (
                <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: '#fecaca' }}>
                  {collapseRisk.recommendations[0]}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <div className="grid-2">
        {/* Infrastructure Network Visualization */}
        <Card title="Infrastructure Network">
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
            gap: '1rem',
            padding: '1rem'
          }}>
            {nodes.map((node) => (
              <div
                key={node.node_id}
                onClick={() => setSelectedNode(node)}
                style={{
                  padding: '1rem',
                  background: selectedNode?.node_id === node.node_id ? '#1e293b' : '#0f172a',
                  borderRadius: '0.5rem',
                  border: `2px solid ${getNodeColor(node)}`,
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                  position: 'relative',
                  overflow: 'hidden'
                }}
              >
                {/* Pulse animation for critical nodes */}
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
                  <div style={{ fontSize: '2rem', textAlign: 'center', marginBottom: '0.5rem' }}>
                    {getNodeIcon(node.type)}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', textAlign: 'center', marginBottom: '0.5rem' }}>
                    {node.node_id}
                  </div>
                  <div style={{ fontSize: '0.875rem', fontWeight: 'bold', textAlign: 'center', color: getNodeColor(node) }}>
                    {node.health_score?.toFixed(0)}%
                  </div>
                  
                  {/* Probability bars */}
                  <div style={{ marginTop: '0.5rem', fontSize: '0.625rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.125rem' }}>
                      <span style={{ color: '#10b981' }}>H</span>
                      <span style={{ color: '#10b981' }}>{(node.probabilities.healthy * 100).toFixed(0)}%</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.125rem' }}>
                      <span style={{ color: '#f59e0b' }}>D</span>
                      <span style={{ color: '#f59e0b' }}>{(node.probabilities.degraded * 100).toFixed(0)}%</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#ef4444' }}>F</span>
                      <span style={{ color: '#ef4444' }}>{(node.probabilities.failed * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Node Details */}
        <Card title={selectedNode ? `Node: ${selectedNode.node_id}` : "Select a Node"}>
          {selectedNode ? (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '0.5rem' }}>
                  {getNodeIcon(selectedNode.type)}
                </div>
                <div style={{ textAlign: 'center', fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                  {selectedNode.type} • {selectedNode.ward}
                </div>
                <div style={{ textAlign: 'center', fontSize: '2rem', fontWeight: 'bold', color: getNodeColor(selectedNode) }}>
                  {selectedNode.health_score?.toFixed(1)}%
                </div>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                  Probability Distribution
                </div>
                <div style={{ marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem', fontSize: '0.75rem' }}>
                    <span style={{ color: '#10b981' }}>Healthy</span>
                    <span style={{ color: '#10b981', fontWeight: 'bold' }}>
                      {(selectedNode.probabilities.healthy * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: '#1e293b', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${selectedNode.probabilities.healthy * 100}%`,
                      height: '100%',
                      background: '#10b981',
                      transition: 'width 0.5s'
                    }} />
                  </div>
                </div>
                <div style={{ marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem', fontSize: '0.75rem' }}>
                    <span style={{ color: '#f59e0b' }}>Degraded</span>
                    <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>
                      {(selectedNode.probabilities.degraded * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: '#1e293b', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${selectedNode.probabilities.degraded * 100}%`,
                      height: '100%',
                      background: '#f59e0b',
                      transition: 'width 0.5s'
                    }} />
                  </div>
                </div>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem', fontSize: '0.75rem' }}>
                    <span style={{ color: '#ef4444' }}>Failed</span>
                    <span style={{ color: '#ef4444', fontWeight: 'bold' }}>
                      {(selectedNode.probabilities.failed * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: '#1e293b', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${selectedNode.probabilities.failed * 100}%`,
                      height: '100%',
                      background: '#ef4444',
                      transition: 'width 0.5s'
                    }} />
                  </div>
                </div>
              </div>

              <div style={{ 
                padding: '0.75rem',
                background: '#0f172a',
                borderRadius: '0.5rem',
                fontSize: '0.75rem',
                color: '#94a3b8'
              }}>
                <div style={{ marginBottom: '0.5rem' }}>
                  <strong style={{ color: 'white' }}>Most Likely State:</strong> {selectedNode.most_likely_state}
                </div>
                <div style={{ marginBottom: '0.5rem' }}>
                  <strong style={{ color: 'white' }}>Risk Score:</strong> {selectedNode.risk_score?.toFixed(1)}%
                </div>
                <div>
                  <strong style={{ color: 'white' }}>Dependencies:</strong> {selectedNode.num_dependencies}
                </div>
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              Click on a node to view details
            </div>
          )}
        </Card>
      </div>

      {/* Predictions */}
      {predictions && (
        <Card title="🔮 Future Predictions (5 Steps Ahead)">
          <div style={{ marginBottom: '1rem' }}>
            {predictions.warnings && predictions.warnings.length > 0 && (
              <div style={{ marginBottom: '1rem' }}>
                {predictions.warnings.map((warning, idx) => (
                  <div key={idx} style={{
                    padding: '0.5rem',
                    background: '#78350f',
                    borderLeft: '3px solid #f59e0b',
                    borderRadius: '0.25rem',
                    marginBottom: '0.5rem',
                    fontSize: '0.75rem',
                    color: '#fbbf24'
                  }}>
                    {warning}
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.5rem' }}>
            {predictions.aggregate_predictions?.map((pred, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                borderTop: `3px solid ${pred.avg_risk > 60 ? '#ef4444' : pred.avg_risk > 40 ? '#f59e0b' : '#10b981'}`
              }}>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                  T+{pred.step_ahead}
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: pred.avg_risk > 60 ? '#ef4444' : pred.avg_risk > 40 ? '#f59e0b' : '#10b981' }}>
                  {pred.avg_health?.toFixed(0)}%
                </div>
                <div style={{ fontSize: '0.625rem', color: '#64748b' }}>
                  Risk: {pred.avg_risk?.toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Cascade Analysis */}
      {cascadeAnalysis && cascadeAnalysis.vulnerability_analysis && (
        <Card title="⚡ Cascading Failure Analysis">
          <div className="grid-2">
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Network Resilience
              </div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3b82f6', marginBottom: '1rem' }}>
                {(cascadeAnalysis.vulnerability_analysis.network_resilience * 100).toFixed(0)}%
              </div>
              
              <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Most Vulnerable Nodes
              </div>
              {cascadeAnalysis.vulnerability_analysis.most_vulnerable?.slice(0, 5).map(([nodeId, data], idx) => (
                <div key={idx} style={{
                  padding: '0.5rem',
                  background: '#1e293b',
                  borderRadius: '0.25rem',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid ${data.risk_level === 'HIGH' ? '#ef4444' : data.risk_level === 'MEDIUM' ? '#f59e0b' : '#10b981'}`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                    <span style={{ color: 'white' }}>{nodeId}</span>
                    <span style={{ 
                      color: data.risk_level === 'HIGH' ? '#ef4444' : data.risk_level === 'MEDIUM' ? '#f59e0b' : '#10b981',
                      fontWeight: 'bold'
                    }}>
                      {data.risk_level}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.625rem', color: '#64748b', marginTop: '0.25rem' }}>
                    Vulnerability: {(data.score * 100).toFixed(0)}% • 
                    Failure: {(data.failure_prob * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
            
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#94a3b8', marginBottom: '0.5rem' }}>
                Recent Cascade Events
              </div>
              {cascadeAnalysis.cascade_history?.slice(-5).reverse().map((cascade, idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid ${cascade.severity === 'CRITICAL' ? '#ef4444' : cascade.severity === 'HIGH' ? '#f59e0b' : '#3b82f6'}`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                      {cascade.cascade_detected ? '⚡ Cascade Detected' : '✓ No Cascade'}
                    </span>
                    <span style={{ 
                      fontSize: '0.75rem',
                      padding: '0.125rem 0.5rem',
                      borderRadius: '0.25rem',
                      background: cascade.severity === 'CRITICAL' ? '#7f1d1d' : cascade.severity === 'HIGH' ? '#78350f' : '#1e293b',
                      color: cascade.severity === 'CRITICAL' ? '#ef4444' : cascade.severity === 'HIGH' ? '#f59e0b' : '#3b82f6'
                    }}>
                      {cascade.severity}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.625rem', color: '#64748b' }}>
                    {cascade.num_events} events • {cascade.affected_nodes?.length || 0} nodes affected
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
};

export default InfrastructureDashboard;
