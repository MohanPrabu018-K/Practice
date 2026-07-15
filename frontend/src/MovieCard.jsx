import { Link } from 'react-router-dom'

export default function MovieCard({ movie }) {
  return (
    <Link to={`/movie/${movie.id}`} className="movie-card">
      <div className="movie-poster">
        {movie.poster_url ? <img src={movie.poster_url} alt={movie.title} loading="lazy" /> : <div className="no-poster">🎬</div>}
      </div>
      <div className="movie-info">
        <h3>{movie.title}</h3>
        <span className="genre-badge">{movie.genre}</span>
        <span className="duration">{movie.duration} min</span>
        <span className="language">{movie.language}</span>
        {movie.average_rating > 0 && <div className="rating">★ {movie.average_rating}<span>({movie.total_reviews})</span></div>}
      </div>
    </Link>
  )
}
