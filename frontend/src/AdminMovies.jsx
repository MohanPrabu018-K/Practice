import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { fetchAdminMovies, createMovie, deleteMovie } from './api'

export default function AdminMovies() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [title, setTitle] = useState('')
  const [genre, setGenre] = useState('')
  const [language, setLanguage] = useState('')
  const [duration, setDuration] = useState('')

  useEffect(() => { fetchAdminMovies().then(setMovies).catch(console.error).finally(() => setLoading(false)) }, [])

  const handleCreate = async e => {
    e.preventDefault()
    await createMovie({ title, genre, language, duration: parseInt(duration) || 120, description: '', poster_url: '', is_upcoming: false })
    const m = await fetchAdminMovies(); setMovies(m); setTitle(''); setGenre(''); setLanguage(''); setDuration('')
  }

  const handleDelete = async id => { await deleteMovie(id); setMovies(ms => ms.filter(m => m.id !== id)) }

  return (
    <div className="page">
      <div className="admin-layout">
        <div className="admin-sidebar">
          <Link to="/admin">Dashboard</Link>
          <Link to="/admin/movies" className="active">Movies</Link>
        </div>
        <div className="admin-content">
          <h2>Manage Movies</h2>
          <div className="admin-card" style={{ marginBottom: 20 }}>
            <h3 style={{ marginBottom: 12 }}>Add Movie</h3>
            <form onSubmit={handleCreate} className="form-row">
              <input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} required />
              <input placeholder="Genre" value={genre} onChange={e => setGenre(e.target.value)} />
              <input placeholder="Language" value={language} onChange={e => setLanguage(e.target.value)} />
              <input placeholder="Duration (min)" type="number" value={duration} onChange={e => setDuration(e.target.value)} />
              <button className="btn btn-primary btn-sm" type="submit">Add</button>
            </form>
          </div>
          <table className="table">
            <thead><tr><th>ID</th><th>Title</th><th>Genre</th><th>Lang</th><th>Duration</th><th></th></tr></thead>
            <tbody>
              {movies.map(m => (
                <tr key={m.id}>
                  <td>{m.id}</td><td>{m.title}</td><td>{m.genre}</td><td>{m.language}</td><td>{m.duration} min</td>
                  <td><button className="btn btn-danger btn-sm" onClick={() => handleDelete(m.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
