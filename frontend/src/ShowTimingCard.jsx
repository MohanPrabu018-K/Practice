import { useNavigate } from 'react-router-dom'

export default function ShowTimingCard({ timing }) {
  const navigate = useNavigate()
  return (
    <div className="show-card">
      <div className="show-info">
        <strong>{timing.hall_name} - {timing.screen_name}</strong>
        <span>{new Date(timing.show_time).toLocaleString('en-IN')}</span>
        <span className="price">₹{timing.base_price.toFixed(2)}</span>
      </div>
      <button className="btn btn-primary" onClick={() => navigate(`/book/${timing.id}`)}>Book</button>
    </div>
  )
}
