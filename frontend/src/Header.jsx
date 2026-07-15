import { Link, useNavigate } from 'react-router-dom'
import { useAuth, useTheme } from './store'

export default function Header() {
  const { user, logout } = useAuth()
  const { dark, toggle } = useTheme()
  const navigate = useNavigate()

  const handleLogout = () => { logout(); navigate('/') }

  return (
    <header className="header">
      <Link to="/" className="logo">🎬 MovieBooker</Link>
      <nav>
        <Link to="/">Movies</Link>
        {user ? (
          <>
            <Link to="/my-bookings">My Bookings</Link>
            {user.role === 'admin' && <Link to="/admin">Admin</Link>}
            <Link to="/profile">👤 {user.username}</Link>
            <button onClick={handleLogout} className="btn-logout">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
        <button onClick={toggle} className="theme-btn" title="Toggle theme">{dark ? '☀️' : '🌙'}</button>
      </nav>
    </header>
  )
}
