import { useState, useEffect } from 'react';
import { Brain, TrendingUp, AlertCircle, BarChart3, Activity, GitBranch, Target, Zap } from 'lucide-react';
import Card from '../components/Card';
import { useWard } from '../context/WardContext';
import { explainabilityAPI } from '../services/api';
import './Pages.css';

const DecisionExplainer = () => {
  const { selectedWard } = useWard();
  const [decisions, setDecisions] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [selectedDecision, setSelectedDecision] = useState(null);
  const [globalImportance, setGlobalImportance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('decisions');
  const [counterfactual, setCounterfactual] = useState(null);
  const [causalGraph, setCausalGraph] = useState(null);
  const [uncertainty, setUncertainty] = useState(null);
  const [comprehensiveReport, setComprehensiveReport] = useState(null);

  useEffect(() => {
    loadDecisions();
    loadGlobalImportance();
    loadCausalGraph();
    const interval = setInterval(() => {
      loadDecisions();
      loadGlobalImportance();
    }, 3000); // Faster refresh for real-time
    return () => clearInterval(interval);
  }, [selectedWard]); // Reload when ward changes

  const loadDecisions = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/api/explainability/decisions/recent?limit=50');
      const data = await response.json();
      
      let filteredDecisions = data.decisions || [];
      
      // Show all decisions if no ward selected, or filter by ward
      if (selectedWard && selectedWard.ward_id) {
        // For now, show all decisions since grid IDs don't directly map to wards
        // In future, backend should include ward_name in decision logging
        console.log(`Ward ${selectedWard.ward_name} selected, showing all decisions (grid-to-ward mapping needed)`);
      }
      
      setDecisions(filteredDecisions);
      setStatistics(data.statistics || {});
      
      // Auto-select most recent decision
      if (filteredDecisions.length > 0 && !selectedDecision) {
        setSelectedDecision(filteredDecisions[0]);
      }
    } catch (error) {
      console.error('Failed to load decisions:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadGlobalImportance = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/explainability/global-importance');
      const data = await response.json();
      if (data.status === 'success') {
        setGlobalImportance(data);
      }
    } catch (error) {
      console.error('Failed to load global importance:', error);
    }
  };

  const loadCausalGraph = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/explainability/causal-graph');
      const data = await response.json();
      if (data.status === 'success') {
        setCausalGraph(data.causal_graph);
      }
    } catch (error) {
      console.error('Failed to load causal graph:', error);
    }
  };

  const generateCounterfactual = async () => {
    if (!selectedDecision || !selectedDecision.features_used) return;
    
    try {
      // Add unique context to prevent caching - include decision ID and timestamp
      const requestBody = {
        ...selectedDecision.features_used,
        _decision_id: selectedDecision.decision_id,
        _timestamp: selectedDecision.timestamp,
        _cache_bust: Date.now() // Force unique request
      };
      
      const response = await fetch('http://localhost:8001/api/explainability/counterfactual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      if (data.status === 'success') {
        setCounterfactual(data.counterfactual);
      }
    } catch (error) {
      console.error('Failed to generate counterfactual:', error);
    }
  };

  const analyzeUncertainty = async () => {
    if (!selectedDecision || !selectedDecision.features_used) return;
    
    try {
      // Add unique context to prevent caching
      const requestBody = {
        ...selectedDecision.features_used,
        _decision_id: selectedDecision.decision_id,
        _timestamp: selectedDecision.timestamp,
        _cache_bust: Date.now()
      };
      
      const response = await fetch('http://localhost:8001/api/explainability/uncertainty-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      if (data.status === 'success') {
        setUncertainty(data.uncertainty_analysis);
      }
    } catch (error) {
      console.error('Failed to analyze uncertainty:', error);
    }
  };

  const generateReport = async () => {
    if (!selectedDecision || !selectedDecision.features_used) return;
    
    try {
      const wardId = selectedDecision.ward_id || selectedDecision.grid_id || 'UNKNOWN';
      
      // Get disaster type from context or decision
      const disasterType = selectedDecision.disaster_type || 'flood';
      
      // Add unique context to prevent caching
      const requestBody = {
        ...selectedDecision.features_used,
        _decision_id: selectedDecision.decision_id,
        _timestamp: selectedDecision.timestamp,
        _cache_bust: Date.now()
      };
      
      const response = await fetch(`http://localhost:8001/api/explainability/comprehensive-report?ward_id=${wardId}&disaster_type=${disasterType}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      if (data.status === 'success') {
        setComprehensiveReport(data);
      }
    } catch (error) {
      console.error('Failed to generate report:', error);
    }
  };

  // Auto-generate analyses when decision changes
  useEffect(() => {
    if (selectedDecision && selectedDecision.features_used) {
      // Clear previous analyses first
      setCounterfactual(null);
      setUncertainty(null);
      setComprehensiveReport(null);
      
      // Then generate new ones
      setTimeout(() => {
        generateCounterfactual();
        analyzeUncertainty();
        generateReport();
      }, 100);
    }
  }, [selectedDecision]);

  const renderFeatureContributions = (decision) => {
    if (!decision.feature_contributions) return null;
    
    const contributions = Object.entries(decision.feature_contributions)
      .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
      .slice(0, 5);
    
    return (
      <div style={{ marginTop: '1rem' }}>
        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
          Top Risk Drivers
        </div>
        {contributions.map(([feature, value]) => (
          <div key={feature} style={{ marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>{feature}</span>
              <span style={{ fontSize: '0.75rem', color: value > 0 ? '#ef4444' : '#10b981' }}>
                {value > 0 ? '+' : ''}{value.toFixed(2)}
              </span>
            </div>
            <div style={{ 
              width: '100%', 
              height: '6px', 
              background: '#1e293b', 
              borderRadius: '3px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${Math.min(Math.abs(value) * 10, 100)}%`,
                height: '100%',
                background: value > 0 ? '#ef4444' : '#10b981',
                transition: 'width 0.3s'
              }} />
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderCounterfactual = () => {
    if (!selectedDecision) {
      return <div className="loading">Select a decision from Level 1-2 tab to see counterfactual analysis</div>;
    }

    if (!counterfactual) {
      return (
        <div className="loading">
          <div style={{ 
            marginBottom: '1rem',
            padding: '0.75rem',
            background: '#1e293b',
            borderRadius: '0.5rem',
            borderLeft: '3px solid #3b82f6'
          }}>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#3b82f6' }}>
              Analyzing Decision
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginTop: '0.25rem' }}>
              Ward: {selectedDecision.ward_id || selectedDecision.grid_id}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
              Risk: {selectedDecision.risk_score?.toFixed(3) || 'N/A'}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
              Time: {new Date(selectedDecision.timestamp).toLocaleTimeString()}
            </div>
          </div>
          ⏳ Generating unique counterfactual analysis...
        </div>
      );
    }

    if (!counterfactual.success) {
      return <div className="loading">No counterfactual found for this scenario</div>;
    }

    return (
      <div>
        <div style={{ 
          fontSize: '0.75rem', 
          color: '#64748b', 
          marginBottom: '0.5rem',
          padding: '0.5rem',
          background: '#0f172a',
          borderRadius: '0.375rem',
          borderLeft: '3px solid #10b981'
        }}>
          <div style={{ fontWeight: 'bold', color: '#10b981', marginBottom: '0.25rem' }}>
            ✓ Analysis Complete
          </div>
          <div>Ward: {selectedDecision.ward_id || selectedDecision.grid_id}</div>
          <div>Original Risk: {selectedDecision.risk_score?.toFixed(3) || 'N/A'}</div>
          <div>Decision ID: {selectedDecision.decision_id?.substring(0, 8)}...</div>
        </div>
        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
          Level 3: Counterfactual Analysis
        </div>
        <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>Original Risk</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ef4444' }}>
            {counterfactual.original_output.risk_score.toFixed(2)}
          </div>
        </div>
        <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>Counterfactual Risk</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#10b981' }}>
            {counterfactual.counterfactual_output.risk_score.toFixed(2)}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#10b981', marginTop: '0.25rem' }}>
            ↓ {(counterfactual.risk_reduction * 100).toFixed(1)}% reduction
          </div>
        </div>
        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
          Required Changes:
        </div>
        {counterfactual.recommendations && counterfactual.recommendations.map((rec, idx) => (
          <div key={idx} style={{ 
            padding: '0.5rem', 
            background: '#0f172a', 
            borderRadius: '0.375rem',
            marginBottom: '0.5rem',
            fontSize: '0.75rem',
            color: '#cbd5e1'
          }}>
            • {rec}
          </div>
        ))}
        <div style={{ 
          marginTop: '1rem',
          padding: '0.75rem',
          background: '#1e293b',
          borderRadius: '0.5rem',
          fontSize: '0.75rem',
          color: '#94a3b8'
        }}>
          <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>Feature Changes:</div>
          {Object.entries(counterfactual.changes).map(([feature, change]) => (
            <div key={feature} style={{ marginBottom: '0.25rem' }}>
              {feature}: {change.original.toFixed(2)} → {change.modified.toFixed(2)} 
              ({change.change_factor < 1 ? '↓' : '↑'} {Math.abs((1 - change.change_factor) * 100).toFixed(0)}%)
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderCausalGraph = () => {
    if (!causalGraph) return <div className="loading">Loading causal graph...</div>;

    return (
      <div>
        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
          Level 4: Causal Relationships
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.5rem' }}>
            {causalGraph.nodes.length} Nodes, {causalGraph.edges.length} Causal Links
          </div>
        </div>
        {causalGraph.edges.map((edge, idx) => (
          <div key={idx} style={{ 
            padding: '0.75rem', 
            background: '#1e293b', 
            borderRadius: '0.5rem',
            marginBottom: '0.5rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#3b82f6', fontWeight: 'bold' }}>
                {edge.source}
              </span>
              <span style={{ color: '#64748b' }}>→</span>
              <span style={{ fontSize: '0.75rem', color: '#8b5cf6', fontWeight: 'bold' }}>
                {edge.target}
              </span>
              <span style={{ 
                marginLeft: 'auto',
                fontSize: '0.625rem',
                padding: '0.125rem 0.375rem',
                background: edge.strength > 0 ? '#10b981' : '#ef4444',
                borderRadius: '0.25rem'
              }}>
                {Math.abs(edge.strength * 100).toFixed(0)}%
              </span>
            </div>
            <div style={{ fontSize: '0.625rem', color: '#94a3b8', marginTop: '0.25rem' }}>
              {edge.explanation}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderUncertainty = () => {
    if (!selectedDecision) {
      return <div className="loading">Select a decision to see uncertainty analysis</div>;
    }

    if (!uncertainty) {
      return (
        <div className="loading">
          <div style={{ 
            marginBottom: '1rem',
            padding: '0.75rem',
            background: '#1e293b',
            borderRadius: '0.5rem',
            borderLeft: '3px solid #8b5cf6'
          }}>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#8b5cf6' }}>
              Running Monte Carlo Simulation
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginTop: '0.25rem' }}>
              Ward: {selectedDecision.ward_id || selectedDecision.grid_id}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
              Decision: {selectedDecision.decision_id?.substring(0, 8)}...
            </div>
          </div>
          ⏳ Running 100 iterations...
        </div>
      );
    }

    return (
      <div>
        <div style={{ 
          fontSize: '0.75rem', 
          color: '#64748b', 
          marginBottom: '0.5rem',
          padding: '0.5rem',
          background: '#0f172a',
          borderRadius: '0.375rem',
          borderLeft: '3px solid #10b981'
        }}>
          <div style={{ fontWeight: 'bold', color: '#10b981', marginBottom: '0.25rem' }}>
            ✓ Simulation Complete
          </div>
          <div>Ward: {selectedDecision.ward_id || selectedDecision.grid_id}</div>
          <div>Decision ID: {selectedDecision.decision_id?.substring(0, 8)}...</div>
        </div>
        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
          Level 6: Uncertainty Analysis
        </div>
        <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '1rem' }}>
          Based on {uncertainty.num_simulations} Monte Carlo simulations
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginBottom: '1rem' }}>
          <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.625rem', color: '#94a3b8' }}>Mean Prediction</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#3b82f6' }}>
              {uncertainty.mean_prediction.toFixed(3)}
            </div>
          </div>
          <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.625rem', color: '#94a3b8' }}>Confidence</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#10b981' }}>
              {(uncertainty.confidence_score * 100).toFixed(0)}%
            </div>
          </div>
        </div>
        <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', marginBottom: '0.5rem' }}>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
            95% Confidence Interval
          </div>
          <div style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>
            [{uncertainty.confidence_interval_95.lower.toFixed(3)}, {uncertainty.confidence_interval_95.upper.toFixed(3)}]
          </div>
        </div>
        <div style={{ padding: '0.75rem', background: '#0f172a', borderRadius: '0.5rem' }}>
          <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
            {uncertainty.interpretation}
          </div>
        </div>
      </div>
    );
  };

  const renderComprehensiveReport = () => {
    if (!selectedDecision) {
      return <div className="loading">Select a decision to generate comprehensive report</div>;
    }

    if (!comprehensiveReport) {
      return (
        <div className="loading">
          <div style={{ 
            marginBottom: '1rem',
            padding: '0.75rem',
            background: '#1e293b',
            borderRadius: '0.5rem',
            borderLeft: '3px solid #f59e0b'
          }}>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#f59e0b' }}>
              Generating Natural Language Report
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginTop: '0.25rem' }}>
              Ward: {selectedDecision.ward_id || selectedDecision.grid_id}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
              Decision: {selectedDecision.decision_id?.substring(0, 8)}...
            </div>
          </div>
          ⏳ Generating natural language explanation...
        </div>
      );
    }

    return (
      <div>
        <div style={{ 
          fontSize: '0.75rem', 
          color: '#64748b', 
          marginBottom: '0.5rem',
          padding: '0.5rem',
          background: '#0f172a',
          borderRadius: '0.375rem',
          borderLeft: '3px solid #10b981'
        }}>
          <div style={{ fontWeight: 'bold', color: '#10b981', marginBottom: '0.25rem' }}>
            ✓ Report Generated
          </div>
          <div>Ward: {selectedDecision.ward_id || selectedDecision.grid_id}</div>
          <div>Decision ID: {selectedDecision.decision_id?.substring(0, 8)}...</div>
        </div>
        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
          Level 7: Natural Language Explanation
        </div>
        <div style={{ 
          padding: '1rem', 
          background: '#1e293b', 
          borderRadius: '0.5rem',
          fontSize: '0.75rem',
          color: '#cbd5e1',
          lineHeight: '1.5',
          whiteSpace: 'pre-wrap',
          fontFamily: 'monospace',
          maxHeight: '400px',
          overflowY: 'auto'
        }}>
          {comprehensiveReport.report}
        </div>
      </div>
    );
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🧠 Advanced Explainable AI (7 Levels)</h1>
          <p>Complete XAI system: Descriptive → Local/Global → Counterfactual → Causal → Path → Uncertainty → NL</p>
          {selectedWard && (
            <div style={{ 
              marginTop: '0.5rem',
              padding: '0.5rem 1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              display: 'inline-block',
              fontSize: '0.875rem',
              color: '#94a3b8'
            }}>
              📍 Showing decisions from all grids (Ward: <strong style={{ color: '#3b82f6' }}>{selectedWard.ward_name}</strong>)
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
                Grid IDs don't directly map to wards yet - showing all evacuation decisions
              </div>
            </div>
          )}
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
            <div style={{ fontSize: '0.625rem', color: '#64748b', marginTop: '0.25rem' }}>
              🔴 Live • Updating every 3s
            </div>
          </div>
        )}
      </div>

      <div className="stats-grid">
        <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
          <div className="stat-icon" style={{ color: '#3b82f6' }}>
            <Brain size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">{selectedWard ? 'Ward Decisions' : 'Total Decisions'}</div>
            <div className="stat-value">{decisions.length}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
          <div className="stat-icon" style={{ color: '#10b981' }}>
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Avg Confidence</div>
            <div className="stat-value">{((statistics.avg_confidence || 0) * 100).toFixed(0)}%</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
          <div className="stat-icon" style={{ color: '#f59e0b' }}>
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Evacuations</div>
            <div className="stat-value">{statistics.by_type?.evacuation_path || 0}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#8b5cf6' }}>
          <div className="stat-icon" style={{ color: '#8b5cf6' }}>
            <BarChart3 size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Risk Assessments</div>
            <div className="stat-value">{decisions.filter(d => d.decision_type === 'risk_assessment').length}</div>
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', borderBottom: '1px solid #334155', paddingBottom: '0.5rem' }}>
        {[
          { id: 'decisions', label: 'Level 1-2', icon: Brain },
          { id: 'counterfactual', label: 'Level 3', icon: Target },
          { id: 'causal', label: 'Level 4+7', icon: GitBranch },
          { id: 'uncertainty', label: 'Level 6', icon: Zap }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '0.5rem 1rem',
              background: activeTab === tab.id ? '#3b82f6' : '#1e293b',
              color: 'white',
              border: 'none',
              borderRadius: '0.375rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '0.875rem'
            }}
          >
            <tab.icon size={16} />
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'decisions' && (
        <div className="grid-2">
          <Card title={selectedWard ? `Decisions from Evacuation System (Level 1)` : "Recent Decisions (Level 1)"}>
            {loading ? (
              <div className="loading">Loading decisions...</div>
            ) : decisions.length > 0 ? (
              <div className="activity-list" style={{ maxHeight: '500px', overflowY: 'auto' }}>
                {decisions.map((decision, idx) => (
                  <div key={idx} className="activity-item" style={{ 
                    cursor: 'pointer',
                    background: selectedDecision?.decision_id === decision.decision_id ? '#1e293b' : 'transparent',
                    padding: '0.75rem',
                    borderRadius: '0.5rem',
                    marginBottom: '0.5rem'
                  }}
                       onClick={() => setSelectedDecision(decision)}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                          {decision.decision_type?.replace('_', ' ').toUpperCase()}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                          {decision.ward_id || decision.grid_id || decision.agent_id}
                        </div>
                      </div>
                      {decision.confidence && (
                        <div style={{ 
                          padding: '0.25rem 0.5rem',
                          background: decision.confidence > 0.7 ? '#10b981' : '#f59e0b',
                          borderRadius: '0.25rem',
                          fontSize: '0.75rem',
                          fontWeight: 'bold'
                        }}>
                          {(decision.confidence * 100).toFixed(0)}%
                        </div>
                      )}
                    </div>
                    <div style={{ fontSize: '0.625rem', color: '#64748b', marginTop: '0.25rem' }}>
                      {new Date(decision.timestamp).toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="loading">
                {selectedWard 
                  ? `No decisions yet. Go to Urban Evacuation page and start simulation to generate decisions.`
                  : 'Go to Urban Evacuation and start simulation to see decisions'}
              </div>
            )}
          </Card>

          <Card title="Feature Analysis (Level 1+2)">
            {selectedDecision ? (
              <div>
                <div className="status-list">
                  <div className="status-item">
                    <span className="status-label">Ward</span>
                    <span>{selectedDecision.ward_id || 'N/A'}</span>
                  </div>
                  {selectedDecision.risk_score !== undefined && (
                    <div className="status-item">
                      <span className="status-label">Risk Score</span>
                      <span style={{ 
                        color: selectedDecision.risk_score > 0.7 ? '#ef4444' : 
                               selectedDecision.risk_score > 0.4 ? '#f59e0b' : '#10b981',
                        fontWeight: 'bold'
                      }}>
                        {selectedDecision.risk_score.toFixed(3)}
                      </span>
                    </div>
                  )}
                </div>
                
                {renderFeatureContributions(selectedDecision)}
              </div>
            ) : (
              <div className="loading">Select a decision to view analysis</div>
            )}
          </Card>
        </div>
      )}

      {activeTab === 'counterfactual' && (
        <div className="grid-2">
          <Card title="Selected Decision">
            {selectedDecision ? (
              <div>
                <div style={{ fontSize: '0.875rem', marginBottom: '1rem' }}>
                  <div style={{ color: '#94a3b8' }}>Ward: {selectedDecision.ward_id || 'N/A'}</div>
                  <div style={{ color: '#94a3b8' }}>Risk: {selectedDecision.risk_score?.toFixed(2) || 'N/A'}</div>
                </div>
                {renderFeatureContributions(selectedDecision)}
              </div>
            ) : (
              <div className="loading">Select a decision from Level 1-2 tab first</div>
            )}
          </Card>

          <Card title="What-If Analysis (Level 3)">
            {renderCounterfactual()}
          </Card>
        </div>
      )}

      {activeTab === 'causal' && (
        <div className="grid-2">
          <Card title="Causal Graph (Level 4)">
            {renderCausalGraph()}
          </Card>

          <Card title="Natural Language Report (Level 7)">
            {renderComprehensiveReport()}
          </Card>
        </div>
      )}

      {activeTab === 'uncertainty' && (
        <div className="grid-2">
          <Card title="Monte Carlo Uncertainty (Level 6)">
            {renderUncertainty()}
          </Card>

          <Card title="Global Feature Importance (Level 2)">
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#94a3b8' }}>
                Aggregated Across All Decisions
              </div>
              {globalImportance && globalImportance.feature_importance ? (
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '1rem' }}>
                    Based on {globalImportance.total_explanations || 0} risk assessments
                  </div>
                  {Object.entries(globalImportance.feature_importance).slice(0, 5).map(([feature, importance]) => {
                    const maxValue = Math.max(...Object.values(globalImportance.feature_importance));
                    return (
                      <div key={feature} style={{ marginBottom: '0.75rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                          <span style={{ fontSize: '0.875rem', color: '#e2e8f0', textTransform: 'capitalize' }}>
                            {feature.replace('_', ' ')}
                          </span>
                          <span style={{ fontSize: '0.875rem', color: '#3b82f6', fontWeight: 'bold' }}>
                            {importance.toFixed(1)}%
                          </span>
                        </div>
                        <div style={{ 
                          width: '100%', 
                          height: '8px', 
                          background: '#1e293b', 
                          borderRadius: '4px',
                          overflow: 'hidden'
                        }}>
                          <div style={{
                            width: `${(importance / maxValue) * 100}%`,
                            height: '100%',
                            background: 'linear-gradient(90deg, #3b82f6, #8b5cf6)',
                            transition: 'width 0.5s'
                          }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="loading">No global data yet. Start simulation to generate.</div>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default DecisionExplainer;
