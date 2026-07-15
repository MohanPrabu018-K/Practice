import { useState } from 'react'
import { useAuth } from './store'
import { updateProfile, changePassword } from './api'

export default function ProfilePage() {
  const { user, login } = useAuth()
  const [email, setEmail] = useState(user?.email || '')
  const [phone, setPhone] = useState(user?.phone || '')
  const [oldPw, setOldPw] = useState('')
  const [newPw, setNewPw] = useState('')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  const handleUpdate = async e => {
    e.preventDefault(); setMsg(''); setErr('')
    try {
      await updateProfile({ email, phone })
      login(localStorage.getItem('token'), { ...user, email, phone })
      setMsg('Profile updated')
    } catch { setErr('Update failed') }
  }

  const handlePassword = async e => {
    e.preventDefault(); setMsg(''); setErr('')
    try {
      await changePassword({ old_password: oldPw, new_password: newPw })
      setOldPw(''); setNewPw('')
      setMsg('Password changed')
    } catch { setErr('Password change failed') }
  }

  return (
    <div className="profile-page page">
      <div className="profile-card" style={{ marginBottom: 20 }}>
        <h2>Profile</h2>
        <form onSubmit={handleUpdate}>
          <div className="form-row"><input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} /></div>
          <div className="form-row"><input type="text" placeholder="Phone" value={phone} onChange={e => setPhone(e.target.value)} /></div>
          {msg && <p className="success">{msg}</p>}{err && <p className="error">{err}</p>}
          <button className="btn btn-primary" type="submit">Update Profile</button>
        </form>
      </div>
      <div className="profile-card">
        <h2>Change Password</h2>
        <form onSubmit={handlePassword}>
          <div className="form-row"><input type="password" placeholder="Current password" value={oldPw} onChange={e => setOldPw(e.target.value)} /></div>
          <div className="form-row"><input type="password" placeholder="New password" value={newPw} onChange={e => setNewPw(e.target.value)} /></div>
          <button className="btn btn-danger" type="submit">Change Password</button>
        </form>
      </div>
    </div>
  )
}
