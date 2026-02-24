/**
 * AI Engine - Intelligent Decision Making System
 * Uses A* Search, CSP, and Explainable AI concepts
 */

// ==================== A* SEARCH ALGORITHM ====================
// Find optimal evacuation routes from danger zones to safe zones

class AStarSearch {
  constructor(grid) {
    this.grid = grid;
    this.gridSize = grid.length;
  }

  // Heuristic: Manhattan distance
  heuristic(cell1, cell2) {
    return Math.abs(cell1.x - cell2.x) + Math.abs(cell1.y - cell2.y);
  }

  // Find optimal evacuation path
  findEvacuationPath(start, goal) {
    const openSet = [start];
    const cameFrom = new Map();
    const gScore = new Map();
    const fScore = new Map();

    gScore.set(`${start.x},${start.y}`, 0);
    fScore.set(`${start.x},${start.y}`, this.heuristic(start, goal));

    while (openSet.length > 0) {
      // Get node with lowest fScore
      openSet.sort((a, b) => {
        const aKey = `${a.x},${a.y}`;
        const bKey = `${b.x},${b.y}`;
        return (fScore.get(aKey) || Infinity) - (fScore.get(bKey) || Infinity);
      });

      const current = openSet.shift();
      const currentKey = `${current.x},${current.y}`;

      if (current.x === goal.x && current.y === goal.y) {
        return this.reconstructPath(cameFrom, current);
      }

      const neighbors = this.getNeighbors(current);
      for (const neighbor of neighbors) {
        const neighborKey = `${neighbor.x},${neighbor.y}`;
        const tentativeGScore = (gScore.get(currentKey) || Infinity) + 1;

        if (tentativeGScore < (gScore.get(neighborKey) || Infinity)) {
          cameFrom.set(neighborKey, current);
          gScore.set(neighborKey, tentativeGScore);
          fScore.set(neighborKey, tentativeGScore + this.heuristic(neighbor, goal));

          if (!openSet.find(n => n.x === neighbor.x && n.y === neighbor.y)) {
            openSet.push(neighbor);
          }
        }
      }
    }

    return null; // No path found
  }

  getNeighbors(cell) {
    const neighbors = [];
    const directions = [
      { dx: -1, dy: 0 }, { dx: 1, dy: 0 },
      { dx: 0, dy: -1 }, { dx: 0, dy: 1 }
    ];

    for (const { dx, dy } of directions) {
      const nx = cell.x + dx;
      const ny = cell.y + dy;

      if (nx >= 0 && nx < this.gridSize && ny >= 0 && ny < this.gridSize) {
        const neighbor = this.grid[ny][nx];
        // Can't evacuate through high disaster zones
        if (neighbor.floodLevel < 0.7 && neighbor.fireIntensity < 0.7) {
          neighbors.push(neighbor);
        }
      }
    }

    return neighbors;
  }

  reconstructPath(cameFrom, current) {
    const path = [current];
    let currentKey = `${current.x},${current.y}`;

    while (cameFrom.has(currentKey)) {
      current = cameFrom.get(currentKey);
      path.unshift(current);
      currentKey = `${current.x},${current.y}`;
    }

    return path;
  }
}

// ==================== CSP (Constraint Satisfaction Problem) ====================
// Resource allocation with constraints

class ResourceAllocationCSP {
  constructor(grid, availableResources) {
    this.grid = grid;
    this.resources = availableResources;
    this.assignments = new Map();
  }

  // Constraints
  constraints = {
    // High-risk cells must get resources first
    priorityConstraint: (cell) => {
      const disasterLevel = Math.max(cell.floodLevel, cell.fireIntensity, cell.contamination);
      return disasterLevel > 0.6;
    },

    // Infrastructure cells need protection
    infrastructureConstraint: (cell) => {
      return cell.infrastructure !== null;
    },

    // High population cells need more resources
    populationConstraint: (cell) => {
      return cell.population > 500;
    },

    // Can't allocate more resources than available
    resourceConstraint: (totalAllocated, resourceType) => {
      return totalAllocated <= this.resources[resourceType];
    }
  };

