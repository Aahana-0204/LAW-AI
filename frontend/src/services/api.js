import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 30000,
})

const token = localStorage.getItem('lawai_token')
if (token) {
  api.defaults.headers.common.Authorization = `Bearer ${token}`
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('lawai_token')
      localStorage.removeItem('lawai_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export default api
