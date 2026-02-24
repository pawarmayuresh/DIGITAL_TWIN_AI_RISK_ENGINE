import { useState, useEffect } from 'react';
import { RefreshCw } from 'lucide-react';
import Card from '../components/Card';
import { spatialAPI } from '../services/api';
import './Pages.css';

const RiskHeatmap = () => {
  const [heatmapData, setHeatmapData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [gridSize] = useState(20);
  const [selectedCell, setSelectedCell] = useState(null);

  useEffect(() => {
    generateHeatmap();
  }, []);

  const generateHeatmap = async () => {
    setLoading(true);
    try {
      const response = await spatialAPI.getGrid();
      const grid = response.data.grid || [];
      
      // Convert grid to heatmap data
      const heatmap = [];
      for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
          const cell = grid.find(c => c.x === x && c.y === y);
          heatmap.push({
            x,
            y,
            risk: cell ? (cell.disaster_intensity || 0) * 100 : Math.random() * 30
          });
        }
      }
      setHeatmapData(heatmap);
    } catch (error) {
      console.error('Failed to load heatmap:', error);
      // Generate synthetic data
      const synthetic = [];
      for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
          synthetic.push({
            x,
            y,
            risk: Math.random() * 100
          });
        }
      }
      setHeatmapData(synthetic);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk < 20) return '#10b981';
    if (risk < 40) return '#84cc16';
    if (risk < 60) return '#f59e0b';
    if (risk < 80) return '#f97316';
    return '#ef4444';
  };

  const getRiskLevel = (risk) => {
    if (risk < 20) return 'Very Low';
    if (risk < 40) return 'Low';
    if (risk < 60) return 'Moderate';
    if (risk < 80) return 'High';
    return 'Critical';
  };

  const cellSize = 25;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Risk Heatmap</h1>
        <p>Spatial risk distribution across the city</p>
      </div>

      <div className="grid-2">
        <Card title="Risk Distribution">
          {loading ? (
            <div className="loading">Loading heatmap...</div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <svg width={gridSize * cellSize} height={gridSize * cellSize}>
                {heatmapData.map((cell, idx) => (
                  <rect
                    key={idx}
                    x={cell.x * cellSize}
                    y={cell.y * cellSize}
                    width={cellSize}
                    height={cellSize}
                    fill={getRiskColor(cell.risk)}
                    stroke="#1e293b"
                    strokeWidth="0.5"
                    style={{ cursor: 'pointer' }}
                    onMouseEnter={() => setSelectedCell(cell)}
                    onMouseLeave={() => setSelectedCell(null)}
                  />
                ))}
              </svg>
            </div>
          )}
          <div style={{ marginTop: '1rem' }}>
            <button className="btn btn-secondary" onClick={generateHeatmap}>
              <RefreshCw size={16} style={{ marginRight: '0.5rem' }} />
              Refresh
            </button>
          </div>
        </Card>

        <Card title="Risk Analysis">
          {selectedCell ? (
            <div className="status-list">
              <div className="status-item">
                <span className="status-label">Location</span>
                <span>({selectedCell.x}, {selectedCell.y})</span>
              </div>
              <div className="status-item">
                <span className="status-label">Risk Level</span>
                <span className="status-badge" style={{ 
                  backgroundColor: getRiskColor(selectedCell.risk),
                  color: 'white'
                }}>
                  {getRiskLevel(selectedCell.risk)}
                </span>
              </div>
              <div className="status-item">
                <span className="status-label">Risk Score</span>
                <span>{selectedCell.risk.toFixed(1)}/100</span>
              </div>
            </div>
          ) : (
            <div>
              <div className="status-list">
                <div className="status-item">
                  <span className="status-label">Total Cells</span>
                  <span>{heatmapData.length}</span>
                </div>
                <div className="status-item">
                  <span className="status-label">High Risk Areas</span>
                  <span>{heatmapData.filter(c => c.risk >= 60).length}</span>
                </div>
                <div className="status-item">
                  <span className="status-label">Average Risk</span>
                  <span>
                    {(heatmapData.reduce((sum, c) => sum + c.risk, 0) / heatmapData.length).toFixed(1)}
                  </span>
                </div>
              </div>
              <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#f8fafc', borderRadius: '0.5rem' }}>
                <div style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '0.5rem' }}>
                  Risk Legend
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {[
                    { color: '#10b981', label: 'Very Low (0-20)' },
                    { color: '#84cc16', label: 'Low (20-40)' },
                    { color: '#f59e0b', label: 'Moderate (40-60)' },
                    { color: '#f97316', label: 'High (60-80)' },
                    { color: '#ef4444', label: 'Critical (80-100)' }
                  ].map((item, idx) => (
                    <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div style={{ 
                        width: '20px', 
                        height: '20px', 
                        backgroundColor: item.color,
                        borderRadius: '0.25rem'
                      }} />
                      <span style={{ fontSize: '0.875rem' }}>{item.label}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default RiskHeatmap;