  // Solve CSP using backtracking
  allocateResources() {
    const cells = [];
    this.grid.forEach(row => {
      row.forEach(cell => {
        const disasterLevel = Math.max(cell.floodLevel, cell.fireIntensity, cell.contamination);
        if (disasterLevel > 0.3) {
          cells.push(cell);
        }
      });
    });

    // Sort by priority (highest risk first)
    cells.sort((a, b) => {
      const aLevel = Math.max(a.floodLevel, a.fireIntensity, a.contamination);
      const bLevel = Math.max(b.floodLevel, b.fireIntensity, b.contamination);
      return bLevel - aLevel;
    });

    const allocation = {
      pumps: [],
      ambulances: [],
      shelters: [],
      firetrucks: []
    };

    let pumpsUsed = 0;
    let ambulancesUsed = 0;
    let sheltersUsed = 0;
    let firetrucksUsed = 0;

    for (const cell of cells) {
      const cellKey = `${cell.x},${cell.y}`;
      const disasterLevel = Math.max(cell.floodLevel, cell.fireIntensity, cell.contamination);

      // Allocate pumps for flood
      if (cell.floodLevel > 0.5 && pumpsUsed < this.resources.pumps) {
        allocation.pumps.push(cellKey);
        pumpsUsed++;
      }

      // Allocate fire trucks for fire
      if (cell.fireIntensity > 0.5 && firetrucksUsed < this.resources.firetrucks) {
        allocation.firetrucks.push(cellKey);
        firetrucksUsed++;
      }

      // Allocate ambulances for casualties
      if (disasterLevel > 0.6 && ambulancesUsed < this.resources.ambulances) {
        allocation.ambulances.push(cellKey);
        ambulancesUsed++;
      }

      // Allocate shelters for evacuation
      if (disasterLevel > 0.7 && sheltersUsed < this.resources.shelters) {
        allocation.shelters.push(cellKey);
        sheltersUsed++;
      }
    }

    return {
      allocation,
      utilization: {
        pumps: `${pumpsUsed}/${this.resources.pumps}`,
        ambulances: `${ambulancesUsed}/${this.resources.ambulances}`,
        shelters: `${sheltersUsed}/${this.resources.shelters}`,
        firetrucks: `${firetrucksUsed}/${this.resources.firetrucks}`
      }
    };
  }
}

// ==================== EXPLAINABLE AI ====================
// SHAP-like feature importance for decisions

class ExplainableAI {
  constructor() {
    this.decisions = [];
  }

  // Calculate feature importance for evacuation decision
  explainEvacuationDecision(cell, ward) {
    const features = {
      floodLevel: cell.floodLevel * 100,
      fireIntensity: cell.fireIntensity * 100,
      contamination: cell.contamination * 100,
      elevation: cell.elevation,
      population: cell.population,
      hasInfrastructure: cell.infrastructure ? 1 : 0,
      wardRiskScore: ward.risk_score * 100
    };

    // Calculate SHAP values (simplified) - INCREASED WEIGHTS FOR MORE EVACUATIONS
    const baseValue = 0.2; // Lower base value to make evacuations more likely
    const shapValues = {
      floodLevel: (features.floodLevel / 100) * 0.50, // Increased weight significantly
      fireIntensity: (features.fireIntensity / 100) * 0.50, // Increased weight significantly
      contamination: (features.contamination / 100) * 0.30, // Increased weight
      elevation: (50 - features.elevation) / 50 * 0.20, // Increased weight
      population: (features.population / 1000) * 0.12, // Increased weight
      hasInfrastructure: features.hasInfrastructure * 0.08, // Increased weight
      wardRiskScore: (features.wardRiskScore / 100) * 0.08 // Increased weight
    };

    const finalProbability = baseValue + Object.values(shapValues).reduce((a, b) => a + b, 0);

    return {
      decision: finalProbability > 0.45 ? 'EVACUATE' : 'MONITOR', // Lowered threshold from 0.55 to 0.45
      confidence: Math.min(finalProbability, 1.0),
      features,
      shapValues,
      explanation: this.generateExplanation(shapValues, features)
    };
  }

