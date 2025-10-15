import React from 'react';
import { Card, CardContent, Typography, IconButton, Box, Chip, Divider } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import HomeIcon from '@mui/icons-material/Home';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';

export default function PropertyCard({ property, aiInsights, onClose }) {
  const valuation = parseFloat(property.primary_valuation) || 0;
  const classification = property.classification || property.classification_hint || 'Unknown';
  
  const getClassificationColor = (cls) => {
    const colors = { Buy: 'success', Hold: 'warning', Watch: 'error', Unknown: 'default' };
    return colors[cls] || 'default';
  };

  return (
    <Card sx={{
      position: 'absolute',
      top: 16,
      left: '50%',
      transform: 'translateX(-50%)',
      width: 400,
      maxWidth: '90vw',
      zIndex: 1000,
      backgroundColor: '#1a1a2e',
      color: '#e0e0e0',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)'
    }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
          <Typography variant="h6" component="div" sx={{ flex: 1 }}>
            <HomeIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            Property Details
          </Typography>
          <IconButton size="small" onClick={onClose} sx={{ color: '#e0e0e0' }}>
            <CloseIcon />
          </IconButton>
        </Box>

        <Typography variant="body2" color="text.secondary" gutterBottom>
          {property.property_address_full}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {property.property_address_city}, {property.property_address_state} {property.property_address_zip}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
          <Chip 
            label={classification} 
            color={getClassificationColor(classification)} 
            size="small" 
          />
          <Chip 
            label={property.valuation_band || 'N/A'} 
            variant="outlined" 
            size="small" 
          />
          <Chip 
            label={property.ownership_type || 'Unknown'} 
            variant="outlined" 
            size="small" 
          />
        </Box>

        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 2 }}>
          <Box>
            <Typography variant="caption" color="text.secondary">Valuation</Typography>
            <Typography variant="body1" sx={{ fontWeight: 600 }}>
              <AttachMoneyIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
              {valuation.toLocaleString()}
            </Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">Year Built</Typography>
            <Typography variant="body1" sx={{ fontWeight: 600 }}>
              {property.year_built || 'N/A'}
            </Typography>
          </Box>
        </Box>

        {property.party_owner1_name_full && (
          <Box sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">Owner</Typography>
            <Typography variant="body2">
              {property.party_owner1_name_full}
            </Typography>
          </Box>
        )}

        {aiInsights && (
          <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(27,169,76,0.1)', borderRadius: 1 }}>
            <Typography variant="caption" sx={{ fontWeight: 600 }}>
              🤖 AI Analysis Available - Click "View AI Insights" for details
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
