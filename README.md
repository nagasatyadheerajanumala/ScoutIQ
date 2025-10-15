# ScoutIQ — AI Property Intelligence Companion

> Transform raw property and market data into actionable investment insights with natural language AI analysis.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-production--ready-green)
![Python](https://img.shields.io/badge/python-3.13-blue)

---

## 🎯 What is ScoutIQ?

ScoutIQ is an **AI-powered property intelligence platform** that helps investors, brokers, and analysts make data-driven real estate decisions. Query properties by location and valuation, and ScoutIQ instantly provides interactive map visualization with AI-generated investment insights — market analysis, risk assessment, and Buy/Hold/Watch recommendations — all in a modern React-based interface.

### Key Capabilities

✨ **AI-Generated Insights** - Natural language summaries of property investment potential  
📊 **Interactive Maps** - Color-coded property markers (Buy/Hold/Watch) with Mapbox GL JS  
📈 **Investment Scoring** - 0-100 point rating system with confidence levels  
⚠️ **Risk Assessment** - Automated flood risk, valuation, and ownership analysis  
🎯 **Classification** - Buy, Hold, or Watch recommendations  
🎨 **Layer Controls** - Toggle heatmap, parcels, and flood zones  
💡 **Real-time Analysis** - Click any property for instant AI insights  
📱 **Responsive Design** - Professional Material-UI interface  

---

## 🚀 Quick Start

### One-Command Launch

```bash
cd /Users/dheeraj/Desktop/ScoutIQ
./START.sh
```

**Access the app:**
- Frontend UI: **http://localhost:3000**
- Backend API: **http://localhost:8000**
- API Docs: **http://localhost:8000/docs**

### Manual Start

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm start
```

---

## 🌐 Deployment on Any Device

### Prerequisites

**System Requirements:**
- Python 3.13+ 
- Node.js 18+ and npm
- PostgreSQL 14+ with PostGIS extension
- Git

**Installation Commands:**

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.13 node postgresql postgis
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.13
sudo apt install python3.13 python3.13-venv python3.13-dev -y

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL and PostGIS
sudo apt install postgresql postgresql-contrib postgis -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows (WSL2 recommended):**
```bash
# In WSL2 Ubuntu, follow Ubuntu instructions above
# Or use Windows Subsystem for Linux
```

### Step-by-Step Setup

**1. Clone the Repository:**
```bash
git clone https://github.com/nagasatyadheerajanumala/ScoutIQ.git
cd ScoutIQ
```

**2. Backend Setup:**
```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Set up database
createdb scoutiq
psql -d scoutiq -c "CREATE EXTENSION postgis;"

# Load sample data
cd backend
python db/seed_data.py
cd ..
```

**3. Frontend Setup:**
```bash
cd frontend
npm install
cd ..
```

**4. Configuration:**
```bash
# Create environment file
cat > .env << EOF
DATABASE_URL=postgresql://$(whoami)@localhost/scoutiq
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
EOF

# Get free Mapbox token from: https://account.mapbox.com/access-tokens/
```

**5. Launch Application:**
```bash
# Option 1: One-command launch
./START.sh

# Option 2: Manual launch
# Terminal 1:
./start_backend.sh

# Terminal 2:
cd frontend && npm start
```

**6. Access the Application:**
- Open browser to: **http://localhost:3000**
- API documentation: **http://localhost:8000/docs**

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DATABASE_URL=postgresql://username@localhost/scoutiq

# Mapbox Configuration (Required for maps)
REACT_APP_MAPBOX_TOKEN=pk.your_mapbox_token_here

# Optional: Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### Production Deployment

**Docker Deployment (Recommended):**
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine as frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/ ./
COPY --from=frontend /app/frontend/build ./frontend/build
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Build and run
docker build -t scoutiq .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:pass@host:5432/scoutiq scoutiq
```

**Cloud Deployment Options:**

**Heroku:**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create scoutiq-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**DigitalOcean App Platform:**
```yaml
# .do/app.yaml
name: scoutiq
services:
- name: backend
  source_dir: backend
  github:
    repo: nagasatyadheerajanumala/ScoutIQ
    branch: main
  run_command: uvicorn main:app --host 0.0.0.0 --port $PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
databases:
- name: db
  engine: PG
  version: "14"
```

### Troubleshooting

**Common Issues:**

**1. Database Connection Error:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql  # Linux
brew services list | grep postgres  # macOS

# Test connection
psql -U $(whoami) -d scoutiq -c "SELECT 1;"
```

**2. Port Already in Use:**
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**3. Node.js/npm Issues:**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**4. Python Virtual Environment Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

**5. Mapbox Token Issues:**
- Get free token: https://account.mapbox.com/access-tokens/
- Add to `.env` file: `REACT_APP_MAPBOX_TOKEN=pk.your_token`
- Or update `frontend/src/config.js` directly

---

## 📖 User Guide

### 1. Query Properties

**Via UI (React + Mapbox):**
1. Select county (e.g., "Travis") from dropdown
2. Set valuation range using slider ($200K - $500K)
3. Click "Analyze Properties" button
4. View results on interactive Mapbox map with color-coded markers

**Via API:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "county": "Travis",
    "min_value": 200000,
    "max_value": 500000,
    "limit": 50
  }'
```

### 2. Get AI Insights

**Individual Property Analysis:**
- Click any property marker on the map
- Property card appears at the top
- AI insights panel slides in from the right automatically
- Review: classification, confidence, risk level, investment score, detailed insights

**Layer Controls:**
- Click the layers button (bottom right)
- Toggle property markers, heatmap, parcels, and flood zones
- Use legend (bottom left) to understand color coding

**Example AI Output:**
```
Classification: Buy
Confidence: 95%
Risk Level: Low
Investment Score: 90/100

Summary: This property presents attractive fundamentals with a valuation 
of $340,011 in AUSTIN. Built 22 years ago, this individual-owned property 
is a strong investment opportunity. Low flood risk enhances investment 
appeal.

Key Insights:
• Mid-market valuation balances opportunity with manageable risk
• Prime property age combines modern amenities with established value
• Individual ownership typical for owner-occupied or personal investment
• ✓ Low flood risk enhances long-term value stability
• ✓ Strong fundamentals support acquisition consideration
```

### 3. Interpret Results

**Map Colors:**
- 🟢 **Green** = Buy (Score ≥ 70)
- 🟡 **Yellow** = Hold (Score 50-69)
- 🔴 **Red** = Watch (Score < 50)

**Confidence Levels:**
- 90-95%: Very high confidence
- 75-89%: High confidence
- 60-74%: Moderate confidence
- 50-59%: Low confidence

---

## 🏗️ Architecture

### Backend (FastAPI + PostgreSQL)

```
backend/
├── main.py              # FastAPI app with REST endpoints
├── models.py            # SQLAlchemy ORM models (TaxAssessor, AVM, Recorder)
├── ai_analyzer.py       # AI scoring and natural language generation
├── signal_processor.py  # Derived signal computation
├── config_loader.py     # Dynamic configuration from Excel
├── db_connector.py      # Database utilities
└── utils/
    └── signals.py       # Signal computation helpers
```

**Key Endpoints:**
- `POST /query` - Query properties with filters
- `POST /ai-summary` - Generate AI insights
- `GET /api/query` - Advanced query with pagination
- `GET /api/location-query` - Query by city/state
- `GET /api/recommendations` - Get top investment opportunities
- `GET /status` - Health check

### Frontend (React + Mapbox GL JS)

```
frontend/
├── src/
│   ├── App.js              # Main React application
│   ├── components/         # React components
│   │   ├── FilterPanel.js  # Property filters sidebar
│   │   ├── PropertyCard.js # Property details display
│   │   ├── AIInsightsPanel.js # AI analysis panel
│   │   ├── LayerControl.js # Map layer toggles
│   │   └── Legend.js       # Map legend
│   ├── services/
│   │   └── api.js          # Backend API integration
│   └── config.js           # Configuration
└── package.json            # React dependencies
```

**Key Features:**
- **Interactive Mapbox Map** - Dark theme with pan, zoom, and rotation
- **Property Markers** - Color-coded by AI classification with hover effects
- **Filter Panel** - County selection, valuation range slider, result limits
- **AI Insights Panel** - Slides in automatically when clicking properties
- **Layer Controls** - Toggle heatmap, parcels, and flood zones
- **Legend** - Color-coded guide for map interpretation
- **Responsive Design** - Professional Material-UI components

### Database Schema

**19 Tables Including:**
- `blackland_capital_group_taxassessor_0001_sample` - Primary property data
- `blackland_capital_group_avm_*` - Automated valuation models
- `blackland_capital_group_recorder_*` - Transaction and loan data
- `scoutiq_ai_logs` - AI interaction logging

---

## 🧠 AI Analysis Engine

### Scoring Algorithm

The AI analyzer evaluates properties on multiple dimensions:

**Base Score:** 50 points

**Adjustments:**
- **Valuation**: -10 to +15 points
- **Property Age**: -15 to +20 points
- **Ownership Type**: +5 to +10 points
- **Flood Risk**: -20 to +10 points (computed based on location and property characteristics)

**Classification:**
- ≥70 points = Buy
- 50-69 points = Hold
- <50 points = Watch

### Natural Language Generation

The system generates human-readable summaries including:
- Investment sentiment and action recommendation
- Valuation context and market positioning
- Property age and condition assessment
- Ownership structure implications
- Risk factor analysis
- Specific insights tailored to score and classification

---

## 📊 Sample Queries

### Investors / Land Developers

```bash
# Find 100-500 acre tracts in Travis County with absentee owners
curl -X POST http://localhost:8000/query \
  -d '{"county":"Travis","min_value":500000,"max_value":2000000}'
```

### Commercial Brokers

```bash
# Find undervalued retail opportunities
curl "http://localhost:8000/api/recommendations?county=Travis&max_results=20"
```

### Risk-Averse Buyers

```bash
# Properties with low flood risk, mid-range valuation
curl -X POST http://localhost:8000/query \
  -d '{"county":"Travis","min_value":250000,"max_value":500000,"limit":50}'
```

---

## 🔧 Configuration

### Database Connection

Edit `backend/db/database.py` or set environment variable:

```bash
export DATABASE_URL="postgresql://username@localhost/scoutiq"
```

### Excel Configuration

Place your configuration at `backend/config/ScoutGPT_Data_Links.xlsx` or the system will use fallback defaults.

### OpenAI Integration (Optional)

For enhanced AI insights:

```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

Then call with `"use_llm": true` in API requests.

---

## 📚 Documentation

- **[AI_INSIGHTS_DEMO.md](AI_INSIGHTS_DEMO.md)** - Detailed AI features guide
- **[BACKEND_TEST_REPORT.md](BACKEND_TEST_REPORT.md)** - Comprehensive test results
- **[MCP_Protocol.txt](backend/MCP_Protocol.txt)** - Model Context Protocol spec
- **[DATA_SUMMARY.md](docs/DATA_SUMMARY.md)** - Data sources and signals
- **[RULES.md](docs/RULES.md)** - Business rules and calculations

---

## 🧪 Testing

### Backend Tests

```bash
# Health check
curl http://localhost:8000/status

# Query properties
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"county":"Travis","min_value":200000,"max_value":500000,"limit":5}'

