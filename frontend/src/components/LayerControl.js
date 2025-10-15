import React from 'react';
import { Paper, Typography, Switch, FormControlLabel, IconButton, Box, Divider } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

export default function LayerControl({ activeLayers, onToggle, onClose }) {
  return (
    <Paper sx={{
      position: 'fixed',
      top: 140,
      right: 320,
      width: 280,
      p: 2,
      backgroundColor: '#1a1a2e',
      color: '#e0e0e0',
      zIndex: 1000,
      maxHeight: 'calc(100vh - 160px)',
      overflow: 'auto',
      '&::-webkit-scrollbar': {
        width: '6px',
      },
      '&::-webkit-scrollbar-track': {
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '3px',
      },
      '&::-webkit-scrollbar-thumb': {
        background: 'rgba(255,255,255,0.3)',
        borderRadius: '3px',
      },
      '&::-webkit-scrollbar-thumb:hover': {
        background: 'rgba(255,255,255,0.5)',
      }
    }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Map Layers</Typography>
        <IconButton size="small" onClick={onClose} sx={{ color: '#e0e0e0' }}>
          <CloseIcon />
        </IconButton>
      </Box>

      <Divider sx={{ mb: 2 }} />

      <FormControlLabel
        control={
          <Switch 
            checked={activeLayers.properties} 
            onChange={() => onToggle('properties')}
            color="success"
          />
        }
        label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ 
              width: 12, 
              height: 12, 
              borderRadius: '50%', 
              bgcolor: '#00C851', 
              mr: 1 
            }} />
            Property Markers
          </Box>
        }
      />
      
      <FormControlLabel
        control={
          <Switch 
            checked={activeLayers.heatmap} 
            onChange={() => onToggle('heatmap')}
            color="primary"
          />
        }
        label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ 
              width: 12, 
              height: 8, 
              background: 'linear-gradient(to right, #0066cc, #ffcc00, #ff0000)',
              mr: 1,
              borderRadius: 1
            }} />
            Valuation Heatmap
          </Box>
        }
      />

      <FormControlLabel
        control={
          <Switch 
            checked={activeLayers.parcels} 
            onChange={() => onToggle('parcels')}
            color="warning"
          />
        }
        label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ 
              width: 12, 
              height: 12, 
              borderRadius: '50%', 
              bgcolor: 'transparent',
              border: '2px solid #FF8800',
              mr: 1 
            }} />
            Property Boundaries
          </Box>
        }
      />

      <FormControlLabel
        control={
          <Switch 
            checked={activeLayers.floodZones} 
            onChange={() => onToggle('floodZones')}
            color="error"
          />
        }
        label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ 
              width: 12, 
              height: 12, 
              borderRadius: '50%', 
              bgcolor: '#FF4444', 
              mr: 1 
            }} />
            Flood Risk Zones
          </Box>
        }
      />

      <Box sx={{ mt: 2, p: 1, bgcolor: 'rgba(255,255,255,0.05)', borderRadius: 1 }}>
        <Typography variant="caption" sx={{ opacity: 0.7, display: 'block', mb: 1 }}>
          💡 <strong>Pro Tip:</strong> Turn off other layers for clearer view
        </Typography>
        <Typography variant="caption" sx={{ opacity: 0.6, fontSize: '0.7rem' }}>
          • Property Markers: Colored by classification<br/>
          • Heatmap: Shows valuation density<br/>
          • Boundaries: Colored by property value<br/>
          • Flood Zones: Colored by risk level
        </Typography>
      </Box>
    </Paper>
  );
}
