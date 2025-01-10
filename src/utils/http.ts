import axios from 'axios'
import { ElNotification } from 'element-plus'

const http = axios.create({
  baseURL: '/api',
  timeout: 60000 // 超时时间
})

// 响应拦截器
http.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const status = error.response.status
      const errorMsg = error.response.data.message || 'Request failed. Please check'

      if (status === 401) {
        ElNotification.error({
          title: 'Unauthorized',
          message: 'Your token has expired. Please login again.'
        })
      } else {
        ElNotification.error({
          title: `Error ${status}`,
          message: errorMsg
        })
      }
    } else {
      ElNotification.error({
        title: 'Network Error',
        message: 'Network error. Please try again later.'
      })
    }

    return Promise.reject(error)
  }
)

export default http
