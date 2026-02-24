#!/bin/bash

echo "🚀 Starting Mumbai Digital Twin System..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if backend is already running
echo "1️⃣ Checking backend status..."
if curl -s http://localhost:8000/api/health/live > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is already running${NC}"
else
    echo -e "${YELLOW}⚠️  Backend not running. Starting...${NC}"
    
    # Start backend
    cd backend
    echo "   Starting uvicorn..."
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    echo "   Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/health/live > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend started successfully (PID: $BACKEND_PID)${NC}"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
fi

# Step 2: Test Mumbai API
echo ""
echo "2️⃣ Testing Mumbai API..."
WARDS=$(curl -s http://localhost:8000/api/mumbai/wards)
if echo "$WARDS" | grep -q "ward_id"; then
    echo -e "${GREEN}✅ Mumbai API is working${NC}"
    echo "   Sample: $(echo "$WARDS" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"{data[0]['ward_name']} - {data[0]['population']:,} people\") if data else print('No data')" 2>/dev/null || echo "Data available")"
else
    echo -e "${RED}❌ Mumbai API not responding${NC}"
    echo "   Response: $WARDS"
    echo ""
    echo "   Check backend logs: tail -f backend.log"
    exit 1
fi

# Step 3: Check if frontend is running
echo ""
echo "3️⃣ Checking frontend status..."
if curl -s http://localhost:8081 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is already running${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend not running. Starting...${NC}"
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "   Installing dependencies..."
        npm install
    fi
    
    echo "   Starting Vite dev server..."
    npm run dev -- --port 8081 > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    echo "   Waiting for frontend to start..."
    sleep 5
    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Mumbai Digital Twin is Running!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Frontend:    http://localhost:8081"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop:"
echo "   pkill -f uvicorn"
echo "   pkill -f vite"
echo ""
echo -e "${YELLOW}📍 Navigate to: Mumbai Real-Time${NC}"
echo ""

# Open browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🌐 Opening browser..."
    sleep 2
    open http://localhost:8081
fi
