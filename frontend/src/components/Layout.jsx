import { Outlet, NavLink } from 'react-router-dom';
import { 
  Home, Grid3x3, AlertTriangle, Network, GitCompare, 
  Shield, Map, Brain, Activity, MapPin, Navigation 
} from 'lucide-react';
import './Layout.css';

const Layout = () => {
  const navItems = [
    { path: '/mumbai-map', icon: MapPin, label: 'Mumbai Live' },
    { path: '/urban-evacuation', icon: Navigation, label: 'Urban Evacuation' },
    { path: '/city-overview', icon: Home, label: 'City Overview' },
    { path: '/spatial-grid', icon: Grid3x3, label: 'Spatial Grid' },
    { path: '/disaster-simulation', icon: AlertTriangle, label: 'Disaster Sim' },
    { path: '/infrastructure', icon: Network, label: 'Infrastructure' },
    { path: '/policy-comparison', icon: GitCompare, label: 'Policy Compare' },
    { path: '/resilience', icon: Shield, label: 'Resilience' },
    { path: '/risk-heatmap', icon: Map, label: 'Risk Heatmap' },
    { path: '/explainability', icon: Brain, label: 'XAI' },
    { path: '/knowledge-engine', icon: Brain, label: 'Knowledge Engine' },
  ];

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <Activity className="logo-icon" />
          <h1>Mumbai Risk Engine</h1>
        </div>
        <nav className="sidebar-nav">
          {navItems.map(({ path, icon: Icon, label }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
