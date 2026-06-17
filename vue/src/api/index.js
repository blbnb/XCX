import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const bookAPI = {
  getList: (params) => api.get('/books', { params }),
  getDetail: (id) => api.get(`/books/${id}`),
  create: (data) => api.post('/books', data),
  update: (id, data) => api.put(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),
  getCategories: () => api.get('/books/categories')
}

export default api
