import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader, Trash2, Globe } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const AIAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('english');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Welcome message
    setMessages([{
      type: 'bot',
      content: "Hello! I'm your AI Disaster Management Assistant. I can help you with risk assessments, evacuation routes, forecasts, and more. How can I assist you today?",
      timestamp: new Date().toLocaleTimeString()
    }]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8001/api/advanced/chatbot/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: input,
          language: language
        })
      });

      const data = await response.json();

      const botMessage = {
        type: 'bot',
        content: data.answer,
        data: data.data,
        suggestions: data.suggestions,
        confidence: data.confidence,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearHistory = () => {
    setMessages([{
      type: 'bot',
      content: "Chat history cleared. How can I help you?",
      timestamp: new Date().toLocaleTimeString()
    }]);
  };

  const handleExampleClick = (example) => {
    setInput(example);
  };

  const examples = [
    "What's the risk in Kurla?",
    "Show evacuation routes from Bandra",
    "Forecast for next 7 days",
    "Generate report for Colaba",
    "What's the current situation in Mumbai?"
  ];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>🤖 AI Assistant</h1>
          <p>Natural language interface for disaster management</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Globe size={20} color="#94a3b8" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{
                padding: '0.5rem',
                background: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '0.375rem',
                color: 'white',
                fontSize: '0.875rem'
              }}
            >
              <option value="english">English</option>
              <option value="hindi">हिंदी (Hindi)</option>
              <option value="marathi">मराठी (Marathi)</option>
            </select>
          </div>
          <button
            className="btn btn-secondary"
            onClick={clearHistory}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Trash2 size={16} />
            Clear
          </button>
        </div>
      </div>

      <div className="grid-2">
        {/* Chat Interface */}
        <Card title="💬 Chat">
          <div style={{ display: 'flex', flexDirection: 'column', height: '600px' }}>
            {/* Messages */}
            <div style={{
              flex: 1,
              overflowY: 'auto',
              padding: '1rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}>
              {messages.map((msg, idx) => (
                <div key={idx} style={{
                  display: 'flex',
                  gap: '0.75rem',
                  alignItems: 'flex-start',
                  flexDirection: msg.type === 'user' ? 'row-reverse' : 'row'
                }}>
                  {/* Avatar */}
                  <div style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '50%',
                    background: msg.type === 'user' ? '#3b82f6' : '#10b981',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    {msg.type === 'user' ? <User size={20} /> : <Bot size={20} />}
                  </div>

                  {/* Message Content */}
                  <div style={{
                    flex: 1,
                    maxWidth: '70%'
                  }}>
                    <div style={{
                      padding: '0.75rem 1rem',
                      background: msg.type === 'user' ? '#1e3a8a' : '#1e293b',
                      borderRadius: '0.75rem',
                      borderTopLeftRadius: msg.type === 'user' ? '0.75rem' : '0.25rem',
                      borderTopRightRadius: msg.type === 'user' ? '0.25rem' : '0.75rem'
                    }}>
                      <div style={{ color: 'white', fontSize: '0.875rem', lineHeight: '1.5' }}>
                        {msg.content}
                      </div>
                      
                      {/* Data Display */}
                      {msg.data && Object.keys(msg.data).length > 0 && (
                        <div style={{
                          marginTop: '0.75rem',
                          padding: '0.75rem',
                          background: '#0f172a',
                          borderRadius: '0.5rem',
                          fontSize: '0.75rem'
                        }}>
                          {/* Risk Score */}
                          {msg.data.risk_score !== undefined && (
                            <div style={{ marginBottom: '0.5rem' }}>
                              <span style={{ color: '#94a3b8' }}>Risk Score: </span>
                              <span style={{ 
                                color: msg.data.risk_score > 0.7 ? '#ef4444' : 
                                       msg.data.risk_score > 0.5 ? '#f59e0b' : '#10b981',
                                fontWeight: 'bold'
                              }}>
                                {(msg.data.risk_score * 100).toFixed(0)}%
                              </span>
                              {msg.data.severity && (
                                <span style={{ 
                                  marginLeft: '0.5rem',
                                  padding: '0.125rem 0.5rem',
                                  borderRadius: '0.25rem',
                                  background: msg.data.risk_score > 0.7 ? '#7f1d1d' : 
                                             msg.data.risk_score > 0.5 ? '#78350f' : '#14532d',
                                  color: msg.data.risk_score > 0.7 ? '#ef4444' : 
                                         msg.data.risk_score > 0.5 ? '#f59e0b' : '#10b981',
                                  fontSize: '0.65rem',
                                  fontWeight: 'bold'
                                }}>
                                  {msg.data.severity}
                                </span>
                              )}
                            </div>
                          )}
                          
                          {/* Safe Zones */}
                          {msg.data.safe_zones && msg.data.safe_zones.length > 0 && (
                            <div>
                              <div style={{ color: '#94a3b8', marginBottom: '0.25rem' }}>Safe Zones:</div>
                              {msg.data.safe_zones.slice(0, 3).map((zone, i) => (
                                <div key={i} style={{ color: '#10b981', fontSize: '0.7rem', marginBottom: '0.125rem' }}>
                                  • {zone.name} - {zone.distance}
                                </div>
                              ))}
                            </div>
                          )}
                          
                          {/* Overall Status */}
                          {msg.data.overall_status && (
                            <div style={{ marginBottom: '0.5rem' }}>
                              <span style={{ color: '#94a3b8' }}>Status: </span>
                              <span style={{ 
                                color: msg.data.overall_status === 'Emergency' ? '#ef4444' :
                                       msg.data.overall_status === 'Warning' ? '#f59e0b' :
                                       msg.data.overall_status === 'Alert' ? '#f59e0b' : '#10b981',
                                fontWeight: 'bold'
                              }}>
                                {msg.data.overall_status}
                              </span>
                            </div>
                          )}
                          
                          {/* Active Incidents */}
                          {msg.data.active_incidents !== undefined && (
                            <div style={{ color: '#94a3b8', fontSize: '0.7rem', marginBottom: '0.25rem' }}>
                              Active Incidents: <span style={{ color: 'white', fontWeight: 'bold' }}>{msg.data.active_incidents}</span>
                            </div>
                          )}
                          
                          {/* Report Info */}
                          {msg.data.report_type && (
                            <div>
                              <div style={{ color: '#94a3b8', marginBottom: '0.25rem' }}>Report Type:</div>
                              <div style={{ color: '#10b981', fontSize: '0.7rem', marginBottom: '0.5rem' }}>
                                {msg.data.report_type}
                              </div>
                              {msg.data.sections && (
                                <div>
                                  <div style={{ color: '#94a3b8', fontSize: '0.65rem', marginBottom: '0.25rem' }}>
                                    Sections: {msg.data.sections.length}
                                  </div>
                                </div>
                              )}
                            </div>
                          )}
                          
                          {/* Emergency Contacts */}
                          {msg.data.emergency_services && msg.data.emergency_services.length > 0 && (
                            <div style={{ marginTop: '0.5rem' }}>
                              <div style={{ color: '#94a3b8', marginBottom: '0.25rem', fontSize: '0.7rem' }}>
                                Emergency Contacts:
                              </div>
                              {msg.data.emergency_services.slice(0, 3).map((contact, i) => (
                                <div key={i} style={{ 
                                  color: '#10b981', 
                                  fontSize: '0.65rem',
                                  marginBottom: '0.125rem',
                                  display: 'flex',
                                  justifyContent: 'space-between'
                                }}>
                                  <span>{contact.service}</span>
                                  <span style={{ fontWeight: 'bold' }}>{contact.number}</span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )}

                      {/* Suggestions */}
                      {msg.suggestions && msg.suggestions.length > 0 && (
                        <div style={{ marginTop: '0.75rem' }}>
                          <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                            Suggestions:
                          </div>
                          {msg.suggestions.map((sug, i) => (
                            <div key={i} style={{
                              fontSize: '0.7rem',
                              color: '#64748b',
                              padding: '0.25rem 0'
                            }}>
                              • {sug}
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Confidence */}
                      {msg.confidence !== undefined && (
                        <div style={{
                          marginTop: '0.5rem',
                          fontSize: '0.65rem',
                          color: '#64748b'
                        }}>
                          Confidence: {(msg.confidence * 100).toFixed(0)}%
                        </div>
                      )}
                    </div>
                    
                    <div style={{
                      fontSize: '0.65rem',
                      color: '#64748b',
                      marginTop: '0.25rem',
                      textAlign: msg.type === 'user' ? 'right' : 'left'
                    }}>
                      {msg.timestamp}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                  <div style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '50%',
                    background: '#10b981',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Loader size={20} className="spin" />
                  </div>
                  <div style={{
                    padding: '0.75rem 1rem',
                    background: '#1e293b',
                    borderRadius: '0.75rem',
                    color: '#94a3b8',
                    fontSize: '0.875rem'
                  }}>
                    Thinking...
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div style={{
              padding: '1rem',
              borderTop: '1px solid #334155',
              display: 'flex',
              gap: '0.75rem'
            }}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask me anything about disaster management..."
                disabled={loading}
                style={{
                  flex: 1,
                  padding: '0.75rem 1rem',
                  background: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '0.5rem',
                  color: 'white',
                  fontSize: '0.875rem'
                }}
              />
              <button
                className="btn btn-primary"
                onClick={handleSend}
                disabled={loading || !input.trim()}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '48px',
                  height: '48px',
                  padding: 0
                }}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </Card>

        {/* Examples & Help */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <Card title="💡 Example Queries">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {examples.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => handleExampleClick(example)}
                  style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    border: '1px solid #334155',
                    borderRadius: '0.5rem',
                    color: '#94a3b8',
                    fontSize: '0.875rem',
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#334155';
                    e.target.style.color = 'white';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = '#1e293b';
                    e.target.style.color = '#94a3b8';
                  }}
                >
                  {example}
                </button>
              ))}
            </div>
          </Card>

          <Card title="❓ Help">
            <div style={{ fontSize: '0.875rem', color: '#94a3b8', lineHeight: '1.6' }}>
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ color: 'white', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                  What I can do:
                </div>
                <ul style={{ paddingLeft: '1.5rem', margin: 0 }}>
                  <li>Check risk levels for any ward</li>
                  <li>Find evacuation routes</li>
                  <li>Provide 7-day forecasts</li>
                  <li>Generate reports</li>
                  <li>Show current status</li>
                </ul>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <div style={{ color: 'white', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                  Tips:
                </div>
                <ul style={{ paddingLeft: '1.5rem', margin: 0 }}>
                  <li>Be specific about ward names</li>
                  <li>Ask one question at a time</li>
                  <li>Use natural language</li>
                  <li>Try different languages</li>
                </ul>
              </div>

              <div style={{
                padding: '0.75rem',
                background: '#0f172a',
                borderRadius: '0.5rem',
                borderLeft: '3px solid #10b981'
              }}>
                <div style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 'bold' }}>
                  Pro Tip
                </div>
                <div style={{ fontSize: '0.75rem', marginTop: '0.25rem' }}>
                  Type "help" anytime to see all available commands
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>

      <style>{`
        .spin {
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default AIAssistant;
