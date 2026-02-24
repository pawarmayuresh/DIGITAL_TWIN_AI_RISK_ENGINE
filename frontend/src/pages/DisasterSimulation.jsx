import { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, AlertTriangle, Flame, Droplets, Biohazard, Brain, TrendingUp, Zap } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import AIAgentLogs from '../components/AIAgentLogs';
import { IntelligentDisasterSimulator } from '../services/aiEngine';
import './Pages.css';

const DisasterSimulation = () => {
  const { selectedWard, selectWard, agentLogs } = useWard();
  const [selectedDisaster, setSelectedDisaster] = useState('flood');
  const [severity, setSeverity] = useState(7);
  const [running, setRunning] = useState(false);
  const [paused, setPaused] = useState(false);
  const [progress, setProgress] = useState(0);
  const [simulationTime, setSimulationTime] = useState(0);
  const [grid, setGrid] = useState([]);
  const [stats, setStats] = useState({
    affectedCells: 0,
    casualties: 0,
    economicLoss: 0,
    evacuated: 0,
    infrastructureDamaged: 0
  });
  const [simLogs, setSimLogs] = useState([]);
  const [aiDecisions, setAiDecisions] = useState([]);
  const [evacuationPaths, setEvacuationPaths] = useState([]);
  const [resourceAllocation, setResourceAllocation] = useState(null);
  const [explainabilityLog, setExplainabilityLog] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const intervalRef = useRef(null);
  const simulatorRef = useRef(null);

  const disasters = [
    { id: 'flood', name: 'Flood', icon: Droplets, color: '#3b82f6', emoji: '🌊' },
    { id: 'fire', name: 'Fire', icon: Flame, color: '#ef4444', emoji: '🔥' },
    { id: 'contamination', name: 'Contamination', icon: Biohazard, color: '#f59e0b', emoji: '☣️' }
  ];

  const wards = [
    { id: 'A', name: 'Colaba', population: 185014 },
    { id: 'E', name: 'Byculla', population: 189986 },
    { id: 'L', name: 'Kurla', population: 800000 },
    { id: 'K/E', name: 'Andheri East', population: 460000 },
    { id: 'H/E', name: 'Bandra East', population: 290000 },
    { id: 'M/E', name: 'Chembur', population: 350000 },
    { id: 'T', name: 'Ghatkopar', population: 420000 },
    { id: 'R/N', name: 'Borivali', population: 710000 }
  ];

  // Initialize 20x20 grid
  useEffect(() => {
    initializeGrid();
  }, [selectedWard, selectedDisaster, severity]);

  const initializeGrid = () => {
    const newGrid = [];
    for (let y = 0; y < 20; y++) {
      const row = [];
      for (let x = 0; x < 20; x++) {
        const elevation = 5 + Math.random() * 45; // 5-50m
        const isLowLying = elevation < 15;
        const nearRiver = y > 8 && y < 12; // Middle rows = Mithi River
        
        row.push({
          x,
          y,
          elevation,
          population: Math.floor(Math.random() * 800) + 100,
          infrastructure: Math.random() > 0.92 ? 
            ['hospital', 'school', 'power', 'water'][Math.floor(Math.random() * 4)] : null,
          floodLevel: (isLowLying || nearRiver) ? Math.random() * 0.2 : 0,
          fireIntensity: 0,
          contamination: 0,
          evacuated: false,
          damaged: false,
          onEvacuationPath: false
        });
      }
      newGrid.push(row);
    }
    
    // Add initial disaster hotspots based on severity
    const numHotspots = Math.ceil(severity / 2); // 1-5 hotspots based on severity
    for (let i = 0; i < numHotspots; i++) {
      const x = Math.floor(Math.random() * 20);
      const y = Math.floor(Math.random() * 20);
      
      if (selectedDisaster === 'flood') {
        newGrid[y][x].floodLevel = 0.5 + (severity / 10) * 0.5; // 0.5-1.0 based on severity
      } else if (selectedDisaster === 'fire') {
        newGrid[y][x].fireIntensity = 0.5 + (severity / 10) * 0.5;
      } else {
        newGrid[y][x].contamination = 0.5 + (severity / 10) * 0.5;
      }
    }
    
    setGrid(newGrid);
    addLog('GRID_INIT', `✅ Initialized 20x20 grid with ${numHotspots} disaster hotspots (severity ${severity}/10)`, 'info');
  };

  const runSimulation = () => {
    if (!selectedWard) {
      alert('Please select a ward first from Mumbai Live page');
      return;
    }

    setRunning(true);
    setPaused(false);
    setProgress(0);
    setSimulationTime(0);
    setStats({
      affectedCells: 0,
      casualties: 0,
      economicLoss: 0,
      evacuated: 0,
      infrastructureDamaged: 0
    });
    setSimLogs([]);
    setAiDecisions([]);
    setEvacuationPaths([]);
    setExplainabilityLog([]);

    addLog('AI_INIT', '🤖 Initializing Intelligent Disaster Simulator...', 'info');
    addLog('WARD', `Selected: ${selectedWard.ward_name} (Population: ${selectedWard.population?.toLocaleString()})`, 'info');
    addLog('DISASTER', `Type: ${disasters.find(d => d.id === selectedDisaster)?.name}, Severity: ${severity}/10`, 'warning');
    addLog('AI_ALGORITHMS', '🧠 Loading: A* Search, CSP Resource Allocation, Explainable AI', 'info');

    // Reinitialize grid with disaster hotspots
    initializeGrid();
    
    addLog('AI_READY', '✅ AI Engine Ready - Starting intelligent simulation', 'success');

    // Start simulation loop
    intervalRef.current = setInterval(() => {
      updateSimulation();
    }, 800); // Update every 800ms for better visualization
  };

  const updateSimulation = () => {
    setProgress(prev => {
      const newProgress = prev + 2;
      if (newProgress >= 100) {
        stopSimulation();
        return 100;
      }
      return newProgress;
    });

    setSimulationTime(prev => prev + 5); // 5 minutes per tick

    // Update grid with disaster spread
    setGrid(prevGrid => {
      // Create clean copy without circular references
      const newGrid = prevGrid.map(row => 
        row.map(cell => ({
          x: cell.x,
          y: cell.y,
          elevation: cell.elevation,
          population: cell.population,
          infrastructure: cell.infrastructure,
          floodLevel: cell.floodLevel,
          fireIntensity: cell.fireIntensity,
          contamination: cell.contamination,
          evacuated: cell.evacuated,
          damaged: cell.damaged,
          onEvacuationPath: false // Reset path markers
        }))
      );
      
      // Initialize AI simulator with current grid if not exists
      if (!simulatorRef.current) {
        simulatorRef.current = new IntelligentDisasterSimulator(
          newGrid,
          selectedWard,
          selectedDisaster,
          severity
        );
      } else {
        // Update simulator's grid reference
        simulatorRef.current.grid = newGrid;
      }
      
      // Run AI simulation step
      const aiResults = simulatorRef.current.simulateStep();
      
      // Update AI decisions
      if (aiResults.decisions.length > 0) {
        setAiDecisions(prev => [...prev, ...aiResults.decisions].slice(-10));
        addLog('AI_DECISION', `🧠 Made ${aiResults.decisions.length} intelligent decisions`, 'info');
        
        // Broadcast to XAI page
        window.dispatchEvent(new CustomEvent('simulationDecisions', {
          detail: { decisions: aiResults.decisions }
        }));
      }

      // Update evacuation paths and mark on grid
      if (aiResults.evacuationPaths && aiResults.evacuationPaths.length > 0) {
        setEvacuationPaths(prev => [...prev, ...aiResults.evacuationPaths]);
        addLog('EVACUATION', `🚨 Evacuated ${aiResults.evacuationPaths.reduce((sum, p) => sum + p.population, 0)} people using A* pathfinding`, 'warning');
        
        // Mark A* paths on grid with proper coordinates
        aiResults.evacuationPaths.forEach(pathInfo => {
          if (pathInfo.path && Array.isArray(pathInfo.path)) {
            pathInfo.path.forEach(pathCell => {
              if (newGrid[pathCell.y] && newGrid[pathCell.y][pathCell.x]) {
                newGrid[pathCell.y][pathCell.x].onEvacuationPath = true;
              }
            });
          }
        });
        
        console.log(`✅ Marked ${aiResults.evacuationPaths.length} A* evacuation paths on grid`);
      }

      // Update resource allocation
      if (aiResults.resourceAllocation) {
        setResourceAllocation(aiResults.resourceAllocation);
        addLog('RESOURCES', `📦 CSP allocated resources: ${JSON.stringify(aiResults.resourceAllocation.utilization)}`, 'info');
      }

      // Update explainability log
      if (aiResults.decisionLog && aiResults.decisionLog.length > 0) {
        setExplainabilityLog(aiResults.decisionLog.slice(-5));
      }

      // Calculate statistics
      let affected = 0;
      let casualties = 0;
      let loss = 0;
      let evacuated = 0;
      let damaged = 0;

      for (let y = 0; y < 20; y++) {
        for (let x = 0; x < 20; x++) {
          const cell = newGrid[y][x];
          
          // Get disaster level based on type
          let disasterLevel = 0;
          if (selectedDisaster === 'flood') {
            disasterLevel = cell.floodLevel;
          } else if (selectedDisaster === 'fire') {
            disasterLevel = cell.fireIntensity;
          } else {
            disasterLevel = cell.contamination;
          }

          // Calculate impacts ONLY if disaster level is significant
          if (disasterLevel > 0.3) {
            affected++;
            casualties += Math.floor(cell.population * disasterLevel * 0.08);
            loss += cell.population * disasterLevel * 0.6;
          }

          if (cell.evacuated) {
            evacuated += cell.population;
          }

          if (cell.damaged) {
            damaged++;
          }
        }
      }

      setStats({
        affectedCells: affected,
        casualties,
        economicLoss: Math.floor(loss / 10),
        evacuated,
        infrastructureDamaged: damaged
      });

      return newGrid;
    });
  };

  const getNeighbors = (x, y) => {
    return [
      [x-1, y], [x+1, y], [x, y-1], [x, y+1],
      [x-1, y-1], [x+1, y-1], [x-1, y+1], [x+1, y+1]
    ];
  };

  const stopSimulation = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    setRunning(false);
    addLog('SIMULATION', 'Simulation completed', 'success');
    addLog('RESULTS', `Casualties: ${stats.casualties}, Economic Loss: ₹${stats.economicLoss} crore`, 'critical');
  };

  const pauseSimulation = () => {
    setPaused(!paused);
    if (paused) {
      intervalRef.current = setInterval(updateSimulation, 500);
      addLog('SIMULATION', 'Resumed', 'info');
    } else {
      clearInterval(intervalRef.current);
      addLog('SIMULATION', 'Paused', 'warning');
    }
  };

  const resetSimulation = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    setRunning(false);
    setPaused(false);
    setProgress(0);
    setSimulationTime(0);
    initializeGrid();
    setStats({
      affectedCells: 0,
      casualties: 0,
      economicLoss: 0,
      evacuated: 0,
      infrastructureDamaged: 0
    });
    setSimLogs([]);
    addLog('SIMULATION', 'Reset complete', 'info');
  };

  const addLog = (type, message, level) => {
    setSimLogs(prev => [...prev, {
      type,
      message,
      level,
      timestamp: new Date().toLocaleTimeString()
    }]);
  };

  const getCellColor = (cell) => {
    let intensity = 0;
    
    if (selectedDisaster === 'flood') {
      intensity = cell.floodLevel;
    } else if (selectedDisaster === 'fire') {
      intensity = cell.fireIntensity;
    } else {
      intensity = cell.contamination;
    }
    
    if (intensity === 0) return '#1e293b';
    
    if (selectedDisaster === 'flood') {
      return `rgba(59, 130, 246, ${intensity})`;
    } else if (selectedDisaster === 'fire') {
      return `rgba(239, 68, 68, ${intensity})`;
    } else {
      return `rgba(245, 158, 11, ${intensity})`;
    }
  };

  const currentDisaster = disasters.find(d => d.id === selectedDisaster);

  return (
    <div className="page">
      <div className="page-header">
        <h1>🌊 Disaster Simulation</h1>
        <p>Real-time disaster spread simulation with AI analysis</p>
      </div>

      {/* Configuration */}
      <div className="grid-3">
        <Card title="Ward Selection">
          <div className="form-group">
            <label className="form-label">Select Ward</label>
            <select 
              className="form-select"
              value={selectedWard?.ward_id || ''}
              onChange={(e) => {
                const ward = wards.find(w => w.id === e.target.value);
                if (ward) selectWard(ward);
              }}
            >
              <option value="">Choose a ward...</option>
              {wards.map(w => (
                <option key={w.id} value={w.id}>{w.name} ({w.population.toLocaleString()})</option>
              ))}
            </select>
          </div>
        </Card>

        <Card title="Disaster Type">
          <div className="form-group">
            <label className="form-label">Select Disaster</label>
            <select 
              className="form-select"
              value={selectedDisaster}
              onChange={(e) => setSelectedDisaster(e.target.value)}
              disabled={running}
            >
              {disasters.map(d => (
                <option key={d.id} value={d.id}>{d.emoji} {d.name}</option>
              ))}
            </select>
          </div>
        </Card>

        <Card title="Severity">
          <div className="form-group">
            <label className="form-label">Severity: {severity}/10</label>
            <input
              type="range"
              min="1"
              max="10"
              value={severity}
              onChange={(e) => setSeverity(parseInt(e.target.value))}
              disabled={running}
              style={{ width: '100%' }}
            />
          </div>
        </Card>
      </div>

      {/* Controls */}
      <Card title="Simulation Controls">
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            className="btn btn-primary"
            onClick={runSimulation}
            disabled={running || !selectedWard}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Play size={16} />
            Run Simulation
          </button>
          <button
            className="btn btn-secondary"
            onClick={pauseSimulation}
            disabled={!running}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Pause size={16} />
            {paused ? 'Resume' : 'Pause'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={resetSimulation}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <RotateCcw size={16} />
            Reset
          </button>
          
          {running && (
            <div style={{ flex: 1, marginLeft: '2rem' }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                Progress: {progress}% | Time: {Math.floor(simulationTime / 60)}h {simulationTime % 60}m
              </div>
              <div style={{ 
                width: '100%', 
                height: '8px', 
                background: '#1e293b', 
                borderRadius: '4px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${progress}%`,
                  height: '100%',
                  background: currentDisaster?.color,
                  transition: 'width 0.3s ease'
                }}></div>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Visualization */}
      <div className="grid-2">
        <Card title={`${currentDisaster?.emoji} Spatial Grid - Real-Time Spread`}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(20, 1fr)',
            gap: '1px',
            background: '#0f172a',
            padding: '0.5rem',
            borderRadius: '0.5rem',
            maxWidth: '650px',
            margin: '0 auto'
          }}>
            {grid.map((row, y) => row.map((cell, x) => {
              const isOnPath = cell.onEvacuationPath;
              const disasterLevel = selectedDisaster === 'flood' ? cell.floodLevel :
                                   selectedDisaster === 'fire' ? cell.fireIntensity :
                                   cell.contamination;
              return (
                <div
                  key={`${x}-${y}`}
                  onClick={() => setSelectedCell(cell)}
                  style={{
                    aspectRatio: '1',
                    background: isOnPath ? 'rgba(16, 185, 129, 0.9)' : getCellColor(cell),
                    border: selectedCell?.x === cell.x && selectedCell?.y === cell.y ? '2px solid #fff' :
                            cell.infrastructure ? '1px solid #fbbf24' : 
                            isOnPath ? '1px solid #34d399' : 'none',
                    borderRadius: '1px',
                    position: 'relative',
                    cursor: 'pointer',
                    boxShadow: selectedCell?.x === cell.x && selectedCell?.y === cell.y ? '0 0 12px rgba(255, 255, 255, 0.9)' :
                               isOnPath ? '0 0 6px rgba(16, 185, 129, 0.8)' : 'none',
                    transform: selectedCell?.x === cell.x && selectedCell?.y === cell.y ? 'scale(1.15)' : 'scale(1)',
                    transition: 'all 0.2s'
                  }}
                  title={`Click for details`}
                >
                  {cell.evacuated && (
                    <div style={{ 
                      position: 'absolute', 
                      top: '-1px', 
                      right: '-1px', 
                      fontSize: '5px',
                      zIndex: 10
                    }}>
                      🚨
                    </div>
                  )}
                  {isOnPath && !cell.evacuated && (
                    <div style={{ 
                      position: 'absolute', 
                      top: '50%', 
                      left: '50%', 
                      transform: 'translate(-50%, -50%)',
                      fontSize: '8px',
                      fontWeight: 'bold',
                      color: 'white',
                      textShadow: '0 0 3px #000',
                      zIndex: 10
                    }}>
                      →
                    </div>
                  )}
                </div>
              );
            }))}
          </div>
          <div style={{ marginTop: '0.75rem', fontSize: '0.7rem', color: '#94a3b8', textAlign: 'center' }}>
            🟡 Infrastructure | 🚨 Evacuated | 🟢 A* Path
          </div>
        </Card>

        <Card title="Impact Statistics">
          <div className="stats-grid">
            <div className="stat-card" style={{ borderLeftColor: currentDisaster?.color }}>
              <div className="stat-content">
                <div className="stat-label">Affected Cells</div>
                <div className="stat-value">{stats.affectedCells}/400</div>
              </div>
            </div>
            <div className="stat-card" style={{ borderLeftColor: '#ef4444' }}>
              <div className="stat-content">
                <div className="stat-label">Casualties</div>
                <div className="stat-value">{stats.casualties.toLocaleString()}</div>
              </div>
            </div>
            <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
              <div className="stat-content">
                <div className="stat-label">Economic Loss</div>
                <div className="stat-value">₹{stats.economicLoss} Cr</div>
              </div>
            </div>
            <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
              <div className="stat-content">
                <div className="stat-label">Evacuated</div>
                <div className="stat-value">{stats.evacuated.toLocaleString()}</div>
              </div>
            </div>
            <div className="stat-card" style={{ borderLeftColor: '#8b5cf6' }}>
              <div className="stat-content">
                <div className="stat-label">Infrastructure Damaged</div>
                <div className="stat-value">{stats.infrastructureDamaged}</div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Simulation Logs */}
      <Card title="📋 Simulation Logs">
        <div style={{ 
          maxHeight: '300px', 
          overflowY: 'auto',
          background: '#0f172a',
          padding: '1rem',
          borderRadius: '0.5rem',
          fontFamily: 'monospace',
          fontSize: '0.875rem'
        }}>
          {simLogs.map((log, idx) => (
            <div key={idx} style={{ 
              marginBottom: '0.5rem',
              color: log.level === 'critical' ? '#ef4444' : 
                     log.level === 'warning' ? '#f59e0b' :
                     log.level === 'success' ? '#10b981' : '#94a3b8'
            }}>
              [{log.timestamp}] [{log.type}] {log.message}
            </div>
          ))}
        </div>
      </Card>

      {/* AI Decision Making & Explainability - Always show during simulation */}
      {running && (
        <div className="grid-2">
          <Card title="🧠 AI Decisions (Explainable AI)">
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              {aiDecisions.length > 0 ? (
                aiDecisions.map((decision, idx) => (
                  <div key={idx} style={{
                    padding: '1rem',
                    marginBottom: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    borderLeft: `4px solid ${decision.decision === 'EVACUATE' ? '#ef4444' : '#3b82f6'}`
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                      <span style={{ fontWeight: 'bold', color: 'white' }}>
                        Cell {decision.cell}
                      </span>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        background: decision.decision === 'EVACUATE' ? '#ef4444' : '#3b82f6',
                        color: 'white',
                        borderRadius: '0.25rem',
                        fontSize: '0.75rem'
                      }}>
                        {decision.decision} ({decision.confidence})
                      </span>
                    </div>
                    <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                      <strong style={{ color: '#60a5fa' }}>Top Reasons:</strong>
                      <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem' }}>
                        {decision.topReasons.map((reason, ridx) => (
                          <li key={ridx} style={{ marginBottom: '0.25rem' }}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
                  <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🧠</div>
                  <div>Analyzing disaster impact...</div>
                  <div style={{ fontSize: '0.75rem', marginTop: '0.5rem', color: '#64748b' }}>
                    AI decisions will appear as the simulation progresses
                  </div>
                </div>
              )}
            </div>
          </Card>

          <Card title="🚁 Evacuation Paths (A* Search)">
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              {evacuationPaths.length > 0 ? (
                <>
                  <div style={{ 
                    padding: '0.75rem', 
                    marginBottom: '1rem',
                    background: '#065f46', 
                    borderRadius: '0.5rem',
                    textAlign: 'center',
                    color: '#10b981',
                    fontWeight: 'bold',
                    fontSize: '0.875rem'
                  }}>
                    ✅ {evacuationPaths.length} Active Evacuation Route{evacuationPaths.length > 1 ? 's' : ''} | {evacuationPaths.reduce((sum, p) => sum + p.population, 0).toLocaleString()} People Evacuated
                  </div>
                  {evacuationPaths.map((path, idx) => (
                    <div key={idx} style={{
                      padding: '1rem',
                      marginBottom: '0.75rem',
                      background: '#1e293b',
                      borderRadius: '0.5rem',
                      borderLeft: '4px solid #10b981'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span style={{ color: 'white', fontWeight: 'bold' }}>
                          {path.from} → {path.to}
                        </span>
                        <span style={{ 
                          padding: '0.25rem 0.5rem',
                          background: '#10b981',
                          color: 'white',
                          borderRadius: '0.25rem',
                          fontSize: '0.75rem'
                        }}>
                          {path.pathLength} steps
                        </span>
                      </div>
                      <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                        👥 {path.population.toLocaleString()} people evacuated
                      </div>
                    </div>
                  ))}
                </>
              ) : (
                <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
                  <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🚁</div>
                  <div>Monitoring for evacuation needs...</div>
                  <div style={{ fontSize: '0.75rem', marginTop: '0.5rem', color: '#64748b' }}>
                    A* pathfinding will activate when disaster severity reaches critical levels
                  </div>
                </div>
              )}
            </div>
          </Card>
        </div>
      )}

      {/* Resource Allocation (CSP) */}
      {resourceAllocation && (
        <Card title="📦 Resource Allocation (CSP - Constraint Satisfaction)">
          <div className="grid-4">
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: '4px solid #3b82f6'
            }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Water Pumps</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white', marginTop: '0.5rem' }}>
                {resourceAllocation.utilization.pumps}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#60a5fa', marginTop: '0.25rem' }}>
                {resourceAllocation.allocation.pumps.length} locations
              </div>
            </div>
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: '4px solid #ef4444'
            }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Fire Trucks</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white', marginTop: '0.5rem' }}>
                {resourceAllocation.utilization.firetrucks}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#f87171', marginTop: '0.25rem' }}>
                {resourceAllocation.allocation.firetrucks.length} locations
              </div>
            </div>
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: '4px solid #10b981'
            }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Ambulances</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white', marginTop: '0.5rem' }}>
                {resourceAllocation.utilization.ambulances}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#34d399', marginTop: '0.25rem' }}>
                {resourceAllocation.allocation.ambulances.length} locations
              </div>
            </div>
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: '4px solid #f59e0b'
            }}>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Shelters</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white', marginTop: '0.5rem' }}>
                {resourceAllocation.utilization.shelters}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#fbbf24', marginTop: '0.25rem' }}>
                {resourceAllocation.allocation.shelters.length} locations
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* AI Recommendations */}
      {running && stats.affectedCells > 0 && (
        <Card title="🎯 AI Recommendations (Intelligent Decision Support)">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {/* Severity Assessment */}
            <div style={{
              padding: '1rem',
              background: stats.affectedCells > 200 ? '#7f1d1d' : stats.affectedCells > 100 ? '#78350f' : '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: `4px solid ${stats.affectedCells > 200 ? '#ef4444' : stats.affectedCells > 100 ? '#f59e0b' : '#10b981'}`
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <AlertTriangle size={20} color={stats.affectedCells > 200 ? '#ef4444' : stats.affectedCells > 100 ? '#f59e0b' : '#10b981'} />
                <span style={{ fontWeight: 'bold', color: 'white', fontSize: '1rem' }}>
                  Situation: {stats.affectedCells > 200 ? 'CRITICAL' : stats.affectedCells > 100 ? 'SEVERE' : 'MODERATE'}
                </span>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#e2e8f0', margin: 0 }}>
                {stats.affectedCells > 200 
                  ? `Emergency response required immediately. ${stats.affectedCells} cells affected with ${stats.casualties} casualties.`
                  : stats.affectedCells > 100
                  ? `Significant disaster spread detected. ${stats.affectedCells} cells affected. Escalate response.`
                  : `Situation under control. ${stats.affectedCells} cells affected. Continue monitoring.`}
              </p>
            </div>

            {/* Immediate Actions */}
            <div>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Zap size={16} />
                Immediate Actions (Priority 1)
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {stats.evacuated === 0 && stats.affectedCells > 50 && (
                  <div style={{ padding: '0.75rem', background: '#7f1d1d', borderRadius: '0.5rem', borderLeft: '3px solid #ef4444' }}>
                    <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      🚨 URGENT: Begin Evacuation
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#fca5a5' }}>
                      No evacuations detected. AI recommends evacuating high-risk cells immediately using A* optimal routes.
                    </div>
                  </div>
                )}
                {stats.casualties > 100 && (
                  <div style={{ padding: '0.75rem', background: '#7f1d1d', borderRadius: '0.5rem', borderLeft: '3px solid #ef4444' }}>
                    <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      🏥 URGENT: Deploy Medical Teams
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#fca5a5' }}>
                      {stats.casualties} casualties reported. Deploy all available ambulances to affected areas.
                    </div>
                  </div>
                )}
                {stats.infrastructureDamaged > 0 && (
                  <div style={{ padding: '0.75rem', background: '#78350f', borderRadius: '0.5rem', borderLeft: '3px solid #f59e0b' }}>
                    <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      ⚡ CRITICAL: Protect Infrastructure
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#fcd34d' }}>
                      {stats.infrastructureDamaged} critical infrastructure at risk. Prioritize hospitals, power stations, and water supply.
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Strategic Recommendations */}
            <div>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#10b981', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Brain size={16} />
                Strategic Recommendations (AI Analysis)
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', borderLeft: '3px solid #3b82f6' }}>
                  <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                    📊 Resource Optimization
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    CSP analysis shows {resourceAllocation ? 
                      `${Math.round((resourceAllocation.allocation.pumps.length / parseInt(resourceAllocation.utilization.pumps.split('/')[1])) * 100)}% pump utilization` 
                      : 'resource allocation in progress'}. 
                    {stats.affectedCells > 150 ? ' Request additional resources from neighboring wards.' : ' Current allocation is sufficient.'}
                  </div>
                </div>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', borderLeft: '3px solid #10b981' }}>
                  <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                    🛣️ Evacuation Routes
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    A* algorithm identified {evacuationPaths.length} optimal evacuation paths. 
                    {evacuationPaths.length > 0 
                      ? ` Average path length: ${Math.round(evacuationPaths.reduce((sum, p) => sum + p.pathLength, 0) / evacuationPaths.length)} steps.`
                      : ' Continue monitoring for evacuation needs.'}
                  </div>
                </div>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', borderLeft: '3px solid #8b5cf6' }}>
                  <div style={{ fontSize: '0.875rem', color: 'white', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                    💰 Economic Impact Mitigation
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    Estimated loss: ₹{stats.economicLoss} crore. 
                    {stats.economicLoss > 500 
                      ? ' Recommend activating disaster relief fund and insurance claims process.'
                      : ' Economic impact is manageable with current resources.'}
                  </div>
                </div>
              </div>
            </div>

            {/* Long-term Actions */}
            <div>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#f59e0b', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <TrendingUp size={16} />
                Long-term Actions (Prevention)
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                  • Build flood barriers in low-lying areas (cells with elevation &lt; 15m)
                </div>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                  • Improve drainage systems near Mithi River corridor
                </div>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                  • Relocate vulnerable populations from high-risk zones
                </div>
                <div style={{ padding: '0.75rem', background: '#1e293b', borderRadius: '0.5rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                  • Strengthen infrastructure resilience (hospitals, power stations)
                </div>
              </div>
            </div>

            {/* AI Confidence */}
            <div style={{
              padding: '1rem',
              background: '#0f172a',
              borderRadius: '0.5rem',
              border: '2px solid #334155',
              display: 'flex',
              alignItems: 'center',
              gap: '1rem'
            }}>
              <Brain size={24} color="#3b82f6" />
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                  AI Recommendation Confidence
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ flex: 1, height: '8px', background: '#1e293b', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${Math.min(95, 60 + (stats.affectedCells / 400) * 35)}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, #3b82f6, #10b981)',
                      transition: 'width 0.5s ease'
                    }}></div>
                  </div>
                  <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                    {Math.min(95, 60 + Math.round((stats.affectedCells / 400) * 35))}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Cell Information Panel */}
      {selectedCell && (
        <Card 
          title={`📍 Cell Details [${selectedCell.x}, ${selectedCell.y}]`}
          actions={
            <button 
              className="btn btn-secondary" 
              onClick={() => setSelectedCell(null)}
              style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
            >
              Close
            </button>
          }
        >
          <div className="grid-2">
            {/* Basic Info */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #3b82f6'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '0.75rem' }}>
                📊 Cell Information
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Position:</span>
                  <span style={{ color: 'white', fontWeight: 'bold' }}>[{selectedCell.x}, {selectedCell.y}]</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Elevation:</span>
                  <span style={{ color: 'white' }}>{selectedCell.elevation.toFixed(1)}m</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Population:</span>
                  <span style={{ color: 'white' }}>{selectedCell.population.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Infrastructure:</span>
                  <span style={{ color: selectedCell.infrastructure ? '#fbbf24' : '#64748b' }}>
                    {selectedCell.infrastructure || 'None'}
                  </span>
                </div>
              </div>
            </div>

            {/* Disaster Impact */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #ef4444'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#f87171', marginBottom: '0.75rem' }}>
                🌊 Disaster Impact
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#94a3b8' }}>💧 Flood Level:</span>
                    <span style={{ color: '#3b82f6', fontWeight: 'bold' }}>
                      {(selectedCell.floodLevel * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '6px', background: '#0f172a', borderRadius: '3px', overflow: 'hidden' }}>
                    <div style={{ 
                      width: `${selectedCell.floodLevel * 100}%`, 
                      height: '100%', 
                      background: '#3b82f6',
                      transition: 'width 0.3s'
                    }}></div>
                  </div>
                </div>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#94a3b8' }}>🔥 Fire Intensity:</span>
                    <span style={{ color: '#ef4444', fontWeight: 'bold' }}>
                      {(selectedCell.fireIntensity * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '6px', background: '#0f172a', borderRadius: '3px', overflow: 'hidden' }}>
                    <div style={{ 
                      width: `${selectedCell.fireIntensity * 100}%`, 
                      height: '100%', 
                      background: '#ef4444',
                      transition: 'width 0.3s'
                    }}></div>
                  </div>
                </div>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#94a3b8' }}>☣️ Contamination:</span>
                    <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>
                      {(selectedCell.contamination * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '6px', background: '#0f172a', borderRadius: '3px', overflow: 'hidden' }}>
                    <div style={{ 
                      width: `${selectedCell.contamination * 100}%`, 
                      height: '100%', 
                      background: '#f59e0b',
                      transition: 'width 0.3s'
                    }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Status Indicators */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #10b981'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#34d399', marginBottom: '0.75rem' }}>
                🚨 Status
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                <div style={{ 
                  padding: '0.5rem', 
                  background: selectedCell.evacuated ? '#065f46' : '#0f172a',
                  borderRadius: '0.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <span style={{ fontSize: '1.25rem' }}>{selectedCell.evacuated ? '✅' : '⏳'}</span>
                  <span style={{ color: selectedCell.evacuated ? '#10b981' : '#94a3b8' }}>
                    {selectedCell.evacuated ? 'Evacuated' : 'Not Evacuated'}
                  </span>
                </div>
                <div style={{ 
                  padding: '0.5rem', 
                  background: selectedCell.damaged ? '#7f1d1d' : '#0f172a',
                  borderRadius: '0.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <span style={{ fontSize: '1.25rem' }}>{selectedCell.damaged ? '💥' : '✅'}</span>
                  <span style={{ color: selectedCell.damaged ? '#ef4444' : '#94a3b8' }}>
                    {selectedCell.damaged ? 'Infrastructure Damaged' : 'Infrastructure Intact'}
                  </span>
                </div>
                <div style={{ 
                  padding: '0.5rem', 
                  background: selectedCell.onEvacuationPath ? '#065f46' : '#0f172a',
                  borderRadius: '0.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <span style={{ fontSize: '1.25rem' }}>{selectedCell.onEvacuationPath ? '🛣️' : '🚫'}</span>
                  <span style={{ color: selectedCell.onEvacuationPath ? '#10b981' : '#94a3b8' }}>
                    {selectedCell.onEvacuationPath ? 'On A* Evacuation Route' : 'Not on Evacuation Route'}
                  </span>
                </div>
              </div>
            </div>

            {/* Risk Analysis */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #f59e0b'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#fbbf24', marginBottom: '0.75rem' }}>
                ⚠️ AI Risk Analysis
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                {(() => {
                  const maxDisaster = Math.max(selectedCell.floodLevel, selectedCell.fireIntensity, selectedCell.contamination);
                  const riskLevel = maxDisaster > 0.7 ? 'CRITICAL' : maxDisaster > 0.5 ? 'HIGH' : maxDisaster > 0.3 ? 'MODERATE' : 'LOW';
                  const riskColor = maxDisaster > 0.7 ? '#ef4444' : maxDisaster > 0.5 ? '#f59e0b' : maxDisaster > 0.3 ? '#fbbf24' : '#10b981';
                  const estimatedCasualties = Math.floor(selectedCell.population * maxDisaster * 0.08);
                  const economicLoss = Math.floor(selectedCell.population * maxDisaster * 0.6 / 10);
                  
                  return (
                    <>
                      <div style={{ 
                        padding: '0.75rem', 
                        background: maxDisaster > 0.5 ? '#7f1d1d' : '#0f172a',
                        borderRadius: '0.5rem',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                          Risk Level
                        </div>
                        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: riskColor }}>
                          {riskLevel}
                        </div>
                        <div style={{ fontSize: '0.875rem', color: riskColor, marginTop: '0.25rem' }}>
                          {(maxDisaster * 100).toFixed(0)}% Severity
                        </div>
                      </div>
                      {maxDisaster > 0.3 && (
                        <>
                          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', background: '#0f172a', borderRadius: '0.25rem' }}>
                            <span style={{ color: '#94a3b8' }}>Est. Casualties:</span>
                            <span style={{ color: '#ef4444', fontWeight: 'bold' }}>{estimatedCasualties}</span>
                          </div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', background: '#0f172a', borderRadius: '0.25rem' }}>
                            <span style={{ color: '#94a3b8' }}>Economic Loss:</span>
                            <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>₹{economicLoss} Cr</span>
                          </div>
                        </>
                      )}
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: '1.5', padding: '0.5rem', background: '#0f172a', borderRadius: '0.25rem' }}>
                        {maxDisaster > 0.7 && '🚨 URGENT: Immediate evacuation required'}
                        {maxDisaster > 0.5 && maxDisaster <= 0.7 && '⚠️ HIGH: Prepare for evacuation'}
                        {maxDisaster > 0.3 && maxDisaster <= 0.5 && '⚡ MODERATE: Monitor closely'}
                        {maxDisaster <= 0.3 && '✅ LOW: Continue monitoring'}
                      </div>
                      {selectedCell.elevation < 15 && (
                        <div style={{ 
                          padding: '0.5rem', 
                          background: '#78350f', 
                          borderRadius: '0.25rem',
                          fontSize: '0.75rem',
                          color: '#fbbf24'
                        }}>
                          ⚠️ Low elevation - High flood vulnerability
                        </div>
                      )}
                    </>
                  );
                })()}
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* AI Agent Logs */}
      {agentLogs.length > 0 && (
        <Card title="🤖 AI Agent Analysis">
          <AIAgentLogs />
        </Card>
      )}
    </div>
  );
};

export default DisasterSimulation;
