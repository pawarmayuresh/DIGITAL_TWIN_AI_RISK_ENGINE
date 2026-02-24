import { useState, useEffect, useRef } from 'react';
import { MapPin, AlertTriangle, Volume2, Bell, Activity, Grid3x3 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useWard } from '../context/WardContext';
import Card from '../components/Card';
import AIAgentLogs from '../components/AIAgentLogs';
import { mumbaiAPI } from '../services/api';
import './Pages.css';

const MumbaiMapRealtime = () => {
  const navigate = useNavigate();
  const { selectedWard, selectWard, agentLogs } = useWard();
  const [wards, setWards] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [sensorData, setSensorData] = useState({});
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [backendConnected, setBackendConnected] = useState(false);
  const audioRef = useRef(null);

  // Mumbai ward positions based on actual geography (North to South)
  const wardPositions = {
    'R/N': { x: 200, y: 80, name: 'Borivali', displayName: 'BORIVALI' },
    'P/N': { x: 220, y: 160, name: 'Malad West', displayName: 'MALAD' },
    'K/E': { x: 280, y: 240, name: 'Andheri East', displayName: 'ANDHERI' },
    'H/E': { x: 300, y: 320, name: 'Bandra East', displayName: 'BANDRA' },
    'L': { x: 380, y: 300, name: 'Kurla', displayName: 'KURLA' },
    'G/N': { x: 320, y: 380, name: 'Mahim', displayName: 'MAHIM' },
    'E': { x: 340, y: 440, name: 'Byculla', displayName: 'BYCULLA' },
    'D': { x: 330, y: 480, name: 'Grant Road', displayName: 'GRANT ROAD' },
    'C': { x: 320, y: 510, name: 'Marine Lines', displayName: 'MARINE LINES' },
    'B': { x: 310, y: 540, name: 'Sandhurst Road', displayName: 'SANDHURST' },
    'A': { x: 300, y: 570, name: 'Colaba', displayName: 'COLABA' },
    'F/S': { x: 360, y: 460, name: 'Parel', displayName: 'PAREL' },
    'M/E': { x: 420, y: 340, name: 'Chembur', displayName: 'CHEMBUR' },
    'T': { x: 400, y: 260, name: 'Ghatkopar', displayName: 'GHATKOPAR' }
  };

  // Key landmarks with actual positions
  const landmarks = [
    { name: 'Borivali', x: 200, y: 80, icon: '🏙️', ward: 'R/N' },
    { name: 'Malad', x: 220, y: 160, icon: '🏘️', ward: 'P/N' },
    { name: 'Andheri', x: 280, y: 240, icon: '🏙️', ward: 'K/E' },
    { name: 'Airport', x: 300, y: 260, icon: '✈️', ward: 'L' },
    { name: 'Bandra', x: 300, y: 320, icon: '🌉', ward: 'H/E' },
    { name: 'Kurla', x: 380, y: 300, icon: '🏙️', ward: 'L' },
    { name: 'Ghatkopar', x: 400, y: 260, icon: '🚇', ward: 'T' },
    { name: 'Chembur', x: 420, y: 340, icon: '🏘️', ward: 'M/E' },
    { name: 'Mahim', x: 320, y: 380, icon: '🏙️', ward: 'G/N' },
    { name: 'Byculla', x: 340, y: 440, icon: '🏙️', ward: 'E' },
    { name: 'JJ Hospital', x: 345, y: 445, icon: '🏥', ward: 'E' },
    { name: 'CST', x: 320, y: 520, icon: '🚉', ward: 'A' },
    { name: 'Gateway', x: 300, y: 580, icon: '🏛️', ward: 'A' },
    { name: 'Colaba', x: 300, y: 570, icon: '📍', ward: 'A' }
  ];

  // Alert thresholds - MANDATORY for buzzer trigger
  const ALERT_THRESHOLDS = {
    SEVERE: { min: 0.8, color: '#ef4444', sound: true, label: 'SEVERE - EVACUATE NOW' },
    HIGH: { min: 0.6, color: '#f97316', sound: true, label: 'HIGH - PREPARE TO EVACUATE' },
    MODERATE: { min: 0.4, color: '#f59e0b', sound: false, label: 'MODERATE - STAY ALERT' },
    LOW: { min: 0.2, color: '#84cc16', sound: false, label: 'LOW - MONITOR' },
    VERY_LOW: { min: 0.0, color: '#10b981', sound: false, label: 'VERY LOW - SAFE' }
  };

  // Get alert level based on risk score
  const getAlertLevel = (riskScore) => {
    if (riskScore >= ALERT_THRESHOLDS.SEVERE.min) return 'SEVERE';
    if (riskScore >= ALERT_THRESHOLDS.HIGH.min) return 'HIGH';
    if (riskScore >= ALERT_THRESHOLDS.MODERATE.min) return 'MODERATE';
    if (riskScore >= ALERT_THRESHOLDS.LOW.min) return 'LOW';
    return 'VERY_LOW';
  };

  useEffect(() => {
    loadMumbaiData();
    const interval = setInterval(updateRealTimeData, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Check for alerts that should trigger sound
    const soundAlerts = alerts.filter(a => a.triggerSound);
    
    if (soundAlerts.length > 0 && audioEnabled) {
      console.log(`🔊 BUZZER TRIGGERED! ${soundAlerts.length} alerts require sound`);
      soundAlerts.forEach(alert => {
        console.log(`   🚨 ${alert.severity} (${(alert.riskScore * 100).toFixed(0)}%) - ${alert.wardName} - Threshold: ${(alert.threshold * 100).toFixed(0)}%`);
      });
      playAlertSound();
    }
  }, [alerts, audioEnabled]);

  const loadMumbaiData = async () => {
    try {
      console.log('🔄 Fetching Mumbai data from backend...');
      const wardsResponse = await mumbaiAPI.getWards();
      console.log('✅ Wards data received:', wardsResponse.data);
      
      if (!wardsResponse.data || wardsResponse.data.length === 0) {
        console.warn('⚠️ No ward data received, using mock data');
        loadMockData();
        setBackendConnected(false);
        return;
      }
      
      // Convert array to object keyed by ward_id
      const wardsObj = {};
      wardsResponse.data.forEach(ward => {
        wardsObj[ward.ward_id] = ward;
      });
      
      setWards(wardsObj);
      updateAlerts(wardsResponse.data);
      setBackendConnected(true);
      console.log('✅ Mumbai data loaded successfully from backend');
    } catch (error) {
      console.error('❌ Failed to load Mumbai data from backend:', error);
      console.error('Error details:', error.response || error.message);
      setBackendConnected(false);
      // Load mock data as fallback
      console.log('📦 Loading mock data as fallback...');
      loadMockData();
    }
  };

  const loadMockData = () => {
    // Mock data matching CSV structure with realistic risk scores
    const mockWards = {
      'A': { ward_id: 'A', ward_name: 'Colaba', zone: 'South', population: 185014, area_sqkm: 3.5, slum_population_percent: 12, population_density: 52861, risk_score: 0.35, severity_level: 'Low' },
      'B': { ward_id: 'B', ward_name: 'Sandhurst Road', zone: 'South', population: 157811, area_sqkm: 2.8, slum_population_percent: 18, population_density: 56361, risk_score: 0.42, severity_level: 'Moderate' },
      'C': { ward_id: 'C', ward_name: 'Marine Lines', zone: 'South', population: 196993, area_sqkm: 3.2, slum_population_percent: 22, population_density: 61560, risk_score: 0.48, severity_level: 'Moderate' },
      'D': { ward_id: 'D', ward_name: 'Grant Road', zone: 'South', population: 174996, area_sqkm: 2.5, slum_population_percent: 28, population_density: 69998, risk_score: 0.55, severity_level: 'Moderate' },
      'E': { ward_id: 'E', ward_name: 'Byculla', zone: 'South', population: 189986, area_sqkm: 3.1, slum_population_percent: 35, population_density: 61286, risk_score: 0.82, severity_level: 'Severe' },
      'H/E': { ward_id: 'H/E', ward_name: 'Bandra East', zone: 'Western', population: 290000, area_sqkm: 8.0, slum_population_percent: 41, population_density: 36250, risk_score: 0.58, severity_level: 'Moderate' },
      'K/E': { ward_id: 'K/E', ward_name: 'Andheri East', zone: 'Western', population: 460000, area_sqkm: 11.0, slum_population_percent: 32, population_density: 41818, risk_score: 0.68, severity_level: 'High' },
      'P/N': { ward_id: 'P/N', ward_name: 'Malad West', zone: 'Western', population: 580000, area_sqkm: 12.0, slum_population_percent: 44, population_density: 48333, risk_score: 0.62, severity_level: 'High' },
      'R/N': { ward_id: 'R/N', ward_name: 'Borivali', zone: 'Western', population: 710000, area_sqkm: 14.5, slum_population_percent: 30, population_density: 48965, risk_score: 0.38, severity_level: 'Low' },
      'L': { ward_id: 'L', ward_name: 'Kurla', zone: 'Central', population: 800000, area_sqkm: 15.0, slum_population_percent: 48, population_density: 53333, risk_score: 0.88, severity_level: 'Severe' },
      'F/S': { ward_id: 'F/S', ward_name: 'Parel', zone: 'South', population: 220000, area_sqkm: 4.2, slum_population_percent: 38, population_density: 52380, risk_score: 0.70, severity_level: 'High' },
      'M/E': { ward_id: 'M/E', ward_name: 'Chembur', zone: 'Eastern', population: 350000, area_sqkm: 7.5, slum_population_percent: 35, population_density: 46666, risk_score: 0.52, severity_level: 'Moderate' },
      'G/N': { ward_id: 'G/N', ward_name: 'Mahim', zone: 'Central', population: 240000, area_sqkm: 5.0, slum_population_percent: 42, population_density: 48000, risk_score: 0.60, severity_level: 'High' },
      'T': { ward_id: 'T', ward_name: 'Ghatkopar', zone: 'Eastern', population: 420000, area_sqkm: 9.0, slum_population_percent: 38, population_density: 46666, risk_score: 0.65, severity_level: 'High' }
    };
    
    setWards(mockWards);
    updateAlerts(Object.values(mockWards));
    
    // Mock sensor data
    setSensorData({
      rain: [
        { sensor_id: 'RS001', ward_id: 'E', rainfall_mm: 65, timestamp: new Date().toISOString() },
        { sensor_id: 'RS002', ward_id: 'K/E', rainfall_mm: 58, timestamp: new Date().toISOString() },
        { sensor_id: 'RS003', ward_id: 'L', rainfall_mm: 82, timestamp: new Date().toISOString() },
        { sensor_id: 'RS004', ward_id: 'T', rainfall_mm: 60, timestamp: new Date().toISOString() }
      ],
      water: [
        { sensor_id: 'WS001', location: 'Sion', river_or_drain: 'Mithi River', water_level_cm: 340, alert_threshold: 300, is_alert: true },
        { sensor_id: 'WS002', location: 'Andheri', river_or_drain: 'Mithi River', water_level_cm: 295, alert_threshold: 300, is_alert: false },
        { sensor_id: 'WS003', location: 'Kurla', river_or_drain: 'Storm Drain', water_level_cm: 210, alert_threshold: 200, is_alert: true },
        { sensor_id: 'WS004', location: 'Ghatkopar', river_or_drain: 'Storm Drain', water_level_cm: 195, alert_threshold: 200, is_alert: false }
      ],
      traffic: [
        { sensor_id: 'TS001', road_id: 'E001', vehicle_count: 1800, avg_speed: 15, congestion_index: 0.88 },
        { sensor_id: 'TS002', road_id: 'E002', vehicle_count: 1200, avg_speed: 35, congestion_index: 0.55 },
        { sensor_id: 'TS003', road_id: 'E003', vehicle_count: 2100, avg_speed: 12, congestion_index: 0.92 },
        { sensor_id: 'TS004', road_id: 'E004', vehicle_count: 1500, avg_speed: 25, congestion_index: 0.68 }
      ]
    });
    
    console.log('📦 Mock data loaded with all Mumbai wards including Ghatkopar');
  };

  const updateRealTimeData = async () => {
    // Always try to fetch data, don't skip based on connection status
    try {
      console.log('🔄 Updating real-time sensor data...');
      const rainData = await mumbaiAPI.getRainSensors();
      const waterData = await mumbaiAPI.getWaterSensors();
      const trafficData = await mumbaiAPI.getTrafficSensors();
      
      setSensorData({
        rain: rainData.data || [],
        water: waterData.data || [],
        traffic: trafficData.data || []
      });

      // Update risk scores and alerts
      const wardsResponse = await mumbaiAPI.getWards();
      const wardsObj = {};
      wardsResponse.data.forEach(ward => {
        wardsObj[ward.ward_id] = ward;
      });
      setWards(wardsObj);
      updateAlerts(wardsResponse.data);
      
      // Mark as connected if we got data successfully
      setBackendConnected(true);
      console.log('✅ Real-time data updated');
    } catch (error) {
      console.error('❌ Failed to update real-time data:', error);
      // Don't set backendConnected to false - keep trying
    }
  };

  const updateAlerts = (wardsData) => {
    const newAlerts = [];
    const timestamp = new Date().toLocaleTimeString();
    
    wardsData.forEach(ward => {
      const riskScore = ward.risk_score || 0;
      const wardName = wardPositions[ward.ward_id]?.name || ward.ward_name || ward.ward_id;
      const alertLevel = getAlertLevel(riskScore);
      const threshold = ALERT_THRESHOLDS[alertLevel];
      
      // Only create alerts for MODERATE and above
      if (riskScore >= ALERT_THRESHOLDS.MODERATE.min) {
        const alert = {
          ward: ward.ward_id,
          wardName: wardName,
          severity: alertLevel,
          riskScore: riskScore,
          threshold: threshold.min,
          triggerSound: threshold.sound,
          message: `${threshold.label} in ${wardName.toUpperCase()}`,
          timestamp: timestamp,
          recommendations: []
        };

        // Add specific recommendations based on severity
        if (alertLevel === 'SEVERE') {
          alert.recommendations = [
            '🚨 EVACUATE low-lying areas IMMEDIATELY',
            '🚫 CLOSE all flood-prone roads',
            '⬆️ MOVE to higher floors (3rd floor or above)',
            '📦 KEEP emergency supplies ready (food, water, medicine)',
            '📱 CALL emergency helpline: 100 / 108',
            '🏥 DEPLOY mobile medical units',
            '💧 DEPLOY 5+ mobile water pumps',
            '🚁 PREPARE helicopter rescue teams'
          ];
        } else if (alertLevel === 'HIGH') {
          alert.recommendations = [
            '⚠️ PREPARE for possible evacuation',
            '📺 MONITOR weather updates continuously',
            '🚗 AVOID unnecessary travel',
            '🚑 PRE-POSITION ambulances and rescue teams',
            '📱 ALERT residents via SMS and sirens',
            '🗺️ PREPARE evacuation routes',
            '🏪 STOCK emergency supplies',
            '⚡ CHECK backup power systems'
          ];
        } else if (alertLevel === 'MODERATE') {
          alert.recommendations = [
            '👀 STAY alert to weather conditions',
            '📞 KEEP emergency contacts ready',
            '📻 MONITOR local news and radio',
            '🚨 STANDBY emergency services',
            '🏢 SECURE important documents',
            '💡 CHECK flashlights and batteries'
          ];
        }

        newAlerts.push(alert);
      }
    });

    // Sort by risk score (highest first)
    newAlerts.sort((a, b) => b.riskScore - a.riskScore);
    
    setAlerts(newAlerts);
    
    // Log alert summary
    console.log(`🚨 Alert Summary: ${newAlerts.length} active alerts`);
    newAlerts.forEach(alert => {
      console.log(`   ${alert.severity} (${(alert.riskScore * 100).toFixed(0)}%) - ${alert.wardName} ${alert.triggerSound ? '🔊 SOUND ALERT' : ''}`);
    });
  };

  const playAlertSound = () => {
    if (audioRef.current) {
      audioRef.current.play().catch(e => console.log('Audio play failed:', e));
    }
  };

  const getRiskColor = (riskScore) => {
    if (riskScore > 0.8) return '#ef4444'; // Severe - Red
    if (riskScore > 0.6) return '#f97316'; // High - Orange
    if (riskScore > 0.4) return '#f59e0b'; // Moderate - Yellow
    if (riskScore > 0.2) return '#84cc16'; // Low - Light Green
    return '#10b981'; // Very Low - Green
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Severe': return '#ef4444';
      case 'Critical': return '#dc2626';
      case 'High': return '#f97316';
      case 'Moderate': return '#f59e0b';
      default: return '#10b981';
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>🌆 Mumbai Real-Time Disaster Monitor</h1>
        <p>Live ward monitoring with audio alerts and recommendations</p>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', alignItems: 'center' }}>
          <button 
            className={`btn ${audioEnabled ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setAudioEnabled(!audioEnabled)}
          >
            <Volume2 size={16} style={{ marginRight: '0.5rem' }} />
            {audioEnabled ? 'Audio Alerts ON' : 'Audio Alerts OFF'}
          </button>
          <div style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: alerts.length > 0 ? '#ef4444' : '#10b981',
            borderRadius: '0.5rem',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Bell size={16} />
            {alerts.length} Active Alerts
          </div>
          <div style={{ 
            padding: '0.5rem 1rem', 
            backgroundColor: backendConnected ? '#10b981' : '#f59e0b',
            borderRadius: '0.5rem',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.875rem'
          }}>
            <Activity size={14} />
            {backendConnected ? 'Backend Connected' : 'Using Mock Data'}
          </div>
        </div>
      </div>

      {/* Hidden audio element for alerts */}
      <audio ref={audioRef} src="/alert-sound.mp3" />

      <div className="grid-2">
        {/* Mumbai Map */}
        <Card title="🗺️ Mumbai City Map - Real-Time Risk Monitor">
          <svg width="550" height="650" style={{ backgroundColor: '#0a0e1a', borderRadius: '0.5rem' }}>
            {/* Arabian Sea - Western side */}
            <rect x="0" y="0" width="180" height="650" fill="#1e3a8a" opacity="0.4" />
            <text x="70" y="325" fill="#60a5fa" fontSize="16" fontWeight="bold" transform="rotate(-90 70 325)">
              ARABIAN SEA
            </text>
            
            {/* Sea waves decoration */}
            <path d="M 20 100 Q 40 90 60 100 T 100 100 T 140 100" stroke="#3b82f6" strokeWidth="1" fill="none" opacity="0.5" />
            <path d="M 20 200 Q 40 190 60 200 T 100 200 T 140 200" stroke="#3b82f6" strokeWidth="1" fill="none" opacity="0.5" />
            <path d="M 20 300 Q 40 290 60 300 T 100 300 T 140 300" stroke="#3b82f6" strokeWidth="1" fill="none" opacity="0.5" />
            <path d="M 20 400 Q 40 390 60 400 T 100 400 T 140 400" stroke="#3b82f6" strokeWidth="1" fill="none" opacity="0.5" />
            <path d="M 20 500 Q 40 490 60 500 T 100 500 T 140 500" stroke="#3b82f6" strokeWidth="1" fill="none" opacity="0.5" />

            {/* Mumbai Western Coastline (Borivali to Colaba) */}
            <path
              d="M 180 60 L 185 100 L 190 140 L 195 180 L 200 220 L 210 260 L 220 300 L 235 340 L 250 380 L 265 420 L 275 460 L 280 500 L 285 540 L 288 580 L 290 620"
              stroke="#60a5fa"
              strokeWidth="4"
              fill="none"
            />

            {/* Eastern Coastline (Thane Creek area) */}
            <path
              d="M 450 200 L 445 240 L 440 280 L 435 320 L 430 360 L 425 400"
              stroke="#3b82f6"
              strokeWidth="2"
              fill="none"
              opacity="0.6"
            />
            <text x="455" y="300" fill="#60a5fa" fontSize="10" transform="rotate(-90 455 300)">
              Thane Creek
            </text>

            {/* Mithi River - flows from East to West */}
            <path
              d="M 430 320 Q 400 310 380 305 Q 360 300 340 305 Q 320 310 300 320 Q 280 330 260 345 Q 240 360 220 370"
              stroke="#06b6d4"
              strokeWidth="3"
              fill="none"
              strokeDasharray="6,4"
            />
            <text x="320" y="295" fill="#06b6d4" fontSize="11" fontWeight="bold">Mithi River</text>
            
            {/* Sion location on Mithi River */}
            <circle cx="340" cy="305" r="3" fill="#06b6d4" />
            <text x="345" y="300" fill="#06b6d4" fontSize="9">Sion</text>

            {/* Wards with risk colors */}
            {Object.entries(wards).map(([wardId, ward]) => {
              const pos = wardPositions[wardId];
              if (!pos) return null;
              
              const radius = Math.sqrt(ward.population) / 150;
              const riskColor = getRiskColor(ward.risk_score || 0);
              
              return (
                <g key={wardId}>
                  {/* Ward circle */}
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={radius}
                    fill={riskColor}
                    opacity="0.6"
                    stroke={ward.risk_score > 0.6 ? '#fff' : riskColor}
                    strokeWidth={selectedWard?.ward_id === wardId ? 4 : ward.risk_score > 0.6 ? 3 : 1}
                    style={{ cursor: 'pointer' }}
                    onClick={() => {
                      const wardData = { ...ward, id: wardId, ...pos };
                      selectWard(wardData);
                    }}
                  />
                  
                  {/* Pulsing animation for high risk */}
                  {ward.risk_score > 0.6 && (
                    <circle
                      cx={pos.x}
                      cy={pos.y}
                      r={radius + 5}
                      fill="none"
                      stroke={riskColor}
                      strokeWidth="2"
                      opacity="0.5"
                    >
                      <animate
                        attributeName="r"
                        from={radius}
                        to={radius + 15}
                        dur="2s"
                        repeatCount="indefinite"
                      />
                      <animate
                        attributeName="opacity"
                        from="0.8"
                        to="0"
                        dur="2s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  )}
                  
                  {/* Ward label - PROMINENT DISPLAY */}
                  <text
                    x={pos.x}
                    y={pos.y - radius - 8}
                    fontSize="13"
                    fill="white"
                    textAnchor="middle"
                    fontWeight="bold"
                    style={{ textShadow: '0 0 4px #000' }}
                  >
                    {pos.displayName || pos.name.toUpperCase()}
                  </text>
                  
                  {/* Risk percentage */}
                  <text
                    x={pos.x}
                    y={pos.y + 4}
                    fontSize="11"
                    fill="white"
                    textAnchor="middle"
                    fontWeight="bold"
                  >
                    {((ward.risk_score || 0) * 100).toFixed(0)}%
                  </text>
                </g>
              );
            })}

            {/* Landmarks */}
            {landmarks.map((landmark, idx) => (
              <g key={idx}>
                <text
                  x={landmark.x}
                  y={landmark.y}
                  fontSize="16"
                  textAnchor="middle"
                >
                  {landmark.icon}
                </text>
                <text
                  x={landmark.x}
                  y={landmark.y + 15}
                  fontSize="9"
                  fill="#94a3b8"
                  textAnchor="middle"
                >
                  {landmark.name}
                </text>
              </g>
            ))}

            {/* Legend */}
            <g transform="translate(380, 480)">
              <rect x="-10" y="-10" width="160" height="150" fill="#1e293b" opacity="0.9" rx="8" />
              <text x="0" y="5" fill="white" fontSize="13" fontWeight="bold">Risk Levels</text>
              {[
                { color: '#10b981', label: 'Very Low (0-20%)' },
                { color: '#84cc16', label: 'Low (20-40%)' },
                { color: '#f59e0b', label: 'Moderate (40-60%)' },
                { color: '#f97316', label: 'High (60-80%)' },
                { color: '#ef4444', label: 'Severe (80-100%)' }
              ].map((item, idx) => (
                <g key={idx} transform={`translate(0, ${(idx + 1) * 22})`}>
                  <circle cx="8" cy="0" r="6" fill={item.color} stroke="white" strokeWidth="1" />
                  <text x="20" y="4" fill="white" fontSize="10">{item.label}</text>
                </g>
              ))}
            </g>
            
            {/* Real-time indicator */}
            <g transform="translate(20, 20)">
              <circle cx="8" cy="8" r="6" fill="#10b981">
                <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
              </circle>
              <text x="20" y="12" fill="#10b981" fontSize="12" fontWeight="bold">LIVE</text>
            </g>
            
            {/* Title */}
            <text x="275" y="30" fill="white" fontSize="16" fontWeight="bold" textAnchor="middle">
              Mumbai Disaster Risk Map
            </text>
            <text x="275" y="50" fill="#94a3b8" fontSize="11" textAnchor="middle">
              Real-time monitoring • Updates every 5 seconds
            </text>
          </svg>
        </Card>

        {/* Ward Details & Alerts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <Card title={selectedWard ? `${selectedWard.ward_name || selectedWard.name} Details` : 'Select a Ward'}>
            {selectedWard ? (
              <div>
                <div className="status-list">
                  <div className="status-item">
                    <span className="status-label">Ward ID</span>
                    <span>{selectedWard.id || selectedWard.ward_id}</span>
                  </div>
                  <div className="status-item">
                    <span className="status-label">Zone</span>
                    <span>{selectedWard.zone || 'N/A'}</span>
                  </div>
                  <div className="status-item">
                    <span className="status-label">Population</span>
                    <span>{selectedWard.population?.toLocaleString()}</span>
                  </div>
                  <div className="status-item">
                    <span className="status-label">Area</span>
                    <span>{selectedWard.area_sqkm} km²</span>
                  </div>
                  <div className="status-item">
                    <span className="status-label">Slum Population</span>
                    <span>{selectedWard.slum_population_percent || selectedWard.slum_percent}%</span>
                  </div>
                  <div className="status-item">
                    <span className="status-label">Density</span>
                    <span>{(selectedWard.population_density || selectedWard.density)?.toLocaleString()}/km²</span>
                  </div>
                  <div className="status-item">
                    <span className="status-label">Risk Score</span>
                    <span className="status-badge" style={{
                      backgroundColor: getRiskColor(selectedWard.risk_score || 0),
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '0.5rem',
                      fontWeight: 'bold'
                    }}>
                      {((selectedWard.risk_score || 0) * 100).toFixed(0)}% - {selectedWard.severity_level}
                    </span>
                  </div>
                </div>
                
                <div style={{ 
                  display: 'flex', 
                  gap: '0.5rem', 
                  marginTop: '1rem',
                  paddingTop: '1rem',
                  borderTop: '2px solid #1e293b'
                }}>
                  <button
                    className="btn btn-primary"
                    onClick={() => navigate('/spatial-grid')}
                    style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                  >
                    <Grid3x3 size={16} />
                    View Spatial Grid
                  </button>
                  <button
                    className="btn btn-secondary"
                    onClick={() => navigate('/disaster-simulation')}
                    style={{ flex: 1 }}
                  >
                    Run Simulation
                  </button>
                </div>
              </div>
            ) : (
              <div className="loading">Click on a ward to view details</div>
            )}
          </Card>

          <Card title="🚨 Active Alerts & Recommendations">
            {alerts.length > 0 ? (
              <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                {alerts.map((alert, idx) => (
                  <div key={idx} style={{
                    padding: '1rem',
                    marginBottom: '0.75rem',
                    backgroundColor: ALERT_THRESHOLDS[alert.severity].color + '20',
                    border: `2px solid ${ALERT_THRESHOLDS[alert.severity].color}`,
                    borderRadius: '0.5rem'
                  }}>
                    <div style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: '0.5rem',
                      marginBottom: '0.75rem',
                      flexWrap: 'wrap'
                    }}>
                      <AlertTriangle size={20} color={ALERT_THRESHOLDS[alert.severity].color} />
                      <span style={{ 
                        fontWeight: 'bold', 
                        color: ALERT_THRESHOLDS[alert.severity].color,
                        fontSize: '1rem'
                      }}>
                        {alert.severity}
                      </span>
                      <span style={{ 
                        fontSize: '0.875rem',
                        color: '#94a3b8',
                        marginLeft: 'auto'
                      }}>
                        {alert.timestamp}
                      </span>
                    </div>
                    
                    <div style={{ 
                      fontSize: '0.95rem', 
                      marginBottom: '0.75rem',
                      fontWeight: 'bold',
                      color: 'white'
                    }}>
                      📍 {alert.wardName.toUpperCase()} - Risk: {(alert.riskScore * 100).toFixed(0)}%
                    </div>
                    
                    <div style={{ 
                      fontSize: '0.85rem', 
                      marginBottom: '0.75rem',
                      padding: '0.5rem',
                      backgroundColor: 'rgba(0,0,0,0.3)',
                      borderRadius: '0.25rem'
                    }}>
                      <strong>Alert Threshold:</strong> {(alert.threshold * 100).toFixed(0)}% 
                      {alert.triggerSound && <span style={{ marginLeft: '0.5rem', color: '#fbbf24' }}>🔊 BUZZER ACTIVE</span>}
                    </div>
                    
                    <div style={{ fontSize: '0.85rem', color: '#e2e8f0' }}>
                      <strong style={{ display: 'block', marginBottom: '0.5rem' }}>
                        📋 MANDATORY ACTIONS:
                      </strong>
                      <ul style={{ margin: '0', paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                        {alert.recommendations.map((rec, i) => (
                          <li key={i} style={{ marginBottom: '0.25rem' }}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="loading" style={{ color: '#10b981', padding: '2rem', textAlign: 'center' }}>
                ✓ No active alerts - All areas safe
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* Alert Threshold Information - MANDATORY */}
      <Card title="🔊 Audio Alert Thresholds (Buzzer Trigger Points)">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
          {Object.entries(ALERT_THRESHOLDS).map(([level, config]) => (
            <div key={level} style={{
              padding: '1rem',
              backgroundColor: config.color + '20',
              border: `2px solid ${config.color}`,
              borderRadius: '0.5rem'
            }}>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                marginBottom: '0.5rem'
              }}>
                <div style={{
                  width: '12px',
                  height: '12px',
                  backgroundColor: config.color,
                  borderRadius: '50%'
                }}></div>
                <span style={{ fontWeight: 'bold', color: config.color }}>
                  {level}
                </span>
                {config.sound && <span style={{ marginLeft: 'auto' }}>🔊</span>}
              </div>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                Threshold: ≥ {(config.min * 100).toFixed(0)}%
              </div>
              <div style={{ fontSize: '0.875rem', color: '#e2e8f0' }}>
                {config.label}
              </div>
              {config.sound && (
                <div style={{ 
                  fontSize: '0.75rem', 
                  color: '#fbbf24',
                  marginTop: '0.5rem',
                  fontWeight: 'bold'
                }}>
                  ⚠️ BUZZER TRIGGERS AT THIS LEVEL
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>

      {/* Real-Time Sensor Data */}
      <div className="grid-3">
        <Card title="🌧️ Rain Sensors">
          {sensorData.rain && sensorData.rain.length > 0 ? (
            <div className="status-list">
              {sensorData.rain.map((sensor, idx) => (
                <div key={idx} className="status-item">
                  <span className="status-label">{sensor.ward_id} - {sensor.sensor_id}</span>
                  <span className="status-badge" style={{
                    backgroundColor: sensor.rainfall_mm > 50 ? '#ef4444' : sensor.rainfall_mm > 30 ? '#f59e0b' : '#10b981',
                    color: 'white'
                  }}>
                    {sensor.rainfall_mm} mm
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="loading">Loading rain sensor data...</div>
          )}
        </Card>

        <Card title="💧 Water Level Sensors">
          {sensorData.water && sensorData.water.length > 0 ? (
            <div className="status-list">
              {sensorData.water.map((sensor, idx) => (
                <div key={idx} className="status-item">
                  <span className="status-label">{sensor.location} - {sensor.river_or_drain}</span>
                  <span className="status-badge" style={{
                    backgroundColor: sensor.is_alert ? '#ef4444' : '#10b981',
                    color: 'white'
                  }}>
                    {sensor.water_level_cm} cm {sensor.is_alert ? '⚠️' : '✓'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="loading">Loading water sensors...</div>
          )}
        </Card>

        <Card title="🚗 Traffic Sensors">
          {sensorData.traffic && sensorData.traffic.length > 0 ? (
            <div className="status-list">
              {sensorData.traffic.map((sensor, idx) => (
                <div key={idx} className="status-item">
                  <span className="status-label">{sensor.road_id} - {sensor.vehicle_count} vehicles</span>
                  <span className="status-badge" style={{
                    backgroundColor: sensor.congestion_index > 0.7 ? '#ef4444' : sensor.congestion_index > 0.5 ? '#f59e0b' : '#10b981',
                    color: 'white'
                  }}>
                    {sensor.avg_speed} km/h
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="loading">Loading traffic data...</div>
          )}
        </Card>
      </div>

      {/* System Status */}
      <Card title="📡 System Status">
        <div className="stats-grid">
          <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
            <div className="stat-icon" style={{ color: '#3b82f6' }}>
              <Activity size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Rain Sensors Active</div>
              <div className="stat-value">{sensorData.rain?.length || 0}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#06b6d4' }}>
            <div className="stat-icon" style={{ color: '#06b6d4' }}>
              <Activity size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Water Level Sensors</div>
              <div className="stat-value">{sensorData.water?.length || 0}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
            <div className="stat-icon" style={{ color: '#f59e0b' }}>
              <Activity size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">Traffic Sensors</div>
              <div className="stat-value">{sensorData.traffic?.length || 0}</div>
            </div>
          </div>
          <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
            <div className="stat-icon" style={{ color: '#10b981' }}>
              <Bell size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-label">System Status</div>
              <div className="stat-value">Online</div>
            </div>
          </div>
        </div>
      </Card>

      {/* AI Agent Reasoning Logs */}
      {agentLogs.length > 0 && (
        <Card title="🤖 AI Agent System - Real-Time Reasoning">
          <AIAgentLogs />
        </Card>
      )}
    </div>
  );
};

export default MumbaiMapRealtime;
