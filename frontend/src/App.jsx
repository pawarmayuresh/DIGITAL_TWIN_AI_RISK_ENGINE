import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { WardProvider } from './context/WardContext';
import Layout from './components/Layout';
import CityOverview from './pages/CityOverview';
import SpatialGrid from './pages/SpatialGrid';
import DisasterSimulation from './pages/DisasterSimulation';
import InfrastructureGraph from './pages/InfrastructureGraph';
import PolicyComparison from './pages/PolicyComparison';
import InfrastructureDashboard from './pages/InfrastructureDashboard';
import ResilienceDashboard from './pages/ResilienceDashboard';
import RiskHeatmap from './pages/RiskHeatmap';
import DecisionExplainer from './pages/DecisionExplainer';
import XAI from './pages/XAI';
import MumbaiMapRealtime from './pages/MumbaiMapRealtime';
import UrbanEvacuation from './pages/UrbanEvacuation';
import KnowledgeEngine from './pages/KnowledgeEngine';

function App() {
  return (
    <WardProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/mumbai-map" replace />} />
            <Route path="mumbai-map" element={<MumbaiMapRealtime />} />
            <Route path="urban-evacuation" element={<UrbanEvacuation />} />
            <Route path="city-overview" element={<CityOverview />} />
            <Route path="spatial-grid" element={<SpatialGrid />} />
            <Route path="disaster-simulation" element={<DisasterSimulation />} />
            <Route path="infrastructure" element={<InfrastructureDashboard />} />
            <Route path="policy-comparison" element={<PolicyComparison />} />
            <Route path="resilience" element={<ResilienceDashboard />} />
            <Route path="risk-heatmap" element={<RiskHeatmap />} />
            <Route path="explainability" element={<DecisionExplainer />} />
            <Route path="xai" element={<XAI />} />
            <Route path="knowledge-engine" element={<KnowledgeEngine />} />
          </Route>
        </Routes>
      </Router>
    </WardProvider>
  );
}

export default App;
