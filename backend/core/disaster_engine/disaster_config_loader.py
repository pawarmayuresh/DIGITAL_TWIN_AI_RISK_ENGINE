"""Disaster Config Loader — loads disaster scenarios and configurations from JSON/YAML."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from .base_disaster import DisasterEvent, DisasterType, Severity
from .disaster_manager import DisasterManager


class DisasterConfigLoader:
    """
    Loads disaster configurations from files or dicts.
    
    Supports:
    - Single disaster events
    - Multi-disaster scenarios
    - Scheduled cascades
    - Dynamic scenario generation
    """

    @staticmethod
    def load_json(file_path: str) -> Dict:
        """Load disaster config from JSON file."""
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def load_scenario(scenario_dict: Dict) -> List[DisasterEvent]:
        """
        Parse scenario dict into list of DisasterEvents.
        
        Expected format:
        {
            "name": "Scenario Name",
            "description": "...",
            "disasters": [
                {
                    "type": "flood",
                    "severity": 0.7,
                    "epicenter": [10, 15],
                    "radius_km": 5.0,
                    "onset_time": 0
                },
                ...
            ]
        }
        """
        events = []
        disaster_counter = 0
        
        for disaster_config in scenario_dict.get("disasters", []):
            disaster_counter += 1
            try:
                dtype = DisasterType[disaster_config.get("type", "FLOOD").upper()]
            except KeyError:
                print(f"Unknown disaster type: {disaster_config.get('type')}")
                continue
            
            severity = disaster_config.get("severity", 0.5)
            epicenter = tuple(disaster_config.get("epicenter", [10, 10]))
            radius_km = disaster_config.get("radius_km", 5.0)
            onset_time = disaster_config.get("onset_time", 0)
            event_id = f"{dtype.value}-{disaster_counter}"
            
            event = DisasterEvent(
                event_id=event_id,
                disaster_type=dtype,
                severity=severity,
                epicenter=epicenter,
                radius_km=radius_km,
                onset_time=onset_time,
            )
            
            events.append(event)
        
        return events

    @staticmethod
    def get_preset_scenario(scenario_name: str) -> Dict:
        """
        Get built-in disaster scenario by name.
        
        Available:
        - "mild_flood": Single low-intensity flood
        - "severe_earthquake": Major seismic event
        - "wildfire_series": Multiple fires across region
        - "pandemic_wave": Slow-burn infection spread
        - "cyber_cascade": Attack triggering infrastructure failures
        - "multi_disaster": Combined hazards with cascades
        """
        
        scenarios = {
            "mild_flood": {
                "name": "Mild Flood Event",
                "description": "Low-intensity localized flooding",
                "disasters": [
                    {
                        "type": "flood",
                        "severity": 0.4,
                        "epicenter": [10, 10],
                        "radius_km": 3.0,
                        "onset_time": 0,
                    }
                ],
            },
            "severe_earthquake": {
                "name": "Major Earthquake",
                "description": "High-magnitude seismic event with aftershocks",
                "disasters": [
                    {
                        "type": "earthquake",
                        "severity": 0.9,
                        "epicenter": [15, 15],
                        "radius_km": 8.0,
                        "onset_time": 0,
                    }
                ],
            },
            "wildfire_series": {
                "name": "Wildfire Series",
                "description": "Multiple fires spreading across region",
                "disasters": [
                    {
                        "type": "wildfire",
                        "severity": 0.6,
                        "epicenter": [8, 8],
                        "radius_km": 4.0,
                        "onset_time": 0,
                    },
                    {
                        "type": "wildfire",
                        "severity": 0.5,
                        "epicenter": [18, 18],
                        "radius_km": 3.5,
                        "onset_time": 5,
                    },
                ],
            },
            "pandemic_wave": {
                "name": "Pandemic Wave",
                "description": "Slow-moving infectious disease spread",
                "disasters": [
                    {
                        "type": "pandemic",
                        "severity": 0.5,
                        "epicenter": [12, 12],
                        "radius_km": 10.0,
                        "onset_time": 0,
                    }
                ],
            },
            "cyber_cascade": {
                "name": "Cyber Attack Cascade",
                "description": "Network attack with cascading infrastructure failures",
                "disasters": [
                    {
                        "type": "cyber_attack",
                        "severity": 0.7,
                        "epicenter": [10, 10],
                        "radius_km": 5.0,
                        "onset_time": 0,
                    }
                ],
            },
            "multi_disaster": {
                "name": "Multi-Disaster Scenario",
                "description": "Combined hazards with trigger cascades",
                "disasters": [
                    {
                        "type": "earthquake",
                        "severity": 0.7,
                        "epicenter": [10, 10],
                        "radius_km": 6.0,
                        "onset_time": 0,
                    },
                    {
                        "type": "flood",
                        "severity": 0.6,
                        "epicenter": [12, 8],
                        "radius_km": 5.0,
                        "onset_time": 2,
                    },
                    {
                        "type": "wildfire",
                        "severity": 0.5,
                        "epicenter": [14, 14],
                        "radius_km": 4.0,
                        "onset_time": 5,
                    },
                    {
                        "type": "pandemic",
                        "severity": 0.4,
                        "epicenter": [10, 10],
                        "radius_km": 8.0,
                        "onset_time": 8,
                    },
                ],
            },
        }
        
        return scenarios.get(scenario_name, scenarios["mild_flood"])

    @staticmethod
    def instantiate_scenario(
        scenario: Dict, disaster_manager: DisasterManager
    ) -> None:
        """
        Load scenario into DisasterManager.
        
        Args:
            scenario: Scenario dict
            disaster_manager: DisasterManager to populate
        """
        events = DisasterConfigLoader.load_scenario(scenario)
        
        for event in events:
            disaster = disaster_manager._create_disaster(event)
            if disaster:
                disaster_manager.add_disaster(disaster)

    @staticmethod
    def create_custom_scenario(
        disasters: List[Dict],
        name: str = "Custom Scenario",
    ) -> Dict:
        """
        Create custom scenario from list of disaster configs.
        
        Args:
            disasters: List of disaster configs
            name: Scenario name
            
        Returns:
            Scenario dict ready for load_scenario()
        """
        return {
            "name": name,
            "description": f"Custom scenario with {len(disasters)} disasters",
            "disasters": disasters,
        }
