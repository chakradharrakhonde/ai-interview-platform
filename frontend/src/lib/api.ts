import axios from 'axios';
import { useAuthStore } from './store';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: any) => api.post('/api/v1/auth/register', data),
  login: (data: any) => api.post('/api/v1/auth/login', data),
  refresh: (token: string) => api.post('/api/v1/auth/refresh', { refresh_token: token }),
};

export const resumeAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/v1/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getResume: (id: string) => api.get(`/api/v1/resumes/${id}`),
  scoreResume: (id: string) => api.post(`/api/v1/resumes/${id}/score`),
  deleteResume: (id: string) => api.delete(`/api/v1/resumes/${id}`),
};

export const interviewAPI = {
  startInterview: (data: any) => api.post('/api/v1/interviews/start', data),
  submitAnswer: (id: string, data: any) => api.post(`/api/v1/interviews/${id}/answer`, data),
  getFeedback: (id: string) => api.get(`/api/v1/interviews/${id}/feedback`),
  getHistory: () => api.get('/api/v1/interviews/history'),
};

export const codingAPI = {
  getQuestions: (difficulty?: string) => api.get('/api/v1/coding/questions', { params: { difficulty } }),
  getQuestion: (id: string) => api.get(`/api/v1/coding/questions/${id}`),
  submitCode: (data: any) => api.post('/api/v1/coding/submit', data),
};

export const dashboardAPI = {
  getStats: () => api.get('/api/v1/dashboard/stats'),
};

export default api;
