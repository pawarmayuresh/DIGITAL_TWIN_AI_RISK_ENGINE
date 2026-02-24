import { useWard } from '../context/WardContext';
import { Activity, CheckCircle, AlertTriangle, XCircle, Loader } from 'lucide-react';

const AIAgentLogs = () => {
  const { agentLogs, isAnalyzing, selectedWard } = useWard();

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processing':
        return <Loader className="animate-spin" size={16} />;
      case 'success':
        return <CheckCircle size={16} />;
      case 'warning':
        return <AlertTriangle size={16} />;
      case 'critical':
        return <XCircle size={16} />;
      default:
        return <Activity size={16} />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processing':
        return '#3b82f6';
      case 'success':
        return '#10b981';
      case 'warning':
        return '#f59e0b';
      case 'critical':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  if (!selectedWard) {
    return (
      <div style={{
        padding: '2rem',
        textAlign: 'center',
        color: '#94a3b8',
        background: '#1e293b',
        borderRadius: '0.5rem',
        border: '2px dashed #334155'
      }}>
        <Activity size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
        <p>Select a ward to see AI agent reasoning</p>
      </div>
    );
  }

  return (
    <div style={{
      background: '#0f172a',
      borderRadius: '0.5rem',
      padding: '1rem',
      maxHeight: '600px',
      overflowY: 'auto'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '1rem',
        paddingBottom: '0.5rem',
        borderBottom: '2px solid #1e293b'
      }}>
        <Activity size={20} color="#3b82f6" />
        <h3 style={{ margin: 0, color: 'white' }}>
          AI Agent System - {selectedWard.ward_name}
        </h3>
        {isAnalyzing && (
          <span style={{
            marginLeft: 'auto',
            padding: '0.25rem 0.75rem',
            background: '#3b82f6',
            color: 'white',
            borderRadius: '1rem',
            fontSize: '0.75rem',
            fontWeight: 'bold'
          }}>
            ANALYZING...
          </span>
        )}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {agentLogs.map((log, idx) => (
          <div
            key={idx}
            style={{
              background: '#1e293b',
              border: `2px solid ${getStatusColor(log.status)}`,
              borderRadius: '0.5rem',
              padding: '0.75rem',
              animation: 'slideIn 0.3s ease-out'
            }}
          >
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              marginBottom: '0.5rem'
            }}>
              <span style={{ color: getStatusColor(log.status) }}>
                {getStatusIcon(log.status)}
              </span>
              <span style={{
                fontWeight: 'bold',
                color: getStatusColor(log.status),
                fontSize: '0.875rem'
              }}>
                {log.agent}
              </span>
              <span style={{
                marginLeft: 'auto',
                fontSize: '0.75rem',
                color: '#64748b'
              }}>
                {log.timestamp}
              </span>
            </div>

            <div style={{
              fontSize: '0.875rem',
              color: '#e2e8f0',
              marginBottom: '0.25rem'
            }}>
              <strong style={{ color: getStatusColor(log.status) }}>
                [{log.action}]
              </strong>{' '}
              {log.message}
            </div>

            {log.data && (
              <div style={{
                marginTop: '0.5rem',
                padding: '0.5rem',
                background: '#0f172a',
                borderRadius: '0.25rem',
                fontSize: '0.75rem',
                color: '#94a3b8',
                fontFamily: 'monospace'
              }}>
                {JSON.stringify(log.data, null, 2)}
              </div>
            )}
          </div>
        ))}
      </div>

      <style>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
      `}</style>
    </div>
  );
};

export default AIAgentLogs;
