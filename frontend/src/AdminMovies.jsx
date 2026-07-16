import { useState, useEffect } from 'react'
import { fetchAdminMovies, createMovie, updateMovie, deleteMovie } from './api'

export default function AdminMovies() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({ title: '', genre: '', language: '', duration: '120', description: '', poster_url: '', is_upcoming: false })
  const [editing, setEditing] = useState(null)

  useEffect(() => { fetchAdminMovies().then(setMovies).catch(console.error).finally(() => setLoading(false)) }, [])

  const handleSubmit = async e => {
    e.preventDefault()
    const data = { ...form, duration: parseInt(form.duration) || 120 }
    if (editing) { await updateMovie(editing, data); setEditing(null) }
    else await createMovie(data)
    const m = await fetchAdminMovies(); setMovies(m)
    setForm({ title: '', genre: '', language: '', duration: '120', description: '', poster_url: '', is_upcoming: false })
  }

  const handleEdit = m => { setForm({ title: m.title, genre: m.genre||'', language: m.language||'', duration: String(m.duration||120), description: m.description||'', poster_url: m.poster_url||'', is_upcoming: m.is_upcoming||false }); setEditing(m.id) }
  const handleDelete = async id => { await deleteMovie(id); setMovies(ms => ms.filter(m => m.id !== id)) }

  if (loading) return <p className="loading">Loading...</p>

  return (
    <div className="page">
      <h2>Manage Movies</h2>
      <div className="admin-card" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 12 }}>{editing ? 'Edit Movie' : 'Add Movie'}</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <input placeholder="Title" value={form.title} onChange={e => setForm({...form, title: e.target.value})} required />
            <input placeholder="Genre" value={form.genre} onChange={e => setForm({...form, genre: e.target.value})} />
            <input placeholder="Language" value={form.language} onChange={e => setForm({...form, language: e.target.value})} />
            <input placeholder="Duration (min)" type="number" value={form.duration} onChange={e => setForm({...form, duration: e.target.value})} />
          </div>
          <div className="form-row">
            <input placeholder="Poster URL" value={form.poster_url} onChange={e => setForm({...form, poster_url: e.target.value})} />
            <label style={{display:'flex',alignItems:'center',gap:8,color:'#aab',fontSize:'.9rem'}}>
              <input type="checkbox" checked={form.is_upcoming} onChange={e => setForm({...form, is_upcoming: e.target.checked})} /> Upcoming
            </label>
          </div>
          <textarea placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} rows={2} style={{width:'100%',marginBottom:12}} />
          <div style={{display:'flex',gap:8}}>
            <button className="btn btn-primary btn-sm" type="submit">{editing ? 'Update' : 'Add'}</button>
            {editing && <button className="btn btn-outline btn-sm" type="button" onClick={() => { setEditing(null); setForm({ title: '', genre: '', language: '', duration: '120', description: '', poster_url: '', is_upcoming: false }) }}>Cancel</button>}
          </div>
        </form>
      </div>
      <table className="table">
        <thead><tr><th>ID</th><th>Title</th><th>Genre</th><th>Lang</th><th>Duration</th><th>Rating</th><th></th></tr></thead>
        <tbody>
          {movies.map(m => (
            <tr key={m.id}>
              <td>{m.id}</td><td>{m.title}</td><td>{m.genre}</td><td>{m.language}</td><td>{m.duration} min</td><td>★ {m.average_rating||0}</td>
              <td style={{display:'flex',gap:4}}>
                <button className="btn btn-outline btn-sm" onClick={() => handleEdit(m)}>Edit</button>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(m.id)}>Del</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
