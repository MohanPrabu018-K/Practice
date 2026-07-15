import { useState, useEffect, useMemo } from 'react'
import { fetchMovies } from './api'
import MovieCard from './MovieCard'

const GENRES = ['All', 'Sci-Fi', 'Action', 'Thriller']
const LANGUAGES = ['All', 'English', 'Korean']

export default function MovieListPage() {
  const [movies, setMovies] = useState([])
  const [search, setSearch] = useState('')
  const [genre, setGenre] = useState('All')
  const [language, setLanguage] = useState('All')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const params = {}
    if (genre !== 'All') params.genre = genre
    if (language !== 'All') params.language = language
    fetchMovies(params)
      .then(setMovies)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [genre, language])

  const filtered = useMemo(() => {
    if (!search.trim()) return movies
    const q = search.toLowerCase()
    return movies.filter(
      (m) =>
        m.title.toLowerCase().includes(q) ||
        m.description?.toLowerCase().includes(q)
    )
  }, [movies, search])

  return (
    <div className="page">
      <h2>Now Showing</h2>

      <div className="filters">
        <input
          type="text"
          placeholder="Search movies..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-bar"
        />
        <div className="filter-tabs">
          {GENRES.map((g) => (
            <button
              key={g}
              className={`tab ${genre === g ? 'active' : ''}`}
              onClick={() => setGenre(g)}
            >
              {g}
            </button>
          ))}
        </div>
        <div className="filter-tabs">
          {LANGUAGES.map((l) => (
            <button
              key={l}
              className={`tab ${language === l ? 'active' : ''}`}
              onClick={() => setLanguage(l)}
            >
              {l}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="loading">Loading movies...</p>
      ) : filtered.length === 0 ? (
        <p className="empty">No movies found.</p>
      ) : (
        <div className="movie-grid">
          {filtered.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  )
}
