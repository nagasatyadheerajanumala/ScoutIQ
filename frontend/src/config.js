// Configuration for ScoutIQ Frontend
// Your personal Mapbox token (free tier: 50,000 loads/month)
export const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || 'pk.eyJ1IjoiZGhlZXJhamFudW1hbGEiLCJhIjoiY21ncmUxbm41MjRpODJucHF4dzV5ajUxOCJ9.t5LeSsJNb-oLZXoCLH2wrg';
export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

// Dark map style - requires Mapbox token above
export const MAP_STYLE = 'mapbox://styles/mapbox/dark-v11';

export const DEFAULT_VIEWPORT = {
  latitude: 30.267,
  longitude: -97.743,
  zoom: 10,
  pitch: 0,
  bearing: 0
};

export const CLASSIFICATION_COLORS = {
  Buy: '#10B981',    // Professional Emerald
  Hold: '#F59E0B',   // Professional Amber
  Watch: '#EF4444',  // Professional Red
  Unknown: '#6B7280' // Professional Gray
};

export const VALUATION_BANDS = {
  Low: '#E74C3C',    // Red
  Mid: '#F0C237',    // Yellow
  High: '#1BA94C'    // Green
};

