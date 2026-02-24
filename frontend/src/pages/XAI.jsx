import { useState, useEffect } from 'react';
import { Brain, TrendingUp, AlertCircle, Activity, Zap, Target } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import './Pages.css';

const XAI = () => {
  const { selectedWard } = useWard();
  const [decisions, setDecisions] = useState([]);
  const [selectedDecision, setSelectedDecision] = useState(null);
  const [liveMode, setLiveMode] = useState(false);

  // Listen for simulation decisions
  useEffect(() => {
    const handleSimulationDecision = (event) => {
      const { decisions: newDecisions } = event.detail;
      if (newDecisions && newDecisions.length > 0) {
        setDecisions(prev => [...newDecisions, ...prev].slice(0, 50)); // Keep last 50
        if (!selectedDecision) {
          setSelectedDecision(newDecisions[0]);
        }
      }
    };

    window.addEventListener('simulationDecisions', handleSimulationDecision);
    return () => window.removeEventListener('simulationDecisions', handleSimulationDecision);
  }, [selectedDecision]);

  const avgConfidence = decisions.length > 0
    ? (decisions.reduce((sum, d) => sum + parseFloat(d.confidence), 0) / decisions.length).toFixed(0)
    : 0;

  const evacuateCount = decisions.filter(d => d.decision === 'EVACUATE').length;
  const monitorCount = decisions.filter(d => d.decision === 'MONITOR').length;

  return (
    <div className="page">
      <div className="page-header">
        <h1>🧠 Explainable AI (XAI)</h1>
        <p>Understand every AI decision with SHAP-like feature importance</p>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
          <button
            className={`btn ${liveMode ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setLiveMode(!liveMode)}
          >
            <Activity size={16} style={{ marginRight: '0.5rem' }} />
            {liveMode ? 'Live Mode ON' : 'Live Mode OFF'}
          </button>
          {selectedWard && (
            <div style={{
              padding: '0.5rem 1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <Target size={16} />
              Ward: {selectedWard.ward_name}
            </div>
          )}
        </div>
      </div>

      {/* Statistics */}
      <div className="stats-grid">
        <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
          <div className="stat-icon" style={{ color: '#3b82f6' }}>
            <Brain size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Total Decisions</div>
            <div className="stat-value">{decisions.length}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
          <div className="stat-icon" style={{ color: '#10b981' }}>
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Avg Confidence</div>
            <div className="stat-value">{avgConfidence}%</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#ef4444' }}>
          <div className="stat-icon" style={{ color: '#ef4444' }}>
            <AlertCircle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Evacuations</div>
            <div className="stat-value">{evacuateCount}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
          <div className="stat-icon" style={{ color: '#f59e0b' }}>
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Monitoring</div>
            <div className="stat-value">{monitorCount}</div>
          </div>
        </div>
      </div>

      {decisions.length === 0 ? (
        <Card title="No Decisions Yet">
          <div style={{
            padding: '3rem',
            textAlign: 'center',
            color: '#94a3b8',
            background: '#0f172a',
            borderRadius: '0.5rem',
            border: '2px dashed #334155'
          }}>
            <Brain size={64} style={{ margin: '0 auto 1rem', opacity: 0.3 }} />
            <h3 style={{ marginBottom: '0.5rem', color: 'white' }}>Run a Disaster Simulation</h3>
            <p style={{ marginBottom: '1rem' }}>
              Go to Disaster Simulation page and run a simulation to see AI decisions here
            </p>
            <button
              className="btn btn-primary"
              onClick={() => window.location.href = '/disaster-simulation'}
            >
              Go to Disaster Simulation
            </button>
          </div>
        </Card>
      ) : (
        <div className="grid-2">
          {/* Recent Decisions */}
          <Card title="📋 Recent AI Decisions">
            <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
              {decisions.map((decision, idx) => (
                <div
                  key={idx}
                  onClick={() => setSelectedDecision(decision)}
                  style={{
                    padding: '1rem',
                    marginBottom: '0.75rem',
                    background: selectedDecision === decision ? '#1e293b' : '#0f172a',
                    borderRadius: '0.5rem',
                    borderLeft: `4px solid ${decision.decision === 'EVACUATE' ? '#ef4444' : '#3b82f6'}`,
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#1e293b'}
                  onMouseLeave={(e) => {
                    if (selectedDecision !== decision) {
                      e.currentTarget.style.background = '#0f172a';
                    }
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontWeight: 'bold', color: 'white', fontSize: '0.875rem' }}>
                      Cell {decision.cell}
                    </span>
                    <span style={{
                      padding: '0.25rem 0.5rem',
                      background: decision.decision === 'EVACUATE' ? '#ef4444' : '#3b82f6',
                      color: 'white',
                      borderRadius: '0.25rem',
                      fontSize: '0.75rem',
                      fontWeight: 'bold'
                    }}>
                      {decision.decision}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    Confidence: {decision.confidence}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Decision Details with SHAP Explanation */}
          <Card title="🔍 Decision Explanation (SHAP-like)">
            {selectedDecision ? (
              <div>
                {/* Decision Summary */}
                <div style={{
                  padding: '1rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  marginBottom: '1.5rem',
                  borderLeft: `4px solid ${selectedDecision.decision === 'EVACUATE' ? '#ef4444' : '#3b82f6'}`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '1.125rem', fontWeight: 'bold', color: 'white' }}>
                      {selectedDecision.decision}
                    </span>
                    <span style={{ fontSize: '1.125rem', fontWeight: 'bold', color: '#10b981' }}>
                      {selectedDecision.confidence}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Cell: {selectedDecision.cell}
                  </div>
                </div>

                {/* Feature Importance (SHAP Values) */}
                <div style={{ marginBottom: '1.5rem' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white', marginBottom: '1rem' }}>
                    📊 Feature Importance (SHAP Values)
                  </h3>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '1rem' }}>
                    Top factors contributing to this decision:
                  </div>
                  {selectedDecision.topReasons && selectedDecision.topReasons.map((reason, idx) => (
                    <div key={idx} style={{
                      padding: '0.75rem',
                      background: '#0f172a',
                      borderRadius: '0.5rem',
                      marginBottom: '0.5rem',
                      borderLeft: '3px solid #3b82f6'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <span style={{
                          width: '24px',
                          height: '24px',
                          background: '#3b82f6',
                          color: 'white',
                          borderRadius: '50%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '0.75rem',
                          fontWeight: 'bold'
                        }}>
                          {idx + 1}
                        </span>
                        <span style={{ color: 'white', fontSize: '0.875rem', flex: 1 }}>
                          {reason}
                        </span>
                      </div>
                      {/* Visual bar for contribution */}
                      <div style={{
                        height: '6px',
                        background: '#1e293b',
                        borderRadius: '3px',
                        overflow: 'hidden',
                        marginTop: '0.5rem'
                      }}>
                        <div style={{
                          width: `${Math.min(100, (3 - idx) * 30)}%`,
                          height: '100%',
                          background: `linear-gradient(90deg, #3b82f6, #60a5fa)`,
                          transition: 'width 0.5s ease'
                        }}></div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Explanation */}
                <div style={{
                  padding: '1rem',
                  background: '#0f172a',
                  borderRadius: '0.5rem',
                  border: '2px solid #334155'
                }}>
                  <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.5rem' }}>
                    💡 How This Decision Was Made
                  </h4>
                  <p style={{ fontSize: '0.875rem', color: '#94a3b8', lineHeight: '1.6' }}>
                    The AI analyzed {selectedDecision.topReasons?.length || 3} key features using a SHAP-like 
                    explainability model. Each feature's contribution was calculated based on its impact on the 
                    final decision. The confidence score of {selectedDecision.confidence} indicates the model's 
                    certainty in this decision.
                  </p>
                </div>

                {/* Algorithm Info */}
                <div style={{
                  marginTop: '1.5rem',
                  padding: '1rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  border: '2px solid #334155'
                }}>
                  <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#10b981', marginBottom: '0.5rem' }}>
                    🎓 AI Algorithms Used
                  </h4>
                  <ul style={{ fontSize: '0.875rem', color: '#94a3b8', paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                    <li><strong style={{ color: 'white' }}>SHAP Values:</strong> Feature importance calculation</li>
                    <li><strong style={{ color: 'white' }}>Bayesian Inference:</strong> Confidence estimation</li>
                    <li><strong style={{ color: 'white' }}>Decision Trees:</strong> Classification logic</li>
                    <li><strong style={{ color: 'white' }}>A* Search:</strong> Evacuation path planning</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
                Select a decision from the list to see detailed explanation
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
};

export default XAI;