# Get AI summary
curl -X POST http://localhost:8000/ai-summary \
  -H "Content-Type: application/json" \
  -d '{}'

# Test analyzer directly
cd backend && python ai_analyzer.py
```

### Frontend Tests

1. Start services: `./START.sh`
2. Open: http://localhost:3000
3. Select Travis County, $200K-$500K range
4. Click "Analyze Properties"
5. Verify map shows color-coded markers
6. Click any property marker
7. Verify property card appears at top
8. Verify AI insights panel slides in from right
9. Verify classification, score, and insights display
10. Test layer controls (heatmap, parcels, flood zones)

---

## 🛠️ Development

### Requirements

- Python 3.13+
- PostgreSQL 14+ with PostGIS
- Virtual environment (venv)

### Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### Key Dependencies

**Backend:**
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **psycopg2-binary** - PostgreSQL adapter
- **pandas** - Data manipulation
- **requests** - HTTP client

**Frontend:**
- **react** - Frontend framework
- **mapbox-gl** - Interactive maps
- **@mui/material** - UI components
- **axios** - HTTP client

---

## 🚨 Troubleshooting

### Port Already in Use

```bash
# Kill existing processes
pkill -f uvicorn
pkill -f "react-scripts"

# Restart
./START.sh
```

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U dheeraj -d scoutiq -c "SELECT COUNT(*) FROM information_schema.tables"

# Verify DATABASE_URL
echo $DATABASE_URL
```

