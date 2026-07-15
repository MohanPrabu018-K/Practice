import Seat from './Seat'

const ROWS = ['A', 'B', 'C', 'D', 'E', 'F']

export default function SeatMap({ seats, selectedIds, onToggleSeat }) {
  const grouped = {}
  for (const row of ROWS) grouped[row] = seats.filter(s => s.row_label === row)

  return (
    <div className="seat-map">
      <div className="screen">SCREEN</div>
      {ROWS.map(row => (
        <div key={row} className="seat-row">
          <span className="row-label">{row}</span>
          {grouped[row].map(seat => (
            <Seat key={seat.id} seat={seat} isSelected={selectedIds.includes(seat.id)} onToggle={onToggleSeat} />
          ))}
        </div>
      ))}
      <div className="seat-legend">
        <span><span className="dot silver" /> Silver</span>
        <span><span className="dot gold" /> Gold</span>
        <span><span className="dot platinum" /> Platinum</span>
        <span><span className="dot selected" /> Selected</span>
        <span><span className="dot booked" /> Booked</span>
      </div>
    </div>
  )
}
