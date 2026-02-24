#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "Starting backend server from: $(pwd)"
echo "Python path: $(which python3)"
echo ""

# Set PYTHONPATH to include the project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the backend server
uvicorn backend.main:app --reload --port 8001
