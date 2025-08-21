import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

export const analyzeReviews = async (reviews) => {
  try {
    const response = await axios.post(`${API_URL}/analyze`, { reviews });
    return response.data;
  } catch (error) {
    console.error("Error calling API:", error);
    throw error;
  }
};
