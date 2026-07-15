import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchSeats, createBooking } from './api'
import SeatMap from './SeatMap'

const ROWS = ['A', 'B', 'C', 'D', 'E', 'F']

export default function SeatSelectionPage() {
  const { showTimingId } = useParams()
  const navigate = useNavigate()

  const [data, setData] = useState(null)
  const [selectedIds, setSelectedIds] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const [userName, setUserName] = useState('')
  const [userEmail, setUserEmail] = useState('')

  const toggleSeat = (seatId) => {
    setSelectedIds((prev) =>
      prev.includes(seatId)
        ? prev.filter((id) => id !== seatId)
        : [...prev, seatId]
    )
    setError('')
  }

  useEffect(() => {
    setLoading(true)
    fetchSeats(showTimingId)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [showTimingId])

  const handleConfirm = async () => {
    if (selectedIds.length === 0) {
      setError('Please select at least one seat.')
      return
    }
    if (!userName.trim() || !userEmail.trim()) {
      setError('Please enter your name and email.')
      return
    }

    setSubmitting(true)
    setError('')

    try {
      const result = await createBooking({
        user_name: userName,
        user_email: userEmail,
        show_timing_id: parseInt(showTimingId),
        seat_ids: selectedIds,
      })
      navigate(`/booking/${result.booking_reference}`)
    } catch (err) {
      const msg =
        err.response?.data?.detail || 'Booking failed. Please try again.'
      setError(msg)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <p className="loading">Loading seats...</p>
  if (!data) return <p className="empty">Show timing not found.</p>

  const total = selectedIds.length * data.price

  return (
    <div className="page">
      <h2>Select Seats</h2>
      <div className="show-summary">
        <span>{data.hall_name}</span>
        <span>{new Date(data.show_time).toLocaleString('en-IN')}</span>
        <span className="price">₹{data.price.toFixed(2)} / seat</span>
      </div>

      <SeatMap
        seats={data.seats}
        selectedIds={selectedIds}
        onToggleSeat={toggleSeat}
      />

      <div className="booking-form">
        <h3>Your Details</h3>
        <div className="form-row">
          <input
            type="text"
            placeholder="Your Name"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
          />
          <input
            type="email"
            placeholder="Your Email"
            value={userEmail}
            onChange={(e) => setUserEmail(e.target.value)}
          />
        </div>

        {selectedIds.length > 0 && (
          <div className="summary-box">
            <p>
              <strong>Seats:</strong>{' '}
              {(() => {
                const grouped = {}
                for (const row of ROWS) {
                  const ids = data.seats
                    .filter((s) => s.row_label === row && selectedIds.includes(s.id))
                    .map((s) => s.seat_number)
                    .sort((a, b) => a - b)
                  if (ids.length > 0) grouped[row] = ids
                }
                return Object.entries(grouped)
                  .map(([row, nums]) => `${row}-${nums.join(',')}`)
                  .join(' | ')
              })()}
            </p>
            <p>
              <strong>Total:</strong> ₹{total.toFixed(2)} ({selectedIds.length}{' '}
              seat{selectedIds.length > 1 ? 's' : ''})
            </p>
          </div>
        )}

        {error && <p className="error">{error}</p>}

        <button
          className="btn-primary btn-large"
          onClick={handleConfirm}
          disabled={submitting}
        >
          {submitting ? 'Booking...' : 'Confirm Booking'}
        </button>
      </div>
    </div>
  )
}
