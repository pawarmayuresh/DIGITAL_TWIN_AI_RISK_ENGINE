#!/bin/bash

echo "🌆 Starting Mumbai Digital Twin Demo..."
echo ""

# Check if Python packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip3 install -q fastapi uvicorn pandas python-dotenv loguru pydantic pydantic-settings
    echo "✅ Dependencies installed"
fi

# Start backend
echo "🚀 Starting backend on port 8000..."
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
echo "🧪 Testing backend..."
curl -s http://localhost:8000/api/health/live > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Backend is running!"
else
    echo "⚠️  Backend may still be starting..."
fi

# Check if node is installed
if command -v npm &> /dev/null; then
    echo "🚀 Starting frontend on port 8081..."
    cd frontend
    npm run dev -- --port 8081 &
    FRONTEND_PID=$!
    cd ..
    sleep 3
    echo "✅ Frontend is running!"
else
    echo "⚠️  npm not found. Frontend not started."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Mumbai Digital Twin is Running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Backend API: http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/docs"
echo "🎨 Frontend:    http://localhost:8081"
echo ""
echo "🧪 Test Mumbai API:"
echo "   curl http://localhost:8000/api/mumbai/wards | python3 -m json.tool"
echo ""
echo "🛑 To stop: pkill -f uvicorn && pkill -f vite"
echo ""

# Keep script running
wait
