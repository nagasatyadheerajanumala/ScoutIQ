# 🚀 Quick Start - ScoutIQ React Frontend

## ✅ All Files Created!

All necessary files are now in place:

```
✅ package.json              # Dependencies
✅ public/index.html          # HTML template
✅ src/App.js                # Main application
✅ src/App.css               # Styles
✅ src/index.js              # Entry point
✅ src/index.css             # Global styles
✅ src/config.js             # Configuration
✅ src/services/api.js       # Backend API ← JUST CREATED
✅ src/components/FilterPanel.js      ← JUST CREATED
✅ src/components/PropertyCard.js
✅ src/components/AIInsightsPanel.js
✅ src/components/LayerControl.js
✅ src/components/Legend.js
```

---

## 📦 Step 1: Install Dependencies

```bash
cd /Users/dheeraj/Desktop/ScoutIQ/frontend-react
npm install
```

**This will install:**
- React 18.2.0
- Mapbox GL JS 3.0.1
- react-map-gl 7.1.7
- Material-UI 5.15.0
- Axios 1.6.2
- All dependencies (~5-10 minutes on first run)

---

## 🚀 Step 2: Start the App

```bash
npm start
```

**The app will:**
1. Compile the React code
2. Open automatically at http://localhost:3000
3. Show the ScoutIQ interface

---

## 🔧 Step 3: Ensure Backend is Running

**In a separate terminal:**
```bash
cd /Users/dheeraj/Desktop/ScoutIQ
./start_backend.sh
```

**Verify backend:** http://localhost:8000/status

---

## 🎯 Step 4: Test the App

### 4.1 Filter Properties
- Left sidebar → Select "Travis" county
- Valuation: $200,000 - $500,000
- Click green "Search Properties" button

### 4.2 View Map
- Map centers on Travis County
- Markers appear (green/yellow/red dots)
- Legend shows at bottom left

### 4.3 Click a Marker
- Property card appears at top
- Shows address, valuation, classification
- "AI Analysis Available" indicator

### 4.4 View AI Insights
- AI panel slides in from right automatically
- Shows classification (Buy/Hold/Watch)
- Displays confidence % and investment score
- Lists 6 key insights

### 4.5 Toggle Layers
- Click layers button (bottom right)
- Toggle "Valuation Heatmap" on/off
- See density visualization

---

## 🎨 What You Should See

### Initial View
```
┌─────────────────────────────────────────────────────┐
│ ☰ ScoutIQ - AI Property Intelligence    │ 0 Props  │
├────────┬────────────────────────────────────────────┤
│ 🔍     │                                            │
│ Filters│           Dark Map View                    │
│        │                                            │
│ County │     (Centered on Austin, TX)              │
│ Travis │                                            │
│        │                                            │
│ [$200K]│                                            │
│ [$500K]│                                            │
│        │                                            │
│[Search]│         [Legend]        [Layers]          │
└────────┴────────────────────────────────────────────┘
```

### After Search
```
┌─────────────────────────────────────────────────────┐
│ ☰ ScoutIQ - AI Property Intelligence  │ 50 Props   │
├────────┬────────────────────────────────────────────┤
│        │           ┌──────────────┐                 │
│ Filters│           │Property Card │                 │
│        │           │5408 REGENCY  │                 │
│ County │           │Buy • $340K   │                 │
│ Travis │           └──────────────┘                 │
│        │                                   ┌────────┤
│ Range  │  🟢  🟡  🟢                       │   AI   │
│ Slider │     🔴                            │Insights│
│        │  🟢  🟢     🟡                    │ Panel  │
│        │                                   │        │
│[Search]│  [Legend: Buy/Hold/Watch] [Layers]└────────┤
└────────┴────────────────────────────────────────────┘
```

---

## 🎉 Success Criteria

You'll know it's working when you see:

✅ Dark themed map loads  
✅ Left sidebar with filters appears  
✅ "Search Properties" button is green  
✅ After search: markers appear on map  
✅ Markers are colored (green/yellow/red)  
✅ Clicking marker shows property card  
✅ AI panel slides in from right  
✅ Layer control button (bottom right)  
✅ Legend visible (bottom left)  

---

## 🚨 Troubleshooting

### Issue: `npm install` fails
**Fix:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: "Module not found: Can't resolve './services/api'"
**Fix:** The file is now created! Try:
```bash
npm start
```

### Issue: Map doesn't load
**Causes:** 
- No internet connection
- Mapbox token issue

**Fix:** Check browser console (F12) for errors

### Issue: No properties show up
**Causes:**
- Backend not running
- No data in database

**Fix:** 
```bash
# Check backend
curl http://localhost:8000/status

# Should return: {"database":"Connected","tables_found":19,...}
```

### Issue: Port 3000 already in use
**Fix:**
```bash
# Kill existing process
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm start
```

---

## 📝 File Locations

All files are in: `/Users/dheeraj/Desktop/ScoutIQ/frontend-react/`

**Key files:**
- `src/services/api.js` ← Backend API integration
- `src/components/FilterPanel.js` ← Filter sidebar
- `src/App.js` ← Main application logic
- `src/config.js` ← Mapbox token & settings

---

## 🎯 Next Steps

1. ✅ **Files created** - All components in place
2. ⏳ **Install** - Run `npm install` (~5-10 min)
3. ⏳ **Start** - Run `npm start`
4. ⏳ **Test** - Try the demo flow above
5. ✨ **Enjoy** - Professional property intelligence interface!

---

## 📞 Need Help?

**Check logs:**
```bash
# Browser console (F12) for frontend errors
# Terminal for compilation errors
```

**Verify file exists:**
```bash
ls -l src/services/api.js
# Should show: -rw-r--r-- ... api.js
```

**Re-run verification:**
```bash
./VERIFY_FILES.sh
```

---

## 🎊 You're Ready!

Run these two commands:

```bash
# Terminal 1 - Install & Start React
cd /Users/dheeraj/Desktop/ScoutIQ/frontend-react
npm install && npm start

# Terminal 2 - Backend (if not running)
cd /Users/dheeraj/Desktop/ScoutIQ
./start_backend.sh
```

**URLs:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Happy mapping!** 🗺️✨

