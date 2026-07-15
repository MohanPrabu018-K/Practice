export default function Seat({ seat, isSelected, onToggle }) {
  let className = 'seat'
  if (seat.is_booked) {
    className += ' booked'
  } else if (isSelected) {
    className += ' selected'
  } else {
    className += ' available'
  }

  const handleClick = () => {
    if (!seat.is_booked) {
      onToggle(seat.id)
    }
  }

  return (
    <div className={className} onClick={handleClick} title={`${seat.row_label}-${seat.seat_number}`}>
      {seat.seat_number}
    </div>
  )
}
