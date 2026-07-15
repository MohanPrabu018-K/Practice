"""Movies, theatres, shows, seats, bookings, reviews APIs."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, and_
from typing import Optional

from app.database import get_db
from app.models.movie import Movie
from app.models.show import ShowTiming
from app.models.screen import Screen
from app.models.theatre import Theatre
from app.models.seat import Seat, SeatCategory
from app.models.review import Review
from app.models.user import User
from app.models.booking import Booking, BookingSeat
from app.dependencies import get_current_user, get_admin_user, get_optional_user
from app.utils.security import generate_booking_reference, create_access_token
from app.utils.pagination import Paginator
from app.schemas import *

router = APIRouter(prefix="/api", tags=["Core"])

# ── Movies ────────────────────────────────────────────

@router.get("/movies", response_model=PaginatedMovies)
def list_movies(
    genre: str | None = None, language: str | None = None,
    theatre_id: int | None = None, date: str | None = None,
    search: str | None = None, upcoming: bool | None = None,
    trending: bool | None = None, page: int = 1, limit: int = 12,
    db: Session = Depends(get_db),
):
    q = select(Movie)
    if genre: q = q.where(Movie.genre == genre)
    if language: q = q.where(Movie.language == language)
    if upcoming is not None: q = q.where(Movie.is_upcoming == upcoming)
    if search: q = q.where(Movie.title.ilike(f"%{search}%"))
    if theatre_id:
        show_movie_ids = select(ShowTiming.movie_id).join(Screen).where(Screen.theatre_id == theatre_id).subquery()
        q = q.where(Movie.id.in_(select(show_movie_ids)))
    if date:
        from datetime import datetime as dt
        parsed = dt.fromisoformat(date)
        show_movie_ids = select(ShowTiming.movie_id).where(func.date(ShowTiming.show_time) == parsed.date()).subquery()
        q = q.where(Movie.id.in_(select(show_movie_ids)))
    if trending:
        week_ago = func.now() - func.make_interval(0, 0, 0, 7)
        trending_q = select(BookingSeat.booking_id).join(Booking).where(Booking.booking_time >= week_ago).subquery()
    p = Paginator(db, q, page, limit); result = p.paginate()
    return result

@router.get("/movies/{movie_id}", response_model=MovieDetailOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    m = db.execute(select(Movie).options(joinedload(Movie.show_timings).joinedload(ShowTiming.screen).joinedload(Screen.theatre)).where(Movie.id == movie_id)).unique().scalar_one_or_none()
    if not m: raise HTTPException(404, "Movie not found")
    out = MovieDetailOut.model_validate(m)
    out.show_timings = [ShowTimingOut(id=s.id,movie_id=s.movie_id,screen_id=s.screen_id,show_time=s.show_time,base_price=s.base_price,screen_name=s.screen.name if s.screen else "",hall_name=s.screen.theatre.name if s.screen and s.screen.theatre else "") for s in m.show_timings]
    return out

# ── Theatres ──────────────────────────────────────────

@router.get("/theatres", response_model=list[TheatreOut])
def list_theatres(db: Session = Depends(get_db)):
    return db.execute(select(Theatre).options(joinedload(Theatre.screens))).unique().scalars().all()

# ── Shows / Seats ─────────────────────────────────────

@router.get("/show-timings/{show_id}/seats", response_model=ShowTimingSeatsOut)
def get_seats(show_id: int, db: Session = Depends(get_db)):
    show = db.execute(select(ShowTiming).options(joinedload(ShowTiming.seats).joinedload(Seat.category), joinedload(ShowTiming.screen).joinedload(Screen.theatre)).where(ShowTiming.id == show_id)).unique().scalar_one_or_none()
    if not show: raise HTTPException(404, "Show not found")
    return ShowTimingSeatsOut(
        show_timing_id=show.id, show_time=show.show_time, base_price=show.base_price,
        screen_name=show.screen.name if show.screen else "",
        hall_name=show.screen.theatre.name if show.screen and show.screen.theatre else "",
        seats=[SeatOut(id=s.id,show_timing_id=s.show_timing_id,row_label=s.row_label,seat_number=s.seat_number,is_booked=s.is_booked,category_id=s.category_id,category_name=s.category.name if s.category else "",price=show.base_price*s.category.price_multiplier if s.category else show.base_price) for s in show.seats]
    )

# ── Recommended Seats ─────────────────────────────────

@router.get("/show-timings/{show_id}/recommended")
def recommend_seats(show_id: int, count: int = 2, preference: str = "best_view", db: Session = Depends(get_db)):
    show = db.execute(select(ShowTiming).options(joinedload(ShowTiming.seats).joinedload(Seat.category)).where(ShowTiming.id == show_id)).unique().scalar_one_or_none()
    if not show: raise HTTPException(404)
    avail = [s for s in show.seats if not s.is_booked]
    if len(avail) < count: raise HTTPException(400, "Not enough seats")
    result = []
    if preference == "couples":
        back_rows = sorted(set(s.row_label for s in avail), reverse=True)
        for row in back_rows:
            row_seats = sorted([s for s in avail if s.row_label == row], key=lambda x: x.seat_number)
            for i in range(len(row_seats)-1):
                if row_seats[i].seat_number+1 == row_seats[i+1].seat_number:
                    result.extend([row_seats[i], row_seats[i+1]])
                    break
            if result: break
        if not result: result = avail[:count]
    elif preference == "budget":
        result = sorted(avail, key=lambda s: (s.category.price_multiplier if s.category else 1.0, s.row_label, s.seat_number))[:count]
    else:  # best_view
        mid_row_idx = len(list(set(s.row_label for s in avail))) // 2
        rows = sorted(set(s.row_label for s in avail))
        mid_row = rows[min(mid_row_idx, len(rows)-1)]
        mid_col_start = max(1, 10//2 - count//2)
        row_seats = {s.seat_number: s for s in avail if s.row_label == mid_row}
        for n in range(mid_col_start, mid_col_start+count):
            if n in row_seats: result.append(row_seats[n])
        if len(result) < count: result = avail[:count]
    return {"seats": [SeatOut(id=s.id,show_timing_id=s.show_timing_id,row_label=s.row_label,seat_number=s.seat_number,is_booked=s.is_booked,category_id=s.category_id,category_name=s.category.name if s.category else "",price=show.base_price*s.category.price_multiplier if s.category else show.base_price) for s in result]}

# ── Bookings ──────────────────────────────────────────

@router.post("/bookings", response_model=BookingResponse)
def create_booking(req: BookingRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    show = db.get(ShowTiming, req.show_timing_id)
    if not show: raise HTTPException(404, "Show not found")
    seats = db.execute(select(Seat).where(and_(Seat.id.in_(req.seat_ids), Seat.show_timing_id == req.show_timing_id)).with_for_update()).scalars().all()
    if len(seats) != len(req.seat_ids): raise HTTPException(400, "Invalid seats")
    booked = [s for s in seats if s.is_booked]
    if booked: raise HTTPException(409, f"Already booked: {', '.join(f'{s.row_label}-{s.seat_number}' for s in booked)}")
    total = sum(show.base_price * (s.category.price_multiplier if s.category else 1.0) for s in seats)
    discount = 0.0
    if req.coupon_code:
        cp = db.execute(select(Coupon).where(Coupon.code == req.coupon_code, Coupon.is_active == True, Coupon.expires_at > func.now(), Coupon.used_count < Coupon.max_uses)).scalar_one_or_none()
        if cp and total >= cp.min_order_amount:
            if cp.discount_percent > 0:
                discount = total * cp.discount_percent / 100
            cp.used_count += 1
    for s in seats: s.is_booked = True
    ref = generate_booking_reference()
    b = Booking(user_id=user.id, booking_reference=ref, status="confirmed", total_amount=total-discount, discount_amount=discount)
    db.add(b); db.flush()
    for s in seats: db.add(BookingSeat(booking_id=b.id, seat_id=s.id))
    db.commit()
    return BookingResponse(booking_reference=ref, total_amount=round(total-discount,2), discount_amount=round(discount,2), seats=[f"{s.row_label}-{s.seat_number}" for s in seats], movie_title=show.movie.title, show_time=show.show_time, hall_name=show.screen.theatre.name if show.screen and show.screen.theatre else "", screen_name=show.screen.name if show.screen else "", status="confirmed", user_name=user.username, user_email=user.email)

@router.get("/bookings/{ref}", response_model=BookingResponse)
def get_booking(ref: str, db: Session = Depends(get_db)):
    b = db.execute(select(Booking).options(joinedload(Booking.seats)).where(Booking.booking_reference == ref)).unique().scalar_one_or_none()
    if not b: raise HTTPException(404, "Not found")
    if not b.seats: raise HTTPException(404)
    show = db.get(ShowTiming, b.seats[0].show_timing_id)
    return BookingResponse(booking_reference=b.booking_reference, total_amount=b.total_amount, discount_amount=b.discount_amount, seats=[f"{s.row_label}-{s.seat_number}" for s in b.seats], movie_title=show.movie.title, show_time=show.show_time, hall_name=show.screen.theatre.name if show.screen and show.screen.theatre else "", screen_name=show.screen.name if show.screen else "", status=b.status, user_name=b.user.username if b.user else "", user_email=b.user.email if b.user else "")

@router.get("/users/me/bookings", response_model=PaginatedBookings)
def my_bookings(page: int = 1, limit: int = 10, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = select(Booking).options(joinedload(Booking.seats)).where(Booking.user_id == user.id).order_by(Booking.booking_time.desc())
    p = Paginator(db, q, page, limit); r = p.paginate()
    items = []
    for b in r["items"]:
        show = db.get(ShowTiming, b.seats[0].show_timing_id) if b.seats else None
        items.append(BookingHistoryItem(booking_reference=b.booking_reference, movie_title=show.movie.title if show and show.movie else "N/A", show_time=show.show_time if show else datetime.now(), hall_name=show.screen.theatre.name if show and show.screen and show.screen.theatre else "", seats=[f"{s.row_label}-{s.seat_number}" for s in b.seats], total_amount=b.total_amount, status=b.status, booking_time=b.booking_time))
    return {"items": items, "total": r["total"], "page": r["page"], "limit": r["limit"], "total_pages": r["total_pages"]}

# ── Reviews ───────────────────────────────────────────

@router.get("/movies/{movie_id}/reviews", response_model=PaginatedReviews)
def get_reviews(movie_id: int, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    q = select(Review).where(Review.movie_id == movie_id).order_by(Review.created_at.desc())
    p = Paginator(db, q, page, limit); r = p.paginate()
    items = [ReviewOut(id=rv.id, user_id=rv.user_id, rating=rv.rating, comment=rv.comment, username=rv.user.username, created_at=rv.created_at) for rv in r["items"]]
    return {"items": items, "total": r["total"], "page": r["page"], "limit": r["limit"], "total_pages": r["total_pages"]}

@router.post("/movies/{movie_id}/reviews", status_code=201)
def add_review(movie_id: int, req: ReviewCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Movie, movie_id): raise HTTPException(404, "Movie not found")
    existing = db.execute(select(Review).where(and_(Review.user_id == user.id, Review.movie_id == movie_id))).scalar_one_or_none()
    if existing: existing.rating, existing.comment = req.rating, req.comment
    else: db.add(Review(user_id=user.id, movie_id=movie_id, rating=req.rating, comment=req.comment))
    db.commit()
    avg = db.scalar(select(func.avg(Review.rating)).where(Review.movie_id == movie_id)) or 0
    count = db.scalar(select(func.count(Review.id)).where(Review.movie_id == movie_id)) or 0
    movie = db.get(Movie, movie_id); movie.average_rating = round(float(avg), 1); movie.total_reviews = count
    db.commit()
    return {"message": "Review saved"}

# ── Coupons ───────────────────────────────────────────

@router.post("/coupons/validate", response_model=CouponValidateResponse)
def validate_coupon(req: CouponValidateRequest, db: Session = Depends(get_db)):
    cp = db.execute(select(Coupon).where(Coupon.code == req.code, Coupon.is_active == True, Coupon.expires_at > func.now(), Coupon.used_count < Coupon.max_uses)).scalar_one_or_none()
    if not cp: return CouponValidateResponse(valid=False, message="Invalid or expired coupon")
    if req.order_amount < cp.min_order_amount:
        return CouponValidateResponse(valid=False, message=f"Minimum order: ₹{cp.min_order_amount}")
    disc = req.order_amount * cp.discount_percent / 100 if cp.discount_percent > 0 else 100
    return CouponValidateResponse(valid=True, discount_percent=cp.discount_percent, discount_amount=round(disc,2), final_amount=round(req.order_amount-disc,2), message=f"{cp.discount_percent}% off applied!")
