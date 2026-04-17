import { useState, useEffect } from 'react';
import { AlertTriangle, Users, Activity, TrendingUp } from 'lucide-react';
import axios from 'axios';
import Card from '../components/Card';
import './Pages.css';

const PolicyComparison = () => {
  const [policies, setPolicies] = useState([]);
  const [situation, setSituation] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState('moderate_flood');
  const [autoUpdate, setAutoUpdate] = useState(false);

  // Load test scenario
  const loadScenario = async (scenarioName) => {
    setLoading(true);
    try {
      const response = await axios.post(
        `http://localhost:8001/api/policy/realtime/test/scenario?scenario_name=${scenarioName}`
      );
      setSituation(response.data.situation_update);
      setRecommendations(response.data.recommendations);
      await loadPolicies();
    } catch (error) {
      console.error('Failed to load scenario:', error);
    }
    setLoading(false);
  };

  // Load all policies
  const loadPolicies = async () => {
    try {
      const response = await axios.get('http://localhost:8001/api/policy/realtime/policies');
      setPolicies(response.data.policies);
    } catch (error) {
      console.error('Failed to load policies:', error);
    }
  };

  // Compare selected policies
  const comparePolicies = async (policyIds) => {
    try {
      const response = await axios.post(
        'http://localhost:8001/api/policy/realtime/policies/compare',
        { policy_ids: policyIds }
      );
      setComparison(response.data);
    } catch (error) {
      console.error('Failed to compare policies:', error);
    }
  };

  // Update situation with random changes
  const updateSituationRealtime = async () => {
    if (!situation || loading) return;
    
    setLoading(true);
    try {
      // Get current values or use defaults
      const currentPanic = situation.human_behavior?.panic_level || 0.5;
      const currentCompliance = situation.human_behavior?.compliance_rate || 0.5;
      
      // Simulate real-time changes with more variation
      const rainChange = (Math.random() - 0.5) * 20;
      const waterChange = (Math.random() - 0.5) * 0.5;
      
      const updated = {
        rain_intensity: Math.max(0, Math.min(150, 65 + rainChange)),
        water_level: Math.max(0, Math.min(3, 1.2 + waterChange)),
        wind_speed: Math.max(0, 30 + (Math.random() - 0.5) * 20),
        visibility: Math.max(50, Math.min(1000, 500 + (Math.random() - 0.5) * 200)),
        power_availability: Math.max(0.1, Math.min(1, 0.6 + (Math.random() - 0.5) * 0.3)),
        communication_status: Math.max(0.1, Math.min(1, 0.6 + (Math.random() - 0.5) * 0.3)),
        road_accessibility: Math.max(0.1, Math.min(1, 0.5 + (Math.random() - 0.5) * 0.3)),
        population_at_risk: 10000,
        population_evacuated: Math.floor(Math.min(10000, currentCompliance * 10000 + Math.random() * 500)),
        casualties: Math.floor(Math.max(0, 5 + (Math.random() - 0.5) * 10)),
        injured: Math.floor(Math.max(0, 20 + (Math.random() - 0.5) * 20)),
        uncertainty_level: ['LOW', 'MEDIUM', 'HIGH', 'EXTREME'][Math.floor(Math.random() * 4)],
        information_accuracy: Math.max(0.3, Math.min(1, 0.6 + (Math.random() - 0.5) * 0.3)),
        rumor_spread_rate: Math.max(0, Math.min(1, 0.5 + (Math.random() - 0.5) * 0.4)),
        emergency_vehicles: Math.floor(20 + Math.random() * 20),
        medical_personnel: Math.floor(50 + Math.random() * 30),
        shelter_capacity: 8000,
        food_supplies: Math.max(1, 3.0 + (Math.random() - 0.5) * 1)
      };

      const response = await axios.post(
        'http://localhost:8001/api/policy/realtime/situation/update',
        updated
      );
      setSituation(response.data);
      
      // Get new recommendations
      const recResponse = await axios.get('http://localhost:8001/api/policy/realtime/recommendations');
      setRecommendations(recResponse.data);
      
      // Update comparison with new policies
      if (recResponse.data.recommended_policies) {
        const topPolicyIds = recResponse.data.recommended_policies
          .slice(0, 3)
          .map(p => p.policy_id);
        if (topPolicyIds.length > 0) {
          await comparePolicies(topPolicyIds);
        }
      }
    } catch (error) {
      console.error('Failed to update situation:', error);
      if (error.response) {
        console.error('Error details:', error.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  // Auto-update effect
  useEffect(() => {
    if (autoUpdate && situation) {
      const interval = setInterval(() => {
        updateSituationRealtime();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [autoUpdate, situation]);

  // Initial load
  useEffect(() => {
    loadScenario(selectedScenario);
  }, []);

  // Compare top 3 policies
  useEffect(() => {
    if (recommendations && recommendations.recommended_policies) {
      const topPolicyIds = recommendations.recommended_policies
        .slice(0, 3)
        .map(p => p.policy_id);
      if (topPolicyIds.length > 0) {
        comparePolicies(topPolicyIds);
      }
    }
  }, [recommendations]);

  if (loading && !situation) {
    return (
      <div className="page">
        <div className="page-header">
          <h1>Real-time Policy Comparison</h1>
          <p>Loading scenario...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Real-time Policy Comparison</h1>
        <p>Compare adaptive policies under current disaster conditions</p>
      </div>

      {/* Control Panel */}
      <Card title="Scenario Control">
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div className="form-group" style={{ flex: 1, minWidth: '200px' }}>
            <label className="form-label">Test Scenario</label>
            <select 
              className="form-select"
              value={selectedScenario}
              onChange={(e) => {
                setSelectedScenario(e.target.value);
                loadScenario(e.target.value);
              }}
            >
              <option value="moderate_flood">Moderate Flood</option>
              <option value="severe_crisis">Severe Crisis</option>
              <option value="communication_failure">Communication Failure</option>
              <option value="high_uncertainty">High Uncertainty</option>
            </select>
          </div>
          
          <button 
            className="btn btn-primary"
            onClick={updateSituationRealtime}
            disabled={!situation || loading}
          >
            {loading ? 'Updating...' : 'Update Situation'}
          </button>
          
          <button 
            className={`btn ${autoUpdate ? 'btn-danger' : 'btn-success'}`}
            onClick={() => setAutoUpdate(!autoUpdate)}
            disabled={!situation}
          >
            {autoUpdate ? 'Stop Auto-Update' : 'Start Auto-Update'}
          </button>
        </div>
      </Card>

      {/* Current Situation */}
      {situation && (
        <Card title="Current Situation">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#ef4444' }}>
                <AlertTriangle size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Severity</div>
                <div className="stat-value">{situation.severity_level || 'UNKNOWN'}</div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#f59e0b' }}>
                <Activity size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Panic Level</div>
                <div className="stat-value">
                  {situation.human_behavior ? 
                    `${(situation.human_behavior.panic_level * 100).toFixed(0)}%` : 
                    'N/A'}
                </div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#3b82f6' }}>
                <Users size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Compliance Rate</div>
                <div className="stat-value">
                  {situation.human_behavior ? 
                    `${(situation.human_behavior.compliance_rate * 100).toFixed(0)}%` : 
                    'N/A'}
                </div>
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#10b981' }}>
                <TrendingUp size={24} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Trust Level</div>
                <div className="stat-value">
                  {situation.human_behavior ? 
                    `${(situation.human_behavior.trust_level * 100).toFixed(0)}%` : 
                    'N/A'}
                </div>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Policy Comparison */}
      {comparison && comparison.comparisons && (
        <Card title="Policy Comparison - Real-time Analysis">
          <div style={{ marginBottom: '1.5rem', padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
            <h4 style={{ color: '#10b981', marginBottom: '0.5rem' }}>✓ Recommended Policy</h4>
            <div style={{ color: '#f1f5f9', fontSize: '1.125rem', fontWeight: '600' }}>
              {comparison.recommendation.policy_name}
            </div>
            <div style={{ color: '#94a3b8', fontSize: '0.875rem', marginTop: '0.25rem' }}>
              {comparison.recommendation.reason}
            </div>
            <div style={{ display: 'flex', gap: '2rem', marginTop: '1rem', fontSize: '0.875rem' }}>
              <div>
                <span style={{ color: '#64748b' }}>Expected Evacuees: </span>
                <span style={{ color: '#10b981', fontWeight: '600' }}>
                  {comparison.recommendation.expected_evacuees}
                </span>
              </div>
              <div>
                <span style={{ color: '#64748b' }}>Expected Casualties: </span>
                <span style={{ color: '#ef4444', fontWeight: '600' }}>
                  {comparison.recommendation.expected_casualties}
                </span>
              </div>
            </div>
          </div>

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: '1rem'
          }}>
            {comparison.comparisons.map((policy) => (
              <div 
                key={policy.policy_id}
                style={{
                  background: '#0f172a',
                  border: `2px solid ${
                    policy.policy_id === comparison.recommendation.policy_id ? '#10b981' : '#334155'
                  }`,
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
                    {policy.policy_name}
                  </h4>
                  {policy.policy_id === comparison.recommendation.policy_id && (
                    <span className="status-badge status-good">Best</span>
                  )}
                </div>

                {/* Effectiveness */}
                <div style={{ 
                  background: '#1e293b', 
                  padding: '1rem', 
                  borderRadius: '0.375rem',
                  marginBottom: '1rem'
                }}>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.25rem' }}>
                    Effectiveness
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#10b981' }}>
                    {(policy.effectiveness * 100).toFixed(0)}%
                  </div>
                  <div style={{ 
                    width: '100%', 
                    height: '4px', 
                    background: '#334155', 
                    borderRadius: '2px',
                    marginTop: '0.5rem',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${policy.effectiveness * 100}%`,
                      height: '100%',
                      background: '#10b981',
                      transition: 'width 0.3s'
                    }} />
                  </div>
                </div>

                {/* Expected Outcomes */}
                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ fontSize: '0.875rem', fontWeight: '600', color: '#cbd5e1', marginBottom: '0.5rem' }}>
                    Expected Outcomes
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#94a3b8' }}>Evacuees</span>
                      <span style={{ color: '#10b981', fontWeight: '600' }}>
                        {policy.expected_outcomes.evacuees} 
                        <span style={{ color: '#64748b', fontSize: '0.75rem', marginLeft: '0.25rem' }}>
                          ({policy.expected_outcomes.evacuees_range[0]}-{policy.expected_outcomes.evacuees_range[1]})
                        </span>
                      </span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#94a3b8' }}>Casualties</span>
                      <span style={{ color: '#ef4444', fontWeight: '600' }}>
                        {policy.expected_outcomes.casualties}
                        <span style={{ color: '#64748b', fontSize: '0.75rem', marginLeft: '0.25rem' }}>
                          ({policy.expected_outcomes.casualties_range[0]}-{policy.expected_outcomes.casualties_range[1]})
                        </span>
                      </span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#94a3b8' }}>Time to Complete</span>
                      <span style={{ color: '#cbd5e1' }}>
                        {policy.expected_outcomes.time_to_complete_hours}h
                      </span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#94a3b8' }}>Success Probability</span>
                      <span style={{ color: '#3b82f6', fontWeight: '600' }}>
                        {(policy.expected_outcomes.success_probability * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Human Factors */}
                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ fontSize: '0.875rem', fontWeight: '600', color: '#cbd5e1', marginBottom: '0.5rem' }}>
                    Human Factors
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#94a3b8' }}>Panic Level</span>
                      <span style={{ color: '#f59e0b' }}>
                        {(policy.human_factors.panic_level * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#94a3b8' }}>Compliance Rate</span>
                      <span style={{ color: '#10b981' }}>
                        {(policy.human_factors.compliance_rate * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Barriers */}
                {policy.barriers && policy.barriers.length > 0 && (
                  <div>
                    <div style={{ fontSize: '0.875rem', fontWeight: '600', color: '#cbd5e1', marginBottom: '0.5rem' }}>
                      Implementation Barriers
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {policy.barriers.slice(0, 2).map((barrier, idx) => (
                        <div 
                          key={idx}
                          style={{
                            padding: '0.5rem',
                            background: '#1e293b',
                            borderRadius: '0.25rem',
                            borderLeft: `3px solid ${
                              barrier.severity === 'HIGH' ? '#ef4444' : 
                              barrier.severity === 'MEDIUM' ? '#f59e0b' : '#3b82f6'
                            }`
                          }}
                        >
                          <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                            {barrier.type}: {barrier.description}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Human Behavior Summary */}
      {comparison && comparison.human_behavior_summary && (
        <Card title="Human Behavior Analysis - Under Uncertainty">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '0.5rem' }}>
                Panic Level
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#f59e0b' }}>
                {(comparison.human_behavior_summary.panic_level * 100).toFixed(0)}%
              </div>
              <div style={{ 
                width: '100%', 
                height: '4px', 
                background: '#334155', 
                borderRadius: '2px',
                marginTop: '0.5rem',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${comparison.human_behavior_summary.panic_level * 100}%`,
                  height: '100%',
                  background: '#f59e0b',
                  transition: 'width 0.5s'
                }} />
              </div>
            </div>

            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '0.5rem' }}>
                Compliance Rate
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#10b981' }}>
                {(comparison.human_behavior_summary.compliance_rate * 100).toFixed(0)}%
              </div>
              <div style={{ 
                width: '100%', 
                height: '4px', 
                background: '#334155', 
                borderRadius: '2px',
                marginTop: '0.5rem',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${comparison.human_behavior_summary.compliance_rate * 100}%`,
                  height: '100%',
                  background: '#10b981',
                  transition: 'width 0.5s'
                }} />
              </div>
            </div>

            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '0.5rem' }}>
                Trust Level
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#3b82f6' }}>
                {(comparison.human_behavior_summary.trust_level * 100).toFixed(0)}%
              </div>
              <div style={{ 
                width: '100%', 
                height: '4px', 
                background: '#334155', 
                borderRadius: '2px',
                marginTop: '0.5rem',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${comparison.human_behavior_summary.trust_level * 100}%`,
                  height: '100%',
                  background: '#3b82f6',
                  transition: 'width 0.5s'
                }} />
              </div>
            </div>

            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '0.5rem' }}>
                Dominant Behavior
              </div>
              <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#cbd5e1' }}>
                {comparison.human_behavior_summary.dominant_behavior}
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

export default PolicyComparison;
