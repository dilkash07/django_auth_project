import axios from "axios";

const api = axios.create({
  baseURL: "https://your-api-url.com/api", // ⛳️ Replace with your real backend
  withCredentials: true,
});

export default api;