  generateExplanation(shapValues, features) {
    const sortedFeatures = Object.entries(shapValues)
      .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
      .slice(0, 3);

    const reasons = sortedFeatures.map(([feature, value]) => {
      const contribution = (Math.abs(value) * 100).toFixed(1);
      const direction = value > 0 ? 'increases' : 'decreases';
      
      let description = '';
      switch(feature) {
        case 'floodLevel':
          description = `Flood level (${features.floodLevel.toFixed(0)}%) ${direction} risk by ${contribution}%`;
          break;
        case 'fireIntensity':
          description = `Fire intensity (${features.fireIntensity.toFixed(0)}%) ${direction} risk by ${contribution}%`;
          break;
        case 'contamination':
          description = `Contamination (${features.contamination.toFixed(0)}%) ${direction} risk by ${contribution}%`;
          break;
        case 'elevation':
          description = `Low elevation (${features.elevation.toFixed(1)}m) ${direction} flood risk by ${contribution}%`;
          break;
        case 'population':
          description = `Population density (${features.population}) ${direction} urgency by ${contribution}%`;
          break;
        case 'hasInfrastructure':
          description = `Critical infrastructure present ${direction} priority by ${contribution}%`;
          break;
        case 'wardRiskScore':
          description = `Ward risk score (${features.wardRiskScore.toFixed(0)}%) ${direction} baseline by ${contribution}%`;
          break;
      }
      return description;
    });

    return reasons;
  }

  // Log decision for audit trail
  logDecision(cell, decision, explanation) {
    this.decisions.push({
      timestamp: new Date().toISOString(),
      cell: `[${cell.x},${cell.y}]`,
      decision: decision.decision,
      confidence: decision.confidence,
      explanation: explanation,
      features: decision.features
    });
  }

  getDecisionLog() {
    return this.decisions;
  }
}

// ==================== INTELLIGENT DISASTER SIMULATOR ====================

export class IntelligentDisasterSimulator {
  constructor(grid, ward, disasterType, severity) {
    this.grid = grid;
    this.ward = ward;
    this.disasterType = disasterType;
    this.severity = severity / 10; // Normalize to 0-1
    this.astar = new AStarSearch(grid);
    this.explainableAI = new ExplainableAI();
    this.resourceCSP = new ResourceAllocationCSP(grid, {
      pumps: Math.ceil(ward.risk_score * 15),
      ambulances: Math.ceil(ward.population / 50000),
      shelters: Math.ceil(ward.population / 100000),
      firetrucks: Math.ceil(ward.risk_score * 10)
    });
  }

