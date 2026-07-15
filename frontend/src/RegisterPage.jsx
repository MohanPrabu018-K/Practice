import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register } from './api'
import { useAuth } from './store'

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const auth = useAuth()

  const handleSubmit = async e => {
    e.preventDefault(); setError('')
    if (!username.trim() || !email.trim() || !password.trim()) return setError('Fill all fields')
    setLoading(true)
    try {
      const r = await register({ username, email, password })
      auth.login(r.access_token, { username: r.username, email: r.email, role: r.role })
      navigate('/')
    } catch (err) { setError(err.response?.data?.detail || 'Registration failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} autoFocus />
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
          {error && <p className="error">{error}</p>}
          <button className="btn btn-primary btn-lg" type="submit" disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
        </form>
        <p className="auth-switch">Have account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  )
}
