import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail
    if (status === 401) {
      if (router.currentRoute.value.name === 'login') {
        // 登录页上的 401 = 登录失败（用户名或密码错误）
        ElMessage.error(detail || '用户名或密码错误')
      } else {
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_username')
        ElMessage.error(detail || '登录已过期，请重新登录')
        router.push('/login')
      }
    } else {
      const msg = typeof detail === 'string' ? detail : '请求失败，请稍后重试'
      ElMessage.error(msg)
    }
    return Promise.reject(error)
  }
)

export default request
