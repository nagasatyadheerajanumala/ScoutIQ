import React, { useState, useCallback } from 'react';
import Map, { Marker, Source, Layer, NavigationControl, FullscreenControl, ScaleControl } from 'react-map-gl';
import { 
  Box, 
  Drawer, 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton,
  Fab,
  Chip,
  Alert
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import LayersIcon from '@mui/icons-material/Layers';
import { MAPBOX_TOKEN, MAP_STYLE, DEFAULT_VIEWPORT, CLASSIFICATION_COLORS } from './config';
import FilterPanel from './components/FilterPanel';
import PropertyCard from './components/PropertyCard';
import LayerControl from './components/LayerControl';
import AIInsightsPanel from './components/AIInsightsPanel';
import Legend from './components/Legend';
import { queryProperties, getAISummary } from './services/api';
import './App.css';

const DRAWER_WIDTH = 360;

function App() {
  // State management
  const [viewport, setViewport] = useState(DEFAULT_VIEWPORT);
  const [properties, setProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [aiInsights, setAIInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(true);
  const [layerControlOpen, setLayerControlOpen] = useState(false);
  const [activeLayers, setActiveLayers] = useState({
    properties: true,
    heatmap: false,
    parcels: false,
    floodZones: false
  });
  const [filters, setFilters] = useState({
    county: 'Travis',
    minValue: 200000,
    maxValue: 500000,
    limit: 100
  });

  // Query properties on mount and filter change
  const handleQueryProperties = useCallback(async (newFilters) => {
    setLoading(true);
    setError(null);
    try {
      const data = await queryProperties(newFilters || filters);
      setProperties(data.properties || []);
      
      // Center map on results
      if (data.properties && data.properties.length > 0) {
        const lats = data.properties.map(p => parseFloat(p.property_latitude)).filter(l => !isNaN(l));
        const lons = data.properties.map(p => parseFloat(p.property_longitude)).filter(l => !isNaN(l));
        
        if (lats.length > 0 && lons.length > 0) {
          setViewport(v => ({
            ...v,
            latitude: lats.reduce((a, b) => a + b) / lats.length,
            longitude: lons.reduce((a, b) => a + b) / lons.length,
            zoom: 11
          }));
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to load properties');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Handle property marker click
  const handlePropertyClick = useCallback(async (property) => {
    setSelectedProperty(property);
    setAIInsights(null); // Clear previous insights
    
    // Fetch AI insights for this property
    try {
      const insights = await getAISummary(property.attom_id);
      setAIInsights(insights);
    } catch (err) {
      console.error('Failed to fetch AI insights:', err);
    }
  }, []);

  // Handle filter submission
  const handleFilterSubmit = (newFilters) => {
    setFilters(newFilters);
    handleQueryProperties(newFilters);
  };

  // Handle map resize when drawer opens/closes
  React.useEffect(() => {
    const timer = setTimeout(() => {
      // Trigger window resize event for map to respond
      window.dispatchEvent(new Event('resize'));
    }, 350); // Slightly longer to ensure animation completes

    return () => clearTimeout(timer);
  }, [drawerOpen]);

  // Get marker color based on classification
  const getMarkerColor = (property) => {
    const classification = property.classification || property.classification_hint || 'Unknown';
    return CLASSIFICATION_COLORS[classification] || CLASSIFICATION_COLORS.Unknown;
  };

  // Create GeoJSON for heatmap
  const createHeatmapData = () => {
    if (!properties || properties.length === 0) return null;
    
    return {
      type: 'FeatureCollection',
      features: properties.map(p => ({
        type: 'Feature',
        properties: {
          value: parseFloat(p.primary_valuation) || 0
        },
        geometry: {
          type: 'Point',
          coordinates: [
            parseFloat(p.property_longitude),
            parseFloat(p.property_latitude)
          ]
        }
      })).filter(f => !isNaN(f.geometry.coordinates[0]) && !isNaN(f.geometry.coordinates[1]))
    };
  };

  const heatmapData = createHeatmapData();

  return (
    <Box sx={{ 
      display: 'flex', 
      height: '100vh', 
      width: '100vw',
      overflow: 'hidden',
      position: 'fixed',
      top: 0,
      left: 0
    }}>
      {/* AppBar */}
      <AppBar 
        position="fixed" 
        sx={{ 
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
          boxShadow: '0 4px 20px rgba(0,0,0,0.4)',
          borderBottom: '1px solid rgba(148, 163, 184, 0.1)'
        }}
      >
        <Toolbar sx={{ py: 1 }}>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setDrawerOpen(!drawerOpen)}
            sx={{ 
              mr: 3,
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              '&:hover': { backgroundColor: 'rgba(16, 185, 129, 0.2)' }
            }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <Box sx={{ 
              width: 32, 
              height: 32, 
              borderRadius: 2, 
              background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
              boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)'
            }}>
              <Typography sx={{ color: 'white', fontWeight: 700, fontSize: '1.2rem' }}>S</Typography>
            </Box>
            <Typography variant="h5" component="div" sx={{ 
              fontWeight: 700, 
              color: '#F8FAFC',
              letterSpacing: '-0.025em'
            }}>
              ScoutIQ
            </Typography>
            <Typography variant="subtitle1" sx={{ 
              ml: 2, 
              color: '#94A3B8',
              fontWeight: 500
            }}>
              AI Property Intelligence
            </Typography>
          </Box>
          <Chip 
            label={`${properties.length} Properties`} 
            sx={{ 
              background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
              color: 'white',
              fontWeight: 600,
              fontSize: '0.875rem',
              px: 2,
              py: 1,
              boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)',
              mr: 2
            }}
          />
          {loading && (
            <Chip 
              label="Analyzing..." 
              sx={{ 
                background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
                color: 'white',
                fontWeight: 600,
                fontSize: '0.875rem',
                px: 2,
                py: 1,
                boxShadow: '0 4px 12px rgba(245, 158, 11, 0.3)'
              }}
            />
          )}
        </Toolbar>
      </AppBar>

      {/* Left Drawer - Filters */}
      <Drawer
        variant="persistent"
        anchor="left"
        open={drawerOpen}
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
            background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
            color: '#F8FAFC',
            marginTop: '64px',
            zIndex: 1200,
            borderRight: '1px solid rgba(148, 163, 184, 0.1)',
            boxShadow: '4px 0 20px rgba(0,0,0,0.3)'
          },
        }}
      >
        <FilterPanel 
          filters={filters}
          onSubmit={handleFilterSubmit}
          loading={loading}
        />
      </Drawer>

      {/* Main Map Area */}
      <Box
        component="main"
        sx={{
          position: 'fixed',
          top: '64px',
          left: drawerOpen ? `${DRAWER_WIDTH}px` : '0px',
          right: '0px',
          bottom: '0px',
          transition: 'left 0.3s ease-in-out',
          zIndex: 1,
          width: drawerOpen ? `calc(100vw - ${DRAWER_WIDTH}px)` : '100vw'
        }}
      >
        {error && (
          <Alert 
            severity="error" 
            onClose={() => setError(null)}
            sx={{ 
              position: 'absolute', 
              top: 16, 
              left: '50%', 
              transform: 'translateX(-50%)',
              zIndex: 1000,
              maxWidth: 500
            }}
          >
            {error}
          </Alert>
        )}

        <Map
          {...viewport}
          onMove={evt => setViewport(evt.viewState)}
          onClick={() => {
            // Deselect property when clicking map background
            setSelectedProperty(null);
            setAIInsights(null);
          }}
          onLoad={(map) => {
            // Store map instance for potential future use
            window.mapboxMap = map;
          }}
          style={{ 
            width: '100%', 
            height: '100%'
          }}
          mapStyle={MAP_STYLE}
          mapboxAccessToken={MAPBOX_TOKEN}
          interactiveLayerIds={[]} // Allow click-through to map
          reuseMaps={true}
          onError={(e) => {
            console.error('Map error:', e);
            setError('Map failed to load. Please check your Mapbox token in GET_MAPBOX_TOKEN.md');
          }}
        >
          {/* Navigation Controls */}
          <NavigationControl position="top-right" />
          <FullscreenControl position="top-right" />
          <ScaleControl position="bottom-right" />

          {/* Heatmap Layer */}
          {activeLayers.heatmap && heatmapData && (
            <Source id="heatmap-data" type="geojson" data={heatmapData}>
              <Layer
                id="heatmap-layer"
                type="heatmap"
                paint={{
                  'heatmap-weight': [
                    'interpolate',
                    ['linear'],
                    ['get', 'value'],
                    0, 0,
                    100000, 0.2,
                    250000, 0.4,
                    500000, 0.7,
                    750000, 0.9,
                    1000000, 1
                  ],
                  'heatmap-intensity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    0, 1,
                    15, 3
                  ],
                  'heatmap-color': [
                    'interpolate',
                    ['linear'],
                    ['heatmap-density'],
                    0, 'rgba(0,0,0,0)',
                    0.1, 'rgba(0,100,200,0.1)',
                    0.2, 'rgba(0,150,255,0.3)',
                    0.4, 'rgba(0,200,255,0.5)',
                    0.6, 'rgba(255,200,0,0.7)',
                    0.8, 'rgba(255,100,0,0.8)',
                    1, 'rgba(255,0,0,0.9)'
                  ],
                  'heatmap-radius': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    0, 2,
                    15, 20
                  ],
                  'heatmap-opacity': 0.8
                }}
              />
            </Source>
          )}

          {/* Flood Risk Zones - Show as colored circles */}
          {activeLayers.floodZones && properties.length > 0 && (
            <Source id="flood-zones" type="geojson" data={{
              type: 'FeatureCollection',
              features: properties.map(p => ({
                type: 'Feature',
                properties: {
                  flood_risk: p.flood_risk || 'Unknown',
                  attom_id: p.attom_id
                },
                geometry: {
                  type: 'Point',
                  coordinates: [parseFloat(p.property_longitude), parseFloat(p.property_latitude)]
                }
              })).filter(f => !isNaN(f.geometry.coordinates[0]) && !isNaN(f.geometry.coordinates[1]))
            }}>
              <Layer
                id="flood-zones-layer"
                type="circle"
                paint={{
                  'circle-radius': 12,
                  'circle-color': [
                    'case',
                    ['==', ['get', 'flood_risk'], 'High'], '#ff4444',
                    ['==', ['get', 'flood_risk'], 'Medium'], '#ffaa44',
                    ['==', ['get', 'flood_risk'], 'Low'], '#44ff44',
                    '#888888'
                  ],
                  'circle-opacity': 0.9,
                  'circle-stroke-width': 3,
                  'circle-stroke-color': '#ffffff'
                }}
              />
            </Source>
          )}

          {/* Property Boundaries - Show as outlined circles */}
          {activeLayers.parcels && properties.length > 0 && (
            <Source id="property-boundaries" type="geojson" data={{
              type: 'FeatureCollection',
              features: properties.map(p => ({
                type: 'Feature',
                properties: {
                  attom_id: p.attom_id,
                  valuation: p.primary_valuation || 0
                },
                geometry: {
                  type: 'Point',
                  coordinates: [parseFloat(p.property_longitude), parseFloat(p.property_latitude)]
                }
              })).filter(f => !isNaN(f.geometry.coordinates[0]) && !isNaN(f.geometry.coordinates[1]))
            }}>
              <Layer
                id="property-boundaries-layer"
                type="circle"
                paint={{
                  'circle-radius': 16,
                  'circle-color': 'transparent',
                  'circle-stroke-width': 4,
                  'circle-stroke-color': [
                    'interpolate',
                    ['linear'],
                    ['get', 'valuation'],
                    0, '#666666',
                    200000, '#ffff00',
                    400000, '#ff8800',
                    600000, '#ff0000'
                  ],
                  'circle-stroke-opacity': 0.9
                }}
              />
            </Source>
          )}

          {/* Property Markers */}
          {activeLayers.properties && properties.map((property, index) => {
            const lat = parseFloat(property.property_latitude);
            const lon = parseFloat(property.property_longitude);
            
            if (isNaN(lat) || isNaN(lon)) return null;
            
            const color = getMarkerColor(property);
            const isSelected = selectedProperty?.attom_id === property.attom_id;
            
            return (
              <Marker
                key={`${property.attom_id}-${index}`}
                latitude={lat}
                longitude={lon}
                anchor="center"
                onClick={(e) => {
                  e.originalEvent.stopPropagation();
                  handlePropertyClick(property);
                }}
              >
                <div
                  className="property-marker"
                  style={{
                    backgroundColor: color,
                    transform: isSelected ? 'scale(1.4)' : 'scale(1)',
                    boxShadow: isSelected 
                      ? `0 0 25px ${color}, 0 0 50px rgba(255,255,255,0.3)` 
                      : `0 3px 12px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.2)`,
                    border: isSelected ? '4px solid white' : '3px solid rgba(255,255,255,0.8)',
                    cursor: 'pointer',
                    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                    filter: isSelected ? 'brightness(1.2)' : 'brightness(1)',
                  }}
                />
              </Marker>
            );
          })}
        </Map>

        {/* Layer Control Button */}
        <Fab
          color="primary"
          size="medium"
          onClick={() => setLayerControlOpen(!layerControlOpen)}
          sx={{
            position: 'fixed',
            top: 80,
            right: 320,
            zIndex: 1000,
            backgroundColor: '#1a1a2e',
            '&:hover': { backgroundColor: '#16213e' }
          }}
        >
          <LayersIcon />
        </Fab>

        {/* Legend */}
        <Legend activeLayers={activeLayers} />

        {/* Layer Control Panel */}
        {layerControlOpen && (
          <LayerControl
            activeLayers={activeLayers}
            onToggle={(layer) => setActiveLayers(prev => ({
              ...prev,
              [layer]: !prev[layer]
            }))}
            onClose={() => setLayerControlOpen(false)}
          />
        )}

        {/* Property Details Card */}
        {selectedProperty && (
          <PropertyCard
            property={selectedProperty}
            aiInsights={aiInsights}
            onClose={() => {
              setSelectedProperty(null);
              setAIInsights(null);
            }}
          />
        )}

        {/* AI Insights Panel */}
        {aiInsights && (
          <AIInsightsPanel
            insights={aiInsights}
            property={selectedProperty}
            onClose={() => setAIInsights(null)}
          />
        )}
      </Box>
    </Box>
  );
}

export default App;

