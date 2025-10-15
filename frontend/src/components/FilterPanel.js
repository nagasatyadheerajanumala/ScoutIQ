import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
  Divider,
  CircularProgress
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const COUNTIES = ['All', 'Travis', 'Williamson', 'Hays', 'Bastrop', 'Caldwell'];

export default function FilterPanel({ filters, onSubmit, loading }) {
  const [localFilters, setLocalFilters] = useState(filters);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(localFilters);
  };

  const handleSliderChange = (event, newValue) => {
    setLocalFilters(prev => ({
      ...prev,
      minValue: newValue[0],
      maxValue: newValue[1]
    }));
  };

  return (
    <Box sx={{ 
      p: 4, 
      backgroundColor: '#0F172A',
      color: '#F8FAFC',
      height: '100%',
      overflow: 'auto',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
      borderRight: '1px solid rgba(148, 163, 184, 0.1)'
    }}>
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        mb: 4,
        pb: 2,
        borderBottom: '2px solid rgba(16, 185, 129, 0.2)'
      }}>
        <Box sx={{ 
          width: 40, 
          height: 40, 
          borderRadius: 2, 
          background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mr: 2,
          boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)'
        }}>
          <SearchIcon sx={{ color: 'white', fontSize: 20 }} />
        </Box>
        <Typography variant="h5" sx={{ 
          fontWeight: 700, 
          color: '#F8FAFC',
          fontSize: '1.5rem',
          letterSpacing: '-0.025em'
        }}>
          Property Intelligence
        </Typography>
      </Box>

      {/* Active Filters Summary */}
      <Box sx={{ 
        mb: 4,
        p: 3,
        background: 'rgba(16, 185, 129, 0.05)',
        borderRadius: 3,
        border: '1px solid rgba(16, 185, 129, 0.2)',
        backdropFilter: 'blur(10px)'
      }}>
        <Typography variant="subtitle1" sx={{ 
          color: '#F8FAFC', 
          fontWeight: 600, 
          mb: 2,
          fontSize: '1rem',
          display: 'flex',
          alignItems: 'center'
        }}>
          <Box sx={{ 
            width: 8, 
            height: 8, 
            borderRadius: '50%', 
            backgroundColor: '#10B981', 
            mr: 1.5 
          }} />
          Active Filters
        </Typography>
        <Box sx={{ display: 'grid', gap: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ color: '#94A3B8', fontWeight: 500 }}>Market Area</Typography>
            <Box sx={{ 
              px: 2, 
              py: 1, 
              backgroundColor: 'rgba(16, 185, 129, 0.15)',
              borderRadius: 2,
              border: '1px solid rgba(16, 185, 129, 0.3)'
            }}>
              <Typography variant="body2" sx={{ 
                color: '#10B981', 
                fontWeight: 600,
                fontSize: '0.875rem'
              }}>
                {localFilters.county} County
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ color: '#94A3B8', fontWeight: 500 }}>Price Range</Typography>
            <Box sx={{ 
              px: 2, 
              py: 1, 
              backgroundColor: 'rgba(16, 185, 129, 0.15)',
              borderRadius: 2,
              border: '1px solid rgba(16, 185, 129, 0.3)'
            }}>
              <Typography variant="body2" sx={{ 
                color: '#10B981', 
                fontWeight: 600,
                fontSize: '0.875rem'
              }}>
                ${(localFilters.minValue / 1000).toFixed(0)}K - ${(localFilters.maxValue / 1000).toFixed(0)}K
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ color: '#94A3B8', fontWeight: 500 }}>Results</Typography>
            <Box sx={{ 
              px: 2, 
              py: 1, 
              backgroundColor: 'rgba(16, 185, 129, 0.15)',
              borderRadius: 2,
              border: '1px solid rgba(16, 185, 129, 0.3)'
            }}>
              <Typography variant="body2" sx={{ 
                color: '#10B981', 
                fontWeight: 600,
                fontSize: '0.875rem'
              }}>
                {localFilters.limit} Properties
              </Typography>
            </Box>
          </Box>
        </Box>
      </Box>

      <form onSubmit={handleSubmit}>
        {/* Market Area Selection */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="subtitle1" sx={{ 
            color: '#F8FAFC', 
            fontWeight: 600, 
            mb: 2,
            fontSize: '1rem'
          }}>
            Market Area
          </Typography>
          <FormControl fullWidth>
            <InputLabel sx={{ 
              color: '#94A3B8',
              '&.Mui-focused': { color: '#10B981' }
            }}>
              Select County
            </InputLabel>
            <Select
              value={localFilters.county}
              label="Select County"
              onChange={(e) => setLocalFilters({...localFilters, county: e.target.value})}
              sx={{ 
                color: '#F8FAFC',
                backgroundColor: 'rgba(15, 23, 42, 0.8)',
                borderRadius: 2,
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(148, 163, 184, 0.3)',
                  borderWidth: 1,
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(16, 185, 129, 0.5)',
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  borderColor: '#10B981',
                  borderWidth: 2,
                }
              }}
            >
              {COUNTIES.map(county => (
                <MenuItem key={county} value={county} sx={{ 
                  color: '#F8FAFC',
                  '&:hover': { backgroundColor: 'rgba(16, 185, 129, 0.1)' },
                  '&.Mui-selected': { backgroundColor: 'rgba(16, 185, 129, 0.2)' }
                }}>
                  {county}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        {/* Price Range */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="subtitle1" sx={{ 
            color: '#F8FAFC', 
            fontWeight: 600, 
            mb: 2,
            fontSize: '1rem'
          }}>
            Price Range
          </Typography>
          <Box sx={{ 
            p: 3, 
            backgroundColor: 'rgba(15, 23, 42, 0.8)', 
            borderRadius: 3,
            border: '1px solid rgba(148, 163, 184, 0.2)',
            backdropFilter: 'blur(10px)'
          }}>
            <Slider
              value={[localFilters.minValue, localFilters.maxValue]}
              onChange={handleSliderChange}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `$${(value / 1000).toFixed(0)}K`}
              min={0}
              max={2000000}
              step={50000}
              sx={{
                color: '#10B981',
                '& .MuiSlider-thumb': {
                  backgroundColor: '#10B981',
                  width: 24,
                  height: 24,
                  border: '4px solid #F8FAFC',
                  boxShadow: '0 4px 12px rgba(16, 185, 129, 0.4)',
                  '&:hover': {
                    boxShadow: '0 6px 16px rgba(16, 185, 129, 0.6)',
                  }
                },
                '& .MuiSlider-track': {
                  backgroundColor: '#10B981',
                  height: 8,
                  borderRadius: 4,
                },
                '& .MuiSlider-rail': {
                  backgroundColor: 'rgba(148, 163, 184, 0.3)',
                  height: 8,
                  borderRadius: 4,
                }
              }}
            />
          </Box>
        </Box>
        {/* Price Input Fields */}
        <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
          <TextField
            label="Minimum Price"
            type="number"
            value={localFilters.minValue}
            onChange={(e) => setLocalFilters({...localFilters, minValue: parseInt(e.target.value) || 0})}
            InputProps={{ startAdornment: '$' }}
            size="small"
            fullWidth
            sx={{
              backgroundColor: 'rgba(15, 23, 42, 0.8)',
              borderRadius: 2,
              '& .MuiInputLabel-root': { 
                color: '#94A3B8',
                '&.Mui-focused': { color: '#10B981' }
              },
              '& .MuiOutlinedInput-root': {
                color: '#F8FAFC',
                '& fieldset': { 
                  borderColor: 'rgba(148, 163, 184, 0.3)',
                  borderWidth: 1,
                },
                '&:hover fieldset': { 
                  borderColor: 'rgba(16, 185, 129, 0.5)',
                },
                '&.Mui-focused fieldset': { 
                  borderColor: '#10B981',
                  borderWidth: 2,
                }
              }
            }}
          />
          <TextField
            label="Maximum Price"
            type="number"
            value={localFilters.maxValue}
            onChange={(e) => setLocalFilters({...localFilters, maxValue: parseInt(e.target.value) || 0})}
            InputProps={{ startAdornment: '$' }}
            size="small"
            fullWidth
            sx={{
              backgroundColor: 'rgba(15, 23, 42, 0.8)',
              borderRadius: 2,
              '& .MuiInputLabel-root': { 
                color: '#94A3B8',
                '&.Mui-focused': { color: '#10B981' }
              },
              '& .MuiOutlinedInput-root': {
                color: '#F8FAFC',
                '& fieldset': { 
                  borderColor: 'rgba(148, 163, 184, 0.3)',
                  borderWidth: 1,
                },
                '&:hover fieldset': { 
                  borderColor: 'rgba(16, 185, 129, 0.5)',
                },
                '&.Mui-focused fieldset': { 
                  borderColor: '#10B981',
                  borderWidth: 2,
                }
              }
            }}
          />
        </Box>

        {/* Results Limit */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="subtitle1" sx={{ 
            color: '#F8FAFC', 
            fontWeight: 600, 
            mb: 2,
            fontSize: '1rem'
          }}>
            Results Limit
          </Typography>
          <TextField
            label="Number of Properties"
            type="number"
            value={localFilters.limit}
            onChange={(e) => setLocalFilters({...localFilters, limit: parseInt(e.target.value) || 100})}
            size="small"
            fullWidth
            sx={{ 
              backgroundColor: 'rgba(15, 23, 42, 0.8)',
              borderRadius: 2,
              '& .MuiInputLabel-root': { 
                color: '#94A3B8',
                '&.Mui-focused': { color: '#10B981' }
              },
              '& .MuiOutlinedInput-root': {
                color: '#F8FAFC',
                '& fieldset': { 
                  borderColor: 'rgba(148, 163, 184, 0.3)',
                  borderWidth: 1,
                },
                '&:hover fieldset': { 
                  borderColor: 'rgba(16, 185, 129, 0.5)',
                },
                '&.Mui-focused fieldset': { 
                  borderColor: '#10B981',
                  borderWidth: 2,
                }
              }
            }}
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Search Button */}
        <Button
          type="submit"
          variant="contained"
          fullWidth
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
          disabled={loading}
          sx={{ 
            py: 3,
            fontSize: '1.1rem',
            fontWeight: 700,
            background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
            borderRadius: 3,
            boxShadow: '0 8px 24px rgba(16, 185, 129, 0.4)',
            textTransform: 'none',
            letterSpacing: '0.025em',
            '&:hover': { 
              background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
              boxShadow: '0 12px 32px rgba(16, 185, 129, 0.6)',
              transform: 'translateY(-2px)'
            },
            '&:active': {
              transform: 'translateY(0)',
              boxShadow: '0 4px 16px rgba(16, 185, 129, 0.4)'
            },
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
          }}
        >
          {loading ? 'Analyzing Properties...' : 'Analyze Properties'}
        </Button>
      </form>

      {/* Quick Tips */}
      <Box sx={{ 
        mt: 4, 
        p: 3, 
        background: 'rgba(15, 23, 42, 0.6)', 
        borderRadius: 3,
        border: '1px solid rgba(148, 163, 184, 0.1)',
        backdropFilter: 'blur(10px)'
      }}>
        <Typography variant="subtitle2" sx={{ 
          color: '#F8FAFC', 
          fontWeight: 600, 
          mb: 2,
          display: 'flex',
          alignItems: 'center'
        }}>
          <Box sx={{ 
            width: 6, 
            height: 6, 
            borderRadius: '50%', 
            backgroundColor: '#F59E0B', 
            mr: 1.5 
          }} />
          Quick Tips
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
          <Typography variant="body2" sx={{ color: '#94A3B8', fontSize: '0.875rem' }}>
            • Use sliders for quick range adjustments
          </Typography>
          <Typography variant="body2" sx={{ color: '#94A3B8', fontSize: '0.875rem' }}>
            • Click markers for AI insights
          </Typography>
          <Typography variant="body2" sx={{ color: '#94A3B8', fontSize: '0.875rem' }}>
            • Toggle layers for detailed view
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}

