import request from './request'

export const getArticles = (params) => request.get('/articles', { params })
export const createArticle = (data) => request.post('/articles', data)
export const updateArticle = (id, data) => request.put(`/articles/${id}`, data)
export const deleteArticle = (id) => request.delete(`/articles/${id}`)
