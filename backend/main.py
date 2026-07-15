from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import random
import string
import time
import time

from database import engine, Base, get_db
from models import User, Movie, ShowTiming, Seat, Booking, BookingSeat
from schemas import (
    RegisterRequest, LoginRequest, TokenResponse, UserOut,
    MovieOut, MovieDetailOut, ShowTimingOut,
    SeatOut, ShowTimingSeatsOut,
    BookingRequest, BookingResponse,
)
from config import CORS_ORIGINS, SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES


# ---------- Password hashing ----------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------- JWT ----------

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = int(time.time()) + (JWT_EXPIRE_MINUTES * 60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ---------- App lifecycle ----------

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Movie Ticket Booking", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Auth endpoints ----------

@app.post("/api/auth/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.execute(select(User).where(User.username == req.username)).scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.execute(select(User).where(User.email == req.email)).scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=req.username,
        email=req.email,
        hashed_password=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "username": user.username})
    return TokenResponse(access_token=token, username=user.username, email=user.email)


@app.post("/api/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(User.username == req.username)
    ).scalar_one_or_none()

    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.id, "username": user.username})
    return TokenResponse(access_token=token, username=user.username, email=user.email)


@app.get("/api/auth/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ---------- Movies ----------

@app.get("/api/movies", response_model=list[MovieOut])
def list_movies(
    genre: str | None = None,
    language: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Movie)
    if genre:
        stmt = stmt.where(Movie.genre == genre)
    if language:
        stmt = stmt.where(Movie.language == language)
    return db.execute(stmt).scalars().all()


@app.get("/api/movies/{movie_id}", response_model=MovieDetailOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.execute(
        select(Movie)
        .options(joinedload(Movie.show_timings))
        .where(Movie.id == movie_id)
    ).unique().scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# ---------- Show Timings / Seats ----------

@app.get("/api/show-timings/{show_timing_id}/seats", response_model=ShowTimingSeatsOut)
def get_show_timing_seats(show_timing_id: int, db: Session = Depends(get_db)):
    timing = db.execute(
        select(ShowTiming)
        .options(joinedload(ShowTiming.seats))
        .where(ShowTiming.id == show_timing_id)
    ).unique().scalar_one_or_none()

    if not timing:
        raise HTTPException(status_code=404, detail="Show timing not found")

    return ShowTimingSeatsOut(
        show_timing_id=timing.id,
        hall_name=timing.hall_name,
        show_time=timing.show_time,
        price=timing.price,
        seats=[
            SeatOut(
                id=s.id,
                show_timing_id=s.show_timing_id,
                row_label=s.row_label,
                seat_number=s.seat_number,
                is_booked=s.is_booked,
            )
            for s in timing.seats
        ],
    )


# ---------- Bookings (protected) ----------

def _generate_reference() -> str:
    chars = string.ascii_uppercase + string.digits
    return "MOV-" + "".join(random.choices(chars, k=6))


@app.post("/api/bookings", response_model=BookingResponse)
def create_booking(
    req: BookingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    timing = db.get(ShowTiming, req.show_timing_id)
    if not timing:
        raise HTTPException(status_code=404, detail="Show timing not found")

    seats = db.execute(
        select(Seat).where(
            and_(
                Seat.id.in_(req.seat_ids),
                Seat.show_timing_id == req.show_timing_id,
            )
        ).with_for_update()
    ).scalars().all()

    if len(seats) != len(req.seat_ids):
        raise HTTPException(status_code=400, detail="Some seats not found for this show")

    already_booked = [s for s in seats if s.is_booked]
    if already_booked:
        conflict = [f"{s.row_label}-{s.seat_number}" for s in already_booked]
        raise HTTPException(status_code=409, detail=f"Seats already booked: {', '.join(conflict)}")

    for s in seats:
        s.is_booked = True

    booking_ref = _generate_reference()
    total_amount = len(seats) * timing.price

    booking = Booking(
        user_id=current_user.id,
        user_name=req.user_name,
        user_email=req.user_email,
        booking_reference=booking_ref,
        total_amount=total_amount,
    )
    db.add(booking)
    db.flush()

    for s in seats:
        db.add(BookingSeat(booking_id=booking.id, seat_id=s.id))

    db.commit()

    movie = db.get(Movie, timing.movie_id)
    seat_labels = [f"{s.row_label}-{s.seat_number}" for s in seats]

    return BookingResponse(
        booking_reference=booking_ref,
        total_amount=total_amount,
        seats=seat_labels,
        movie_title=movie.title,
        show_time=timing.show_time,
        hall_name=timing.hall_name,
        user_name=req.user_name,
        user_email=req.user_email,
    )


@app.get("/api/bookings/{reference}", response_model=BookingResponse)
def get_booking(reference: str, db: Session = Depends(get_db)):
    booking = db.execute(
        select(Booking)
        .options(joinedload(Booking.seats))
        .where(Booking.booking_reference == reference)
    ).unique().scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not booking.seats:
        raise HTTPException(status_code=404, detail="No seats linked to this booking")

    timing = db.get(ShowTiming, booking.seats[0].show_timing_id)
    movie = db.get(Movie, timing.movie_id)

    seat_labels = [f"{s.row_label}-{s.seat_number}" for s in booking.seats]

    return BookingResponse(
        booking_reference=booking.booking_reference,
        total_amount=booking.total_amount,
        seats=seat_labels,
        movie_title=movie.title,
        show_time=timing.show_time,
        hall_name=timing.hall_name,
        user_name=booking.user_name,
        user_email=booking.user_email,
    )
