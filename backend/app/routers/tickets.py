from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
import jwt

from app.database import get_db
from app.models.user import User
from app.models.booking import Booking
from app.models.show import ShowTiming
from app.models.screen import Screen
from app.config import settings
from app.services.ticket_service import generate_qr_base64, generate_ticket_pdf

router = APIRouter(prefix="/api", tags=["Tickets"])


def _resolve_user(header_token: str | None, query_token: str | None, db: Session) -> User:
    """Resolve user from Authorization header or ?token= query param."""
    token = header_token or query_token
    if not token:
        raise HTTPException(401, "Authentication required")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user = db.get(User, payload.get("sub"))
        if not user:
            raise HTTPException(401, "User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")


@router.get("/bookings/{ref}/qr")
def booking_qr(
    ref: str,
    token: str | None = Query(None),
    db: Session = Depends(get_db),
    authorization: str | None = None,
):
    header_token = authorization.replace("Bearer ", "") if authorization and authorization.startswith("Bearer ") else None
    user = _resolve_user(header_token, token, db)
    b = db.execute(select(Booking).options(joinedload(Booking.seats)).where(Booking.booking_reference == ref)).unique().scalar_one_or_none()
    if not b or b.user_id != user.id:
        raise HTTPException(403, "Access denied")
    qr_data = f"MOVIEBOOKER|{b.booking_reference}|{b.user_id}"
    return {"qr_base64": generate_qr_base64(qr_data)}


@router.get("/bookings/{ref}/pdf")
def booking_pdf(
    ref: str,
    token: str | None = Query(None),
    db: Session = Depends(get_db),
    authorization: str | None = None,
):
    header_token = authorization.replace("Bearer ", "") if authorization and authorization.startswith("Bearer ") else None
    user = _resolve_user(header_token, token, db)
    b = db.execute(select(Booking).options(joinedload(Booking.seats)).where(Booking.booking_reference == ref)).unique().scalar_one_or_none()
    if not b or b.user_id != user.id:
        raise HTTPException(403, "Access denied")

    show = None
    if b.seats:
        show = db.execute(
            select(ShowTiming)
            .options(joinedload(ShowTiming.movie), joinedload(ShowTiming.screen).joinedload(Screen.theatre))
            .where(ShowTiming.id == b.seats[0].show_timing_id)
        ).unique().scalar_one_or_none()

    movie_title = show.movie.title if show and show.movie else "N/A"
    hall_name = show.screen.theatre.name if show and show.screen and show.screen.theatre else ""
    screen_name = show.screen.name if show and show.screen else ""
    show_time_str = show.show_time.strftime("%d %b %Y, %I:%M %p") if show and show.show_time else ""

    pdf = generate_ticket_pdf({
        "booking_reference": b.booking_reference,
        "movie_title": movie_title,
        "hall_name": hall_name,
        "screen_name": screen_name,
        "show_time_str": show_time_str,
        "seats": [f"{s.row_label}-{s.seat_number}" for s in b.seats],
        "total_amount": b.total_amount,
        "status": b.status,
        "booking_time_str": b.booking_time.strftime("%d %b %Y, %I:%M %p") if b.booking_time else "",
    })
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=ticket-{b.booking_reference}.pdf"})
