// src/api/usersApi.js
import api from './axios'

export const getUsers = () => api.get('/users/')
export const getUser = (ulid) => api.get(`/users/${ulid}/`)
export const createUser = (data) => api.post('/users/', data)
export const updateUser = (ulid, data) => api.patch(`/users/${ulid}/`, data)
export const deleteUser = (ulid) => api.delete(`/users/${ulid}/`)