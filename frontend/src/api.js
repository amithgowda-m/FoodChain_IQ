const axios = require("axios");

const API_URL = "http://localhost:8000/api/v1";

export const predictRiskLevel = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, data);
    return response.data;
  } catch (error) {
    throw new Error("Failed to predict risk level");
  }
};