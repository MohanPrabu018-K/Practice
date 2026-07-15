import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuth, useTheme } from './store'
import Header from './Header'
import MovieListPage from './MovieListPage'
import MovieDetailPage from './MovieDetailPage'
import SeatSelectionPage from './SeatSelectionPage'
import BookingSuccessPage from './BookingSuccessPage'
import LoginPage from './LoginPage'
import RegisterPage from './RegisterPage'
import ProfilePage from './ProfilePage'
import BookingHistory from './BookingHistory'
import AdminDashboard from './AdminDashboard'
import AdminMovies from './AdminMovies'

function RequireAuth({ children, admin }) {
  const { token, user } = useAuth()
  const location = useLocation()
  if (!token) return <Navigate to="/login" state={{ from: location }} replace />
  if (admin && user?.role !== 'admin') return <Navigate to="/" replace />
  return children
}

export default function App() {
  const { dark } = useTheme()
  document.body.className = dark ? '' : 'light'
  return (
    <>
      <Header />
      <main className="container">
        <Routes>
          <Route path="/" element={<MovieListPage />} />
          <Route path="/movie/:id" element={<MovieDetailPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/book/:showTimingId" element={<RequireAuth><SeatSelectionPage /></RequireAuth>} />
          <Route path="/booking/:reference" element={<RequireAuth><BookingSuccessPage /></RequireAuth>} />
          <Route path="/profile" element={<RequireAuth><ProfilePage /></RequireAuth>} />
          <Route path="/my-bookings" element={<RequireAuth><BookingHistory /></RequireAuth>} />
          <Route path="/admin" element={<RequireAuth admin><AdminDashboard /></RequireAuth>} />
          <Route path="/admin/movies" element={<RequireAuth admin><AdminMovies /></RequireAuth>} />
        </Routes>
      </main>
      <footer className="footer"><p>&copy; 2026 MovieBooker. All rights reserved.</p></footer>
    </>
  )
}
