import axios from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosError } from "axios";


const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL as string,
  timeout: 10000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json"
  }
});

// 🔐 Interceptor REQUEST – agrega token
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem("token");

    if (token && config.headers) {
      config.headers["x-token"] = token;
    }

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// 🚨 Interceptor RESPONSE – manejo de errores globales
api.interceptors.response.use(
  response => response,
  (error: AxiosError) => {
    const status = error.response?.status;

    if (status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }

    if (status === 403) {
      alert("No tienes permisos para acceder a este recurso.");
    }

    if (status && status >= 500) {
      console.error("Error de servidor:", error.response);
    }

    return Promise.reject(error);
  }
);

export default api;
