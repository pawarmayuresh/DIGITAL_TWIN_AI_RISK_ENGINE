import { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, MapPin, Users, AlertTriangle, Navigation, Activity } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import './Pages.css';

const UrbanEvacuation = () => {
  const { selectedWard, selectWard, disasterType, setDisasterType } = useWard();
  const [gridData, setGridData] = useState(null);
  const [simulationActive, setSimulationActive] = useState(false);
  const [simulationStep, setSimulationStep] = useState(0);
  const [agents, setAgents] = useState([]);
  const [paths, setPaths] = useState([]);
  const [stats, setStats] = useState({
    total_agents: 0,
    evacuating: 0,
    safe: 0,
    stuck: 0,
    average_health: 100,
    completion_rate: 0
  });
  const [selectedGrid, setSelectedGrid] = useState(null);
  const [pathExplanation, setPathExplanation] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [cars, setCars] = useState([]);
  const [carSimulationActive, setCarSimulationActive] = useState(false);
  const [carStats, setCarStats] = useState({ total_evacuated: 0, active_missions: 0 });
  const [activityLog, setActivityLog] = useState([]);
  const [infrastructureImpact, setInfrastructureImpact] = useState(null);
  const [resourceNeeds, setResourceNeeds] = useState(null);
  const intervalRef = useRef(null);
  const refreshIntervalRef = useRef(null);
  const carIntervalRef = useRef(null);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setActivityLog(prev => [{
      time: timestamp,
      message,
      type
    }, ...prev].slice(0, 50)); // Keep last 50 logs
  };

  const wards = [
    { ward_id: 'A', ward_name: 'Colaba', population: 185014, risk_score: 0.65, severity_level: 'High' },
    { ward_id: 'E', ward_name: 'Byculla', population: 189986, risk_score: 0.72, severity_level: 'High' },
    { ward_id: 'L', ward_name: 'Kurla', population: 800000, risk_score: 0.88, severity_level: 'Severe' },
    { ward_id: 'K/E', ward_name: 'Andheri East', population: 460000, risk_score: 0.58, severity_level: 'Moderate' },
    { ward_id: 'H/E', ward_name: 'Bandra East', population: 290000, risk_score: 0.54, severity_level: 'Moderate' },
    { ward_id: 'M/E', ward_name: 'Chembur', population: 350000, risk_score: 0.76, severity_level: 'High' },
    { ward_id: 'T', ward_name: 'Ghatkopar', population: 420000, risk_score: 0.69, severity_level: 'High' },
    { ward_id: 'R/N', ward_name: 'Borivali', population: 710000, risk_score: 0.48, severity_level: 'Moderate' }
  ];

  // Fetch grid data on mount and when ward changes
  useEffect(() => {
    const initializeGrid = async () => {
      try {
        // Reset the grid to get fresh state
        await fetch('http://localhost:8001/api/evacuation/reset-all', {
          method: 'POST'
        });
        addLog('Grid reset to initial state', 'info');
      } catch (error) {
        console.error('Error resetting grid:', error);
      }
      
      // Then fetch the grid data
      await fetchGridData();
      
      // Load infrastructure impact if ward selected
      if (selectedWard) {
        await loadInfrastructureImpact();
      }
      
      addLog('Urban Evacuation System initialized', 'info');
    };
    
    initializeGrid();
  }, [selectedWard]);

  const loadInfrastructureImpact = async () => {
    if (!selectedWard) return;
    
    try {
      const response = await fetch(`http://localhost:8001/api/infrastructure/evacuation/ward-impact/${selectedWard.ward_id}`);
      const data = await response.json();
      
      if (data.success) {
        setInfrastructureImpact(data.ward_impact);
        
        // Log infrastructure status
        if (data.ward_impact.infrastructure_available) {
          addLog(`Infrastructure: ${data.ward_impact.avg_health?.toFixed(0)}% health, Priority: ${data.ward_impact.evacuation_priority}`, 
                 data.ward_impact.evacuation_priority === 'CRITICAL' ? 'error' : 'warning');
          
          // Log recommendations
          if (data.ward_impact.recommendations) {
            data.ward_impact.recommendations.forEach(rec => {
              addLog(rec, 'warning');
            });
          }
        }
      }
      
      // Load resource needs
      const resourceResponse = await fetch(`http://localhost:8001/api/infrastructure/evacuation/resource-needs/${selectedWard.ward_id}`);
      const resourceData = await resourceResponse.json();
      
      if (resourceData.success) {
        setResourceNeeds(resourceData.resource_needs);
        
        if (resourceData.resource_needs.needs_additional_resources) {
          addLog(`Additional resources needed: ${resourceData.resource_needs.additional_cars} cars, ${resourceData.resource_needs.additional_agents} agents`, 'warning');
        }
      }
    } catch (error) {
      console.error('Failed to load infrastructure impact:', error);
    }
  };

  // Auto-refresh grid data
  useEffect(() => {
    if (autoRefresh) {
      refreshIntervalRef.current = setInterval(() => {
        updateRealtimeConditions();
      }, 3000); // Update every 3 seconds
    } else {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    }
    
    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, [autoRefresh]);

  const fetchGridData = async () => {
    try {
      const wardParam = selectedWard ? `?ward_id=${selectedWard.ward_id}` : '';
      const response = await fetch(`http://localhost:8001/api/evacuation/grid${wardParam}`);
      const data = await response.json();
      setGridData(data);
      
      // Count dangerous zones
      const dangerousCount = data.grids.filter(g => g.safety_level === 'DANGEROUS').length;
      const safeCount = data.grids.filter(g => g.safety_level === 'SAFE').length;
      const avgRisk = data.grids.reduce((sum, g) => sum + g.risk_score, 0) / data.grids.length;
      
      if (selectedWard) {
        addLog(`Grid loaded for ${selectedWard.ward_name}: ${dangerousCount} dangerous zones, ${safeCount} safe zones`, 'success');
        
        // Broadcast evacuation simulation event for infrastructure integration
        window.dispatchEvent(new CustomEvent('evacuationSimulated', {
          detail: {
            ward: selectedWard,
            dangerousZones: dangerousCount,
            safeZones: safeCount,
            riskLevel: avgRisk,
            rainfall: Math.random() * 0.8 + 0.2, // Simulated rainfall
            waterLevel: avgRisk * 0.8, // Water level based on risk
            timestamp: Date.now()
          }
        }));
      } else {
        addLog(`Grid loaded: ${dangerousCount} dangerous zones, ${safeCount} safe zones`, 'info');
      }
    } catch (error) {
      console.error('Error fetching grid data:', error);
      addLog('Error loading grid data', 'error');
    }
  };

  const updateRealtimeConditions = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/evacuation/update-realtime', {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        setGridData(data.grid_data);
        const dangerousCount = data.grid_data.grids.filter(g => g.safety_level === 'DANGEROUS').length;
        addLog(`Real-time update: ${dangerousCount} dangerous zones detected`, 'warning');
      }
    } catch (error) {
      console.error('Error updating conditions:', error);
    }
  };

  const initializeSimulation = async () => {
    try {
      addLog('Initializing human agent evacuation...', 'info');
      
      const response = await fetch('http://localhost:8001/api/evacuation/initialize-simulation?agents_per_zone=3', {
        method: 'POST'
      });
      const data = await response.json();
      setAgents(data.agents);
      setStats(data.stats);
      
      // Fetch paths
      const pathsResponse = await fetch('http://localhost:8001/api/evacuation/simulation-paths');
      const pathsData = await pathsResponse.json();
      setPaths(pathsData.paths);
      
      addLog(`${data.agents_created} human agents created in dangerous zones`, 'success');
      addLog(`${pathsData.paths.length} evacuation routes calculated`, 'info');
    } catch (error) {
      console.error('Error initializing simulation:', error);
      addLog('Error initializing human evacuation: ' + error.message, 'error');
    }
  };

  const runSimulationStep = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/evacuation/simulation-step', {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }
      
      const data = await response.json();
      setSimulationStep(data.step || 0);
      setAgents(data.agents || []);
      setStats(data.stats || {});
      
      // Log significant events
      if (data.step && data.step % 5 === 0) {
        const stats = data.stats || {};
        addLog(`Step ${data.step}: ${stats.evacuating || 0} agents evacuating, ${stats.safe || 0} reached safety`, 'info');
      }
      
      // Check for newly safe agents
      const newlySafe = (data.agents || []).filter(a => a.status === 'SAFE').length;
      const previouslySafe = agents.filter(a => a.status === 'SAFE').length;
      if (newlySafe > previouslySafe) {
        addLog(`${newlySafe - previouslySafe} agents reached safety!`, 'success');
      }
      
      if (data.stats && data.stats.completion_rate === 100) {
        stopSimulation();
        addLog(`✅ Human evacuation complete! All ${data.stats.total_agents} agents evacuated`, 'success');
      }
    } catch (error) {
      console.error('Error running simulation step:', error);
      addLog('Error in human evacuation step: ' + error.message, 'error');
      stopSimulation(); // Stop on error
    }
  };


  const startSimulation = async () => {
    if (!selectedWard) {
      alert('Please select a ward first to run evacuation simulation');
      return;
    }
    
    addLog('🚶 Starting human agent evacuation simulation...', 'info');
    await initializeSimulation();
    setSimulationActive(true);
    intervalRef.current = setInterval(() => {
      runSimulationStep();
    }, 1000); // 1 step per second
    addLog('Human agents are now evacuating on foot', 'success');
  };

  const stopSimulation = () => {
    setSimulationActive(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  const resetSimulation = async () => {
    stopSimulation();
    try {
      await fetch('http://localhost:8001/api/evacuation/reset-simulation', {
        method: 'POST'
      });
      setSimulationStep(0);
      setAgents([]);
      setPaths([]);
      setStats({});
      setSelectedGrid(null);
      setPathExplanation(null);
      await fetchGridData();
      addLog('Human evacuation simulation reset', 'info');
    } catch (error) {
      console.error('Error resetting simulation:', error);
      addLog('Error resetting simulation: ' + error.message, 'error');
    }
  };

  const handleGridClick = async (grid) => {
    setSelectedGrid(grid);
    addLog(`Grid ${grid.id} (${grid.name}) selected - Risk: ${(grid.risk_score * 100).toFixed(0)}%, Population: ${grid.population_density}, Safety: ${grid.safety_level}`, 'info');
    
    // If grid is dangerous, show evacuation path
    if (grid.safety_level === 'DANGEROUS') {
      try {
        // Find nearest safe zone
        const safeZonesResponse = await fetch('http://localhost:8001/api/evacuation/safe-zones');
        const safeZonesData = await safeZonesResponse.json();
        
        if (safeZonesData.zones.length > 0) {
          const nearestSafe = safeZonesData.zones[0]; // Simplified - take first
          
          // Find path
          const pathResponse = await fetch(
            `http://localhost:8001/api/evacuation/find-path?start_grid_id=${grid.id}&goal_grid_id=${nearestSafe.id}`,
            { method: 'POST' }
          );
          const pathData = await pathResponse.json();
          setPathExplanation(pathData);
          
          if (pathData.success) {
            addLog(`Evacuation path found: ${grid.id} → ${nearestSafe.id} (${pathData.path_length} steps)`, 'success');
          }
        }
      } catch (error) {
        console.error('Error finding path:', error);
      }
    }
  };

  const getGridColor = (grid) => {
    return grid.color;
  };

  const isAgentOnGrid = (gridId) => {
    return agents.some(agent => agent.position.grid_id === gridId);
  };

  const getAgentOnGrid = (gridId) => {
    return agents.find(agent => agent.position.grid_id === gridId);
  };

  const isCarOnGrid = (gridId) => {
    return cars && cars.length > 0 && cars.some(car => car.current_grid_id === gridId);
  };

  const getCarOnGrid = (gridId) => {
    return cars && cars.length > 0 ? cars.find(car => car.current_grid_id === gridId) : null;
  };

  const startCarEvacuation = async () => {
    if (!selectedWard) {
      alert('Please select a ward first to run car evacuation');
      return;
    }

    try {
      addLog('Initializing car evacuation system...', 'info');
      
      // Reset cars first
      addLog('Resetting car system...', 'info');
      const resetResponse = await fetch('http://localhost:8001/api/evacuation/car/reset', { method: 'POST' });
      if (!resetResponse.ok) {
        throw new Error(`Reset failed: ${resetResponse.status}`);
      }
      addLog('Car system reset', 'success');

      // Auto-assign will create cars and assign missions automatically
      addLog('Requesting car deployment and mission assignment...', 'info');
      const assignResponse = await fetch('http://localhost:8001/api/evacuation/car/auto-assign', {
        method: 'POST'
      });
      
      if (!assignResponse.ok) {
        throw new Error(`Auto-assign failed: ${assignResponse.status} ${assignResponse.statusText}`);
      }
      
      const assignData = await assignResponse.json();
      
      console.log('Auto-assign response:', assignData);
      
      if (assignData.success) {
        setCars(assignData.cars || []);
        setCarStats({
          total_evacuated: 0,
          active_missions: assignData.missions_assigned || 0
        });

        addLog(`Found ${assignData.dangerous_zones_found || 0} dangerous zones, ${assignData.safe_zones_found || 0} safe zones`, 'info');
        addLog(`${assignData.cars.length || 0} rescue vehicles deployed (5 cars)`, 'success');
        addLog(`${assignData.missions_assigned || 0} evacuation missions assigned to vehicles`, assignData.missions_assigned > 0 ? 'success' : 'warning');
        
        if (assignData.missions_assigned > 0) {
          setCarSimulationActive(true);

          // Start simulation loop
          carIntervalRef.current = setInterval(() => {
            runCarSimulationStep();
          }, 1500); // 1.5 seconds per step
          
          addLog('Car simulation started - vehicles are moving', 'success');
        } else {
          addLog('⚠️ No missions assigned - no dangerous zones with population found', 'warning');
          addLog('Try enabling "Real-time Updates" to create dangerous zones', 'info');
        }
      } else {
        addLog('Failed to deploy cars: ' + (assignData.message || 'Unknown error'), 'error');
      }
    } catch (error) {
      console.error('Error starting car evacuation:', error);
      addLog(`❌ Error: ${error.message}`, 'error');
      addLog('Make sure backend is running on port 8001', 'error');
    }
  };

  const runCarSimulationStep = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/evacuation/car/simulate-step', {
        method: 'POST'
      });
      const data = await response.json();
      
      // Log state changes
      if (data.state_changes && data.state_changes.length > 0) {
        data.state_changes.forEach(change => {
          if (change.action === 'PICKED_UP') {
            addLog(`${change.car_id} picked up ${change.count} people from ${change.grid_id}`, 'warning');
          } else if (change.action === 'DROPPED_OFF') {
            addLog(`${change.car_id} dropped off ${change.count} people at safe zone ${change.grid_id}`, 'success');
          } else if (change.new_state) {
            addLog(`${change.car_id} ${change.new_state.toLowerCase().replace(/_/g, ' ')} at ${change.grid_id}`, 'info');
          }
        });
      }
      
      setCars(data.cars || []);
      setCarStats({
        total_evacuated: data.total_evacuated || 0,
        active_missions: data.active_missions || 0
      });

      // Update grid data to reflect population changes
      await fetchGridData();

      // Stop if no active missions
      if ((data.active_missions || 0) === 0) {
        stopCarSimulation();
        addLog(`All car missions complete! Total evacuated: ${data.total_evacuated}`, 'success');
      }
    } catch (error) {
      console.error('Error running car simulation step:', error);
    }
  };

  const stopCarSimulation = () => {
    setCarSimulationActive(false);
    if (carIntervalRef.current) {
      clearInterval(carIntervalRef.current);
    }
  };

  const resetCarSimulation = async () => {
    stopCarSimulation();
    try {
      await fetch('http://localhost:8001/api/evacuation/car/reset', { method: 'POST' });
      setCars([]);
      setCarStats({ total_evacuated: 0, active_missions: 0 });
      await fetchGridData();
    } catch (error) {
      console.error('Error resetting car simulation:', error);
    }
  };

  if (!gridData) {
    return <div className="page"><div style={{ padding: '2rem', textAlign: 'center' }}>Loading grid data...</div></div>;
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>🏙️ Urban Evacuation Simulation</h1>
        {selectedWard ? (
          <p>
            AI-powered evacuation planning for <strong style={{ color: '#3b82f6' }}>{selectedWard.ward_name}</strong> ward
            <span style={{ 
              marginLeft: '1rem',
              padding: '0.25rem 0.75rem',
              background: selectedWard.severity_level === 'Severe' ? '#7f1d1d' : 
                         selectedWard.severity_level === 'High' ? '#78350f' : '#1e293b',
              color: selectedWard.severity_level === 'Severe' ? '#ef4444' : 
                     selectedWard.severity_level === 'High' ? '#f59e0b' : '#10b981',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
              fontWeight: 'bold'
            }}>
              {selectedWard.severity_level} Risk
            </span>
          </p>
        ) : (
          <p>AI-powered evacuation planning with A* pathfinding and human agent simulation</p>
        )}
      </div>

      {/* Ward Selection */}
      {!selectedWard && (
        <Card title="⚠️ Select Ward and Disaster Type">
          <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem', marginBottom: '1rem' }}>
            <p style={{ color: '#94a3b8', marginBottom: '1rem' }}>
              Please select a Mumbai ward and disaster type to see evacuation planning for that specific scenario.
            </p>
            <div className="grid-2" style={{ gap: '1rem' }}>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Select Ward</label>
                <select 
                  className="form-select"
                  value=""
                  onChange={(e) => {
                    const ward = wards.find(w => w.ward_id === e.target.value);
                    if (ward) {
                      selectWard(ward, disasterType || 'flood');
                      // Refresh grid data after ward selection
                      setTimeout(() => fetchGridData(), 500);
                    }
                  }}
                >
                  <option value="">Choose a ward...</option>
                  {wards.map(w => (
                    <option key={w.ward_id} value={w.ward_id}>
                      {w.ward_name} - {w.severity_level} Risk (Pop: {w.population.toLocaleString()})
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Disaster Type</label>
                <select 
                  className="form-select"
                  value={disasterType || 'flood'}
                  onChange={(e) => setDisasterType && setDisasterType(e.target.value)}
                >
                  <option value="flood">🌊 Flood</option>
                  <option value="fire">🔥 Fire</option>
                  <option value="contamination">☢️ Contamination</option>
                </select>
              </div>
            </div>
          </div>
          <div style={{ 
            padding: '1rem', 
            background: '#0f172a', 
            borderRadius: '0.5rem',
            borderLeft: '4px solid #3b82f6'
          }}>
            <div style={{ fontSize: '0.875rem', color: '#94a3b8', lineHeight: '1.6' }}>
              <strong style={{ color: '#60a5fa' }}>💡 Tip:</strong> You can also select a ward from the 
              <strong style={{ color: 'white' }}> Mumbai Live</strong> page, and it will automatically be used here.
            </div>
          </div>
        </Card>
      )}

      {/* Ward Info Banner */}
      {selectedWard && gridData && (
        <Card title={`📍 ${selectedWard.ward_name} Ward Information`}>
          <div className="grid-3">
            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem', borderLeft: '4px solid #3b82f6' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>Population</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                {selectedWard.population.toLocaleString()}
              </div>
            </div>
            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem', borderLeft: '4px solid #f59e0b' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>Risk Score</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#f59e0b' }}>
                {(selectedWard.risk_score * 100).toFixed(0)}%
              </div>
            </div>
            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem', borderLeft: '4px solid #ef4444' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>Severity Level</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: selectedWard.severity_level === 'Severe' ? '#ef4444' : selectedWard.severity_level === 'High' ? '#f59e0b' : '#10b981' }}>
                {selectedWard.severity_level}
              </div>
            </div>
          </div>
          
          {/* Infrastructure Impact */}
          {infrastructureImpact && infrastructureImpact.infrastructure_available && (
            <div style={{ marginTop: '1rem' }}>
              <div style={{ 
                padding: '0.75rem', 
                background: infrastructureImpact.evacuation_priority === 'CRITICAL' ? '#7f1d1d' : 
                           infrastructureImpact.evacuation_priority === 'HIGH' ? '#78350f' : '#1e293b',
                borderRadius: '0.5rem',
                fontSize: '0.875rem',
                borderLeft: `4px solid ${infrastructureImpact.evacuation_priority === 'CRITICAL' ? '#ef4444' : 
                                         infrastructureImpact.evacuation_priority === 'HIGH' ? '#f59e0b' : '#10b981'}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <strong style={{ color: 'white' }}>🏗️ Infrastructure Status:</strong>
                  <span style={{ 
                    padding: '0.125rem 0.5rem',
                    borderRadius: '0.25rem',
                    background: infrastructureImpact.evacuation_priority === 'CRITICAL' ? '#991b1b' : 
                               infrastructureImpact.evacuation_priority === 'HIGH' ? '#92400e' : '#065f46',
                    color: infrastructureImpact.evacuation_priority === 'CRITICAL' ? '#fca5a5' : 
                           infrastructureImpact.evacuation_priority === 'HIGH' ? '#fbbf24' : '#6ee7b7',
                    fontSize: '0.75rem',
                    fontWeight: 'bold'
                  }}>
                    {infrastructureImpact.evacuation_priority}
                  </span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem', fontSize: '0.75rem', color: '#cbd5e1' }}>
                  <div>
                    Health: <strong style={{ color: infrastructureImpact.avg_health > 70 ? '#10b981' : infrastructureImpact.avg_health > 50 ? '#f59e0b' : '#ef4444' }}>
                      {infrastructureImpact.avg_health?.toFixed(0)}%
                    </strong>
                  </div>
                  <div>
                    {infrastructureImpact.hospital_operational ? '✓' : '✗'} Hospital
                  </div>
                  <div>
                    {infrastructureImpact.emergency_services_operational ? '✓' : '✗'} Emergency
                  </div>
                </div>
                {infrastructureImpact.recommendations && infrastructureImpact.recommendations.length > 0 && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: '#fbbf24' }}>
                    {infrastructureImpact.recommendations[0]}
                  </div>
                )}
              </div>
            </div>
          )}
          
          <div style={{ 
            marginTop: '1rem',
            padding: '0.75rem', 
            background: '#0f172a', 
            borderRadius: '0.5rem',
            fontSize: '0.875rem',
            color: '#94a3b8',
            borderLeft: '4px solid #10b981'
          }}>
            <strong style={{ color: '#10b981' }}>✓ Connected:</strong> Grid data is now customized for {selectedWard.ward_name} ward with real risk scores and population data.
          </div>
        </Card>
      )}

      {/* Controls */}
      <Card title="Simulation Controls">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {/* Quick Start Button */}
          <div style={{ 
            padding: '1rem', 
            background: '#1e293b', 
            borderRadius: '0.5rem',
            borderLeft: '4px solid #3b82f6'
          }}>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.5rem' }}>
              🚀 Quick Start
            </div>
            <button
              className="btn btn-primary"
              onClick={async () => {
                if (!selectedWard) {
                  alert('Please select a ward first');
                  return;
                }
                addLog('🚀 Quick Start: Initializing complete evacuation system...', 'info');
                await startSimulation();
                setTimeout(async () => {
                  await startCarEvacuation();
                  addLog('✅ Both human and car evacuation systems are now running!', 'success');
                }, 1000);
              }}
              disabled={simulationActive || carSimulationActive || !selectedWard}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                fontSize: '1rem',
                padding: '0.75rem 1.5rem',
                background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                border: 'none'
              }}
              title={!selectedWard ? 'Select a ward first' : 'Start both human and car evacuation simultaneously'}
            >
              <Play size={20} />
              Quick Start All Systems
            </button>
            <div style={{ 
              marginTop: '0.5rem',
              fontSize: '0.75rem',
              color: '#94a3b8'
            }}>
              Starts both human agents and car evacuation with one click
            </div>
          </div>

          {/* Human Agent Controls */}
          <div>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.5rem' }}>
              👥 Human Agent Evacuation
            </div>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
              <button
                className="btn btn-primary"
                onClick={startSimulation}
                disabled={simulationActive || !selectedWard}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
                title={!selectedWard ? 'Select a ward first' : 'Start evacuation simulation'}
              >
                <Play size={16} />
                Start Human Evacuation
              </button>
              <button
                className="btn btn-secondary"
                onClick={stopSimulation}
                disabled={!simulationActive}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <Pause size={16} />
                Pause
              </button>
              <button
                className="btn btn-secondary"
                onClick={resetSimulation}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <RotateCcw size={16} />
                Reset
              </button>
              
              {simulationActive && (
                <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Step: <span style={{ color: 'white', fontWeight: 'bold' }}>{simulationStep}</span>
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Completion: <span style={{ color: '#10b981', fontWeight: 'bold' }}>{stats.completion_rate || 0}%</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Car Evacuation Controls */}
          <div style={{ paddingTop: '1rem', borderTop: '1px solid #1e293b' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#f59e0b', marginBottom: '0.5rem' }}>
              🚗 Car-Based Evacuation
            </div>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
              <button
                className="btn btn-primary"
                onClick={startCarEvacuation}
                disabled={carSimulationActive || !selectedWard}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#f59e0b', borderColor: '#f59e0b' }}
                title={!selectedWard ? 'Select a ward first' : 'Start car evacuation'}
              >
                <Play size={16} />
                Start Car Evacuation
              </button>
              <button
                className="btn btn-secondary"
                onClick={stopCarSimulation}
                disabled={!carSimulationActive}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <Pause size={16} />
                Pause Cars
              </button>
              <button
                className="btn btn-secondary"
                onClick={resetCarSimulation}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                <RotateCcw size={16} />
                Reset Cars
              </button>
              
              {carSimulationActive && (
                <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Active Missions: <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>{carStats.active_missions}</span>
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                    Evacuated by Cars: <span style={{ color: '#10b981', fontWeight: 'bold' }}>{carStats.total_evacuated}</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Real-time Updates */}
          <div style={{ paddingTop: '1rem', borderTop: '1px solid #1e293b' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                disabled={!selectedWard}
                style={{ width: '18px', height: '18px', cursor: selectedWard ? 'pointer' : 'not-allowed' }}
              />
              <span style={{ fontSize: '0.875rem', color: selectedWard ? '#94a3b8' : '#64748b' }}>
                Real-time Grid Updates {autoRefresh && '🔄'}
              </span>
            </label>
          </div>
        </div>
      </Card>

      {/* Statistics */}
      {stats.total_agents > 0 && (
        <div className="stats-grid">
          <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
            <div className="stat-icon" style={{ color: '#3b82f6' }}>
              <Users size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Total Agents</div>
              <div className="stat-value">{stats.total_agents}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
            <div className="stat-icon" style={{ color: '#f59e0b' }}>
              <Activity size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Evacuating</div>
              <div className="stat-value">{stats.evacuating}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
            <div className="stat-icon" style={{ color: '#10b981' }}>
              <MapPin size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Reached Safety</div>
              <div className="stat-value">{stats.safe}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#ef4444' }}>
            <div className="stat-icon" style={{ color: '#ef4444' }}>
              <AlertTriangle size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Stuck</div>
              <div className="stat-value">{stats.stuck}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#8b5cf6' }}>
            <div className="stat-content">
              <div className="stat-label">Avg Health</div>
              <div className="stat-value">{stats.average_health}%</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
            <div className="stat-content">
              <div className="stat-label">Completion</div>
              <div className="stat-value">{stats.completion_rate}%</div>
            </div>
          </div>
        </div>
      )}


      {/* Mumbai Grid Visualization */}
      {selectedWard && gridData && (
        <Card title={`🗺️ ${selectedWard.ward_name} Ward - Evacuation Grid`}>
        <div style={{ marginBottom: '1rem', display: 'flex', gap: '2rem', fontSize: '0.875rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '20px', height: '20px', background: '#10b981', borderRadius: '4px' }}></div>
            <span style={{ color: '#94a3b8' }}>Safe Zone</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '20px', height: '20px', background: '#f59e0b', borderRadius: '4px' }}></div>
            <span style={{ color: '#94a3b8' }}>Medium Risk</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '20px', height: '20px', background: '#ef4444', borderRadius: '4px' }}></div>
            <span style={{ color: '#94a3b8' }}>Dangerous</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.25rem' }}>👤</span>
            <span style={{ color: '#94a3b8' }}>Human Agent</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.25rem' }}>🚗</span>
            <span style={{ color: '#94a3b8' }}>Rescue Car</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.25rem' }}>🏁</span>
            <span style={{ color: '#94a3b8' }}>Evacuation Point</span>
          </div>
        </div>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${gridData.grid_cols}, 1fr)`,
          gap: '2px',
          background: '#0f172a',
          padding: '1rem',
          borderRadius: '0.5rem',
          maxWidth: '900px',
          margin: '0 auto'
        }}>
          {gridData.grids.map((grid) => {
            const hasAgent = isAgentOnGrid(grid.id);
            const agent = getAgentOnGrid(grid.id);
            const hasCar = isCarOnGrid(grid.id);
            const car = getCarOnGrid(grid.id);
            const isSelected = selectedGrid?.id === grid.id;
            
            return (
              <div
                key={grid.id}
                onClick={() => handleGridClick(grid)}
                style={{
                  aspectRatio: '1',
                  background: getGridColor(grid),
                  border: isSelected ? '2px solid white' : grid.is_evacuation_point ? '2px solid #fbbf24' : '1px solid #1e293b',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  position: 'relative',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '10px',
                  transition: 'all 0.3s',
                  boxShadow: isSelected ? '0 0 15px rgba(255, 255, 255, 0.8)' : 'none',
                  transform: isSelected ? 'scale(1.1)' : 'scale(1)'
                }}
                title={`${grid.name} (${grid.id})\nRisk: ${(grid.risk_score * 100).toFixed(0)}%\nPopulation: ${grid.population_density}\nSafety: ${grid.safety_level}`}
              >
                {/* Grid ID */}
                <span style={{ 
                  position: 'absolute', 
                  top: '2px', 
                  left: '2px', 
                  fontSize: '7px', 
                  color: 'rgba(255,255,255,0.6)',
                  fontWeight: 'bold'
                }}>
                  {grid.id}
                </span>
                
                {/* Evacuation Point Marker */}
                {grid.is_evacuation_point && (
                  <span style={{ fontSize: '12px', filter: 'drop-shadow(0 0 2px #000)' }}>🏁</span>
                )}
                
                {/* Car Agent - Bigger and Animated */}
                {hasCar && (
                  <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: hasAgent ? '70%' : '50%',  // Shift right if agent present
                    transform: 'translate(-50%, -50%)',
                    fontSize: '24px',
                    zIndex: 10,
                    animation: car && car.state !== 'IDLE' ? 'carMove 0.8s ease-in-out infinite' : 'none',
                    filter: 'drop-shadow(0 0 8px #f59e0b) drop-shadow(0 0 4px #fbbf24)',
                    transition: 'all 0.3s ease'
                  }}>
                    🚗
                  </div>
                )}
                
                {/* Human Agent - Always show if present */}
                {hasAgent && (
                  <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: hasCar ? '30%' : '50%',  // Shift left if car present
                    transform: 'translate(-50%, -50%)',
                    fontSize: '14px',
                    zIndex: 5,
                    animation: 'pulse 1s infinite',
                    filter: 'drop-shadow(0 0 3px #fff)'
                  }}>
                    👤
                  </div>
                )}
                
                {/* Agent Health Bar */}
                {hasAgent && agent && (
                  <div style={{
                    position: 'absolute',
                    bottom: '2px',
                    left: '2px',
                    right: hasCar ? '50%' : '2px',  // Make room for car indicator
                    height: '3px',
                    background: '#1e293b',
                    borderRadius: '2px',
                    overflow: 'hidden',
                    zIndex: 3
                  }}>
                    <div style={{
                      width: `${agent.health}%`,
                      height: '100%',
                      background: agent.health > 70 ? '#10b981' : agent.health > 40 ? '#f59e0b' : '#ef4444',
                      transition: 'width 0.3s'
                    }}></div>
                  </div>
                )}
                
                {/* Car Passenger Indicator */}
                {hasCar && car && car.passengers > 0 && (
                  <div style={{
                    position: 'absolute',
                    top: '2px',
                    right: '2px',
                    background: '#f59e0b',
                    color: 'white',
                    fontSize: '8px',
                    fontWeight: 'bold',
                    padding: '1px 3px',
                    borderRadius: '3px',
                    lineHeight: '1'
                  }}>
                    {car.passengers}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </Card>
      )}

      {/* Selected Grid Details */}
      {selectedGrid && (
        <Card 
          title={`📍 Grid Details: ${selectedGrid.name} (${selectedGrid.id})`}
          actions={
            <button 
              className="btn btn-secondary" 
              onClick={() => setSelectedGrid(null)}
              style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
            >
              Close
            </button>
          }
        >
          <div className="grid-2">
            <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.75rem' }}>
                Grid Information
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Grid ID:</span>
                  <span style={{ color: 'white', fontWeight: 'bold' }}>{selectedGrid.id}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Name:</span>
                  <span style={{ color: 'white' }}>{selectedGrid.name}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Safety Level:</span>
                  <span style={{ 
                    color: selectedGrid.safety_level === 'SAFE' ? '#10b981' : 
                           selectedGrid.safety_level === 'MEDIUM_RISK' ? '#f59e0b' : '#ef4444',
                    fontWeight: 'bold'
                  }}>
                    {selectedGrid.safety_level}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Risk Score:</span>
                  <span style={{ color: 'white' }}>{(selectedGrid.risk_score * 100).toFixed(0)}%</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Population:</span>
                  <span style={{ color: 'white' }}>{selectedGrid.population_density.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Water Level:</span>
                  <span style={{ color: 'white' }}>{selectedGrid.water_level.toFixed(2)}m</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Infrastructure:</span>
                  <span style={{ color: 'white' }}>{selectedGrid.infrastructure_status}</span>
                </div>
              </div>
            </div>

            {pathExplanation && pathExplanation.success && (
              <div style={{ padding: '1rem', background: '#1e293b', borderRadius: '0.5rem' }}>
                <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#10b981', marginBottom: '0.75rem' }}>
                  🛣️ Evacuation Path (A* Algorithm)
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#94a3b8' }}>Path Length:</span>
                    <span style={{ color: 'white', fontWeight: 'bold' }}>{pathExplanation.path_length} steps</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#94a3b8' }}>Average Risk:</span>
                    <span style={{ color: '#f59e0b' }}>{(pathExplanation.explanation.average_risk * 100).toFixed(0)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#94a3b8' }}>Grids Avoided:</span>
                    <span style={{ color: '#ef4444' }}>{pathExplanation.explanation.grids_avoided}</span>
                  </div>
                  <div style={{ marginTop: '0.5rem', padding: '0.75rem', background: '#0f172a', borderRadius: '0.5rem' }}>
                    <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.5rem' }}>
                      Why This Path?
                    </div>
                    <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.75rem', color: '#94a3b8', lineHeight: '1.6' }}>
                      {pathExplanation.explanation.reasons.map((reason, idx) => (
                        <li key={idx}>{reason}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Active Agents */}
      {agents.length > 0 && (
        <Card title={`👥 Active Evacuation Agents (${agents.length} total)`}>
          <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1rem' }}>
              {agents.map((agent) => (
                <div key={agent.id} style={{
                  padding: '1rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  borderLeft: `4px solid ${
                    agent.status === 'SAFE' ? '#10b981' :
                    agent.status === 'EVACUATING' ? '#f59e0b' :
                    agent.status === 'STUCK' ? '#ef4444' : '#64748b'
                  }`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                      {agent.name}
                    </span>
                    <span style={{
                      padding: '0.125rem 0.5rem',
                      background: agent.status === 'SAFE' ? '#065f46' :
                                 agent.status === 'EVACUATING' ? '#78350f' :
                                 agent.status === 'STUCK' ? '#7f1d1d' : '#1e293b',
                      color: agent.status === 'SAFE' ? '#10b981' :
                             agent.status === 'EVACUATING' ? '#f59e0b' :
                             agent.status === 'STUCK' ? '#ef4444' : '#94a3b8',
                      borderRadius: '0.25rem',
                      fontSize: '0.75rem',
                      fontWeight: 'bold'
                    }}>
                      {agent.status}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                    📍 {agent.position.grid_name} ({agent.position.grid_id})
                  </div>
                  <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                    <div>
                      <span style={{ color: '#60a5fa' }}>Health:</span> {agent.health}%
                    </div>
                    <div>
                      <span style={{ color: '#60a5fa' }}>Progress:</span> {agent.progress.toFixed(0)}%
                    </div>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.5rem' }}>
                    👤 {agent.age_group} | 🚶 {agent.steps_taken} steps
                  </div>
                  
                  {/* Show evacuation path if available */}
                  {agent.path && agent.path.length > 0 && (
                    <div style={{ 
                      marginTop: '0.75rem', 
                      paddingTop: '0.75rem', 
                      borderTop: '1px solid #0f172a',
                      fontSize: '0.75rem'
                    }}>
                      <div style={{ color: '#60a5fa', marginBottom: '0.25rem', fontWeight: 'bold' }}>
                        🛣️ Evacuation Path:
                      </div>
                      <div style={{ color: '#94a3b8', lineHeight: '1.4' }}>
                        {agent.path.slice(0, 5).join(' → ')}
                        {agent.path.length > 5 && ` ... (${agent.path.length} total)`}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Evacuation Paths Summary */}
      {paths.length > 0 && (
        <Card title={`🛣️ Evacuation Paths (${paths.length} routes)`}>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            <div style={{ display: 'grid', gap: '1rem' }}>
              {paths.map((path, idx) => (
                <div key={idx} style={{
                  padding: '1rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  borderLeft: '4px solid #3b82f6'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                    <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                      Route {idx + 1}: {path.start_grid} → {path.goal_grid}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                      {path.path_length} steps
                    </span>
                  </div>
                  
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: '1fr 1fr 1fr', 
                    gap: '0.5rem',
                    marginBottom: '0.75rem',
                    fontSize: '0.75rem'
                  }}>
                    <div>
                      <span style={{ color: '#94a3b8' }}>Avg Risk:</span>
                      <span style={{ color: '#f59e0b', marginLeft: '0.25rem', fontWeight: 'bold' }}>
                        {(path.average_risk * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span style={{ color: '#94a3b8' }}>Avoided:</span>
                      <span style={{ color: '#ef4444', marginLeft: '0.25rem', fontWeight: 'bold' }}>
                        {path.grids_avoided}
                      </span>
                    </div>
                    <div>
                      <span style={{ color: '#94a3b8' }}>Agents:</span>
                      <span style={{ color: '#3b82f6', marginLeft: '0.25rem', fontWeight: 'bold' }}>
                        {path.agents_using}
                      </span>
                    </div>
                  </div>
                  
                  <div style={{ 
                    padding: '0.75rem',
                    background: '#0f172a',
                    borderRadius: '0.5rem',
                    fontSize: '0.75rem',
                    color: '#94a3b8',
                    lineHeight: '1.6'
                  }}>
                    <div style={{ color: '#60a5fa', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                      Path Details:
                    </div>
                    {path.path_ids.slice(0, 10).join(' → ')}
                    {path.path_ids.length > 10 && ` ... +${path.path_ids.length - 10} more`}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Car Statistics */}
      {cars.length > 0 && (
        <Card title={`🚗 Rescue Cars (${cars.length} active)`}>
          <div style={{ marginBottom: '1rem' }}>
            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
              <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
                <div className="stat-content">
                  <div className="stat-label">Total Evacuated by Cars</div>
                  <div className="stat-value" style={{ color: '#f59e0b' }}>{carStats.total_evacuated}</div>
                </div>
              </div>
              <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
                <div className="stat-content">
                  <div className="stat-label">Active Missions</div>
                  <div className="stat-value" style={{ color: '#3b82f6' }}>{carStats.active_missions}</div>
                </div>
              </div>
              <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
                <div className="stat-content">
                  <div className="stat-label">Total Trips</div>
                  <div className="stat-value" style={{ color: '#10b981' }}>
                    {cars && cars.length > 0 ? cars.reduce((sum, car) => sum + car.trips_completed, 0) : 0}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
              {cars.map((car) => (
                <div key={car.id} style={{
                  padding: '1rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  borderLeft: `4px solid ${
                    car.state === 'IDLE' ? '#64748b' :
                    car.state === 'LOADING' || car.state === 'UNLOADING' ? '#10b981' :
                    '#f59e0b'
                  }`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                      🚗 {car.name}
                    </span>
                    <span style={{
                      padding: '0.125rem 0.5rem',
                      background: car.state === 'IDLE' ? '#1e293b' :
                                 car.state === 'LOADING' || car.state === 'UNLOADING' ? '#065f46' :
                                 '#78350f',
                      color: car.state === 'IDLE' ? '#94a3b8' :
                             car.state === 'LOADING' || car.state === 'UNLOADING' ? '#10b981' :
                             '#f59e0b',
                      borderRadius: '0.25rem',
                      fontSize: '0.75rem',
                      fontWeight: 'bold'
                    }}>
                      {car.state.replace(/_/g, ' ')}
                    </span>
                  </div>
                  
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.75rem' }}>
                    📍 Current: <span style={{ color: 'white', fontWeight: 'bold' }}>{car.current_grid_id}</span>
                  </div>

                  {car.target_danger_grid && (
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                      🎯 Target: <span style={{ color: '#ef4444' }}>{car.target_danger_grid}</span> → 
                      <span style={{ color: '#10b981' }}> {car.target_safe_grid}</span>
                    </div>
                  )}

                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: '1fr 1fr', 
                    gap: '0.5rem', 
                    fontSize: '0.75rem', 
                    color: '#94a3b8',
                    marginTop: '0.75rem',
                    paddingTop: '0.75rem',
                    borderTop: '1px solid #0f172a'
                  }}>
                    <div>
                      <span style={{ color: '#60a5fa' }}>Passengers:</span> {car.passengers}/{car.capacity}
                    </div>
                    <div>
                      <span style={{ color: '#60a5fa' }}>Trips:</span> {car.trips_completed}
                    </div>
                    <div>
                      <span style={{ color: '#60a5fa' }}>Evacuated:</span> {car.total_evacuated}
                    </div>
                    <div>
                      <span style={{ color: '#60a5fa' }}>Distance:</span> {car.total_distance}
                    </div>
                  </div>

                  {car.state !== 'IDLE' && (
                    <div style={{ marginTop: '0.75rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                        Progress: {car.progress.toFixed(0)}%
                      </div>
                      <div style={{
                        height: '4px',
                        background: '#0f172a',
                        borderRadius: '2px',
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          width: `${car.progress}%`,
                          height: '100%',
                          background: 'linear-gradient(90deg, #f59e0b, #fbbf24)',
                          transition: 'width 0.3s'
                        }}></div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Activity Log - Always Visible */}
      <Card title="📋 Activity Log">
        <div style={{ 
          maxHeight: '300px', 
          overflowY: 'auto',
          background: '#0f172a',
          borderRadius: '0.5rem',
          padding: '1rem',
          minHeight: '150px'
        }}>
          {activityLog.length === 0 ? (
            <div style={{ 
              textAlign: 'center', 
              color: '#64748b', 
              padding: '2rem',
              fontSize: '0.875rem'
            }}>
              No activity yet. Start a simulation to see real-time logs.
            </div>
          ) : (
            activityLog.map((log, idx) => (
              <div key={idx} style={{
                padding: '0.5rem',
                marginBottom: '0.5rem',
                background: '#1e293b',
                borderRadius: '0.25rem',
                borderLeft: `3px solid ${
                  log.type === 'success' ? '#10b981' :
                  log.type === 'warning' ? '#f59e0b' :
                  log.type === 'error' ? '#ef4444' :
                  '#3b82f6'
                }`,
                fontSize: '0.875rem',
                display: 'flex',
                gap: '0.75rem',
                alignItems: 'flex-start'
              }}>
                <span style={{ color: '#64748b', fontSize: '0.75rem', minWidth: '70px' }}>
                  {log.time}
                </span>
                <span style={{ 
                  color: log.type === 'success' ? '#10b981' :
                         log.type === 'warning' ? '#f59e0b' :
                         log.type === 'error' ? '#ef4444' :
                         '#94a3b8',
                  flex: 1
                }}>
                  {log.message}
                </span>
              </div>
            ))
          )}
        </div>
      </Card>

      <style>{`
        @keyframes carMove {
          0%, 100% { transform: translate(-50%, -50%) scale(1); }
          50% { transform: translate(-50%, -50%) scale(1.1); }
        }
      `}</style>
    </div>
  );
};

export default UrbanEvacuation;
