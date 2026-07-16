"""Extras router — wishlist, cancellation, mock payment."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.movie import Movie
from app.models.booking import Booking, BookingSeat
from app.models.wishlist import Wishlist
from app.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["Extras"])

# ── Wishlist ────────────────────────────────────────

@router.get("/wishlist")
def get_wishlist(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.execute(select(Wishlist).options(joinedload(Wishlist.movie)).where(Wishlist.user_id == user.id)).unique().scalars().all()
    return [{"id": w.id, "movie": {"id": w.movie.id, "title": w.movie.title, "poster_url": w.movie.poster_url, "genre": w.movie.genre, "duration": w.movie.duration, "language": w.movie.language, "average_rating": w.movie.average_rating}} for w in items]

@router.post("/wishlist/{movie_id}", status_code=201)
def add_wishlist(movie_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Movie, movie_id): raise HTTPException(404, "Movie not found")
    existing = db.execute(select(Wishlist).where(and_(Wishlist.user_id == user.id, Wishlist.movie_id == movie_id))).scalar_one_or_none()
    if existing: return {"message": "Already in wishlist"}
    db.add(Wishlist(user_id=user.id, movie_id=movie_id)); db.commit()
    return {"message": "Added to wishlist"}

@router.delete("/wishlist/{movie_id}")
def remove_wishlist(movie_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.execute(select(Wishlist).where(and_(Wishlist.user_id == user.id, Wishlist.movie_id == movie_id))).scalar_one_or_none()
    if not w: raise HTTPException(404)
    db.delete(w); db.commit()
    return {"message": "Removed from wishlist"}

# ── Cancellation ────────────────────────────────────

@router.post("/bookings/{ref}/cancel")
def cancel_booking(ref: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    b = db.execute(select(Booking).options(joinedload(Booking.seats)).where(Booking.booking_reference == ref)).unique().scalar_one_or_none()
    if not b or b.user_id != user.id: raise HTTPException(404, "Booking not found")
    if b.status == "cancelled": raise HTTPException(400, "Already cancelled")

    # Refund policy: >24h before show = 90%, <24h = 50%
    show = None
    if b.seats:
        from app.models.show import ShowTiming
        show = db.get(ShowTiming, b.seats[0].show_timing_id)
    hours_left = 48
    if show and show.show_time:
        hours_left = (show.show_time - datetime.utcnow()).total_seconds() / 3600
    refund_pct = 90 if hours_left > 24 else (50 if hours_left > 0 else 0)
    refund_amount = round(b.total_amount * refund_pct / 100, 2)

    b.status = "cancelled"; b.cancelled_at = datetime.utcnow()
    for seat in b.seats: seat.is_booked = False
    db.commit()
    return {"message": "Booking cancelled", "refund_amount": refund_amount, "refund_percent": refund_pct}

# ── Mock Payment ────────────────────────────────────

@router.post("/mock-payment")
def mock_payment(user: User = Depends(get_current_user)):
    """Simulate a successful payment — always succeeds with transaction ID."""
    import random, string
    txn_id = "TXN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return {"success": True, "transaction_id": txn_id, "message": "Payment successful (mock)"}
