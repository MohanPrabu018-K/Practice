import { useState, useEffect } from 'react'
import { fetchDashboard } from './api'

export default function AdminDashboard() {
  const [dash, setDash] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchDashboard().then(setDash).catch(console.error).finally(() => setLoading(false)) }, [])

  if (loading) return <p className="loading">Loading dashboard...</p>
  if (!dash) return <p className="empty">Failed to load dashboard.</p>

  const maxR = Math.max(...dash.revenue_trend.map(x => x.revenue), 1)

  return (
    <div className="page">
      <h2>Admin Dashboard</h2>
      <div className="stats-grid">
        <div className="stat-card"><div className="stat-value">{dash.stats.total_bookings}</div><div className="stat-label">Total Bookings</div></div>
        <div className="stat-card"><div className="stat-value">₹{dash.stats.total_revenue.toFixed(0)}</div><div className="stat-label">Total Revenue</div></div>
        <div className="stat-card"><div className="stat-value">{dash.stats.total_users}</div><div className="stat-label">Total Users</div></div>
        <div className="stat-card"><div className="stat-value">{dash.stats.today_bookings}</div><div className="stat-label">Today's Bookings</div></div>
        <div className="stat-card"><div className="stat-value">₹{dash.stats.today_revenue.toFixed(0)}</div><div className="stat-label">Today's Revenue</div></div>
        <div className="stat-card"><div className="stat-value">{dash.stats.occupancy_rate}%</div><div className="stat-label">Occupancy Rate</div></div>
      </div>
      <div className="admin-card" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 12 }}>Revenue Trend (Last 30 Days)</h3>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 2, height: 150, overflow: 'hidden' }}>
          {dash.revenue_trend.map((d, i) => (
            <div key={i} title={`${d.date}: ₹${d.revenue} (${d.bookings} bookings)`} style={{ flex: 1, height: `${(d.revenue/maxR)*100}%`, background: '#7b4fbf', borderRadius: '2px 2px 0 0', minHeight: 4, opacity: .8 }} />
          ))}
        </div>
      </div>
      <div className="admin-card" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 12 }}>Top Movies by Bookings</h3>
        <table className="table">
          <thead><tr><th>Movie</th><th>Bookings</th></tr></thead>
          <tbody>
            {dash.popular_movies.map(m => (
              <tr key={m.movie_id}><td>{m.title}</td><td style={{color:'#e0aaff',fontWeight:600}}>{m.booking_count}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
