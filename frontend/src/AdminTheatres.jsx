import { useState, useEffect } from 'react'
import { fetchAdminTheatres, createTheatre, createScreen, deleteTheatre, deleteScreen } from './api'

export default function AdminTheatres() {
  const [theatres, setTheatres] = useState([])
  const [loading, setLoading] = useState(true)
  const [name, setName] = useState('')
  const [location, setLocation] = useState('')
  const [city, setCity] = useState('')
  const [addScreenTid, setAddScreenTid] = useState(null)
  const [screenName, setScreenName] = useState('')

  const load = () => { fetchAdminTheatres().then(setTheatres).catch(console.error).finally(() => setLoading(false)) }
  useEffect(() => { load() }, [])

  const handleAddTheatre = async e => {
    e.preventDefault()
    await createTheatre({ name, location, city, contact: '' })
    setName(''); setLocation(''); setCity('')
    load()
  }

  const handleAddScreen = async tid => {
    if (!screenName.trim()) return
    await createScreen({ theatre_id: tid, name: screenName, total_rows: 6, total_cols: 10 })
    setScreenName(''); setAddScreenTid(null)
    load()
  }

  if (loading) return <p className="loading">Loading...</p>

  return (
    <div className="page">
      <h2>Manage Theatres & Screens</h2>
      <div className="admin-card" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 12 }}>Add Theatre</h3>
        <form onSubmit={handleAddTheatre} className="form-row">
          <input placeholder="Theatre Name" value={name} onChange={e => setName(e.target.value)} required />
          <input placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} required />
          <input placeholder="City" value={city} onChange={e => setCity(e.target.value)} required />
          <button className="btn btn-primary btn-sm" type="submit">Add</button>
        </form>
      </div>
      {theatres.map(t => (
        <div key={t.id} className="admin-card" style={{ marginBottom: 12 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div><strong>{t.name}</strong><span style={{color:'#888',marginLeft:12}}>{t.location}, {t.city}</span></div>
            <button className="btn btn-danger btn-sm" onClick={() => deleteTheatre(t.id).then(load)}>Delete</button>
          </div>
          <div style={{ marginTop: 12 }}>
            <strong style={{ fontSize: '.9rem' }}>Screens:</strong>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 8 }}>
              {(t.screens||[]).map(s => (
                <span key={s.id} style={{ background: '#252540', padding: '4px 12px', borderRadius: 8, fontSize: '.85rem', display: 'flex', alignItems: 'center', gap: 8 }}>
                  {s.name}
                  <button onClick={() => deleteScreen(s.id).then(load)} style={{ background: 'none', border: 'none', color: '#ef5350', cursor: 'pointer', fontSize: '1rem' }}>×</button>
                </span>
              ))}
              {addScreenTid === t.id ? (
                <span style={{ display: 'flex', gap: 4 }}>
                  <input placeholder="Screen name" value={screenName} onChange={e => setScreenName(e.target.value)} style={{ width: 120, padding: '4px 8px', borderRadius: 6, border: '1px solid #333', background: '#0f0f1a', color: '#e4e4f0', fontSize: '.85rem' }} />
                  <button className="btn btn-primary btn-sm" style={{ padding: '2px 8px', fontSize: '.75rem' }} onClick={() => handleAddScreen(t.id)}>OK</button>
                  <button className="btn btn-outline btn-sm" style={{ padding: '2px 8px', fontSize: '.75rem' }} onClick={() => setAddScreenTid(null)}>×</button>
                </span>
              ) : (
                <button className="btn btn-outline btn-sm" style={{ padding: '2px 10px', fontSize: '.8rem' }} onClick={() => setAddScreenTid(t.id)}>+ Add Screen</button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
