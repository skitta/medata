import axios from 'axios'
import Cookies from 'js-cookie'
import { TokenStorage } from '@/utils/tokenStorage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// 创建用于认证的 Axios 实例
const authApi = axios.create({
  baseURL: `${API_BASE_URL}/api/`,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'X-CSRFToken': Cookies.get('csrftoken') || '',
  },
})

// 创建用于 Kawasaki API 的 Axios 实例
const kawasakiApi = axios.create({
  baseURL: `${API_BASE_URL}/api/kawasaki/`,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'X-CSRFToken': Cookies.get('csrftoken') || '',
  },
})

//为 kawasakiApi 添加请求拦截器以注入 token
kawasakiApi.interceptors.request.use(
  (config) => {
    const token = TokenStorage.getToken()
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

export { authApi, kawasakiApi }
