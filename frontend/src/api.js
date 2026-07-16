import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000/api' })

api.interceptors.request.use(c => {
  const t = localStorage.getItem('token')
  if (t) c.headers.Authorization = `Bearer ${t}`
  return c
})

// Auth
export const register = d => api.post('/auth/register', d).then(r => r.data)
export const login = d => api.post('/auth/login', d).then(r => r.data)
export const refreshToken = d => api.post('/auth/refresh', d).then(r => r.data)
export const logout = d => api.post('/auth/logout', d)
export const fetchMe = () => api.get('/auth/me').then(r => r.data)
export const updateProfile = d => api.put('/auth/me', d).then(r => r.data)
export const changePassword = d => api.put('/auth/me/password', d)

// Movies
export const fetchMovies = (p = {}) => api.get('/movies', { params: p }).then(r => r.data)
export const fetchMovie = id => api.get(`/movies/${id}`).then(r => r.data)
export const fetchReviews = (id, p) => api.get(`/movies/${id}/reviews`, { params: p }).then(r => r.data)
export const addReview = (id, d) => api.post(`/movies/${id}/reviews`, d).then(r => r.data)

// Theatres
export const fetchTheatres = () => api.get('/theatres').then(r => r.data)

// Shows & Seats
export const fetchSeats = id => api.get(`/show-timings/${id}/seats`).then(r => r.data)
export const fetchRecommended = (id, p) => api.get(`/show-timings/${id}/recommended`, { params: p }).then(r => r.data)

// Bookings
export const createBooking = d => api.post('/bookings', d).then(r => r.data)
export const fetchBooking = ref => api.get(`/bookings/${ref}`).then(r => r.data)
export const fetchMyBookings = p => api.get('/users/me/bookings', { params: p }).then(r => r.data)

// Tickets (QR + PDF)
export const fetchBookingQR = ref => api.get(`/bookings/${ref}/qr`).then(r => r.data)
export const getTicketPdfUrl = ref => `${api.defaults.baseURL}/bookings/${ref}/pdf?token=${localStorage.getItem('token')}`

// Coupons
export const validateCoupon = d => api.post('/coupons/validate', d).then(r => r.data)

// Admin
export const fetchDashboard = () => api.get('/admin/dashboard').then(r => r.data)
export const fetchAdminMovies = p => api.get('/admin/movies', { params: p }).then(r => r.data)
export const createMovie = d => api.post('/admin/movies', d)
export const updateMovie = (id, d) => api.put(`/admin/movies/${id}`, d)
export const deleteMovie = id => api.delete(`/admin/movies/${id}`)
export const fetchAdminTheatres = () => api.get('/admin/theatres').then(r => r.data)
export const createTheatre = d => api.post('/admin/theatres', d)
export const updateTheatre = (id, d) => api.put(`/admin/theatres/${id}`, d)
export const deleteTheatre = id => api.delete(`/admin/theatres/${id}`)
export const createScreen = d => api.post('/admin/screens', d)
export const deleteScreen = id => api.delete(`/admin/screens/${id}`)
export const createShow = d => api.post('/admin/shows', d)
export const fetchAdminBookings = p => api.get('/admin/bookings', { params: p }).then(r => r.data)
export const cancelBooking = id => api.put(`/admin/bookings/${id}/cancel`)
export const fetchAdminUsers = p => api.get('/admin/users', { params: p }).then(r => r.data)
export const updateUserRole = (id, d) => api.put(`/admin/users/${id}/role`, d)
export const deleteUser = id => api.delete(`/admin/users/${id}`)
export const fetchAdminCoupons = () => api.get('/admin/coupons').then(r => r.data)
export const createCoupon = d => api.post('/admin/coupons', d)
export const deleteCoupon = id => api.delete(`/admin/coupons/${id}`)
export const fetchAdminReviews = p => api.get('/admin/reviews', { params: p }).then(r => r.data)
export const deleteReview = id => api.delete(`/admin/reviews/${id}`)

export default api
