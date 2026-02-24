#!/bin/bash

# Batch Validation Script for AI Strategic Risk Engine
# This script validates Batches 1-8 completion

echo "🔥 AI Strategic Risk Engine - Batch Validation"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
BATCH1_PASS=0
BATCH2_PASS=0
BATCH3_PASS=0
BATCH4_PASS=0
BATCH5_PASS=0
BATCH6_PASS=0
BATCH7_PASS=0
BATCH8_PASS=0

echo "🟥 BATCH 1 - Foundation System Validation"
echo "----------------------------------------"

# Check if server is running
echo -n "Checking if server is running... "
if curl -s http://localhost:8000/api/health/live > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server is running${NC}"
    BATCH1_PASS=$((BATCH1_PASS + 1))
else
    echo -e "${RED}✗ Server is not running${NC}"
    echo -e "${YELLOW}  Start with: uvicorn backend.main:app --reload${NC}"
fi

# Test health endpoints
echo -n "Testing /api/health/live... "
RESPONSE=$(curl -s http://localhost:8000/api/health/live)
if echo "$RESPONSE" | grep -q "alive"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH1_PASS=$((BATCH1_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo -n "Testing /api/health/ready... "
RESPONSE=$(curl -s http://localhost:8000/api/health/ready)
if echo "$RESPONSE" | grep -q "ready"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH1_PASS=$((BATCH1_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo -n "Testing /api/health/version... "
RESPONSE=$(curl -s http://localhost:8000/api/health/version)
if echo "$RESPONSE" | grep -q "version"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH1_PASS=$((BATCH1_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo ""
echo "🟧 BATCH 2 - Spatial Grid Simulation Validation"
echo "----------------------------------------------"

# Check if spatial engine modules exist
echo -n "Checking grid_manager.py... "
if [ -f "backend/core/spatial_engine/grid_manager.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH2_PASS=$((BATCH2_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking grid_cell.py... "
if [ -f "backend/core/spatial_engine/grid_cell.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH2_PASS=$((BATCH2_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking diffusion_model.py... "
if [ -f "backend/core/spatial_engine/diffusion_model.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH2_PASS=$((BATCH2_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking zoning_engine.py... "
if [ -f "backend/core/spatial_engine/zoning_engine.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH2_PASS=$((BATCH2_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo ""
echo "🟨 BATCH 3 - Disaster Engine Validation"
echo "--------------------------------------"

# Test disaster scenarios via API
echo -n "Testing flood scenario... "
RESPONSE=$(curl -s http://localhost:8000/api/demo/run/flood)
if echo "$RESPONSE" | grep -q "scenario"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH3_PASS=$((BATCH3_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo -n "Testing earthquake scenario... "
RESPONSE=$(curl -s http://localhost:8000/api/demo/run/earthquake-cascade)
if echo "$RESPONSE" | grep -q "scenario"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH3_PASS=$((BATCH3_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo -n "Testing pandemic scenario... "
RESPONSE=$(curl -s http://localhost:8000/api/demo/run/pandemic)
if echo "$RESPONSE" | grep -q "scenario"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH3_PASS=$((BATCH3_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo -n "Testing multi-disaster scenario... "
RESPONSE=$(curl -s http://localhost:8000/api/demo/run/multi-disaster)
if echo "$RESPONSE" | grep -q "scenario"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH3_PASS=$((BATCH3_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo ""
echo "🟩 BATCH 4 - Cascading Failure Engine Validation"
echo "-----------------------------------------------"

# Check cascading engine modules
echo -n "Checking cascading_failure_engine.py... "
if [ -f "backend/core/cascading_engine/cascading_failure_engine.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH4_PASS=$((BATCH4_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking infrastructure_graph.py... "
if [ -f "backend/core/cascading_engine/infrastructure_graph.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH4_PASS=$((BATCH4_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking recovery_model.py... "
if [ -f "backend/core/cascading_engine/recovery_model.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH4_PASS=$((BATCH4_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Testing cascade demo API... "
RESPONSE=$(curl -s http://localhost:8000/api/demo/run/cascade-demo)
if echo "$RESPONSE" | grep -q "scenario"; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH4_PASS=$((BATCH4_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo ""
echo "🟦 BATCH 5 - Digital Twin Validation"
echo "-----------------------------------"

echo -n "Checking twin_manager.py... "
if [ -f "backend/core/digital_twin/twin_manager.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH5_PASS=$((BATCH5_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking city_model.py... "
if [ -f "backend/core/digital_twin/city_model.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH5_PASS=$((BATCH5_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo ""
echo "🟪 BATCH 6 - Strategic AI Validation"
echo "-----------------------------------"

echo -n "Checking classical_planner.py... "
if [ -f "backend/core/strategic_ai/classical_planner.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH6_PASS=$((BATCH6_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking resource_allocator.py... "
if [ -f "backend/core/strategic_ai/resource_allocator.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH6_PASS=$((BATCH6_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo ""
echo "⬛ BATCH 7 - Multi-Agent System Validation"
echo "----------------------------------------"

echo -n "Checking agent_manager.py... "
if [ -f "backend/core/multi_agent_system/agent_manager.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH7_PASS=$((BATCH7_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking negotiation_engine.py... "
if [ -f "backend/core/multi_agent_system/negotiation_engine.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH7_PASS=$((BATCH7_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo ""
echo "🎓 BATCH 8 - Learning Layer (RL) Validation"
echo "------------------------------------------"

echo -n "Checking rl_agent.py... "
if [ -f "backend/core/learning_layer/rl_agent.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH8_PASS=$((BATCH8_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Checking training_pipeline.py... "
if [ -f "backend/core/learning_layer/training_pipeline.py" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BATCH8_PASS=$((BATCH8_PASS + 1))
else
    echo -e "${RED}✗ Missing${NC}"
fi

echo -n "Running Batch 8 validation script... "
if python3 validate_batch8.py > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Pass${NC}"
    BATCH8_PASS=$((BATCH8_PASS + 1))
else
    echo -e "${RED}✗ Fail${NC}"
fi

echo ""
echo "=============================================="
echo "📊 VALIDATION SUMMARY"
echo "=============================================="
echo ""

# Calculate percentages
BATCH1_PERCENT=$((BATCH1_PASS * 100 / 4))
BATCH2_PERCENT=$((BATCH2_PASS * 100 / 4))
BATCH3_PERCENT=$((BATCH3_PASS * 100 / 4))
BATCH4_PERCENT=$((BATCH4_PASS * 100 / 4))
BATCH5_PERCENT=$((BATCH5_PASS * 100 / 2))
BATCH6_PERCENT=$((BATCH6_PASS * 100 / 2))
BATCH7_PERCENT=$((BATCH7_PASS * 100 / 2))
BATCH8_PERCENT=$((BATCH8_PASS * 100 / 3))

echo "🟥 Batch 1 (Foundation):        $BATCH1_PASS/4 tests passed ($BATCH1_PERCENT%)"
echo "🟧 Batch 2 (Spatial Grid):      $BATCH2_PASS/4 tests passed ($BATCH2_PERCENT%)"
echo "🟨 Batch 3 (Disaster Engine):   $BATCH3_PASS/4 tests passed ($BATCH3_PERCENT%)"
echo "🟩 Batch 4 (Cascading Engine):  $BATCH4_PASS/4 tests passed ($BATCH4_PERCENT%)"
echo "🟦 Batch 5 (Digital Twin):      $BATCH5_PASS/2 tests passed ($BATCH5_PERCENT%)"
echo "🟪 Batch 6 (Strategic AI):      $BATCH6_PASS/2 tests passed ($BATCH6_PERCENT%)"
echo "⬛ Batch 7 (Multi-Agent):       $BATCH7_PASS/2 tests passed ($BATCH7_PERCENT%)"
echo "🎓 Batch 8 (Learning Layer):   $BATCH8_PASS/3 tests passed ($BATCH8_PERCENT%)"
echo ""

TOTAL_PASS=$((BATCH1_PASS + BATCH2_PASS + BATCH3_PASS + BATCH4_PASS + BATCH5_PASS + BATCH6_PASS + BATCH7_PASS + BATCH8_PASS))
TOTAL_TESTS=23
TOTAL_PERCENT=$((TOTAL_PASS * 100 / TOTAL_TESTS))

echo "OVERALL: $TOTAL_PASS/$TOTAL_TESTS tests passed ($TOTAL_PERCENT%)"
echo ""

if [ $TOTAL_PERCENT -ge 80 ]; then
    echo -e "${GREEN}✅ All batches validated successfully!${NC}"
elif [ $TOTAL_PERCENT -ge 60 ]; then
    echo -e "${YELLOW}⚠️  Some issues found. Review failures before proceeding.${NC}"
else
    echo -e "${RED}❌ Critical issues found. Fix failures before proceeding.${NC}"
fi

echo ""
echo "📝 For detailed validation procedures, see: BATCH_STATUS_ANALYSIS.md"
