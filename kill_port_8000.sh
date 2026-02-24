#!/bin/bash

echo "🔍 Finding process on port 8000..."

# Find the process ID using port 8000
PID=$(lsof -ti:8000)

if [ -z "$PID" ]; then
    echo "✅ No process found on port 8000"
else
    echo "⚠️  Found process $PID on port 8000"
    echo "🛑 Killing process..."
    kill -9 $PID
    sleep 1
    
    # Verify it's killed
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "❌ Failed to kill process"
    else
        echo "✅ Process killed successfully"
    fi
fi

echo ""
echo "🚀 Port 8000 is now available"
echo "   You can now run: python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
