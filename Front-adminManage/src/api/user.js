import request from './request'

export const getUsers = (params) => request.get('/users', { params })
export const getUserStats = (params) => request.get('/users/stats', { params })
export const createUser = (data) => request.post('/users', data)
export const updateUser = (id, data) => request.put(`/users/${id}`, data)
export const deleteUser = (id) => request.delete(`/users/${id}`)
export const uploadAvatar = (file) => {
  const form = new FormData()
  form.append('file', file)
  return request.post('/upload', form)
}
