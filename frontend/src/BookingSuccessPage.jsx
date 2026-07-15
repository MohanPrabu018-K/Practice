import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchBooking } from './api'

export default function BookingSuccessPage() {
  const { reference } = useParams()
  const [booking, setBooking] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetchBooking(reference)
      .then(setBooking)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [reference])

  if (loading) return <p className="loading">Loading booking...</p>
  if (!booking) return <p className="empty">Booking not found.</p>

  return (
    <div className="page success-page">
      <div className="success-card">
        <div className="success-icon">✅</div>
        <h2>Booking Confirmed!</h2>

        <div className="detail-rows">
          <div className="detail-row">
            <span className="label">Booking Ref</span>
            <span className="value highlight">{booking.booking_reference}</span>
          </div>
          <div className="detail-row">
            <span className="label">Movie</span>
            <span className="value">{booking.movie_title}</span>
          </div>
          <div className="detail-row">
            <span className="label">Hall</span>
            <span className="value">{booking.hall_name}</span>
          </div>
          <div className="detail-row">
            <span className="label">Show Time</span>
            <span className="value">
              {new Date(booking.show_time).toLocaleString('en-IN')}
            </span>
          </div>
          <div className="detail-row">
            <span className="label">Seats</span>
            <span className="value">{booking.seats.join(', ')}</span>
          </div>
          <div className="detail-row">
            <span className="label">Amount Paid</span>
            <span className="value">₹{booking.total_amount.toFixed(2)}</span>
          </div>
        </div>

        <div className="success-actions">
          <Link to="/" className="btn-primary">Browse More Movies</Link>
        </div>
      </div>
    </div>
  )
}
