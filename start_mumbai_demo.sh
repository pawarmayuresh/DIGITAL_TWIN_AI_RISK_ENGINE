#!/bin/bash

# Mumbai Digital Twin - Quick Start Script
# This script starts both backend and frontend for the Mumbai demonstration

echo "🌆 Starting Mumbai Digital Twin System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Backend already running on port 8000${NC}"
else
    echo -e "${BLUE}🚀 Starting Backend (FastAPI)...${NC}"
    cd backend
    source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
    pip install -q -r requirements.txt
    
    # Start backend in background
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
    echo "   Logs: tail -f backend.log"
    cd ..
    
    # Wait for backend to be ready
    echo -e "${BLUE}⏳ Waiting for backend to be ready...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/health/live > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend is ready!${NC}"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
fi

# Check if frontend is already running
if lsof -Pi :8081 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Frontend already running on port 8081${NC}"
else
    echo -e "${BLUE}🚀 Starting Frontend (React + Vite)...${NC}"
    cd frontend
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo -e "${BLUE}📦 Installing dependencies...${NC}"
        npm install
    fi
    
    # Start frontend in background
    nohup npm run dev -- --port 8081 > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo "   Logs: tail -f frontend.log"
    cd ..
    
    # Wait for frontend to be ready
    echo -e "${BLUE}⏳ Waiting for frontend to be ready...${NC}"
    sleep 5
    echo -e "${GREEN}✅ Frontend is ready!${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Mumbai Digital Twin System is Running!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}🌐 Frontend:${NC}  http://localhost:8081"
echo -e "${BLUE}🔧 Backend API:${NC} http://localhost:8000"
echo -e "${BLUE}📚 API Docs:${NC}   http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}📍 Navigate to: Mumbai Real-Time Map${NC}"
echo ""
echo -e "${BLUE}🎯 Quick Test:${NC}"
echo "   curl http://localhost:8000/api/mumbai/wards | jq '.[] | {ward_id, ward_name, risk_score}'"
echo ""
echo -e "${BLUE}🛑 To Stop:${NC}"
echo "   ./manage_backend.sh stop"
echo "   pkill -f 'vite'"
echo ""
echo -e "${GREEN}📖 Faculty Demo Guide: MUMBAI_FACULTY_DEMO_GUIDE.md${NC}"
echo ""

# Open browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${BLUE}🌐 Opening browser...${NC}"
    sleep 2
    open http://localhost:8081
fi
