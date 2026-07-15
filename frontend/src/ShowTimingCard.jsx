import { useNavigate } from 'react-router-dom'

export default function ShowTimingCard({ timing }) {
  const navigate = useNavigate()

  const formatDate = (iso) => {
    const d = new Date(iso)
    return d.toLocaleString('en-IN', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className="show-card">
      <div className="show-info">
        <strong>{timing.hall_name}</strong>
        <span>{formatDate(timing.show_time)}</span>
        <span className="price">₹{timing.price.toFixed(2)}</span>
      </div>
      <button
        className="btn-primary"
        onClick={() => navigate(`/book/${timing.id}`)}
      >
        Book
      </button>
    </div>
  )
}
