#!/bin/bash

# ScoutIQ - Complete Application Starter
# Starts backend and React frontend

set -e
cd "$(dirname "$0")"

echo "🚀 Starting ScoutIQ..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Kill existing processes
echo "🧹 Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
sleep 2

# Start Backend
echo ""
echo "${BLUE}=========================================="
echo "🔧 Starting Backend (FastAPI)..."
echo "==========================================${NC}"

cd backend
source ../venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid

echo "⏳ Waiting for backend..."
sleep 5

if curl -s http://localhost:8000/status > /dev/null; then
    echo "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"
else
    echo "${YELLOW}⚠️  Backend may still be starting...${NC}"
fi

# Start Frontend
echo ""
echo "${BLUE}=========================================="
echo "🎨 Starting Frontend (React + Mapbox)..."
echo "==========================================${NC}"

cd ../frontend

# Install deps if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies (first time only)..."
    npm install
fi

# Start React
BROWSER=none PORT=3000 npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid

echo "⏳ Waiting for React to compile..."
sleep 15

if curl -s http://localhost:3000 > /dev/null; then
    echo "${GREEN}✅ Frontend running (PID: $FRONTEND_PID)${NC}"
else
    echo "${YELLOW}⚠️  Frontend may still be compiling...${NC}"
fi

# Display info
echo ""
echo "${GREEN}=========================================="
echo "✨ ScoutIQ is Running!"
echo "==========================================${NC}"
echo ""
echo "📱 ${BLUE}Main Application:${NC}"
echo "   👉 ${GREEN}http://localhost:3000${NC}"
echo ""
echo "🔧 Backend API:"
echo "   - Status: http://localhost:8000/status"
echo "   - Docs: http://localhost:8000/docs"
echo ""
echo "📊 Process IDs:"
echo "   - Backend: $BACKEND_PID"
echo "   - Frontend: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   - Backend: logs/backend.log"
echo "   - Frontend: logs/frontend.log"
echo ""
echo "${YELLOW}=========================================="
echo "🛑 To Stop:"
echo "==========================================${NC}"
echo "Press Ctrl+C or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Open browser
if command -v open &> /dev/null; then
    sleep 3
    open http://localhost:3000
fi

# Keep script alive
echo "${GREEN}Application is running. Press Ctrl+C to stop.${NC}"
echo ""

cleanup() {
    echo ""
    echo "${YELLOW}🛑 Shutting down...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "${GREEN}✅ Stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Monitor
while kill -0 $BACKEND_PID 2>/dev/null && kill -0 $FRONTEND_PID 2>/dev/null; do
    sleep 10
done

echo "${YELLOW}⚠️  Process stopped unexpectedly${NC}"
cleanup

