#!/bin/bash

# ScoutIQ Frontend Startup Script
echo "🚀 Starting ScoutIQ Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
fi

# Check for Mapbox token
if [ -z "$REACT_APP_MAPBOX_TOKEN" ]; then
    echo "⚠️  Warning: REACT_APP_MAPBOX_TOKEN environment variable not set."
    echo "   The map will use the token from frontend/src/config.js"
    echo "   For production, set your Mapbox token:"
    echo "   export REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here"
    echo ""
fi

# Start the React development server
echo "🌐 Starting React development server..."
npm start
