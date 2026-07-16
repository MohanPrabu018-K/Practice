import { useState, useEffect } from 'react'
import { fetchAdminCoupons, createCoupon, deleteCoupon } from './api'

export default function AdminCoupons() {
  const [coupons, setCoupons] = useState([])
  const [loading, setLoading] = useState(true)
  const [code, setCode] = useState('')
  const [discount, setDiscount] = useState('')
  const [maxUses, setMaxUses] = useState('100')
  const [minOrder, setMinOrder] = useState('0')
  const [expiry, setExpiry] = useState('')

  const load = () => { fetchAdminCoupons().then(setCoupons).catch(console.error).finally(() => setLoading(false)) }
  useEffect(() => { load() }, [])

  const handleAdd = async e => {
    e.preventDefault()
    if (!code.trim() || !discount.trim() || !expiry.trim()) return
    await createCoupon({ code: code.toUpperCase(), discount_percent: parseFloat(discount), max_uses: parseInt(maxUses)||100, min_order_amount: parseFloat(minOrder)||0, expires_at: new Date(expiry).toISOString(), is_active: true, used_count: 0 })
    setCode(''); setDiscount(''); setMaxUses('100'); setMinOrder('0'); setExpiry('')
    load()
  }

  if (loading) return <p className="loading">Loading...</p>

  return (
    <div className="page">
      <h2>Manage Coupons</h2>
      <div className="admin-card" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 12 }}>Add Coupon</h3>
        <form onSubmit={handleAdd} className="form-row">
          <input placeholder="Code" value={code} onChange={e => setCode(e.target.value)} required />
          <input placeholder="Discount %" type="number" value={discount} onChange={e => setDiscount(e.target.value)} required />
          <input placeholder="Max Uses" type="number" value={maxUses} onChange={e => setMaxUses(e.target.value)} />
          <input placeholder="Min Order" type="number" value={minOrder} onChange={e => setMinOrder(e.target.value)} />
          <input type="datetime-local" value={expiry} onChange={e => setExpiry(e.target.value)} required />
          <button className="btn btn-primary btn-sm" type="submit">Add</button>
        </form>
      </div>
      <table className="table">
        <thead><tr><th>Code</th><th>Discount</th><th>Used / Max</th><th>Min Order</th><th>Expires</th><th></th></tr></thead>
        <tbody>
          {coupons.map(c => (
            <tr key={c.id}>
              <td style={{ color: '#e0aaff', fontWeight: 600 }}>{c.code}</td>
              <td>{c.discount_percent}%</td>
              <td>{c.used_count}/{c.max_uses}</td>
              <td>₹{c.min_order_amount}</td>
              <td>{new Date(c.expires_at).toLocaleDateString('en-IN')}</td>
              <td><button className="btn btn-danger btn-sm" onClick={() => deleteCoupon(c.id).then(load)}>Del</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
