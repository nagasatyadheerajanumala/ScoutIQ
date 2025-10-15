#!/bin/bash

# ScoutIQ Backend Startup Script
echo "🚀 Starting ScoutIQ Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r backend/requirements.txt

# Check if PostgreSQL is running
echo "🗄️ Checking PostgreSQL connection..."
if ! pg_isready -q; then
    echo "❌ PostgreSQL is not running. Please start PostgreSQL first."
    echo "   On macOS: brew services start postgresql"
    echo "   On Ubuntu: sudo systemctl start postgresql"
    exit 1
fi

# Check if database exists
echo "🔍 Checking database..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw scoutiq; then
    echo "📊 Creating database..."
    createdb scoutiq
fi

# Load data if tables are empty
echo "📊 Checking if data needs to be loaded..."
TABLE_COUNT=$(psql -d scoutiq -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
if [ "$TABLE_COUNT" -eq 0 ]; then
    echo "📥 Loading sample data..."
    cd backend
    python db/seed_data.py
    cd ..
fi

# Start the FastAPI server
echo "🌐 Starting FastAPI server..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
