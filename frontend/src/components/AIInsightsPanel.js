import React from 'react';
import { Drawer, Box, Typography, IconButton, Chip, Divider, LinearProgress } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

export default function AIInsightsPanel({ insights, property, onClose }) {
  if (!insights) return null;

  const analysis = insights.analysis || {};
  const classification = analysis.classification || 'Unknown';
  const confidence = (analysis.confidence || 0) * 100;
  const riskLevel = analysis.risk_level || 'Unknown';
  const score = analysis.investment_score || 0;

  const getClassificationIcon = () => {
    if (classification === 'Buy') return <CheckCircleIcon sx={{ color: '#1BA94C' }} />;
    if (classification === 'Watch') return <WarningIcon sx={{ color: '#E74C3C' }} />;
    return <TrendingUpIcon sx={{ color: '#F0C237' }} />;
  };

  return (
    <Drawer
      anchor="right"
      open={true}
      onClose={onClose}
      PaperProps={{
        sx: {
          width: 400,
          backgroundColor: '#16213e',
          color: '#e0e0e0',
          marginTop: '64px'
        }
      }}
    >
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 3 }}>
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            🤖 AI Investment Analysis
          </Typography>
          <IconButton onClick={onClose} sx={{ color: '#e0e0e0' }}>
            <CloseIcon />
          </IconButton>
        </Box>

        {/* Classification */}
        <Box sx={{ mb: 3, textAlign: 'center' }}>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 1 }}>
            {getClassificationIcon()}
            <Typography variant="h4" sx={{ ml: 1, fontWeight: 700 }}>
              {classification}
            </Typography>
          </Box>
          <Chip 
            label={`${riskLevel} Risk`} 
            color={riskLevel === 'Low' ? 'success' : riskLevel === 'High' ? 'error' : 'warning'}
            size="small"
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Metrics */}
        <Box sx={{ mb: 3 }}>
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="body2">Confidence</Typography>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {confidence.toFixed(0)}%
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={confidence} 
              sx={{ 
                height: 8, 
                borderRadius: 1,
                backgroundColor: 'rgba(255,255,255,0.1)'
              }} 
            />
          </Box>

          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="body2">Investment Score</Typography>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {score}/100
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={score} 
              color={score >= 70 ? 'success' : score >= 50 ? 'warning' : 'error'}
              sx={{ 
                height: 8, 
                borderRadius: 1,
                backgroundColor: 'rgba(255,255,255,0.1)'
              }} 
            />
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Summary */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            Executive Summary
          </Typography>
          <Typography variant="body2" sx={{ lineHeight: 1.7, opacity: 0.9 }}>
            {analysis.summary}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Key Insights */}
        {analysis.insights && analysis.insights.length > 0 && (
          <Box>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Key Insights
            </Typography>
            {analysis.insights.map((insight, idx) => (
              <Box 
                key={idx} 
                sx={{ 
                  mb: 1.5, 
                  p: 1.5, 
                  bgcolor: 'rgba(255,255,255,0.05)', 
                  borderRadius: 1,
                  borderLeft: insight.includes('✓') ? '3px solid #1BA94C' : 
                             insight.includes('⚠️') ? '3px solid #F0C237' : 
                             '3px solid #3498DB'
                }}
              >
                <Typography variant="body2" sx={{ fontSize: '0.9rem', lineHeight: 1.6 }}>
                  {insight}
                </Typography>
              </Box>
            ))}
          </Box>
        )}

        <Box sx={{ mt: 3, p: 2, bgcolor: 'rgba(27,169,76,0.1)', borderRadius: 1 }}>
          <Typography variant="caption" display="block" gutterBottom sx={{ fontWeight: 600 }}>
            💡 Analysis Generated by AI
          </Typography>
          <Typography variant="caption" sx={{ opacity: 0.7 }}>
            This analysis uses property signals, market data, and AI scoring to provide investment guidance.
          </Typography>
        </Box>
      </Box>
    </Drawer>
  );
}
