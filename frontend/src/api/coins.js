import api from "./axios";

export const getTopCoins = (page = 1, perPage = 50) =>
  api.get("/coins/top", { params: { page, per_page: perPage } });

export const getCoinDetail = (coinId) => api.get(`/coins/${coinId}`);

export const getCoinChart = (coinId, days = 7) =>
  api.get(`/coins/${coinId}/chart`, { params: { days } });

export const searchCoins = (q) => api.get("/coins/search", { params: { q } });

export const getFavorites = () => api.get("/favorites");

export const addFavorite = (data) => api.post("/favorites", data);

export const removeFavorite = (coinId) => api.delete(`/favorites/${coinId}`);

export const checkFavorite = (coinId) => api.get(`/favorites/${coinId}/check`);

export const getAlerts = () => api.get("/alerts");

export const createAlert = (data) => api.post("/alerts", data);

export const deleteAlert = (alertId) => api.delete(`/alerts/${alertId}`);

export const convertCurrency = (from_id, to_id, amount) =>
  api.get("/converter/convert", { params: { from_id, to_id, amount } });

export const getPopularCoins = () => api.get("/converter/popular-coins");

export const getFiatList = () => api.get("/converter/fiat-list");