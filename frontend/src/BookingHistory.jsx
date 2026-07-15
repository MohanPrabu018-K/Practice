import { useState, useEffect } from 'react'
import { fetchMyBookings } from './api'

export default function BookingHistory() {
  const [data, setData] = useState({ items: [], total: 0, page: 1, total_pages: 1 })
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetchMyBookings({ page, limit: 10 }).then(setData).catch(console.error).finally(() => setLoading(false))
  }, [page])

  return (
    <div className="page">
      <h2>My Bookings</h2>
      {loading ? <p className="loading">Loading...</p> : data.items.length === 0 ? <p className="empty">No bookings yet.</p> : (
        <>
          {data.items.map(b => (
            <div key={b.booking_reference} className="booking-history-item">
              <div className="bh-header">
                <span className="bh-ref">{b.booking_reference}</span>
                <span className={`bh-status ${b.status}`}>{b.status}</span>
              </div>
              <div className="bh-details">
                <div><strong>{b.movie_title}</strong> · {b.hall_name}</div>
                <div>{new Date(b.show_time).toLocaleString('en-IN')}</div>
                <div>Seats: {b.seats.join(', ')} · ₹{b.total_amount.toFixed(2)}</div>
              </div>
            </div>
          ))}
          {data.total_pages > 1 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 24 }}>
              <button className="btn btn-outline btn-sm" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>Prev</button>
              <span style={{ padding: '8px 12px', color: '#888' }}>{page} / {data.total_pages}</span>
              <button className="btn btn-outline btn-sm" disabled={page >= data.total_pages} onClick={() => setPage(p => p + 1)}>Next</button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
