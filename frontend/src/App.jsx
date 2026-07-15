import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Header from './Header'
import MovieListPage from './MovieListPage'
import MovieDetailPage from './MovieDetailPage'
import SeatSelectionPage from './SeatSelectionPage'
import BookingSuccessPage from './BookingSuccessPage'
import LoginPage from './LoginPage'
import RegisterPage from './RegisterPage'

function RequireAuth({ children }) {
  const token = localStorage.getItem('token')
  const location = useLocation()

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}

export default function App() {
  return (
    <>
      <Header />
      <main className="container">
        <Routes>
          <Route path="/" element={<MovieListPage />} />
          <Route path="/movie/:id" element={<MovieDetailPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/book/:showTimingId"
            element={
              <RequireAuth>
                <SeatSelectionPage />
              </RequireAuth>
            }
          />
          <Route
            path="/booking/:reference"
            element={
              <RequireAuth>
                <BookingSuccessPage />
              </RequireAuth>
            }
          />
        </Routes>
      </main>
      <footer className="footer">
        <p>&copy; 2026 MovieBooker. All rights reserved.</p>
      </footer>
    </>
  )
}
