import { useState, useEffect, useMemo, useCallback } from 'react'
import { fetchMovies } from './api'
import MovieCard from './MovieCard'

const GENRES = ['All','Sci-Fi','Action','Drama','Thriller']
const LANGS = ['All','English','Tamil','Korean']

export default function MovieListPage() {
  const [movies, setMovies] = useState({ items: [], total: 0, page: 1, total_pages: 1 })
  const [search, setSearch] = useState('')
  const [genre, setGenre] = useState('All')
  const [lang, setLang] = useState('All')
  const [tab, setTab] = useState('now')
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    const p = { page, limit: 12 }
    if (genre !== 'All') p.genre = genre
    if (lang !== 'All') p.language = lang
    if (search.trim()) p.search = search
    if (tab === 'upcoming') p.upcoming = true
    else if (tab === 'trending') p.trending = true
    fetchMovies(p).then(setMovies).catch(console.error).finally(() => setLoading(false))
  }, [genre, lang, search, tab, page])

  useEffect(() => { load() }, [load])

  return (
    <div className="page">
      <h2>Now Showing</h2>
      <div className="filters">
        <input type="text" placeholder="Search movies..." value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} className="search-bar" />
        <div className="filter-tabs">
          <button className={`tab ${tab === 'now' ? 'active' : ''}`} onClick={() => { setTab('now'); setPage(1) }}>Now Showing</button>
          <button className={`tab ${tab === 'upcoming' ? 'active' : ''}`} onClick={() => { setTab('upcoming'); setPage(1) }}>Upcoming</button>
          <button className={`tab ${tab === 'trending' ? 'active' : ''}`} onClick={() => { setTab('trending'); setPage(1) }}>Trending</button>
        </div>
        <div className="filter-tabs">{GENRES.map(g => <button key={g} className={`tab ${genre === g ? 'active' : ''}`} onClick={() => { setGenre(g); setPage(1) }}>{g}</button>)}</div>
        <div className="filter-tabs">{LANGS.map(l => <button key={l} className={`tab ${lang === l ? 'active' : ''}`} onClick={() => { setLang(l); setPage(1) }}>{l}</button>)}</div>
      </div>
      {loading ? <p className="loading">Loading...</p> : movies.items.length === 0 ? <p className="empty">No movies found.</p> : (
        <>
          <div className="movie-grid">{movies.items.map(m => <MovieCard key={m.id} movie={m} />)}</div>
          {movies.total_pages > 1 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 24 }}>
              <button className="btn btn-outline btn-sm" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Prev</button>
              <span style={{ padding: '8px 12px', color: '#888' }}>{page} / {movies.total_pages}</span>
              <button className="btn btn-outline btn-sm" disabled={page >= movies.total_pages} onClick={() => setPage(p => p + 1)}>Next</button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
