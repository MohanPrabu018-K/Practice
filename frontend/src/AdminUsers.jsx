import { useState, useEffect } from 'react'
import { fetchAdminUsers, updateUserRole, deleteUser } from './api'

export default function AdminUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => { fetchAdminUsers().then(setUsers).catch(console.error).finally(() => setLoading(false)) }
  useEffect(() => { load() }, [])

  if (loading) return <p className="loading">Loading users...</p>

  return (
    <div className="page">
      <h2>Manage Users</h2>
      <table className="table">
        <thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Actions</th></tr></thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td><td>{u.username}</td><td>{u.email}</td>
              <td><span className={`ticket-status ${u.role === 'admin' ? 'cancelled' : 'confirmed'}`}>{u.role}</span></td>
              <td style={{display:'flex',gap:4}}>
                <button className="btn btn-outline btn-sm" onClick={() => updateUserRole(u.id, {role: u.role==='admin'?'user':'admin'}).then(load)}>{u.role==='admin'?'Demote':'Promote'}</button>
                <button className="btn btn-danger btn-sm" onClick={() => deleteUser(u.id).then(load)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
