import axios from "axios";

export const generateCampaign = async (data) => {
  const res = await axios.post("http://localhost:5001/generate", data);
  return res.data;
};