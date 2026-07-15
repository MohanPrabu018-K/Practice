import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchMovie, fetchReviews, addReview } from './api'
import { useAuth } from './store'

export default function MovieDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [movie, setMovie] = useState(null)
  const [reviews, setReviews] = useState({ items: [], total: 0 })
  const [rating, setRating] = useState(5)
  const [comment, setComment] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    setLoading(true)
    Promise.all([fetchMovie(id), fetchReviews(id, { page: 1, limit: 10 })]).then(([m, r]) => { setMovie(m); setReviews(r) }).catch(console.error).finally(() => setLoading(false))
  }, [id])

  const handleReview = async () => {
    setSubmitting(true)
    try {
      await addReview(id, { rating, comment })
      const r = await fetchReviews(id, { page: 1, limit: 10 })
      setReviews(r); setComment('')
    } catch (e) { console.error(e) }
    finally { setSubmitting(false) }
  }

  if (loading) return <p className="loading">Loading...</p>
  if (!movie) return <p className="empty">Movie not found.</p>

  return (
    <div className="page">
      <div className="movie-detail">
        <div className="detail-poster">{movie.poster_url ? <img src={movie.poster_url} alt={movie.title} /> : <div className="no-poster large">🎬</div>}</div>
        <div className="detail-info">
          <h2>{movie.title}</h2>
          <div className="detail-meta">
            <span className="genre-badge">{movie.genre}</span>
            <span>{movie.duration} min</span>
            <span>{movie.language}</span>
            {movie.average_rating > 0 && <span className="rating">★ {movie.average_rating} ({movie.total_reviews} reviews)</span>}
          </div>
          <p className="description">{movie.description}</p>
        </div>
      </div>
      <h3>Show Timings</h3>
      {!movie.show_timings?.length ? <p className="empty">No shows available.</p> : (
        <div className="show-list">{movie.show_timings.map(t => (
          <div key={t.id} className="show-card">
            <div className="show-info"><strong>{t.hall_name} - {t.screen_name}</strong><span>{new Date(t.show_time).toLocaleString('en-IN')}</span><span className="price">₹{t.base_price.toFixed(2)}</span></div>
            <button className="btn btn-primary" onClick={() => navigate(`/book/${t.id}`)}>Book</button>
          </div>
        ))}</div>
      )}
      <div className="review-section">
        <h3>Reviews ({reviews.total})</h3>
        {user && (
          <div className="form-row" style={{ marginTop: 12 }}>
            <select value={rating} onChange={e => setRating(+e.target.value)} style={{ padding: '10px', borderRadius: 8, border: '1px solid #333', background: '#1a1a2e', color: '#e4e4f0' }}>
              {[5,4,3,2,1].map(n => <option key={n} value={n}>{n} ★</option>)}
            </select>
            <input type="text" placeholder="Write a review..." value={comment} onChange={e => setComment(e.target.value)} />
            <button className="btn btn-primary btn-sm" onClick={handleReview} disabled={submitting}>Submit</button>
          </div>
        )}
        {reviews.items.map(r => (
          <div key={r.id} className="review-card">
            <div className="rev-header"><span className="rev-user">{r.username}</span><span>{'★'.repeat(r.rating)}{'☆'.repeat(5 - r.rating)}</span></div>
            {r.comment && <p style={{ color: '#aab', fontSize: '.9rem' }}>{r.comment}</p>}
            <span className="rev-date">{new Date(r.created_at).toLocaleDateString('en-IN')}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
