import { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Zap, Droplets, Flame, Biohazard } from 'lucide-react';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import AIAgentLogs from '../components/AIAgentLogs';
import { IntelligentDisasterSimulator } from '../services/aiEngine';
import './Pages.css';

const SpatialGrid = () => {
  const { selectedWard, selectWard, agentLogs, setDisasterType: setContextDisasterType } = useWard();
  const [gridSize] = useState(20);
  const [grid, setGrid] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [step, setStep] = useState(0);
  const [disasterType, setDisasterType] = useState('flood');
  const [severity, setSeverity] = useState(7);
  const [selectedCell, setSelectedCell] = useState(null);
  const [fireReport, setFireReport] = useState(null);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [reasoningResult, setReasoningResult] = useState(null);
  const [loadingReasoning, setLoadingReasoning] = useState(false);
  const intervalRef = useRef(null);
  const simulatorRef = useRef(null);

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

  useEffect(() => {
    initializeGrid();
    // Fetch real-time disaster data only once when component mounts or ward changes
    if (selectedWard) {
      fetchRealTimeDisasterData();
    }
  }, [selectedWard]); // Removed disasterType and severity from dependencies

  useEffect(() => {
    // Reinitialize grid when disaster type or severity changes significantly
    if (!isRunning) {
      initializeGrid();
    }
  }, [disasterType, severity]);

  const fetchRealTimeDisasterData = async () => {
    if (!selectedWard) return;
    
    try {
      console.log(`🔄 Fetching real-time ${disasterType} data for ward ${selectedWard.ward_id}...`);
      const response = await fetch(`http://localhost:8001/api/mumbai/spatial/disasters/${selectedWard.ward_id}`);
      const data = await response.json();
      
      console.log(`✅ Real-time ${disasterType} data received:`, data);
      
      // Update grid with real-time disaster probabilities
      if (data.disasters && data.disasters[disasterType]) {
        const disasterData = data.disasters[disasterType];
        console.log(`📊 ${disasterType} probability: ${disasterData.probability}, severity: ${disasterData.severity}`);
        
        // You can use this data to adjust the simulation
        setSeverity(Math.ceil(disasterData.probability * 10));
      }
    } catch (error) {
      console.error(`❌ Failed to fetch real-time ${disasterType} data:`, error);
    }
  };
  
  // Update context when disaster type changes
  useEffect(() => {
    if (setContextDisasterType) {
      setContextDisasterType(disasterType);
    }
  }, [disasterType, setContextDisasterType]);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        updateGrid();
        setStep(s => s + 1);
      }, 800); // Increased from 500ms to 800ms for smoother performance
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
  }, [isRunning, grid, disasterType, severity, selectedWard, step]); // Added dependencies

  const initializeGrid = () => {
    const newGrid = [];
    
    for (let y = 0; y < gridSize; y++) {
      const row = [];
      for (let x = 0; x < gridSize; x++) {
        const elevation = 5 + Math.random() * 45;
        const isLowLying = elevation < 15;
        const nearRiver = y > 8 && y < 12;
        
        row.push({
          x,
          y,
          elevation,
          population: Math.floor(Math.random() * 800) + 100,
          infrastructure: Math.random() > 0.92 ? 
            ['hospital', 'school', 'power', 'water', 'fire_station'][Math.floor(Math.random() * 5)] : null,
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
    
    // Add initial disaster hotspots
    if (selectedWard && selectedWard.risk_score > 0.5) {
      const hotspots = Math.ceil(severity / 2);
      for (let i = 0; i < hotspots; i++) {
        const x = Math.floor(Math.random() * gridSize);
        const y = Math.floor(Math.random() * gridSize);
        
        if (disasterType === 'flood') {
          newGrid[y][x].floodLevel = 0.5 + (severity / 10) * 0.5;
        } else if (disasterType === 'fire') {
          newGrid[y][x].fireIntensity = 0.5 + (severity / 10) * 0.5;
        } else {
          newGrid[y][x].contamination = 0.5 + (severity / 10) * 0.5;
        }
      }
    }
    
    setGrid(newGrid);
    setStep(0);
  };

  const updateGrid = () => {
    setGrid(prevGrid => {
      // Shallow copy for better performance - only copy what changes
      const newGrid = prevGrid.map(row => [...row]);
      
      // Initialize simulator if needed
      if (!simulatorRef.current && selectedWard) {
        simulatorRef.current = new IntelligentDisasterSimulator(
          newGrid,
          selectedWard,
          disasterType,
          severity
        );
      } else if (simulatorRef.current) {
        simulatorRef.current.grid = newGrid;
      }
      
      // Run simulation step
      if (simulatorRef.current) {
        const aiResults = simulatorRef.current.simulateStep();
        
        // Mark A* evacuation paths on grid (only if paths exist)
        if (aiResults.evacuationPaths && aiResults.evacuationPaths.length > 0) {
          aiResults.evacuationPaths.forEach(pathInfo => {
            if (pathInfo.path && Array.isArray(pathInfo.path)) {
              pathInfo.path.forEach(pathCell => {
                if (newGrid[pathCell.y] && newGrid[pathCell.y][pathCell.x]) {
                  newGrid[pathCell.y][pathCell.x] = {
                    ...newGrid[pathCell.y][pathCell.x],
                    onEvacuationPath: true
                  };
                }
              });
            }
          });
        }
      }
      
      return newGrid;
    });
  };

  const analyzeWithAdvancedReasoning = async () => {
    if (!selectedWard || loadingReasoning) return;
    
    setLoadingReasoning(true);
    try {
      // Calculate simulation data from grid
      const simulationData = calculateSimulationData();
      
      const response = await fetch('http://localhost:8001/api/knowledge/advanced/grid-simulation-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ward: selectedWard.ward_name,
          rainfall_mm: disasterType === 'flood' ? severity * 10 : 0,
          water_level_m: simulationData.avgWaterLevel,
          traffic_density: 0.7 + (severity / 20),
          temperature: disasterType === 'fire' ? 35 + severity : 28,
          failed_infrastructure: simulationData.damagedInfra,
          evacuation_progress: simulationData.evacuationProgress,
          simulation_step: step,
          events: simulationData.events
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        setReasoningResult(result);
      }
    } catch (error) {
      console.error('Failed to analyze with advanced reasoning:', error);
    } finally {
      setLoadingReasoning(false);
    }
  };

  // Trigger reasoning analysis separately, less frequently
  useEffect(() => {
    if (isRunning && selectedWard && step > 0 && step % 5 === 0) { // Changed from 3 to 5 steps
      analyzeWithAdvancedReasoning();
    }
  }, [step, isRunning, selectedWard]);

  const calculateSimulationData = () => {
    let totalWaterLevel = 0;
    let waterCells = 0;
    let damagedInfra = 0;
    let evacuatedCells = 0;
    let totalCells = 0;
    const events = [];
    
    grid.forEach(row => {
      row.forEach(cell => {
        totalCells++;
        
        if (disasterType === 'flood' && cell.floodLevel > 0) {
          totalWaterLevel += cell.floodLevel;
          waterCells++;
        }
        
        if (cell.damaged) damagedInfra++;
        if (cell.evacuated) evacuatedCells++;
        
        // Generate events based on cell state
        if (cell.floodLevel > 0.7 && step % 5 === 0) {
          events.push({
            event: 'severe_flooding',
            time: `${Math.floor(step / 2)}:${(step % 2) * 30}`,
            location: `[${cell.x}, ${cell.y}]`
          });
        }
        if (cell.fireIntensity > 0.7 && step % 5 === 0) {
          events.push({
            event: 'fire_outbreak',
            time: `${Math.floor(step / 2)}:${(step % 2) * 30}`,
            location: `[${cell.x}, ${cell.y}]`
          });
        }
      });
    });
    
    return {
      avgWaterLevel: waterCells > 0 ? (totalWaterLevel / waterCells) * 3 : 0,
      damagedInfra,
      evacuationProgress: totalCells > 0 ? evacuatedCells / totalCells : 0,
      events: events.slice(0, 5) // Limit to 5 most recent events
    };
  };

  const getCellColor = (cell) => {
    let intensity = 0;
    
    if (disasterType === 'flood') {
      intensity = cell.floodLevel;
    } else if (disasterType === 'fire') {
      intensity = cell.fireIntensity;
    } else {
      intensity = cell.contamination;
    }
    
    if (intensity === 0) return '#0f172a';
    
    if (disasterType === 'fire') {
      return `rgba(239, 68, 68, ${intensity})`;
    } else if (disasterType === 'flood') {
      return `rgba(59, 130, 246, ${intensity})`;
    } else {
      return `rgba(245, 158, 11, ${intensity})`;
    }
  };

  const getInfraIcon = (type) => {
    const icons = {
      hospital: '🏥',
      school: '🏫',
      power: '⚡',
      water: '💧',
      fire_station: '🚒'
    };
    return icons[type] || '';
  };

  const calculateStats = () => {
    let affected = 0;
    let casualties = 0;
    let evacuated = 0;
    let damaged = 0;
    
    grid.forEach(row => {
      row.forEach(cell => {
        const level = disasterType === 'flood' ? cell.floodLevel :
                     disasterType === 'fire' ? cell.fireIntensity :
                     cell.contamination;
        
        if (level > 0.3) {
          affected++;
          casualties += Math.floor(cell.population * level * 0.05);
        }
        if (cell.evacuated) evacuated += cell.population;
        if (cell.damaged) damaged++;
      });
    });
    
    return { affected, casualties, evacuated, damaged };
  };

  const stats = calculateStats();
  const totalCells = gridSize * gridSize;
  const spreadPercentage = ((stats.affected / totalCells) * 100).toFixed(1);

  const disasterIcons = {
    flood: { icon: Droplets, color: '#3b82f6', emoji: '🌊' },
    fire: { icon: Flame, color: '#ef4444', emoji: '🔥' },
    contamination: { icon: Biohazard, color: '#f59e0b', emoji: '☣️' }
  };

  const currentDisaster = disasterIcons[disasterType];

  const generateFireReport = async () => {
    if (!selectedWard || disasterType !== 'fire') {
      console.warn('⚠️ Fire report can only be generated for fire disaster type');
      return;
    }

    setGeneratingReport(true);
    try {
      console.log(`🔥 Generating fire report for ward ${selectedWard.ward_id}...`);
      
      // Fetch real-time disaster data
      const disasterResponse = await fetch(`http://localhost:8001/api/mumbai/spatial/disasters/${selectedWard.ward_id}`);
      const disasterData = await disasterResponse.json();
      
      // Fetch expert system analysis for fire
      const expertResponse = await fetch(`http://localhost:8001/api/knowledge/expert-system/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ward_id: selectedWard.ward_id,
          disaster_type: 'fire'
        })
      });
      const expertData = await expertResponse.json();
      
      // Calculate fire statistics from grid
      let totalFireCells = 0;
      let maxFireIntensity = 0;
      let affectedPopulation = 0;
      let damagedInfrastructure = [];
      
      grid.forEach(row => {
        row.forEach(cell => {
          if (cell.fireIntensity > 0) {
            totalFireCells++;
            maxFireIntensity = Math.max(maxFireIntensity, cell.fireIntensity);
            affectedPopulation += Math.floor(cell.population * cell.fireIntensity * 0.8);
            
            if (cell.infrastructure && cell.fireIntensity > 0.5) {
              damagedInfrastructure.push({
                type: cell.infrastructure,
                location: `[${cell.x}, ${cell.y}]`,
                intensity: cell.fireIntensity
              });
            }
          }
        });
      });
      
      const report = {
        ward_id: selectedWard.ward_id,
        ward_name: selectedWard.ward_name,
        disaster_type: 'fire',
        timestamp: new Date().toISOString(),
        simulation_step: step,
        fire_statistics: {
          total_affected_cells: totalFireCells,
          total_cells: gridSize * gridSize,
          spread_percentage: ((totalFireCells / (gridSize * gridSize)) * 100).toFixed(1),
          max_fire_intensity: (maxFireIntensity * 100).toFixed(0),
          affected_population: affectedPopulation,
          damaged_infrastructure_count: damagedInfrastructure.length,
          damaged_infrastructure: damagedInfrastructure
        },
        real_time_data: disasterData.disasters?.fire || {},
        expert_analysis: {
          risk_level: expertData.risk_level || 'UNKNOWN',
          rules_fired: expertData.rules_fired || [],
          decisions: expertData.decisions || [],
          total_rules: expertData.total_rules || 0
        },
        recommendations: generateFireRecommendations(maxFireIntensity, totalFireCells, damagedInfrastructure.length)
      };
      
      setFireReport(report);
      console.log('✅ Fire report generated:', report);
      
    } catch (error) {
      console.error('❌ Failed to generate fire report:', error);
      alert('Failed to generate fire report. Please ensure the backend is running.');
    } finally {
      setGeneratingReport(false);
    }
  };

  const generateFireRecommendations = (maxIntensity, affectedCells, damagedInfra) => {
    const recommendations = [];
    
    if (maxIntensity > 0.7) {
      recommendations.push('🚨 CRITICAL: Deploy all available fire brigades immediately');
      recommendations.push('🚁 Request aerial firefighting support');
      recommendations.push('🚑 Evacuate all residents within 500m radius');
      recommendations.push('💧 Establish water supply lines from nearest sources');
    } else if (maxIntensity > 0.5) {
      recommendations.push('⚠️ HIGH RISK: Deploy fire brigades to affected areas');
      recommendations.push('🚨 Alert residents to prepare for evacuation');
      recommendations.push('💧 Ensure adequate water supply for firefighting');
    } else if (maxIntensity > 0.3) {
      recommendations.push('⚡ MODERATE: Monitor fire spread closely');
      recommendations.push('🚒 Position fire brigades at strategic locations');
      recommendations.push('📢 Issue public safety announcements');
    }
    
    if (affectedCells > (gridSize * gridSize * 0.3)) {
      recommendations.push('🌊 Fire spreading rapidly - establish firebreaks');
      recommendations.push('🚧 Close roads in affected areas');
    }
    
    if (damagedInfra > 0) {
      recommendations.push(`🏥 ${damagedInfra} critical infrastructure at risk - prioritize protection`);
      recommendations.push('⚡ Shut down power supply to prevent electrical fires');
    }
    
    recommendations.push('📱 Activate emergency communication systems');
    recommendations.push('🏥 Alert hospitals to prepare for casualties');
    
    return recommendations;
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
        <h1>🗺️ Spatial Grid Simulation</h1>
        <p>Visualize spatial disaster propagation with AI</p>
      </div>

      {/* Ward Selection */}
      <Card title="Configuration">
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div className="form-group" style={{ flex: 1, minWidth: '200px', marginBottom: 0 }}>
            <label className="form-label">Select Ward</label>
            <select 
              className="form-select"
              value={selectedWard?.ward_id || ''}
              onChange={(e) => {
                const ward = wards.find(w => w.ward_id === e.target.value);
                if (ward) selectWard(ward);
              }}
            >
              <option value="">Choose a ward...</option>
              {wards.map(w => (
                <option key={w.ward_id} value={w.ward_id}>
                  {w.ward_name} - {w.severity_level}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group" style={{ flex: 1, minWidth: '200px', marginBottom: 0 }}>
            <label className="form-label">Disaster Type</label>
            <select 
              className="form-select"
              value={disasterType}
              onChange={(e) => {
                setDisasterType(e.target.value);
                setIsRunning(false);
              }}
              disabled={isRunning}
            >
              <option value="flood">🌊 Flood</option>
              <option value="fire">🔥 Fire</option>
              <option value="contamination">☣️ Contamination</option>
            </select>
          </div>

          <div className="form-group" style={{ flex: 1, minWidth: '200px', marginBottom: 0 }}>
            <label className="form-label">Severity: {severity}/10</label>
            <input
              type="range"
              min="1"
              max="10"
              value={severity}
              onChange={(e) => setSeverity(parseInt(e.target.value))}
              disabled={isRunning}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      </Card>

      {/* Statistics */}
      <div className="stats-grid">
        <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
          <div className="stat-icon" style={{ color: '#3b82f6' }}>
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Simulation Step</div>
            <div className="stat-value">{step}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: currentDisaster.color }}>
          <div className="stat-icon" style={{ color: currentDisaster.color }}>
            <currentDisaster.icon size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Affected Cells</div>
            <div className="stat-value">{stats.affected}/{totalCells}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
          <div className="stat-icon" style={{ color: '#f59e0b' }}>
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Spread</div>
            <div className="stat-value">{spreadPercentage}%</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#ef4444' }}>
          <div className="stat-content">
            <div className="stat-label">Casualties</div>
            <div className="stat-value">{stats.casualties.toLocaleString()}</div>
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
            <div className="stat-value">{stats.damaged}</div>
          </div>
        </div>
      </div>

      {/* Fire Report Generation Button */}
      {disasterType === 'fire' && selectedWard && (
        <Card title="🔥 Fire Report Generation">
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
            <button
              className="btn btn-primary"
              onClick={generateFireReport}
              disabled={generatingReport || !selectedWard}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            >
              <Flame size={16} />
              {generatingReport ? 'Generating Report...' : 'Generate Fire Report'}
            </button>
            {fireReport && (
              <div style={{ 
                padding: '0.5rem 1rem', 
                backgroundColor: '#10b981', 
                borderRadius: '0.5rem', 
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                ✓ Report Generated for {fireReport.ward_name}
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Advanced Reasoning Analysis */}
      {reasoningResult && (
        <Card title={`🧠 AI Reasoning Analysis - ${reasoningResult.primary_strategy.toUpperCase()}`}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {/* Strategy Badge */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
              background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
              borderRadius: '0.5rem'
            }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: '#93c5fd', marginBottom: '0.25rem' }}>
                  Current Strategy
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'white' }}>
                  {reasoningResult.primary_strategy.replace('_', ' ').toUpperCase()}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.75rem', color: '#93c5fd', marginBottom: '0.25rem' }}>
                  Next Strategy
                </div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#fbbf24' }}>
                  {reasoningResult.next_strategy.replace('_', ' ').toUpperCase()}
                </div>
              </div>
            </div>

            {/* Primary Conclusion */}
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: '4px solid #3b82f6'
            }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                🎯 Primary Conclusion
              </div>
              <div style={{ fontSize: '1rem', color: 'white', lineHeight: '1.6' }}>
                {reasoningResult.primary_conclusion}
              </div>
            </div>

            {/* Expert System Conclusion */}
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              borderLeft: '4px solid #8b5cf6'
            }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                🤖 Expert System Analysis
              </div>
              <div style={{ fontSize: '1rem', color: 'white', lineHeight: '1.6' }}>
                {reasoningResult.expert_conclusion}
              </div>
            </div>

            {/* Risk Score */}
            <div style={{
              padding: '1rem',
              background: '#1e293b',
              borderRadius: '0.5rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                  Average Risk Score
                </div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: getRiskColor(reasoningResult.average_risk_score) }}>
                  {(reasoningResult.average_risk_score * 100).toFixed(0)}%
                </div>
              </div>
              <div style={{
                padding: '0.5rem 1rem',
                background: getRiskColor(reasoningResult.average_risk_score),
                borderRadius: '0.5rem',
                fontSize: '1rem',
                fontWeight: 'bold',
                color: 'white'
              }}>
                {reasoningResult.average_risk_score > 0.8 ? 'CRITICAL' :
                 reasoningResult.average_risk_score > 0.6 ? 'HIGH' :
                 reasoningResult.average_risk_score > 0.4 ? 'MODERATE' : 'LOW'}
              </div>
            </div>

            {/* Recommendations */}
            {reasoningResult.recommendations && reasoningResult.recommendations.length > 0 && (
              <div style={{
                padding: '1rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                borderLeft: '4px solid #10b981'
              }}>
                <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#10b981', marginBottom: '0.75rem' }}>
                  📋 Recommendations
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {reasoningResult.recommendations.map((rec, idx) => (
                    <div key={idx} style={{
                      padding: '0.75rem',
                      background: '#0f172a',
                      borderRadius: '0.375rem',
                      fontSize: '0.875rem',
                      color: '#e2e8f0',
                      lineHeight: '1.5'
                    }}>
                      {rec}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Reasoning Details */}
            {reasoningResult.reasoning_results && (
              <details style={{
                padding: '1rem',
                background: '#1e293b',
                borderRadius: '0.5rem',
                cursor: 'pointer'
              }}>
                <summary style={{
                  fontSize: '0.875rem',
                  fontWeight: 'bold',
                  color: '#94a3b8',
                  cursor: 'pointer',
                  userSelect: 'none'
                }}>
                  🔍 View Detailed Reasoning Results
                </summary>
                <div style={{
                  marginTop: '1rem',
                  padding: '1rem',
                  background: '#0f172a',
                  borderRadius: '0.375rem',
                  fontSize: '0.75rem',
                  color: '#94a3b8',
                  maxHeight: '300px',
                  overflow: 'auto'
                }}>
                  <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                    {JSON.stringify(reasoningResult.reasoning_results, null, 2)}
                  </pre>
                </div>
              </details>
            )}
          </div>
        </Card>
      )}

      {/* Loading Reasoning Indicator */}
      {loadingReasoning && (
        <div style={{
          padding: '1rem',
          background: '#1e293b',
          borderRadius: '0.5rem',
          textAlign: 'center',
          color: '#94a3b8',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.5rem'
        }}>
          <div className="spinner" style={{
            width: '20px',
            height: '20px',
            border: '3px solid #334155',
            borderTop: '3px solid #3b82f6',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }}></div>
          Analyzing with advanced reasoning...
        </div>
      )}

      {/* Fire Report Display */}
      {fireReport && disasterType === 'fire' && (
        <Card title={`🔥 Fire Disaster Report - ${fireReport.ward_name}`}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* Report Header */}
            <div style={{ 
              padding: '1rem', 
              background: 'linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)',
              borderRadius: '0.5rem',
              border: '2px solid #ef4444'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'white', margin: 0 }}>
                  🔥 FIRE DISASTER ANALYSIS REPORT
                </h3>
                <span style={{ 
                  padding: '0.25rem 0.75rem', 
                  backgroundColor: '#ef4444', 
                  borderRadius: '0.25rem',
                  fontSize: '0.875rem',
                  fontWeight: 'bold'
                }}>
                  {fireReport.expert_analysis.risk_level}
                </span>
              </div>
              <div style={{ fontSize: '0.875rem', color: '#fca5a5' }}>
                <div>Ward: {fireReport.ward_name} ({fireReport.ward_id})</div>
                <div>Generated: {new Date(fireReport.timestamp).toLocaleString()}</div>
                <div>Simulation Step: {fireReport.simulation_step}</div>
              </div>
            </div>

            {/* Fire Statistics */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #ef4444'
            }}>
              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#f87171', marginBottom: '1rem' }}>
                📊 Fire Statistics
              </h4>
              <div className="grid-2" style={{ gap: '1rem' }}>
                <div style={{ 
                  padding: '0.75rem', 
                  background: '#0f172a', 
                  borderRadius: '0.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.25rem'
                }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Affected Cells</span>
                  <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ef4444' }}>
                    {fireReport.fire_statistics.total_affected_cells}
                  </span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                    of {fireReport.fire_statistics.total_cells} total
                  </span>
                </div>
                <div style={{ 
                  padding: '0.75rem', 
                  background: '#0f172a', 
                  borderRadius: '0.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.25rem'
                }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Fire Spread</span>
                  <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#f97316' }}>
                    {fireReport.fire_statistics.spread_percentage}%
                  </span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>of total area</span>
                </div>
                <div style={{ 
                  padding: '0.75rem', 
                  background: '#0f172a', 
                  borderRadius: '0.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.25rem'
                }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Max Fire Intensity</span>
                  <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#dc2626' }}>
                    {fireReport.fire_statistics.max_fire_intensity}%
                  </span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>peak intensity</span>
                </div>
                <div style={{ 
                  padding: '0.75rem', 
                  background: '#0f172a', 
                  borderRadius: '0.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.25rem'
                }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Affected Population</span>
                  <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#fbbf24' }}>
                    {fireReport.fire_statistics.affected_population.toLocaleString()}
                  </span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>people at risk</span>
                </div>
              </div>
            </div>

            {/* Real-Time Data */}
            {fireReport.real_time_data && (
              <div style={{ 
                padding: '1rem', 
                background: '#1e293b', 
                borderRadius: '0.5rem',
                borderLeft: '4px solid #3b82f6'
              }}>
                <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#60a5fa', marginBottom: '1rem' }}>
                  📡 Real-Time Fire Conditions
                </h4>
                <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                  <div style={{ 
                    padding: '0.75rem', 
                    background: '#0f172a', 
                    borderRadius: '0.5rem',
                    flex: 1,
                    minWidth: '150px'
                  }}>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                      Fire Probability
                    </div>
                    <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#ef4444' }}>
                      {(fireReport.real_time_data.probability * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div style={{ 
                    padding: '0.75rem', 
                    background: '#0f172a', 
                    borderRadius: '0.5rem',
                    flex: 1,
                    minWidth: '150px'
                  }}>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                      Severity Level
                    </div>
                    <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#f97316' }}>
                      {fireReport.real_time_data.severity}
                    </div>
                  </div>
                  {fireReport.real_time_data.factors && (
                    <div style={{ 
                      padding: '0.75rem', 
                      background: '#0f172a', 
                      borderRadius: '0.5rem',
                      flex: 1,
                      minWidth: '150px'
                    }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                        Dry Conditions
                      </div>
                      <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: fireReport.real_time_data.factors.dry_conditions ? '#ef4444' : '#10b981' }}>
                        {fireReport.real_time_data.factors.dry_conditions ? 'YES ⚠️' : 'NO ✓'}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Damaged Infrastructure */}
            {fireReport.fire_statistics.damaged_infrastructure.length > 0 && (
              <div style={{ 
                padding: '1rem', 
                background: '#1e293b', 
                borderRadius: '0.5rem',
                borderLeft: '4px solid #fbbf24'
              }}>
                <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#fbbf24', marginBottom: '1rem' }}>
                  🏥 Damaged Infrastructure ({fireReport.fire_statistics.damaged_infrastructure_count})
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {fireReport.fire_statistics.damaged_infrastructure.map((infra, idx) => (
                    <div key={idx} style={{ 
                      padding: '0.75rem', 
                      background: '#0f172a', 
                      borderRadius: '0.5rem',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontSize: '1.25rem' }}>
                          {infra.type === 'hospital' ? '🏥' : 
                           infra.type === 'school' ? '🏫' :
                           infra.type === 'power' ? '⚡' :
                           infra.type === 'water' ? '💧' :
                           infra.type === 'fire_station' ? '🚒' : '🏢'}
                        </span>
                        <div>
                          <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                            {infra.type.replace('_', ' ').toUpperCase()}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                            Location: {infra.location}
                          </div>
                        </div>
                      </div>
                      <div style={{ 
                        padding: '0.25rem 0.75rem', 
                        backgroundColor: infra.intensity > 0.7 ? '#7f1d1d' : '#78350f',
                        borderRadius: '0.25rem',
                        fontSize: '0.75rem',
                        fontWeight: 'bold',
                        color: 'white'
                      }}>
                        {(infra.intensity * 100).toFixed(0)}% Damage
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Expert System Analysis */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #8b5cf6'
            }}>
              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#a78bfa', marginBottom: '1rem' }}>
                🤖 AI Expert System Analysis
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <div style={{ 
                  padding: '0.75rem', 
                  background: '#0f172a', 
                  borderRadius: '0.5rem'
                }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                    Rules Fired: {fireReport.expert_analysis.total_rules}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#e2e8f0', lineHeight: '1.6' }}>
                    {fireReport.expert_analysis.rules_fired.slice(0, 5).map((rule, idx) => (
                      <div key={idx} style={{ marginBottom: '0.25rem' }}>
                        • {rule}
                      </div>
                    ))}
                  </div>
                </div>
                <div style={{ 
                  padding: '0.75rem', 
                  background: '#0f172a', 
                  borderRadius: '0.5rem'
                }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                    AI Decisions:
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#e2e8f0', lineHeight: '1.6' }}>
                    {fireReport.expert_analysis.decisions.slice(0, 5).map((decision, idx) => (
                      <div key={idx} style={{ marginBottom: '0.25rem' }}>
                        • {decision}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #10b981'
            }}>
              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#10b981', marginBottom: '1rem' }}>
                📋 Emergency Response Recommendations
              </h4>
              <div style={{ fontSize: '0.875rem', color: '#e2e8f0', lineHeight: '1.8' }}>
                <ul style={{ margin: 0, paddingLeft: '1.5rem' }}>
                  {fireReport.recommendations.map((rec, idx) => (
                    <li key={idx} style={{ marginBottom: '0.5rem' }}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Grid Visualization */}
      <Card 
        title={`${currentDisaster.emoji} Spatial Grid - Real-Time Spread`}
        actions={
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button 
              className="btn btn-primary" 
              onClick={() => setIsRunning(!isRunning)}
              disabled={!selectedWard}
              style={{ padding: '0.25rem 0.75rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
            >
              {isRunning ? <><Pause size={16} /> Pause</> : <><Play size={16} /> Run</>}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={initializeGrid}
              style={{ padding: '0.25rem 0.75rem' }}
            >
              <RotateCcw size={16} />
            </button>
          </div>
        }
      >
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
          gap: '2px',
          background: '#0f172a',
          padding: '0.75rem',
          borderRadius: '0.5rem',
          maxWidth: '650px',
          margin: '0 auto'
        }}>
          {grid.map((row, y) => 
            row.map((cell, x) => {
              const isOnPath = cell.onEvacuationPath;
              return (
                <div
                  key={`${x}-${y}`}
                  onClick={() => setSelectedCell(cell)}
                  style={{
                    aspectRatio: '1',
                    background: isOnPath ? 'rgba(16, 185, 129, 0.9)' : getCellColor(cell),
                    border: selectedCell?.x === cell.x && selectedCell?.y === cell.y ? '2px solid #fff' : 
                            cell.infrastructure ? '2px solid #fbbf24' : 
                            isOnPath ? '2px solid #10b981' : '1px solid #1e293b',
                    borderRadius: '2px',
                    transition: 'all 0.3s',
                    cursor: 'pointer',
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '10px',
                    boxShadow: selectedCell?.x === cell.x && selectedCell?.y === cell.y ? '0 0 15px rgba(255, 255, 255, 0.8)' :
                               isOnPath ? '0 0 10px rgba(16, 185, 129, 0.8), inset 0 0 10px rgba(16, 185, 129, 0.3)' : 'none',
                    transform: selectedCell?.x === cell.x && selectedCell?.y === cell.y ? 'scale(1.1)' : 'scale(1)'
                  }}
                  title={`Click for details`}
                >
                  {cell.infrastructure && <span style={{ fontSize: '10px', filter: 'drop-shadow(0 0 2px #000)' }}>{getInfraIcon(cell.infrastructure)}</span>}
                  {cell.evacuated && <span style={{ position: 'absolute', top: '1px', right: '1px', fontSize: '8px', filter: 'drop-shadow(0 0 2px #000)' }}>🚨</span>}
                  {isOnPath && (
                    <span style={{ 
                      position: 'absolute', 
                      top: '50%', 
                      left: '50%', 
                      transform: 'translate(-50%, -50%)', 
                      fontSize: '12px', 
                      fontWeight: 'bold',
                      color: 'white',
                      textShadow: '0 0 4px #000, 0 0 8px #10b981',
                      zIndex: 10 
                    }}>
                      →
                    </span>
                  )}
                </div>
              );
            })
          )}
        </div>
        <div style={{ marginTop: '1rem', fontSize: '0.875rem', color: '#94a3b8', textAlign: 'center', display: 'flex', gap: '1.5rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: '20px', height: '20px', background: '#fbbf24', border: '2px solid #fbbf24', borderRadius: '2px' }}></span>
            Infrastructure
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: '20px', height: '20px', background: 'rgba(16, 185, 129, 0.9)', border: '2px solid #10b981', borderRadius: '2px', boxShadow: '0 0 8px rgba(16, 185, 129, 0.6)' }}></span>
            A* Evacuation Path
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '16px' }}>🚨</span>
            Evacuated
          </span>
        </div>
      </Card>

      {/* Cell Information Panel */}
      {selectedCell && (
        <Card 
          title={`📍 Cell Information [${selectedCell.x}, ${selectedCell.y}]`}
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
                📊 Basic Information
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Coordinates:</span>
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
                    {selectedCell.infrastructure ? `${getInfraIcon(selectedCell.infrastructure)} ${selectedCell.infrastructure}` : 'None'}
                  </span>
                </div>
              </div>
            </div>

            {/* Disaster Levels */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #ef4444'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#f87171', marginBottom: '0.75rem' }}>
                🌊 Disaster Levels
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#94a3b8' }}>💧 Flood:</span>
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
                    <span style={{ color: '#94a3b8' }}>🔥 Fire:</span>
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

            {/* Status */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: selectedCell.evacuated ? '4px solid #10b981' : '4px solid #8b5cf6'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#a78bfa', marginBottom: '0.75rem' }}>
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
                    {selectedCell.onEvacuationPath ? 'On A* Evacuation Path' : 'Not on Evacuation Path'}
                  </span>
                </div>
              </div>
            </div>

            {/* Risk Assessment */}
            <div style={{ 
              padding: '1rem', 
              background: '#1e293b', 
              borderRadius: '0.5rem',
              borderLeft: '4px solid #f59e0b'
            }}>
              <h4 style={{ fontSize: '0.875rem', fontWeight: 'bold', color: '#fbbf24', marginBottom: '0.75rem' }}>
                ⚠️ Risk Assessment
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.875rem' }}>
                {(() => {
                  const maxDisaster = Math.max(selectedCell.floodLevel, selectedCell.fireIntensity, selectedCell.contamination);
                  const riskLevel = maxDisaster > 0.7 ? 'CRITICAL' : maxDisaster > 0.5 ? 'HIGH' : maxDisaster > 0.3 ? 'MODERATE' : 'LOW';
                  const riskColor = maxDisaster > 0.7 ? '#ef4444' : maxDisaster > 0.5 ? '#f59e0b' : maxDisaster > 0.3 ? '#fbbf24' : '#10b981';
                  
                  return (
                    <>
                      <div style={{ 
                        padding: '0.75rem', 
                        background: maxDisaster > 0.5 ? '#7f1d1d' : '#0f172a',
                        borderRadius: '0.5rem',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                          Overall Risk Level
                        </div>
                        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: riskColor }}>
                          {riskLevel}
                        </div>
                        <div style={{ fontSize: '0.875rem', color: riskColor, marginTop: '0.25rem' }}>
                          {(maxDisaster * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: '1.5' }}>
                        {maxDisaster > 0.7 && '🚨 Immediate evacuation required. Critical danger level.'}
                        {maxDisaster > 0.5 && maxDisaster <= 0.7 && '⚠️ High risk detected. Prepare for evacuation.'}
                        {maxDisaster > 0.3 && maxDisaster <= 0.5 && '⚡ Moderate risk. Monitor situation closely.'}
                        {maxDisaster <= 0.3 && '✅ Low risk. Continue normal operations.'}
                      </div>
                      {selectedCell.elevation < 15 && (
                        <div style={{ 
                          padding: '0.5rem', 
                          background: '#78350f', 
                          borderRadius: '0.25rem',
                          fontSize: '0.75rem',
                          color: '#fbbf24'
                        }}>
                          ⚠️ Low-lying area - High flood risk
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

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default SpatialGrid;
