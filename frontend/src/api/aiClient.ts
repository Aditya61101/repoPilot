import axios from "axios";

export const aiClient = axios.create({
    baseURL: import.meta.env.VITE_AI_BASE_URL || "http://localhost:8000/ai",
})