# ScoutIQ React Frontend

Professional React + Mapbox GL JS interface with AI-driven property insights, interactive layers, and modern UI.

## 🚀 Quick Start

```bash
# 1. Create all components
chmod +x CREATE_ALL_COMPONENTS.sh
./CREATE_ALL_COMPONENTS.sh

# 2. Install dependencies
npm install

# 3. Start development server
npm start
```

Access at: **http://localhost:3000**

## ✨ Features

### Interactive Map
- **Mapbox GL JS** with dark theme
- **Pan & Zoom** navigation
- **Fullscreen** mode
- **Scale** indicator
- **3D** pitch control

### Property Visualization
- **Color-coded markers**:
  - 🟢 Green = Buy opportunities
  - 🟡 Yellow = Hold candidates
  - 🔴 Red = Watch list
  - 🔵 Blue = Unknown/No data
- **Hover effects** - Scale and highlight on mouse over
- **Click interaction** - View detailed property info + AI insights

### Layer System
- ✅ **Property Markers** - Individual property locations
- ✅ **Valuation Heatmap** - Density visualization of property values
- ⏸️ **Parcels** - Coming soon
- ⏸️ **Flood Zones** - Coming soon

### AI Integration
- **Individual Property Analysis**
  - Buy/Hold/Watch classification
  - Confidence score (0-100%)
  - Risk level assessment
  - Investment score (0-100 points)
  - Natural language summary
  - 6 key insights
  
- **Market Analysis** (accessible via backend)
  - Portfolio-wide trends
  - Buy/Hold/Watch breakdown
  - Average valuation
  - Market sentiment

### UI Components

#### 1. Filter Panel (Left Sidebar)
- County selection dropdown
- Valuation range slider + inputs
- Result limit control
- Search button with loading state
- Quick tips section

#### 2. Property Card (Top Center)
- Property address
- Classification badge
- Valuation, year built
- Owner information
- Quick AI status indicator

#### 3. AI Insights Panel (Right Drawer)
- Slides in when property has AI analysis
- Executive summary
- Confidence progress bar
- Investment score visualization
- Color-coded insights
- Risk level badge

#### 4. Layer Control (Bottom Right)
- Toggle layers on/off
- Enable/disable heatmap
- Future layer additions

#### 5. Legend (Bottom Left)
- Classification color guide
- Always visible for reference

## 🛠️ Technology Stack

- **React 18** - UI framework
- **Mapbox GL JS 3.0** - Interactive maps
- **react-map-gl 7.1** - React wrapper for Mapbox
- **Material-UI 5** - Component library
- **Axios** - HTTP client
- **Emotion** - CSS-in-JS styling

## 📂 Project Structure

```
frontend-react/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── FilterPanel.js      # Left sidebar filters
│   │   ├── PropertyCard.js     # Property details card
│   │   ├── AIInsightsPanel.js  # AI analysis drawer
│   │   ├── LayerControl.js     # Layer toggle panel
│   │   └── Legend.js           # Map legend
│   ├── services/
│   │   └── api.js              # Backend API calls
│   ├── App.js                  # Main application
│   ├── App.css                 # App-specific styles
│   ├── config.js               # Configuration
│   ├── index.js                # Entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies
└── README.md                   # This file
```

## 🎨 Design System

### Color Palette
- **Background**: `#0f172a` (Dark blue-gray)
- **Surface**: `#1a1a2e` (Slightly lighter)
- **Accent**: `#16213e` (Hover states)
- **Text Primary**: `#e0e0e0` (Light gray)
- **Text Secondary**: `#a0a0a0` (Medium gray)

### Status Colors
- **Buy/Success**: `#1BA94C` (Green)
- **Hold/Warning**: `#F0C237` (Yellow)
- **Watch/Error**: `#E74C3C` (Red)
- **Info**: `#3498DB` (Blue)

### Typography
- **System font stack** for native feel
- **Font weights**: 400 (normal), 600 (semi-bold), 700 (bold)

## 🔧 Configuration

Edit `src/config.js`:

```javascript
export const MAPBOX_TOKEN = 'your-mapbox-token';
export const BACKEND_URL = 'http://localhost:8000';
export const MAP_STYLE = 'mapbox://styles/mapbox/dark-v11';
```

## 📡 API Integration

### Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/query` | POST | Search properties with filters |
| `/ai-summary` | POST | Get AI analysis (market or individual) |
| `/status` | GET | Check backend health |

### Example API Calls

**Query Properties:**
```javascript
import { queryProperties } from './services/api';

const filters = {
  county: 'Travis',
  minValue: 200000,
  maxValue: 500000,
  limit: 100
};

const data = await queryProperties(filters);
```

**Get AI Summary:**
```javascript
import { getAISummary } from './services/api';

// Individual property
const insights = await getAISummary('property-id-123');

// Market analysis
const marketData = await getAISummary(null, { county: 'Travis' });
```

## 🎯 Usage Guide

### Basic Workflow

1. **Filter Properties**
   - Select county from dropdown
   - Adjust valuation range with slider
   - Click "Search Properties"

2. **View Results**
   - Map centers on results
   - Markers appear color-coded by classification
   - Legend shows color meanings

3. **Explore Property**
   - Click any marker
   - Property card appears at top
   - View basic details

4. **Get AI Insights**
   - Property card shows "AI Analysis Available"
   - AI panel opens automatically with analysis
   - View classification, score, and insights

5. **Toggle Layers**
   - Click layers button (bottom right)
   - Enable/disable heatmap
   - Additional layers coming soon

### Keyboard Shortcuts

- **Esc** - Close open panels
- **Arrow Keys** - Pan map
- **+/-** - Zoom in/out

## 🚨 Troubleshooting

### Map Not Loading
- Verify Mapbox token in `config.js`
- Check browser console for errors
- Ensure internet connection

### No Properties Showing
- Check backend is running (`http://localhost:8000/status`)
- Verify filters aren't too restrictive
- Check browser console for API errors

### AI Insights Not Loading
- Ensure backend is running
- Check that properties have been queried first
- Verify network tab for API responses

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📦 Build for Production

```bash
# Create optimized build
npm run build

# Serve build folder
npx serve -s build -p 3000
```

## 🔮 Future Enhancements

### Phase 1: Layer Integration
- ✅ Property markers
- ✅ Valuation heatmap
- ⏸️ Parcel boundaries (GeoJSON)
- ⏸️ FEMA flood zones (GeoJSON)
- ⏸️ School districts
- ⏸️ Transit routes

### Phase 2: Advanced Features
- ⏸️ Property comparison side-by-side
- ⏸️ Save favorites to localStorage
- ⏸️ Export filtered results to CSV
- ⏸️ Custom map styling
- ⏸️ 3D building extrusions
- ⏸️ Street view integration

### Phase 3: Collaboration
- ⏸️ User authentication
- ⏸️ Share saved searches
- ⏸️ Team workspaces
- ⏸️ Comment on properties
- ⏸️ Activity feed

## 📄 License

Proprietary - ScoutIQ Team

---

## 🆘 Support

For issues or questions:
- Check browser console for errors
- Verify backend is running
- Review API responses in Network tab
- See main project README for backend setup

---

**ScoutIQ React Frontend v1.0** - Professional Property Intelligence Interface 🏠✨

