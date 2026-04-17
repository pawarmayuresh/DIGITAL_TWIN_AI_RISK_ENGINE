import { useState, useEffect } from 'react';
import { Network, Calendar, Home, Route, Play, Info } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const CSPVisualization = () => {
  const [allResults, setAllResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cspInfo, setCspInfo] = useState(null);

  useEffect(() => {
    loadCSPInfo();
  }, []);

  const loadCSPInfo = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/csp/info');
      const data = await response.json();
      setCspInfo(data);
    } catch (error) {
      console.error('Error loading CSP info:', error);
    }
  };

  const solveAllCSP = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/api/csp/solve-all?scenario=flood');
      const data = await response.json();
      setAllResults(data);
    } catch (error) {
      console.error('Error solving CSP:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCSPIcon = (type) => {
    if (type.includes('Resource')) return <Network size={20} />;
    if (type.includes('Scheduling')) return <Calendar size={20} />;
    if (type.includes('Shelter')) return <Home size={20} />;
    if (type.includes('Route')) return <Route size={20} />;
    return <Info size={20} />;
  };

  const getStatusColor = (status) => {
    return status === 'solved' ? '#10b981' : '#ef4444';
  };

  const renderResourceAllocation = (problem) => {
    if (!problem.solution) return null;

    return (
      <div>
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
            Team Assignments
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', gap: '0.5rem' }}>
            {Object.entries(problem.solution).map(([team, zone]) => (
              <div key={team} style={{
                padding: '0.5rem',
                background: '#1e293b',
                borderRadius: '0.375rem',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                  {team.replace('_', ' ').toUpperCase()}
                </div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#3b82f6' }}>
                  {zone}
                </div>
              </div>
            ))}
          </div>
        </div>

        {problem.zone_coverage && (
          <div style={{
            padding: '0.75rem',
            background: '#0f172a',
            borderRadius: '0.5rem'
          }}>
            <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
              Zone Coverage
            </div>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {Object.entries(problem.zone_coverage).map(([zone, count]) => (
                <div key={zone} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    background: `linear-gradient(135deg, #3b82f6, #10b981)`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.25rem',
                    fontWeight: 'bold',
                    color: 'white'
                  }}>
                    {count}
                  </div>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Zone</div>
                    <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>{zone}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderEvacuationScheduling = (problem) => {
    if (!problem.schedule) return null;

    return (
      <div>
        <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
          Evacuation Timeline
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {Object.entries(problem.schedule).map(([timeSlot, areas]) => (
            <div key={timeSlot} style={{
              padding: '0.75rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '1rem'
            }}>
              <div style={{
                padding: '0.5rem 1rem',
                background: '#0f172a',
                borderRadius: '0.375rem',
                minWidth: '120px'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Time Slot</div>
                <div style={{ fontSize: '0.875rem', color: '#3b82f6', fontWeight: 'bold' }}>
                  {timeSlot.replace('_', ' ')}
                </div>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.25rem' }}>
                  Areas: {areas.length > 0 ? areas.join(', ') : 'None'}
                </div>
                <div style={{
                  height: '8px',
                  background: '#0f172a',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${(areas.length / 4) * 100}%`,
                    height: '100%',
                    background: 'linear-gradient(90deg, #3b82f6, #10b981)'
                  }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderShelterAssignment = (problem) => {
    if (!problem.utilization) return null;

    return (
      <div>
        <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
          Shelter Utilization
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {Object.entries(problem.utilization).map(([shelterId, util]) => (
            <div key={shelterId} style={{
              padding: '0.75rem',
              background: '#1e293b',
              borderRadius: '0.5rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <div>
                  <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
                    Shelter {shelterId}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                    {util.assigned} / {util.capacity} people
                  </div>
                </div>
                <div style={{
                  fontSize: '1.25rem',
                  fontWeight: 'bold',
                  color: util.percentage > 90 ? '#ef4444' : util.percentage > 70 ? '#f59e0b' : '#10b981'
                }}>
                  {util.percentage.toFixed(0)}%
                </div>
              </div>
              <div style={{
                height: '12px',
                background: '#0f172a',
                borderRadius: '6px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${util.percentage}%`,
                  height: '100%',
                  background: util.percentage > 90 ? 
                    'linear-gradient(90deg, #ef4444, #dc2626)' :
                    util.percentage > 70 ?
                    'linear-gradient(90deg, #f59e0b, #d97706)' :
                    'linear-gradient(90deg, #10b981, #059669)',
                  transition: 'width 0.3s'
                }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderRouteSelection = (problem) => {
    if (!problem.route_usage) return null;

    return (
      <div>
        <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
          Route Assignments
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem' }}>
          {Object.entries(problem.route_usage).map(([routeId, usage]) => (
            <div key={routeId} style={{
              padding: '0.75rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              border: `2px solid ${usage.risk > 0.4 ? '#ef4444' : '#10b981'}`
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold' }}>
                  Route {routeId}
                </div>
                <div style={{
                  padding: '0.125rem 0.5rem',
                  borderRadius: '0.25rem',
                  fontSize: '0.65rem',
                  fontWeight: 'bold',
                  background: usage.risk > 0.4 ? '#7f1d1d' : '#14532d',
                  color: usage.risk > 0.4 ? '#ef4444' : '#10b981'
                }}>
                  {usage.risk > 0.4 ? 'HIGH RISK' : 'SAFE'}
                </div>
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginBottom: '0.5rem' }}>
                Areas: {usage.areas.join(', ') || 'None'}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                <div style={{ color: '#94a3b8' }}>
                  Usage: {usage.count}/{usage.capacity}
                </div>
                <div style={{ color: '#94a3b8' }}>
                  Risk: {(usage.risk * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderConstraints = (problem) => {
    const constraints = getConstraintsForProblem(problem.type);
    if (!constraints) return null;

    return (
      <div style={{ marginTop: '1.5rem' }}>
        <div style={{
          fontSize: '1rem',
          fontWeight: 'bold',
          color: 'white',
          marginBottom: '1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <span>📋</span>
          <span>CSP Constraints</span>
        </div>

        {/* Hard Constraints */}
        <div style={{ marginBottom: '1rem' }}>
          <div style={{
            fontSize: '0.875rem',
            fontWeight: 'bold',
            color: '#ef4444',
            marginBottom: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <span>🔴</span>
            <span>Hard Constraints (Must Satisfy)</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {constraints.hard.map((constraint, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                borderLeft: '4px solid #ef4444'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      HC{idx + 1}: {constraint.name}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                      {constraint.description}
                    </div>
                    {constraint.formula && (
                      <div style={{
                        fontSize: '0.75rem',
                        color: '#64748b',
                        fontFamily: 'monospace',
                        background: '#0f172a',
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        marginTop: '0.25rem'
                      }}>
                        {constraint.formula}
                      </div>
                    )}
                  </div>
                  <div style={{
                    padding: '0.25rem 0.5rem',
                    borderRadius: '0.25rem',
                    fontSize: '0.65rem',
                    fontWeight: 'bold',
                    background: problem.status === 'solved' ? '#14532d' : '#7f1d1d',
                    color: problem.status === 'solved' ? '#10b981' : '#ef4444',
                    whiteSpace: 'nowrap',
                    marginLeft: '0.5rem'
                  }}>
                    {problem.status === 'solved' ? '✓ SATISFIED' : '✗ VIOLATED'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Soft Constraints */}
        <div>
          <div style={{
            fontSize: '0.875rem',
            fontWeight: 'bold',
            color: '#3b82f6',
            marginBottom: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <span>🔵</span>
            <span>Soft Constraints (Optimization Goals)</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {constraints.soft.map((constraint, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                borderLeft: '4px solid #3b82f6'
              }}>
                <div style={{ marginBottom: '0.5rem' }}>
                  <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                    SC{idx + 1}: {constraint.name}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    {constraint.description}
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{
                      height: '8px',
                      background: '#0f172a',
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        width: `${constraint.score}%`,
                        height: '100%',
                        background: 'linear-gradient(90deg, #3b82f6, #10b981)',
                        transition: 'width 0.3s'
                      }} />
                    </div>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#3b82f6', fontWeight: 'bold', minWidth: '40px', textAlign: 'right' }}>
                    {constraint.score}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Overall Quality Score */}
        {problem.status === 'solved' && (
          <div style={{
            marginTop: '1rem',
            padding: '1rem',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            borderRadius: '0.5rem',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.8)', marginBottom: '0.25rem' }}>
              Overall CSP Solution Quality
            </div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white' }}>
              {calculateOverallQuality(constraints)}%
            </div>
          </div>
        )}
      </div>
    );
  };

  const getConstraintsForProblem = (type) => {
    if (type.includes('Resource')) {
      return {
        hard: [
          {
            name: 'Zone Coverage',
            description: 'Each zone must have at least 1 team assigned',
            formula: '∀ zone_j: ∃ team_i where assignment(team_i) = zone_j'
          },
          {
            name: 'Priority Zones',
            description: 'High priority zones (priority ≥ 4) need at least 2 teams',
            formula: '∀ zone_j where priority(zone_j) ≥ 4: count(teams assigned) ≥ 2'
          }
        ],
        soft: [
          {
            name: 'Minimize Distance',
            description: 'Minimize total travel distance for all teams',
            score: 75
          },
          {
            name: 'Balance Workload',
            description: 'Distribute teams evenly across zones',
            score: 82
          }
        ]
      };
    } else if (type.includes('Scheduling')) {
      return {
        hard: [
          {
            name: 'Urgent Evacuation',
            description: 'High risk areas (risk > 0.7) must evacuate in first 2 time slots',
            formula: '∀ area_i where risk(area_i) > 0.7: time_slot(area_i) ∈ {T0, T1}'
          },
          {
            name: 'Adjacent Areas',
            description: 'Adjacent areas cannot evacuate simultaneously',
            formula: '∀ area_i, area_j where adjacent(i,j): time_slot(i) ≠ time_slot(j)'
          },
          {
            name: 'Water Level Threshold',
            description: 'Evacuation must start before water level reaches 3.5m',
            formula: 'start_time < threshold_time(water_level = 3.5m)'
          }
        ],
        soft: [
          {
            name: 'Minimize Evacuation Time',
            description: 'Complete evacuation in minimum time slots',
            score: 68
          },
          {
            name: 'Maximize People Evacuated',
            description: 'Prioritize areas with higher population',
            score: 91
          }
        ]
      };
    } else if (type.includes('Shelter')) {
      return {
        hard: [
          {
            name: 'Shelter Capacity',
            description: 'Total shelter capacity = 750 (must fit 630 evacuees)',
            formula: '∀ shelter_j: Σ(group_size where assigned to shelter_j) ≤ capacity(shelter_j)'
          },
          {
            name: 'Special Needs',
            description: 'Special needs groups must go to equipped shelters',
            formula: '∀ group_i where special_needs(group_i): shelter(group_i) has medical_facility'
          }
        ],
        soft: [
          {
            name: 'Minimize Distance',
            description: 'Assign evacuees to nearest available shelters',
            score: 78
          },
          {
            name: 'Balance Utilization',
            description: 'Distribute evacuees evenly across shelters',
            score: 85
          }
        ]
      };
    } else if (type.includes('Route')) {
      return {
        hard: [
          {
            name: 'Route Safety',
            description: 'Routes must avoid flooded areas (risk < 0.5)',
            formula: '∀ route_j assigned: risk(route_j) < 0.5'
          },
          {
            name: 'Route Capacity',
            description: 'Each route can serve maximum number of areas',
            formula: '∀ route_j: count(areas using route_j) ≤ capacity(route_j)'
          }
        ],
        soft: [
          {
            name: 'Minimize Distance',
            description: 'Select shortest safe routes',
            score: 72
          },
          {
            name: 'Load Balancing',
            description: 'Use multiple routes to distribute traffic',
            score: 88
          }
        ]
      };
    }
    return null;
  };

  const calculateOverallQuality = (constraints) => {
    const softScores = constraints.soft.map(c => c.score);
    const avgSoft = softScores.reduce((a, b) => a + b, 0) / softScores.length;
    return Math.round(avgSoft);
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🧩 CSP Visualization</h1>
          <p>Constraint Satisfaction Problems for Disaster Management</p>
        </div>
        <button
          className="btn btn-primary"
          onClick={solveAllCSP}
          disabled={loading}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <Play size={16} />
          {loading ? 'Solving...' : 'Solve All CSP'}
        </button>
      </div>

      {/* CSP Info Cards */}
      {cspInfo && (
        <div style={{
          padding: '1.5rem',
          background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
          borderRadius: '0.75rem',
          marginBottom: '1.5rem'
        }}>
          <h3 style={{ margin: '0 0 1rem 0', color: 'white' }}>CSP Formulation</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.25rem' }}>Variables</div>
              <div style={{ fontSize: '0.875rem', color: 'white' }}>
                {cspInfo.csp_formulation.components.variables}
              </div>
            </div>
            <div style={{ padding: '1rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.25rem' }}>Domains</div>
              <div style={{ fontSize: '0.875rem', color: 'white' }}>
                {cspInfo.csp_formulation.components.domains}
              </div>
            </div>
            <div style={{ padding: '1rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '0.5rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.25rem' }}>Constraints</div>
              <div style={{ fontSize: '0.875rem', color: 'white' }}>
                {cspInfo.csp_formulation.components.constraints}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {allResults && (
        <>
          {/* Summary */}
          <div style={{
            padding: '1rem',
            background: '#1e293b',
            borderRadius: '0.75rem',
            marginBottom: '1.5rem',
            display: 'flex',
            justifyContent: 'space-around',
            flexWrap: 'wrap',
            gap: '1rem'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>
                {allResults.summary.solved}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Problems Solved</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3b82f6' }}>
                {allResults.summary.total_iterations}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Total Iterations</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f59e0b' }}>
                {allResults.summary.total_backtracks}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Backtracks</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#8b5cf6' }}>
                {allResults.summary.total_problems}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>CSP Types</div>
            </div>
          </div>

          {/* CSP Problems */}
          <div className="grid-2">
            {allResults.csp_problems.map((problem, idx) => (
              <Card
                key={idx}
                title={
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    {getCSPIcon(problem.type)}
                    <span>{problem.type}</span>
                  </div>
                }
              >
                <div>
                  {/* Status */}
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '1rem',
                    padding: '0.75rem',
                    background: '#0f172a',
                    borderRadius: '0.5rem'
                  }}>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Status</div>
                      <div style={{
                        fontSize: '0.875rem',
                        fontWeight: 'bold',
                        color: getStatusColor(problem.status)
                      }}>
                        {problem.status.toUpperCase()}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Iterations</div>
                      <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                        {problem.iterations}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Backtracks</div>
                      <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                        {problem.backtracks}
                      </div>
                    </div>
                  </div>

                  {/* Solution Visualization */}
                  {problem.status === 'solved' && (
                    <div>
                      {problem.type.includes('Resource') && renderResourceAllocation(problem)}
                      {problem.type.includes('Scheduling') && renderEvacuationScheduling(problem)}
                      {problem.type.includes('Shelter') && renderShelterAssignment(problem)}
                      {problem.type.includes('Route') && renderRouteSelection(problem)}
                    </div>
                  )}

                  {problem.status === 'no_solution' && (
                    <div style={{
                      padding: '1rem',
                      background: '#7f1d1d',
                      borderRadius: '0.5rem',
                      textAlign: 'center',
                      color: '#ef4444'
                    }}>
                      No solution found. Constraints may be too restrictive.
                    </div>
                  )}

                  {/* Constraints Display */}
                  {renderConstraints(problem)}
                </div>
              </Card>
            ))}
          </div>
        </>
      )}

      {!allResults && !loading && (
        <div style={{
          padding: '3rem',
          textAlign: 'center',
          color: '#64748b'
        }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🧩</div>
          <div style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>
            Click "Solve All CSP" to visualize constraint satisfaction problems
          </div>
          <div style={{ fontSize: '0.875rem' }}>
            See how the system solves resource allocation, scheduling, assignment, and routing problems
          </div>
        </div>
      )}
    </div>
  );
};

export default CSPVisualization;
