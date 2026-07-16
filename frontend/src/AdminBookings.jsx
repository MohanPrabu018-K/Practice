import { useState, useEffect } from 'react'
import { fetchAdminBookings } from './api'

export default function AdminBookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchAdminBookings().then(setBookings).catch(console.error).finally(() => setLoading(false)) }, [])

  if (loading) return <p className="loading">Loading...</p>

  return (
    <div className="page">
      <h2>All Bookings</h2>
      <table className="table">
        <thead><tr><th>Ref</th><th>User ID</th><th>Amount</th><th>Status</th><th>Booked At</th></tr></thead>
        <tbody>
          {bookings.map(b => (
            <tr key={b.id}>
              <td style={{ color: '#e0aaff', fontWeight: 600 }}>{b.booking_reference}</td>
              <td>{b.user_id} - {b.user_name}</td>
              <td>₹{b.total_amount?.toFixed(2)}</td>
              <td><span className={`ticket-status ${b.status}`}>{b.status}</span></td>
              <td>{b.booking_time ? new Date(b.booking_time).toLocaleString('en-IN') : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
