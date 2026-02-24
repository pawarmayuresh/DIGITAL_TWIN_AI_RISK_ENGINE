import { createContext, useContext, useState, useEffect } from 'react';

const WardContext = createContext();

export const useWard = () => {
  const context = useContext(WardContext);
  if (!context) {
    throw new Error('useWard must be used within WardProvider');
  }
  return context;
};

export const WardProvider = ({ children }) => {
  const [selectedWard, setSelectedWard] = useState(null);
  const [wardData, setWardData] = useState(null);
  const [agentLogs, setAgentLogs] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [disasterType, setDisasterType] = useState('flood'); // Add disaster type state

  // AI Agent System - Triggers when ward changes
  useEffect(() => {
    if (selectedWard) {
      triggerAIAgents(selectedWard);
    }
  }, [selectedWard]);

  const triggerAIAgents = async (ward) => {
    setIsAnalyzing(true);
    const logs = [];
    const timestamp = new Date().toLocaleTimeString();

    // Agent 1: Risk Assessment Agent
    logs.push({
      agent: 'Risk Assessment Agent',
      timestamp,
      action: 'ANALYZING',
      message: `Evaluating risk factors for ${ward.ward_name}...`,
      status: 'processing'
    });

    // Simulate AI reasoning delay
    await new Promise(resolve => setTimeout(resolve, 500));

    logs.push({
      agent: 'Risk Assessment Agent',
      timestamp,
      action: 'COMPLETED',
      message: `Risk Score: ${(ward.risk_score * 100).toFixed(0)}% - ${ward.severity_level}. Factors: Rainfall (35%), Water Level (25%), Slum Density (${ward.slum_population_percent}%)`,
      status: 'success',
      data: {
        riskScore: ward.risk_score,
        severity: ward.severity_level,
        factors: ['rainfall', 'water_level', 'slum_density']
      }
    });

    // Agent 2: Infrastructure Agent
    logs.push({
      agent: 'Infrastructure Agent',
      timestamp,
      action: 'ANALYZING',
      message: `Checking critical infrastructure in ${ward.ward_name}...`,
      status: 'processing'
    });

    await new Promise(resolve => setTimeout(resolve, 300));

    logs.push({
      agent: 'Infrastructure Agent',
      timestamp,
      action: 'COMPLETED',
      message: `Found hospitals, power stations, and transport hubs. Vulnerability: ${ward.risk_score > 0.7 ? 'HIGH' : 'MODERATE'}`,
      status: 'success'
    });

    // Agent 3: Population Agent
    logs.push({
      agent: 'Population Agent',
      timestamp,
      action: 'ANALYZING',
      message: `Analyzing population distribution and evacuation needs...`,
      status: 'processing'
    });

    await new Promise(resolve => setTimeout(resolve, 400));

    const evacuationNeeded = Math.floor(ward.population * (ward.risk_score > 0.8 ? 0.6 : ward.risk_score > 0.6 ? 0.3 : 0.1));
    logs.push({
      agent: 'Population Agent',
      timestamp,
      action: 'COMPLETED',
      message: `Population: ${ward.population.toLocaleString()}. Estimated evacuation needed: ${evacuationNeeded.toLocaleString()} people`,
      status: 'success',
      data: { evacuationNeeded }
    });

    // Agent 4: Resource Allocation Agent
    logs.push({
      agent: 'Resource Allocation Agent',
      timestamp,
      action: 'REASONING',
      message: `Calculating optimal resource deployment...`,
      status: 'processing'
    });

    await new Promise(resolve => setTimeout(resolve, 600));

    const resources = {
      pumps: Math.ceil(ward.risk_score * 10),
      ambulances: Math.ceil(ward.population / 50000),
      shelters: Math.ceil(evacuationNeeded / 1000)
    };

    logs.push({
      agent: 'Resource Allocation Agent',
      timestamp,
      action: 'COMPLETED',
      message: `Recommended: ${resources.pumps} mobile pumps, ${resources.ambulances} ambulances, ${resources.shelters} emergency shelters`,
      status: 'success',
      data: resources
    });

    // Agent 5: Decision Making Agent
    logs.push({
      agent: 'Decision Making Agent',
      timestamp,
      action: 'SYNTHESIZING',
      message: `Integrating all agent inputs to generate action plan...`,
      status: 'processing'
    });

    await new Promise(resolve => setTimeout(resolve, 500));

    const decision = ward.risk_score > 0.8 ? 'IMMEDIATE EVACUATION' : 
                     ward.risk_score > 0.6 ? 'PREPARE FOR EVACUATION' : 
                     'MONITOR SITUATION';

    logs.push({
      agent: 'Decision Making Agent',
      timestamp,
      action: 'DECISION',
      message: `FINAL DECISION: ${decision}. Confidence: ${(ward.risk_score * 100).toFixed(0)}%`,
      status: ward.risk_score > 0.8 ? 'critical' : ward.risk_score > 0.6 ? 'warning' : 'success',
      data: { decision, confidence: ward.risk_score }
    });

    // Agent 6: Communication Agent
    logs.push({
      agent: 'Communication Agent',
      timestamp,
      action: 'BROADCASTING',
      message: `Sending alerts to residents, emergency services, and government officials...`,
      status: 'processing'
    });

    await new Promise(resolve => setTimeout(resolve, 300));

    logs.push({
      agent: 'Communication Agent',
      timestamp,
      action: 'COMPLETED',
      message: `Alerts sent via SMS, sirens, and mobile app. Estimated reach: ${Math.floor(ward.population * 0.85).toLocaleString()} people`,
      status: 'success'
    });

    setAgentLogs(logs);
    setIsAnalyzing(false);
  };

  const selectWard = (ward, disaster = 'flood') => {
    console.log('🎯 Ward Selected:', ward.ward_name, 'Disaster:', disaster);
    setSelectedWard(ward);
    setWardData(ward);
    setDisasterType(disaster);
    
    // Broadcast to all modules
    window.dispatchEvent(new CustomEvent('wardSelected', { 
      detail: { ward, disaster_type: disaster } 
    }));
  };

  const clearSelection = () => {
    setSelectedWard(null);
    setWardData(null);
    setAgentLogs([]);
  };

  return (
    <WardContext.Provider value={{
      selectedWard,
      wardData,
      agentLogs,
      isAnalyzing,
      disasterType,
      selectWard,
      setDisasterType,
      clearSelection
    }}>
      {children}
    </WardContext.Provider>
  );
};
