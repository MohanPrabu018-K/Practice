"""Admin dashboard APIs — complete CRUD, analytics, user/booking management."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, text, and_
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.movie import Movie
from app.models.theatre import Theatre
from app.models.screen import Screen
from app.models.show import ShowTiming
from app.models.seat import Seat, SeatCategory
from app.models.booking import Booking, BookingSeat
from app.models.coupon import Coupon
from app.models.review import Review
from app.dependencies import get_admin_user
from app.schemas import *

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# ── Dashboard ───────────────────────────────────────

@router.get("/dashboard", response_model=AdminDashboardResponse)
def dashboard(db: Session = Depends(get_db), _=Depends(get_admin_user)):
    today = datetime.utcnow().date()
    total_b = db.scalar(select(func.count(Booking.id))) or 0
    total_r = db.scalar(select(func.coalesce(func.sum(Booking.total_amount), 0))) or 0
    total_u = db.scalar(select(func.count(User.id))) or 0
    today_b = db.scalar(select(func.count(Booking.id)).where(func.date(Booking.booking_time) == today)) or 0
    today_r = db.scalar(select(func.coalesce(func.sum(Booking.total_amount), 0)).where(func.date(Booking.booking_time) == today)) or 0
    total_seats = db.scalar(select(func.count(Seat.id))) or 1
    booked_seats = db.scalar(select(func.count(Seat.id)).where(Seat.is_booked == True)) or 0
    occupancy = round(booked_seats / max(total_seats, 1) * 100, 1)

    stats = AdminStats(total_bookings=total_b, total_revenue=round(total_r, 2), total_users=total_u, today_bookings=today_b, today_revenue=round(today_r, 2), occupancy_rate=occupancy)

    revenue_trend = []
    for d in range(30, 0, -1):
        dt = today - timedelta(days=d)
        day_rev = db.scalar(select(func.coalesce(func.sum(Booking.total_amount), 0)).where(func.date(Booking.booking_time) == dt)) or 0
        day_b = db.scalar(select(func.count(Booking.id)).where(func.date(Booking.booking_time) == dt)) or 0
        revenue_trend.append(RevenueDataPoint(date=dt.isoformat(), revenue=round(day_rev, 2), bookings=day_b))

    occupancy_data = []
    shows = db.execute(select(ShowTiming).options(joinedload(ShowTiming.seats)).limit(10)).unique().scalars().all()
    for s in shows:
        total_s = len(s.seats) or 1
        booked_s = sum(1 for seat in s.seats if seat.is_booked) if s.seats else 0
        occupancy_data.append(OccupancyDataPoint(show_label=f"Show #{s.id}", occupancy=round(booked_s / total_s * 100, 1)))

    popular = db.execute(
        select(Movie.id, Movie.title, func.count(Booking.id).label("cnt"))
        .join(ShowTiming, ShowTiming.movie_id == Movie.id)
        .join(Seat, Seat.show_timing_id == ShowTiming.id)
        .join(BookingSeat, BookingSeat.seat_id == Seat.id)
        .join(Booking, Booking.id == BookingSeat.booking_id)
        .group_by(Movie.id).order_by(func.count(Booking.id).desc()).limit(5)
    ).all()
    popular_movies = [PopularMovie(movie_id=p[0], title=p[1], booking_count=p[2] or 0) for p in popular]

    return AdminDashboardResponse(stats=stats, revenue_trend=revenue_trend, occupancy_data=occupancy_data, popular_movies=popular_movies)

# ── Movies CRUD ─────────────────────────────────────

@router.get("/movies")
def admin_movies(page: int = 1, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.execute(select(Movie).offset((page-1)*20).limit(20)).scalars().all()

@router.post("/movies", status_code=201)
def create_movie(data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    m = Movie(**data); db.add(m); db.commit(); return {"id": m.id}

@router.put("/movies/{mid}")
def update_movie(mid: int, data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    m = db.get(Movie, mid)
    if not m: raise HTTPException(404)
    for k, v in data.items(): setattr(m, k, v)
    db.commit(); return {"ok": True}

@router.delete("/movies/{mid}")
def delete_movie(mid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    db.delete(db.get(Movie, mid)); db.commit(); return {"ok": True}

# ── Theatres CRUD ───────────────────────────────────

@router.get("/theatres")
def admin_theatres(db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.execute(select(Theatre).options(joinedload(Theatre.screens))).unique().scalars().all()

@router.post("/theatres", status_code=201)
def create_theatre(data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    t = Theatre(**data); db.add(t); db.commit(); return {"id": t.id}

@router.put("/theatres/{tid}")
def update_theatre(tid: int, data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    t = db.get(Theatre, tid)
    if not t: raise HTTPException(404)
    for k, v in data.items(): setattr(t, k, v)
    db.commit(); return {"ok": True}

@router.delete("/theatres/{tid}")
def delete_theatre(tid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    db.delete(db.get(Theatre, tid)); db.commit(); return {"ok": True}

@router.post("/screens", status_code=201)
def create_screen(data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    s = Screen(**data); db.add(s); db.commit(); return {"id": s.id}

@router.delete("/screens/{sid}")
def delete_screen(sid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    db.delete(db.get(Screen, sid)); db.commit(); return {"ok": True}

# ── Shows ───────────────────────────────────────────

@router.post("/shows", status_code=201)
def create_show(data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    s = ShowTiming(**data); db.add(s); db.flush()
    cats = db.query(SeatCategory).all()
    for row in ["A","B","C","D","E","F"]:
        for n in range(1, 11):
            cat = cats[2] if row in ("E","F") else (cats[1] if row in ("C","D") else cats[0])
            db.add(Seat(show_timing_id=s.id, row_label=row, seat_number=n, category_id=cat.id))
    db.commit(); return {"id": s.id}

@router.delete("/shows/{sid}")
def delete_show(sid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    db.delete(db.get(ShowTiming, sid)); db.commit(); return {"ok": True}

# ── Users ───────────────────────────────────────────

@router.get("/users")
def admin_users(page: int = 1, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.execute(select(User).offset((page-1)*20).limit(20)).scalars().all()

@router.put("/users/{uid}/role")
def change_role(uid: int, data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    u = db.get(User, uid)
    if not u: raise HTTPException(404)
    u.role = data.get("role", "user"); db.commit(); return {"ok": True}

@router.delete("/users/{uid}")
def delete_user(uid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    db.delete(db.get(User, uid)); db.commit(); return {"ok": True}

# ── Bookings ────────────────────────────────────────

@router.get("/bookings")
def admin_bookings(page: int = 1, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.execute(select(Booking).options(joinedload(Booking.seats)).order_by(Booking.booking_time.desc()).offset((page-1)*20).limit(20)).unique().scalars().all()

@router.put("/bookings/{bid}/cancel")
def cancel_booking(bid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    b = db.execute(select(Booking).options(joinedload(Booking.seats)).where(Booking.id == bid)).unique().scalar_one_or_none()
    if not b: raise HTTPException(404)
    b.status = "cancelled"; b.cancelled_at = datetime.utcnow()
    for seat in b.seats: seat.is_booked = False
    db.commit(); return {"ok": True}

# ── Reviews ─────────────────────────────────────────

@router.get("/reviews")
def admin_reviews(page: int = 1, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.execute(select(Review).options(joinedload(Review.user), joinedload(Review.movie)).order_by(Review.created_at.desc()).offset((page-1)*20).limit(20)).unique().scalars().all()

@router.delete("/reviews/{rid}")
def delete_review(rid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    r = db.get(Review, rid)
    if not r: raise HTTPException(404)
    movie_id = r.movie_id; db.delete(r); db.commit()
    avg = db.scalar(select(func.avg(Review.rating)).where(Review.movie_id == movie_id)) or 0
    count = db.scalar(select(func.count(Review.id)).where(Review.movie_id == movie_id)) or 0
    movie = db.get(Movie, movie_id); movie.average_rating = round(float(avg), 1); movie.total_reviews = count
    db.commit(); return {"ok": True}

# ── Coupons ─────────────────────────────────────────

@router.get("/coupons")
def admin_coupons(db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.execute(select(Coupon)).scalars().all()

@router.post("/coupons", status_code=201)
def create_coupon(data: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    c = Coupon(**data); db.add(c); db.commit(); return {"id": c.id}

@router.delete("/coupons/{cid}")
def delete_coupon(cid: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    db.delete(db.get(Coupon, cid)); db.commit(); return {"ok": True}
