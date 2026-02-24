#!/usr/bin/env python3
"""
Batch Validation Script for AI Strategic Risk Engine
Validates Batches 1-4 completion status
"""

import requests
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class BatchValidator:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.results = {
            "batch1": [],
            "batch2": [],
            "batch3": [],
            "batch4": []
        }
    
    def print_header(self, text: str, color: str = BLUE):
        print(f"\n{color}{text}{NC}")
        print("=" * len(text))
    
    def print_test(self, name: str, passed: bool, details: str = ""):
        status = f"{GREEN}✓ PASS{NC}" if passed else f"{RED}✗ FAIL{NC}"
        print(f"  {name}: {status}")
        if details:
            print(f"    {details}")
        return passed
    
    def validate_batch1(self) -> int:
        """Validate Batch 1 - Foundation System"""
        self.print_header("🟥 BATCH 1 - Foundation System Validation")
        passed = 0
        
        # Test 1: Server running
        try:
            response = requests.get(f"{self.base_url}/api/health/live", timeout=5)
            test_passed = response.status_code == 200
            if self.print_test("Server Running", test_passed):
                passed += 1
        except Exception as e:
            self.print_test("Server Running", False, f"Error: {e}")
        
        # Test 2: Health live endpoint
        try:
            response = requests.get(f"{self.base_url}/api/health/live", timeout=5)
            test_passed = response.status_code == 200 and "alive" in response.text
            if self.print_test("Health Live Endpoint", test_passed):
                passed += 1
        except Exception as e:
            self.print_test("Health Live Endpoint", False, f"Error: {e}")
        
        # Test 3: Health ready endpoint
        try:
            response = requests.get(f"{self.base_url}/api/health/ready", timeout=5)
            test_passed = response.status_code == 200 and "ready" in response.text
            if self.print_test("Health Ready Endpoint", test_passed):
                passed += 1
        except Exception as e:
            self.print_test("Health Ready Endpoint", False, f"Error: {e}")
        
        # Test 4: Version endpoint
        try:
            response = requests.get(f"{self.base_url}/api/health/version", timeout=5)
            test_passed = response.status_code == 200 and "version" in response.text
            if self.print_test("Version Endpoint", test_passed):
                passed += 1
        except Exception as e:
            self.print_test("Version Endpoint", False, f"Error: {e}")
        
        self.results["batch1"] = [passed, 4]
        return passed
    
    def validate_batch2(self) -> int:
        """Validate Batch 2 - Spatial Grid Simulation"""
        self.print_header("🟧 BATCH 2 - Spatial Grid Simulation Validation")
        passed = 0
        
        # Check file existence
        files = [
            "backend/core/spatial_engine/grid_manager.py",
            "backend/core/spatial_engine/grid_cell.py",
            "backend/core/spatial_engine/diffusion_model.py",
            "backend/core/spatial_engine/zoning_engine.py",
            "backend/core/spatial_engine/spatial_risk_calculator.py",
            "backend/core/spatial_engine/grid_visual_exporter.py",
        ]
        
        for file_path in files:
            test_passed = Path(file_path).exists()
            if self.print_test(f"Module: {Path(file_path).name}", test_passed):
                passed += 1
        
        self.results["batch2"] = [passed, len(files)]
        return passed
    
    def validate_batch3(self) -> int:
        """Validate Batch 3 - Disaster Engine"""
        self.print_header("🟨 BATCH 3 - Disaster Engine Validation")
        passed = 0
        
        scenarios = [
            ("flood", "Flood Scenario"),
            ("earthquake-cascade", "Earthquake Cascade"),
            ("pandemic", "Pandemic Scenario"),
            ("multi-disaster", "Multi-Disaster Scenario"),
            ("cyber-cascade", "Cyber Attack Scenario"),
        ]
        
        for scenario_id, scenario_name in scenarios:
            try:
                response = requests.get(
                    f"{self.base_url}/api/demo/run/{scenario_id}",
                    timeout=30
                )
                test_passed = response.status_code == 200 and "scenario" in response.text
                if self.print_test(scenario_name, test_passed):
                    passed += 1
                    if test_passed:
                        data = response.json()
                        print(f"      Cells affected: {data.get('total_cells_affected', 'N/A')}")
            except Exception as e:
                self.print_test(scenario_name, False, f"Error: {e}")
        
        self.results["batch3"] = [passed, len(scenarios)]
        return passed
    
    def validate_batch4(self) -> int:
        """Validate Batch 4 - Cascading Failure Engine"""
        self.print_header("🟩 BATCH 4 - Cascading Failure Engine Validation")
        passed = 0
        
        # Check file existence
        files = [
            "backend/core/cascading_engine/cascading_failure_engine.py",
            "backend/core/cascading_engine/infrastructure_graph.py",
            "backend/core/cascading_engine/recovery_model.py",
            "backend/core/cascading_engine/stability_calculator.py",
            "backend/core/cascading_engine/disaster_cascade_integration.py",
        ]
        
        for file_path in files:
            test_passed = Path(file_path).exists()
            if self.print_test(f"Module: {Path(file_path).name}", test_passed):
                passed += 1
        
        # Test cascade demo API
        try:
            response = requests.get(
                f"{self.base_url}/api/demo/run/cascade-demo",
                timeout=30
            )
            test_passed = response.status_code == 200 and "scenario" in response.text
            if self.print_test("Cascade Demo API", test_passed):
                passed += 1
                if test_passed:
                    data = response.json()
                    print(f"      Affected cells: {data.get('affected_cells', 'N/A')}")
                    print(f"      Critical zones: {data.get('critical_zones', 'N/A')}")
        except Exception as e:
            self.print_test("Cascade Demo API", False, f"Error: {e}")
        
        self.results["batch4"] = [passed, len(files) + 1]
        return passed
    
    def print_summary(self):
        """Print validation summary"""
        self.print_header("📊 VALIDATION SUMMARY", BLUE)
        
        total_passed = 0
        total_tests = 0
        
        for batch_name, (passed, total) in self.results.items():
            percentage = (passed / total * 100) if total > 0 else 0
            color = GREEN if percentage >= 80 else YELLOW if percentage >= 60 else RED
            
            batch_display = {
                "batch1": "🟥 Batch 1 (Foundation)",
                "batch2": "🟧 Batch 2 (Spatial Grid)",
                "batch3": "🟨 Batch 3 (Disaster Engine)",
                "batch4": "🟩 Batch 4 (Cascading Engine)"
            }
            
            print(f"{batch_display[batch_name]}: {color}{passed}/{total} ({percentage:.0f}%){NC}")
            total_passed += passed
            total_tests += total
        
        print()
        overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_percentage:.0f}%)")
        print()
        
        if overall_percentage >= 80:
            print(f"{GREEN}✅ System is ready for Batch 5 implementation!{NC}")
            return 0
        elif overall_percentage >= 60:
            print(f"{YELLOW}⚠️  Some issues found. Review failures before proceeding.{NC}")
            return 1
        else:
            print(f"{RED}❌ Critical issues found. Fix failures before proceeding.{NC}")
            return 2


def main():
    print(f"{BLUE}🔥 AI Strategic Risk Engine - Batch Validation{NC}")
    print("=" * 50)
    
    validator = BatchValidator()
    
    try:
        validator.validate_batch1()
        validator.validate_batch2()
        validator.validate_batch3()
        validator.validate_batch4()
        
        exit_code = validator.print_summary()
        
        print()
        print("📝 For detailed validation procedures, see: BATCH_STATUS_ANALYSIS.md")
        print("🚀 To start server: uvicorn backend.main:app --reload")
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Validation interrupted by user{NC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Validation error: {e}{NC}")
        sys.exit(2)


if __name__ == "__main__":
    main()
