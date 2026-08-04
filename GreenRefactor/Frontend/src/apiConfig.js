// API Base URL configuration helper for production and development deployments

export const API_BASE_URL = (import.meta.env && import.meta.env.VITE_API_BASE_URL) || '';
