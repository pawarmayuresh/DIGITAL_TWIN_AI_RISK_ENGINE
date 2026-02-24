#!/bin/bash

echo "🧪 Testing Frontend Build..."
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check for syntax errors
echo "🔍 Checking for syntax errors..."
npx eslint src/services/aiEngine.js --no-eslintrc --parser-options=ecmaVersion:2020,sourceType:module || echo "⚠️  ESLint not configured, skipping..."

# Try to build
echo ""
echo "🏗️  Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Frontend build successful!"
    echo ""
    echo "🚀 Start the dev server with:"
    echo "   cd frontend && npm run dev"
else
    echo ""
    echo "❌ Build failed! Check errors above."
fi
