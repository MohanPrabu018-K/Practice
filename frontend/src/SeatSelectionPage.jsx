import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchSeats, fetchRecommended, validateCoupon, createBooking } from './api'
import SeatMap from './SeatMap'

export default function SeatSelectionPage() {
  const { showTimingId } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [selectedIds, setSelectedIds] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [coupon, setCoupon] = useState('')
  const [couponResult, setCouponResult] = useState(null)

  useEffect(() => { fetchSeats(showTimingId).then(setData).catch(console.error).finally(() => setLoading(false)) }, [showTimingId])

  const toggleSeat = id => { setSelectedIds(p => p.includes(id) ? p.filter(x => x !== id) : [...p, id]); setError('') }
  const applyRecommendation = async pref => {
    try {
      const res = await fetchRecommended(showTimingId, { count: 2, preference: pref })
      setSelectedIds(res.seats.map(s => s.id))
    } catch (e) { console.error(e) }
  }

  const basePrice = data?.base_price || 0
  const subtotal = selectedIds.reduce((sum, sid) => {
    const s = data?.seats?.find(x => x.id === sid)
    return sum + (s?.price || basePrice)
  }, 0)
  const discount = couponResult?.valid ? couponResult.discount_amount : 0
  const total = Math.max(0, subtotal - discount)

  const validateCouponCode = async () => {
    if (!coupon.trim()) return
    try { const r = await validateCoupon({ code: coupon, order_amount: subtotal }); setCouponResult(r); if (!r.valid) setError(r.message) }
    catch (e) { setError('Coupon validation failed') }
  }

  const handleConfirm = async () => {
    if (selectedIds.length === 0) return setError('Select at least one seat')
    setSubmitting(true); setError('')
    try {
      const r = await createBooking({ show_timing_id: parseInt(showTimingId), seat_ids: selectedIds, coupon_code: couponResult?.valid ? coupon : undefined })
      navigate(`/booking/${r.booking_reference}`)
    } catch (e) { setError(e.response?.data?.detail || 'Booking failed') }
    finally { setSubmitting(false) }
  }

  if (loading) return <p className="loading">Loading seats...</p>
  if (!data) return <p className="empty">Show not found.</p>

  return (
    <div className="page">
      <h2>Select Seats</h2>
      <div className="show-summary"><span>{data.hall_name} - {data.screen_name}</span><span>{new Date(data.show_time).toLocaleString('en-IN')}</span><span className="price">₹{basePrice.toFixed(2)}+</span></div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        <button className="btn btn-outline btn-sm" onClick={() => applyRecommendation('best_view')}>🎯 Best View</button>
        <button className="btn btn-outline btn-sm" onClick={() => applyRecommendation('couples')}>💑 Couples</button>
        <button className="btn btn-outline btn-sm" onClick={() => applyRecommendation('budget')}>💰 Budget</button>
      </div>
      <SeatMap seats={data.seats} selectedIds={selectedIds} onToggleSeat={toggleSeat} />
      <div className="booking-form">
        {selectedIds.length > 0 && (
          <div className="summary-box">
            <p><strong>Seats:</strong> {selectedIds.map(sid => { const s = data.seats.find(x => x.id === sid); return s ? `${s.row_label}-${s.seat_number}` : '' }).filter(Boolean).join(', ')}</p>
            <p><strong>Subtotal:</strong> ₹{subtotal.toFixed(2)}</p>
            <div className="coupon-input">
              <input type="text" placeholder="Coupon code" value={coupon} onChange={e => setCoupon(e.target.value)} />
              <button className="btn btn-outline btn-sm" onClick={validateCouponCode}>Apply</button>
            </div>
            {couponResult?.valid && <p className="success">Discount: -₹{discount.toFixed(2)}</p>}
            <p><strong>Total:</strong> ₹{total.toFixed(2)} ({selectedIds.length} seat{selectedIds.length > 1 ? 's' : ''})</p>
          </div>
        )}
        {error && <p className="error">{error}</p>}
        <button className="btn btn-primary btn-lg" onClick={handleConfirm} disabled={submitting}>{submitting ? 'Booking...' : 'Confirm Booking'}</button>
      </div>
    </div>
  )
}