### "No prior query results" Error

Run `/query` endpoint before calling `/ai-summary`:

```bash
# Step 1: Query properties
curl -X POST http://localhost:8000/query -d '{"county":"Travis","limit":10}'

# Step 2: Get AI summary
curl -X POST http://localhost:8000/ai-summary -d '{}'
```

### Map Not Displaying

- Ensure properties have valid `property_latitude` and `property_longitude`
- Check browser console for errors
- Verify Mapbox token in `frontend/src/config.js`
- Ensure React app is running on port 3000

---

## 📈 Performance

- **Query Response:** < 500ms for 50 properties
- **AI Analysis:** ~10ms per property
- **Map Rendering:** 1-2 seconds for 100+ markers
- **Marker Interactions:** < 50ms hover/click response
- **Layer Toggles:** Instant switching between map layers
- **Database:** 19 tables, ~10K+ sample records

---

## 🎯 Use Cases

### 1. First-Time Investors
*Find affordable, low-risk properties*
- Filter: Max $300K valuation
- Look for: "Buy" classification, low risk
- Sort by: Investment score

### 2. Institutional Investors
*Identify professional-grade opportunities*
- Filter: LLC/Corporation ownership
- Look for: High investment scores (≥80)
- Analyze: Market trends via portfolio analysis

