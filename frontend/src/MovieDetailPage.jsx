import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { fetchMovie } from './api'
import ShowTimingCard from './ShowTimingCard'

export default function MovieDetailPage() {
  const { id } = useParams()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetchMovie(id)
      .then(setMovie)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <p className="loading">Loading...</p>
  if (!movie) return <p className="empty">Movie not found.</p>

  return (
    <div className="page">
      <div className="movie-detail">
        <div className="detail-poster">
          {movie.poster_url ? (
            <img src={movie.poster_url} alt={movie.title} />
          ) : (
            <div className="no-poster large">🎬</div>
          )}
        </div>
        <div className="detail-info">
          <h2>{movie.title}</h2>
          <div className="detail-meta">
            <span className="genre-badge">{movie.genre}</span>
            <span>{movie.duration} min</span>
            <span>{movie.language}</span>
          </div>
          <p className="description">{movie.description}</p>
        </div>
      </div>

      <h3>Show Timings</h3>
      {movie.show_timings.length === 0 ? (
        <p className="empty">No show timings available.</p>
      ) : (
        <div className="show-list">
          {movie.show_timings.map((t) => (
            <ShowTimingCard key={t.id} timing={t} />
          ))}
        </div>
      )}
    </div>
  )
}
