import { useState } from 'react';
import { Network, Zap, AlertTriangle } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const InfrastructureGraph = () => {
  const [selectedNode, setSelectedNode] = useState(null);
  
  const nodes = [
    { id: 1, name: 'Power Grid', type: 'power', x: 200, y: 100, health: 85, dependencies: [2, 3] },
    { id: 2, name: 'Water Supply', type: 'water', x: 400, y: 100, health: 90, dependencies: [4] },
    { id: 3, name: 'Hospital', type: 'medical', x: 200, y: 250, health: 95, dependencies: [1, 2] },
    { id: 4, name: 'Data Center', type: 'data', x: 400, y: 250, health: 80, dependencies: [1] },
    { id: 5, name: 'Emergency Services', type: 'emergency', x: 300, y: 400, health: 88, dependencies: [1, 2, 4] },
  ];

  const getNodeColor = (health) => {
    if (health >= 80) return '#10b981';
    if (health >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getTypeIcon = (type) => {
    switch(type) {
      case 'power': return '⚡';
      case 'water': return '💧';
      case 'medical': return '🏥';
      case 'data': return '💻';
      case 'emergency': return '🚨';
      default: return '📍';
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Infrastructure Graph</h1>
        <p>Network dependencies and cascading failures</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card" style={{ borderLeftColor: '#10b981' }}>
          <div className="stat-icon" style={{ color: '#10b981' }}>
            <Network size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Total Nodes</div>
            <div className="stat-value">{nodes.length}</div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#3b82f6' }}>
          <div className="stat-icon" style={{ color: '#3b82f6' }}>
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Avg Health</div>
            <div className="stat-value">
              {(nodes.reduce((sum, n) => sum + n.health, 0) / nodes.length).toFixed(0)}%
            </div>
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#f59e0b' }}>
          <div className="stat-icon" style={{ color: '#f59e0b' }}>
            <AlertTriangle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-label">At Risk</div>
            <div className="stat-value">{nodes.filter(n => n.health < 85).length}</div>
          </div>
        </div>
      </div>

      <div className="grid-2">
        <Card title="Infrastructure Network">
          <svg width="100%" height="500" style={{ background: '#0f172a', borderRadius: '0.5rem' }}>
            {/* Draw connections */}
            {nodes.map(node => 
              node.dependencies.map(depId => {
                const depNode = nodes.find(n => n.id === depId);
                if (!depNode) return null;
                return (
                  <line
                    key={`${node.id}-${depId}`}
                    x1={node.x}
                    y1={node.y}
                    x2={depNode.x}
                    y2={depNode.y}
                    stroke="#334155"
                    strokeWidth="2"
                    strokeDasharray="5,5"
                  />
                );
              })
            )}
            
            {/* Draw nodes */}
            {nodes.map(node => (
              <g key={node.id} onClick={() => setSelectedNode(node)} style={{ cursor: 'pointer' }}>
                <circle
                  cx={node.x}
                  cy={node.y}
                  r="30"
                  fill={getNodeColor(node.health)}
                  opacity="0.2"
                  stroke={getNodeColor(node.health)}
                  strokeWidth="2"
                />
                <circle
                  cx={node.x}
                  cy={node.y}
                  r="20"
                  fill={selectedNode?.id === node.id ? getNodeColor(node.health) : '#1e293b'}
                  stroke={getNodeColor(node.health)}
                  strokeWidth="2"
                />
                <text
                  x={node.x}
                  y={node.y + 5}
                  textAnchor="middle"
                  fill="#fff"
                  fontSize="20"
                >
                  {getTypeIcon(node.type)}
                </text>
                <text
                  x={node.x}
                  y={node.y + 50}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="12"
                >
                  {node.name}
                </text>
              </g>
            ))}
          </svg>
        </Card>

        <Card title="Node Details">
          {selectedNode ? (
            <div className="status-list">
              <div className="status-item">
                <span className="status-label">Name</span>
                <span>{selectedNode.name}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Type</span>
                <span>{selectedNode.type}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Health</span>
                <span className={`status-badge ${
                  selectedNode.health >= 80 ? 'status-good' : 
                  selectedNode.health >= 60 ? 'status-warning' : 'status-critical'
                }`}>
                  {selectedNode.health}%
                </span>
              </div>
              <div className="status-item">
                <span className="status-label">Dependencies</span>
                <span>{selectedNode.dependencies.length}</span>
              </div>
              <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#0f172a', borderRadius: '0.375rem' }}>
                <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                  Depends on:
                </div>
                {selectedNode.dependencies.map(depId => {
                  const dep = nodes.find(n => n.id === depId);
                  return dep ? (
                    <div key={depId} style={{ color: '#cbd5e1', fontSize: '0.875rem' }}>
                      • {dep.name}
                    </div>
                  ) : null;
                })}
              </div>
            </div>
          ) : (
            <div className="loading">Click a node to view details</div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default InfrastructureGraph;
