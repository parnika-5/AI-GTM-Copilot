import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "";

export const generateCampaign = async (data) => {
  const res = await axios.post(`${API_BASE}/generate`, data);
  return res.data;
};