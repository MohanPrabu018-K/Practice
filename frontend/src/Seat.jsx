export default function Seat({ seat, isSelected, onToggle }) {
  let cls = 'seat'
  if (seat.is_booked) { cls += ' booked' }
  else if (isSelected) { cls += ' selected' }
  else {
    const cn = seat.category_name?.toLowerCase() || ''
    if (cn === 'silver') cls += ' silver'
    else if (cn === 'gold') cls += ' gold'
    else if (cn === 'platinum') cls += ' platinum'
    else cls += ' available'
  }

  return (
    <div className={cls} onClick={() => !seat.is_booked && onToggle(seat.id)} title={`${seat.row_label}-${seat.seat_number} · ${seat.category_name || 'Standard'} · ₹${seat.price?.toFixed(2)}`}>
      {seat.seat_number}
    </div>
  )
}
