#!/bin/bash

echo "🧪 Testing Mumbai Backend API..."
echo ""

# Check if backend is running
echo "1️⃣ Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/api/health/live)
if [ $? -eq 0 ]; then
    echo "✅ Backend is running"
    echo "   Response: $HEALTH"
else
    echo "❌ Backend is not running on port 8000"
    echo "   Start it with: cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    exit 1
fi

echo ""
echo "2️⃣ Testing Mumbai wards endpoint..."
WARDS=$(curl -s http://localhost:8000/api/mumbai/wards)
if echo "$WARDS" | grep -q "ward_id"; then
    echo "✅ Wards endpoint working"
    echo "   Sample data:"
    echo "$WARDS" | python3 -m json.tool | head -20
else
    echo "❌ Wards endpoint failed"
    echo "   Response: $WARDS"
fi

echo ""
echo "3️⃣ Testing rain sensors endpoint..."
RAIN=$(curl -s http://localhost:8000/api/mumbai/sensors/rain)
if echo "$RAIN" | grep -q "sensor_id"; then
    echo "✅ Rain sensors endpoint working"
    echo "   Data: $RAIN" | python3 -m json.tool
else
    echo "❌ Rain sensors endpoint failed"
    echo "   Response: $RAIN"
fi

echo ""
echo "4️⃣ Testing water sensors endpoint..."
WATER=$(curl -s http://localhost:8000/api/mumbai/sensors/water)
if echo "$WATER" | grep -q "sensor_id"; then
    echo "✅ Water sensors endpoint working"
    echo "   Data: $WATER" | python3 -m json.tool
else
    echo "❌ Water sensors endpoint failed"
    echo "   Response: $WATER"
fi

echo ""
echo "5️⃣ Testing traffic sensors endpoint..."
TRAFFIC=$(curl -s http://localhost:8000/api/mumbai/sensors/traffic)
if echo "$TRAFFIC" | grep -q "sensor_id"; then
    echo "✅ Traffic sensors endpoint working"
    echo "   Data: $TRAFFIC" | python3 -m json.tool
else
    echo "❌ Traffic sensors endpoint failed"
    echo "   Response: $TRAFFIC"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ API Testing Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next Steps:"
echo "   1. If all tests passed, check browser console for frontend errors"
echo "   2. Open DevTools (F12) → Console tab"
echo "   3. Look for API call errors or CORS issues"
echo "   4. Check Network tab to see if requests are being made"
echo ""
echo "🌐 Frontend should be at: http://localhost:8081"
echo "📚 API Docs: http://localhost:8000/docs"
