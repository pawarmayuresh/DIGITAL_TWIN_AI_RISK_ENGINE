#!/bin/bash

case "$1" in
  start)
    echo "🚀 Starting backend server..."
    echo ""
    echo "Backend will be available at: http://localhost:8000"
    echo "API docs at: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ;;
    
  stop)
    echo "🛑 Stopping backend server..."
    PID=$(lsof -ti:8000 2>/dev/null)
    if [ -z "$PID" ]; then
      echo "No process found on port 8000"
    else
      kill -9 $PID
      echo "✓ Stopped process $PID on port 8000"
    fi
    ;;
    
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
    
  status)
    PID=$(lsof -ti:8000 2>/dev/null)
    if [ -z "$PID" ]; then
      echo "❌ Backend is not running"
      exit 1
    else
      echo "✓ Backend is running (PID: $PID)"
      echo "  URL: http://localhost:8000"
      exit 0
    fi
    ;;
    
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    echo ""
    echo "Commands:"
    echo "  start   - Start the backend server"
    echo "  stop    - Stop the backend server"
    echo "  restart - Restart the backend server"
    echo "  status  - Check if backend is running"
    exit 1
    ;;
esac
