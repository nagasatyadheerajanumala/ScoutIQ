import React from 'react';
import { Paper, Typography, Box, Divider } from '@mui/material';

export default function Legend({ activeLayers }) {
  const classificationItems = [
    { color: '#10B981', label: 'Buy' },
    { color: '#F59E0B', label: 'Hold' },
    { color: '#EF4444', label: 'Watch' },
    { color: '#6B7280', label: 'Unknown' }
  ];

      const floodRiskItems = [
        { color: '#ff4444', label: 'High Risk' },
        { color: '#ffaa44', label: 'Medium Risk' },
        { color: '#44ff44', label: 'Low Risk' },
        { color: '#888888', label: 'Unknown' }
      ];

  const valuationItems = [
    { color: '#888888', label: 'Under $200K' },
    { color: '#ffff00', label: '$200K-$400K' },
    { color: '#ff8800', label: '$400K-$600K' },
    { color: '#ff0000', label: 'Over $600K' }
  ];

  return (
    <Paper sx={{
      position: 'fixed',
      bottom: 20,
      left: 20,
      p: 3,
      background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%)',
      color: '#F8FAFC',
      backdropFilter: 'blur(20px)',
      minWidth: 220,
      maxHeight: 'calc(100vh - 120px)',
      overflow: 'auto',
      zIndex: 1000,
      borderRadius: 3,
      border: '1px solid rgba(148, 163, 184, 0.2)',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      '&::-webkit-scrollbar': {
        width: '6px',
      },
      '&::-webkit-scrollbar-track': {
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '3px',
      },
      '&::-webkit-scrollbar-thumb': {
        background: 'rgba(16, 185, 129, 0.5)',
        borderRadius: '3px',
      },
      '&::-webkit-scrollbar-thumb:hover': {
        background: 'rgba(16, 185, 129, 0.7)',
      }
    }}>
      {activeLayers.properties && (
        <>
          <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
            Classification
          </Typography>
          {classificationItems.map(item => (
            <Box key={item.label} sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
              <Box sx={{ 
                width: 16, 
                height: 16, 
                borderRadius: '50%', 
                bgcolor: item.color, 
                mr: 1,
                border: '2px solid rgba(255,255,255,0.3)'
              }} />
              <Typography variant="caption">{item.label}</Typography>
            </Box>
          ))}
        </>
      )}

      {activeLayers.floodZones && (
        <>
          {activeLayers.properties && <Divider sx={{ my: 1 }} />}
          <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
            Flood Risk
          </Typography>
          {floodRiskItems.map(item => (
            <Box key={item.label} sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
              <Box sx={{ 
                width: 16, 
                height: 16, 
                borderRadius: '50%', 
                bgcolor: item.color, 
                mr: 1,
                border: '2px solid rgba(255,255,255,0.3)'
              }} />
              <Typography variant="caption">{item.label}</Typography>
            </Box>
          ))}
        </>
      )}

      {activeLayers.parcels && (
        <>
          {(activeLayers.properties || activeLayers.floodZones) && <Divider sx={{ my: 1 }} />}
          <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
            Property Values
          </Typography>
          {valuationItems.map(item => (
            <Box key={item.label} sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
              <Box sx={{ 
                width: 16, 
                height: 16, 
                borderRadius: '50%', 
                bgcolor: 'transparent',
                border: `2px solid ${item.color}`,
                mr: 1
              }} />
              <Typography variant="caption">{item.label}</Typography>
            </Box>
          ))}
        </>
      )}

      {activeLayers.heatmap && (
        <>
          {(activeLayers.properties || activeLayers.floodZones || activeLayers.parcels) && <Divider sx={{ my: 1 }} />}
          <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
            Heatmap Intensity
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
            <Box sx={{ 
              width: 60, 
              height: 8, 
              background: 'linear-gradient(to right, rgba(0,100,200,0.1), rgba(255,200,0,0.7), rgba(255,0,0,0.9))',
              mr: 1,
              borderRadius: 1
            }} />
            <Typography variant="caption">Low → High</Typography>
          </Box>
        </>
      )}
    </Paper>
  );
}