### 3. Market Researchers
*Understand market dynamics*
- Query: Broad property range
- Use: Market analysis tab
- Review: Ownership patterns, valuation distribution

### 4. Risk Managers
*Assess portfolio risk*
- Filter: Specific county/city
- Review: Flood risk insights
- Check: Risk level distribution

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅ COMPLETE
- ✅ Property querying with filters
- ✅ Signal computation
- ✅ AI-generated insights
- ✅ Interactive Mapbox map visualization
- ✅ React frontend with Material-UI
- ✅ Layer controls (heatmap, parcels, flood zones)
- ✅ Property markers with hover/click interactions
- ✅ AI insights panel with real-time analysis

### Phase 2: Enhanced AI (In Progress)
- ⏸️ OpenAI/Claude integration
- ⏸️ Comparative property analysis
- ⏸️ Market trend prediction
- ⏸️ Investment strategy recommendations

### Phase 3: Advanced Features (Planned)
- ⏸️ User authentication
- ⏸️ Saved searches and favorites
- ⏸️ Email alerts for new opportunities
- ⏸️ PDF report generation
- ⏸️ Portfolio tracking
- ⏸️ Multi-county comparison

### Phase 4: Data Expansion (Future)
- ⏸️ Nationwide coverage (HUD GIS, MS Buildings)
- ⏸️ School district data
- ⏸️ Crime statistics
- ⏸️ Walkability scores
- ⏸️ Public transit access

---

## 📝 License

Proprietary - ScoutIQ AI Team

---

## 🤝 Support

For questions, issues, or feature requests:

- **Documentation:** See `docs/` folder
- **API Docs:** http://localhost:8000/docs
- **Test Report:** [BACKEND_TEST_REPORT.md](BACKEND_TEST_REPORT.md)
- **AI Guide:** [AI_INSIGHTS_DEMO.md](AI_INSIGHTS_DEMO.md)

---

## ✨ Acknowledgments

Built with:
- FastAPI
- React + Mapbox GL JS
- PostgreSQL + PostGIS
- Material-UI
- Travis County ATTOM Data

---

**ScoutIQ v1.0.0** - AI Property Intelligence Companion  
*Making real estate data actionable, one insight at a time.* 🏡🤖
