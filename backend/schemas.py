from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ---------- Auth schemas ----------

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    email: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


# ---------- Movie schemas ----------

class MovieOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    language: Optional[str] = None

    model_config = {"from_attributes": True}


class ShowTimingOut(BaseModel):
    id: int
    movie_id: int
    hall_name: str
    show_time: datetime
    price: float

    model_config = {"from_attributes": True}


class MovieDetailOut(MovieOut):
    show_timings: List[ShowTimingOut] = []


# ---------- Seat schemas ----------

class SeatOut(BaseModel):
    id: int
    show_timing_id: int
    row_label: str
    seat_number: int
    is_booked: bool

    model_config = {"from_attributes": True}


class ShowTimingSeatsOut(BaseModel):
    show_timing_id: int
    hall_name: str
    show_time: datetime
    price: float
    seats: List[SeatOut]


# ---------- Booking schemas ----------

class BookingRequest(BaseModel):
    user_name: str
    user_email: str
    show_timing_id: int
    seat_ids: List[int]


class BookingSeatDetail(BaseModel):
    seat_id: int
    row_label: str
    seat_number: int


class BookingResponse(BaseModel):
    booking_reference: str
    total_amount: float
    seats: List[str]  # e.g. ["A-4", "A-5"]
    movie_title: str
    show_time: datetime
    hall_name: str
    user_name: str
    user_email: str
