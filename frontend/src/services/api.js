import axios from 'axios';
import { BACKEND_URL } from '../config';

const api = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Query properties with filters
 * @param {Object} filters - { county, minValue, maxValue, limit }
 * @returns {Promise} Response with properties array
 */
export const queryProperties = async (filters) => {
  const response = await api.post('/query', {
    county: filters.county === 'All' ? null : filters.county,
    min_value: filters.minValue,
    max_value: filters.maxValue,
    limit: filters.limit || 100
  });
  return response.data;
};

/**
 * Get AI summary for a property or market analysis
 * @param {string|null} propertyId - Property ID for individual analysis, null for market
 * @param {Object} context - Additional context (county, etc.)
 * @returns {Promise} AI analysis response
 */
export const getAISummary = async (propertyId = null, context = {}) => {
  const payload = { context };
  if (propertyId) {
    payload.property_id = propertyId;
  }
  const response = await api.post('/ai-summary', payload);
  return response.data;
};

/**
 * Get market-level AI analysis
 * @param {Object} context - { county, etc. }
 * @returns {Promise} Market analysis response
 */
export const getMarketAnalysis = async (context = {}) => {
  const response = await api.post('/ai-summary', { context });
  return response.data;
};

/**
 * Check backend status
 * @returns {Promise} Status response
 */
export const checkStatus = async () => {
  const response = await api.get('/status');
  return response.data;
};

/**
 * Get property recommendations
 * @param {string|null} county - County filter
 * @param {number} maxResults - Max number of results
 * @returns {Promise} Recommendations response
 */
export const getRecommendations = async (county = null, maxResults = 20) => {
  const params = new URLSearchParams();
  if (county) params.append('county', county);
  params.append('max_results', maxResults);
  
  const response = await api.get(`/api/recommendations?${params.toString()}`);
  return response.data;
};

/**
 * Query properties by location
 * @param {string} city - City name
 * @param {string} state - State code
 * @param {number} limit - Result limit
 * @returns {Promise} Properties response
 */
export const queryByLocation = async (city, state, limit = 50) => {
  const params = new URLSearchParams();
  if (city) params.append('city', city);
  if (state) params.append('state', state);
  params.append('limit', limit);
  
  const response = await api.get(`/api/location-query?${params.toString()}`);
  return response.data;
};

export default api;