  // Intelligent disaster spread using physics and AI
  simulateStep() {
    const decisions = [];
    const evacuationPaths = [];

    for (let y = 0; y < this.grid.length; y++) {
      for (let x = 0; x < this.grid[y].length; x++) {
        const cell = this.grid[y][x];
        
        // Get current disaster level
        let disasterLevel = 0;
        if (this.disasterType === 'flood') {
          disasterLevel = cell.floodLevel;
        } else if (this.disasterType === 'fire') {
          disasterLevel = cell.fireIntensity;
        } else {
          disasterLevel = cell.contamination;
        }

        // Only spread if disaster exists and severity is high enough
        if (disasterLevel > 0.1) {
          this.spreadDisaster(cell, x, y);
        }

        // AI Decision: Should we evacuate this cell?
        const decision = this.explainableAI.explainEvacuationDecision(cell, this.ward);
        
        if (decision.decision === 'EVACUATE' && !cell.evacuated) {
          // Find evacuation path using A*
          const safeZone = this.findNearestSafeZone(cell);
          if (safeZone) {
            const path = this.astar.findEvacuationPath(cell, safeZone);
            if (path) {
              cell.evacuated = true;
              cell.evacuationPath = path;
              evacuationPaths.push({
                from: `[${cell.x},${cell.y}]`,
                to: `[${safeZone.x},${safeZone.y}]`,
                pathLength: path.length,
                population: cell.population,
                path: path // Include full path for visualization
              });
              console.log(`✅ Evacuation: Cell [${cell.x},${cell.y}] → [${safeZone.x},${safeZone.y}], ${cell.population} people, ${path.length} steps`);
            } else {
              console.log(`⚠️ No path found from [${cell.x},${cell.y}] to [${safeZone.x},${safeZone.y}]`);
            }
          } else {
            console.log(`⚠️ No safe zone found for cell [${cell.x},${cell.y}]`);
          }
        }

        // Log decision
        if (disasterLevel > 0.3) {
          this.explainableAI.logDecision(cell, decision, decision.explanation);
          decisions.push({
            cell: `[${x},${y}]`,
            decision: decision.decision,
            confidence: (decision.confidence * 100).toFixed(0) + '%',
            topReasons: decision.explanation
          });
        }

        // Infrastructure damage based on disaster level
        if (disasterLevel > 0.7 && cell.infrastructure && !cell.damaged) {
          cell.damaged = true;
        }
      }
    }

    // Allocate resources using CSP
    const resourceAllocation = this.resourceCSP.allocateResources();

    return {
      decisions,
      evacuationPaths,
      resourceAllocation,
      decisionLog: this.explainableAI.getDecisionLog()
    };
  }

  spreadDisaster(cell, x, y) {
    const neighbors = this.getNeighbors(x, y);
    
    for (const neighbor of neighbors) {
      let spreadRate = 0;
      
      if (this.disasterType === 'flood') {
        // Flood spreads based on elevation and severity
        if (neighbor.elevation < cell.elevation) {
          spreadRate = 0.15 * this.severity;
        } else {
          spreadRate = 0.03 * this.severity;
        }
        neighbor.floodLevel = Math.min(1, neighbor.floodLevel + spreadRate * cell.floodLevel);
      } else if (this.disasterType === 'fire') {
        // Fire spreads based on wind and severity
        spreadRate = 0.12 * this.severity;
        neighbor.fireIntensity = Math.min(1, neighbor.fireIntensity + spreadRate * cell.fireIntensity);
      } else {
        // Contamination spreads uniformly
        spreadRate = 0.08 * this.severity;
        neighbor.contamination = Math.min(1, neighbor.contamination + spreadRate * cell.contamination);
      }
    }

    // Natural decay
    if (this.disasterType === 'flood') {
      cell.floodLevel = Math.max(0, cell.floodLevel - 0.01 * (1 - this.severity));
    } else if (this.disasterType === 'fire') {
      cell.fireIntensity = Math.max(0, cell.fireIntensity - 0.03 * (1 - this.severity));
    } else {
      cell.contamination = Math.max(0, cell.contamination - 0.02 * (1 - this.severity));
    }
  }

  getNeighbors(x, y) {
    const neighbors = [];
    const directions = [
      [-1, 0], [1, 0], [0, -1], [0, 1],
      [-1, -1], [1, -1], [-1, 1], [1, 1]
    ];

    for (const [dx, dy] of directions) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx >= 0 && nx < this.grid[0].length && ny >= 0 && ny < this.grid.length) {
        neighbors.push(this.grid[ny][nx]);
      }
    }

    return neighbors;
  }

  findNearestSafeZone(cell) {
    let nearest = null;
    let minDistance = Infinity;

    for (let y = 0; y < this.grid.length; y++) {
      for (let x = 0; x < this.grid[y].length; x++) {
        const candidate = this.grid[y][x];
        const disasterLevel = Math.max(
          candidate.floodLevel,
          candidate.fireIntensity,
          candidate.contamination
        );

        if (disasterLevel < 0.2) {
          const distance = Math.abs(cell.x - x) + Math.abs(cell.y - y);
          if (distance < minDistance) {
            minDistance = distance;
            nearest = candidate;
          }
        }
      }
    }

    return nearest;
  }
}

export { AStarSearch, ResourceAllocationCSP, ExplainableAI };
