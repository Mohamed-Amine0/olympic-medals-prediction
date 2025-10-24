/**
 * API Service pour communiquer avec le backend Django REST
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour gérer les erreurs globalement
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Services pour les différentes entités

export const statsService = {
  getOverview: () => api.get('/stats/overview/'),
};

export const gamesService = {
  getAll: (page = 1) => api.get(`/games/?page=${page}`),
  getById: (id) => api.get(`/games/${id}/`),
  getTopCountries: (id) => api.get(`/games/${id}/top_countries/`),
};

export const countriesService = {
  getAll: (page = 1) => api.get(`/countries/?page=${page}`),
  getById: (id) => api.get(`/countries/${id}/`),
  getTop: () => api.get('/countries/top/'),
};

export const athletesService = {
  getAll: (page = 1) => api.get(`/athletes/?page=${page}`),
  getById: (id) => api.get(`/athletes/${id}/`),
};

export const medalsService = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    return api.get(`/medals/?${queryParams}`);
  },
};

export const predictionsService = {
  getAll: (page = 1) => api.get(`/predictions/?page=${page}`),
};

export default api;
