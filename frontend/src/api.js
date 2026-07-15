import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

// ---------- Auth token interceptor ----------

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ---------- Auth ----------

export const registerUser = (data) =>
  api.post('/auth/register', data).then((r) => r.data)

export const loginUser = (data) =>
  api.post('/auth/login', data).then((r) => r.data)

export const fetchMe = () =>
  api.get('/auth/me').then((r) => r.data)

// ---------- Movies ----------

export const fetchMovies = (params = {}) =>
  api.get('/movies', { params }).then((r) => r.data)

export const fetchMovie = (id) =>
  api.get(`/movies/${id}`).then((r) => r.data)

// ---------- Seats ----------

export const fetchSeats = (showTimingId) =>
  api.get(`/show-timings/${showTimingId}/seats`).then((r) => r.data)

// ---------- Bookings ----------

export const createBooking = (bookingData) =>
  api.post('/bookings', bookingData).then((r) => r.data)

export const fetchBooking = (reference) =>
  api.get(`/bookings/${reference}`).then((r) => r.data)

export default api
