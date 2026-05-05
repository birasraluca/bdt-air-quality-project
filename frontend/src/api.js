import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export async function getSummary() {
  const response = await axios.get(`${API_BASE_URL}/api/summary`);
  return response.data;
}

export async function getCities() {
  const response = await axios.get(`${API_BASE_URL}/api/cities`);
  return response.data;
}

export async function getParameters() {
  const response = await axios.get(`${API_BASE_URL}/api/parameters`);
  return response.data;
}

export async function getPollution(city, parameter) {
  const response = await axios.get(`${API_BASE_URL}/api/pollution`, {
    params: { city, parameter },
  });
  return response.data;
}

export async function getTrend(city, parameter) {
  const response = await axios.get(`${API_BASE_URL}/api/trend`, {
    params: { city, parameter },
  });
  return response.data;
}

export async function getPrediction(city, parameter) {
  const response = await axios.post(`${API_BASE_URL}/api/predict`, {
    city,
    parameter,
  });

  return response.data;
}

export async function getModelInfo() {
  const response = await axios.get(`${API_BASE_URL}/api/model/info`);
  return response.data;
}

export async function getDescriptiveStatistics(parameter = null) {
  const response = await axios.get(`${API_BASE_URL}/api/descriptive/statistics`, {
    params: parameter ? { parameter } : {},
  });

  return response.data;
}

export async function getCityProfile(city) {
  const response = await axios.get(`${API_BASE_URL}/api/descriptive/city-profile`, {
    params: { city },
  });

  return response.data;
}

export async function getMonthlyAverage(city, parameter) {
  const response = await axios.get(`${API_BASE_URL}/api/descriptive/monthly-average`, {
    params: { city, parameter },
  });

  return response.data;
}

export async function getAlerts(city, parameter) {
  const response = await axios.get(`${API_BASE_URL}/api/alerts`, {
    params: { city, parameter },
  });

  return response.data;
}