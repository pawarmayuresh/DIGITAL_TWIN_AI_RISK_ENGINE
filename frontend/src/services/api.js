import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health API
export const healthAPI = {
  checkHealth: () => api.get('/api/health/live'),
  getVersion: () => api.get('/api/health/version'),
};

// Demo API
export const demoAPI = {
  runScenario: (scenarioType) => api.get(`/api/demo/run/${scenarioType}`),
  listScenarios: () => api.get('/api/demo/scenarios'),
};

// Twin API
export const twinAPI = {
  getTwinState: (twinId) => api.get(`/api/twin/${twinId}/state`),
  updateTwinState: (twinId, state) => api.put(`/api/twin/${twinId}/state`, state),
  simulateDisaster: (twinId, disasterType, severity) => 
    api.post(`/api/twin/${twinId}/simulate`, { disaster_type: disasterType, severity }),
};

// Strategic AI API
export const strategicAPI = {
  generatePlan: (scenario) => api.post('/api/strategic/plan', scenario),
  comparePolicies: (policies) => api.post('/api/strategic/compare-policies', { policies }),
  optimizeResources: (constraints) => api.post('/api/strategic/optimize-resources', constraints),
};

// Multi-Agent API
export const agentAPI = {
  getAgents: () => api.get('/api/agents'),
  getAgentState: (agentId) => api.get(`/api/agents/${agentId}`),
  formCoalition: (agentIds, objective) => 
    api.post('/api/agents/coalition', { agent_ids: agentIds, objective }),
};

// Learning API
export const learningAPI = {
  trainEpisode: (disasterType, severity) => 
    api.post('/api/learning/train/episode', { disaster_type: disasterType, severity }),
  getTrainingSummary: () => api.get('/api/learning/training/summary'),
  evaluatePolicy: (scenarios) => api.post('/api/learning/evaluate', { test_scenarios: scenarios }),
};

// Explainability API
export const explainabilityAPI = {
  explainDecision: (decisionData) => api.post('/api/explainability/explain', decisionData),
  getExplanation: (decisionId) => api.get(`/api/explainability/explanation/${decisionId}`),
  askWhy: (decisionId, question) => 
    api.post('/api/explainability/why', { decision_id: decisionId, question }),
  getAuditLogs: (limit = 10) => api.get(`/api/explainability/audit/logs?limit=${limit}`),
};

// Analytics API
export const analyticsAPI = {
  getKPIs: () => api.get('/api/analytics/kpis'),
  getResilienceIndex: () => api.get('/api/analytics/resilience-index'),
  getResilienceScore: () => api.get('/api/analytics/resilience'),
  getEconomicLosses: () => api.get('/api/analytics/economic-losses'),
  compareScenarios: (scenarioIds) => 
    api.post('/api/analytics/compare-scenarios', { scenario_ids: scenarioIds }),
};

// Spatial API
export const spatialAPI = {
  getGrid: () => api.get('/api/spatial/grid'),
  updateCell: (x, y, data) => api.put(`/api/spatial/grid/${x}/${y}`, data),
};

// Mumbai API
export const mumbaiAPI = {
  getWards: () => api.get('/api/mumbai/wards'),
  getWard: (wardId) => api.get(`/api/mumbai/ward/${wardId}`),
  getInfrastructure: () => api.get('/api/mumbai/infrastructure'),
  getMithiStatus: () => api.get('/api/mumbai/mithi-river/status'),
  simulateRainfall: (wardId, rainfall) => 
    api.post('/api/mumbai/simulate/rainfall', { ward_id: wardId, rainfall_mm: rainfall }),
  getHistoricalFloods: () => api.get('/api/mumbai/historical/floods'),
  replayFlood: (eventId) => api.post(`/api/mumbai/simulate/historical/${eventId}`),
  getRiskScores: () => api.get('/api/mumbai/risk-scores'),
  getRainSensors: () => api.get('/api/mumbai/sensors/rain'),
  getWaterSensors: () => api.get('/api/mumbai/sensors/water'),
  getTrafficSensors: () => api.get('/api/mumbai/sensors/traffic'),
  getPowerLoad: () => api.get('/api/mumbai/sensors/power'),
  getAlertSensors: () => api.get('/api/mumbai/sensors/alerts'),
  getCycloneHistory: () => api.get('/api/mumbai/historical/cyclones'),
  getDashboardSummary: () => api.get('/api/mumbai/dashboard/summary'),
};

export default api;
