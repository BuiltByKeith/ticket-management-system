// src/api/ticketsApi.js
import api from './axios'

export const getTickets = () => api.get('/tickets/')
export const getTicket = (ulid) => api.get(`/tickets/${ulid}/`)
export const submitTicket = (data) => api.post('/tickets/', data)
export const updateTicket = (ulid, data) => api.patch(`/tickets/${ulid}/`, data)
export const trackTicket = (data) => api.post('/tickets/track/', data)