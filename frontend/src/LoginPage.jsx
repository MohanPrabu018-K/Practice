import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login } from './api'
import { useAuth } from './store'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const auth = useAuth()

  const handleSubmit = async e => {
    e.preventDefault(); setError('')
    if (!username.trim() || !password.trim()) return setError('Fill all fields')
    setLoading(true)
    try {
      const r = await login({ username, password })
      auth.login(r.access_token, { username: r.username, email: r.email, role: r.role })
      navigate('/')
    } catch (err) { setError(err.response?.data?.detail || 'Login failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} autoFocus />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
          {error && <p className="error">{error}</p>}
          <button className="btn btn-primary btn-lg" type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
        </form>
        <p className="auth-switch">No account? <Link to="/register">Register</Link></p>
        <p className="demo-hint">Demo: <strong>demo</strong> / <strong>demo123</strong></p>
      </div>
    </div>
  )
}
