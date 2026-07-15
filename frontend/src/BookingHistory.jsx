import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { fetchMyBookings, fetchBookingQR, getTicketPdfUrl } from './api'

function TicketCard({ booking }) {
  const [qr, setQr] = useState(null)
  const [modal, setModal] = useState(false)

  useEffect(() => {
    fetchBookingQR(booking.booking_reference).then(r => setQr(r.qr_base64)).catch(() => {})
  }, [booking.booking_reference])

  const pdfUrl = getTicketPdfUrl(booking.booking_reference)

  return (
    <div className="ticket-card">
      <div className="ticket-left">
        <div className="ticket-movie-title">{booking.movie_title}</div>
        <div className="ticket-meta">
          <span>{booking.hall_name}</span>
          <span>{new Date(booking.show_time).toLocaleString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</span>
        </div>
        <div className="ticket-seats">
          {booking.seats.map(s => <span key={s} className="ticket-seat-badge">{s}</span>)}
        </div>
      </div>
      <div className="ticket-center">
        <div className={`ticket-status ${booking.status}`}>{booking.status}</div>
        <div className="ticket-ref">{booking.booking_reference}</div>
        <div className="ticket-price">₹{booking.total_amount.toFixed(2)}</div>
        <div className="ticket-date">Booked: {new Date(booking.booking_time).toLocaleDateString('en-IN')}</div>
      </div>
      <div className="ticket-right">
        {qr ? <img src={`data:image/png;base64,${qr}`} alt="QR" className="ticket-qr" onClick={() => setModal(true)} /> : <div className="ticket-qr-loading" />}
        <div className="ticket-actions">
          <button className="btn btn-outline btn-sm" onClick={() => setModal(true)}>View Ticket</button>
          <a href={pdfUrl} className="btn btn-primary btn-sm" download>Download PDF</a>
        </div>
      </div>

      {/* Ticket Preview Modal */}
      {modal && (
        <div className="modal-overlay" onClick={() => setModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setModal(false)}>×</button>
            <div className="preview-ticket">
              <div className="preview-header">
                <span className="preview-logo">🎬 MovieBooker</span>
                <span className="preview-label">CINEMA TICKET</span>
              </div>
              <div className="preview-title">{booking.movie_title}</div>
              <div className="preview-details">
                <div className="preview-row"><span>Theatre</span><span>{booking.hall_name}</span></div>
                <div className="preview-row"><span>Date & Time</span><span>{new Date(booking.show_time).toLocaleString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</span></div>
                <div className="preview-row"><span>Seats</span><span>{booking.seats.join(', ')}</span></div>
                <div className="preview-row"><span>Amount</span><span>₹{booking.total_amount.toFixed(2)}</span></div>
                <div className="preview-row"><span>Status</span><span className={`status-text ${booking.status}`}>{booking.status.toUpperCase()}</span></div>
                <div className="preview-row"><span>Booking Ref</span><span className="ref-highlight">{booking.booking_reference}</span></div>
                <div className="preview-row"><span>Booked On</span><span>{new Date(booking.booking_time).toLocaleString('en-IN')}</span></div>
              </div>
              {qr && <div className="preview-qr-wrap"><img src={`data:image/png;base64,${qr}`} alt="QR Code" className="preview-qr" /><p className="qr-hint">Scan at entrance</p></div>}
            </div>
            <div className="modal-actions">
              <a href={pdfUrl} className="btn btn-primary" download>📥 Download PDF Ticket</a>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

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
      {loading ? (
        <p className="loading">Loading your bookings...</p>
      ) : data.items.length === 0 ? (
        <div className="empty">
          <p style={{ fontSize: '3rem', marginBottom: 12 }}>🎟️</p>
          <p>You haven't booked any tickets yet.</p>
          <Link to="/" className="btn btn-primary" style={{ marginTop: 16 }}>Browse Movies</Link>
        </div>
      ) : (
        <>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {data.items.map(b => <TicketCard key={b.booking_reference} booking={b} />)}
          </div>
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
