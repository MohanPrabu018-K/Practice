import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { fetchDashboard, fetchAdminMovies, fetchAdminTheatres, fetchAdminBookings, fetchAdminCoupons } from './api'

export default function AdminDashboard() {
  const [dash, setDash] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchDashboard().then(setDash).catch(console.error).finally(() => setLoading(false)) }, [])

  if (loading) return <p className="loading">Loading dashboard...</p>
  if (!dash) return <p className="empty">Failed to load.</p>

  return (
    <div className="page">
      <div className="admin-layout">
        <div className="admin-sidebar">
          <Link to="/admin" className="active">Dashboard</Link>
          <Link to="/admin/movies">Movies</Link>
        </div>
        <div className="admin-content">
          <h2>Admin Dashboard</h2>
          <div className="stats-grid">
            <div className="stat-card"><div className="stat-value">{dash.stats.total_bookings}</div><div className="stat-label">Total Bookings</div></div>
            <div className="stat-card"><div className="stat-value">₹{dash.stats.total_revenue.toFixed(0)}</div><div className="stat-label">Total Revenue</div></div>
            <div className="stat-card"><div className="stat-value">{dash.stats.total_users}</div><div className="stat-label">Users</div></div>
            <div className="stat-card"><div className="stat-value">{dash.stats.occupancy_rate}%</div><div className="stat-label">Occupancy</div></div>
          </div>
          <div className="chart-container" style={{ height: 'auto', minHeight: 200 }}>
            <h3 style={{ marginBottom: 12 }}>Revenue Trend (30 days)</h3>
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: 2, height: 150, overflow: 'hidden' }}>
              {dash.revenue_trend.map((d, i) => {
                const maxR = Math.max(...dash.revenue_trend.map(x => x.revenue), 1)
                const h = (d.revenue / maxR) * 100
                return <div key={i} title={`${d.date}: ₹${d.revenue}`} style={{ flex: 1, height: `${h}%`, background: '#7b4fbf', borderRadius: '2px 2px 0 0', minHeight: 4, opacity: .8 }} />
              })}
            </div>
          </div>
          <div style={{ background: '#1a1a2e', borderRadius: 12, padding: 20, border: '1px solid #2a2a4a' }}>
            <h3 style={{ marginBottom: 12 }}>Popular Movies</h3>
            {dash.popular_movies.map(m => (
              <div key={m.movie_id} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #2a2a4a' }}>
                <span>{m.title}</span><span style={{ color: '#e0aaff', fontWeight: 600 }}>{m.booking_count} bookings</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
