"""All Pydantic schemas — consolidated to avoid circular imports."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ── Auth ────────────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str; email: str; password: str

class LoginRequest(BaseModel):
    username: str; password: str

class TokenResponse(BaseModel):
    access_token: str; refresh_token: str; token_type: str = "bearer"
    username: str; email: str; role: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserOut(BaseModel):
    id: int; username: str; email: str; role: str
    phone: Optional[str] = None; avatar_url: Optional[str] = None
    model_config = {"from_attributes": True}

class ProfileUpdate(BaseModel):
    email: Optional[str] = None; phone: Optional[str] = None
    avatar_url: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str; new_password: str

# ── Movie ───────────────────────────────────────────
class MovieOut(BaseModel):
    id: int; title: str; description: Optional[str] = None
    poster_url: Optional[str] = None; genre: Optional[str] = None
    duration: Optional[int] = None; language: Optional[str] = None
    release_date: Optional[datetime] = None; is_upcoming: bool = False
    average_rating: float = 0.0; total_reviews: int = 0
    model_config = {"from_attributes": True}

class MovieDetailOut(MovieOut):
    show_timings: List["ShowTimingOut"] = []

class PaginatedMovies(BaseModel):
    items: List[MovieOut]; total: int; page: int; limit: int; total_pages: int

# ── Show / Seat ─────────────────────────────────────
class ShowTimingOut(BaseModel):
    id: int; movie_id: int; screen_id: int; show_time: datetime; base_price: float
    screen_name: str = ""; hall_name: str = ""
    model_config = {"from_attributes": True}

class SeatOut(BaseModel):
    id: int; show_timing_id: int; row_label: str; seat_number: int
    is_booked: bool; category_id: Optional[int] = None
    category_name: str = ""; price: float = 0.0
    model_config = {"from_attributes": True}

class ShowTimingSeatsOut(BaseModel):
    show_timing_id: int; show_time: datetime; base_price: float
    screen_name: str; hall_name: str; seats: List[SeatOut]

# ── Theatre ─────────────────────────────────────────
class ScreenOut(BaseModel):
    id: int; theatre_id: int; name: str; total_rows: int; total_cols: int
    model_config = {"from_attributes": True}

class TheatreOut(BaseModel):
    id: int; name: str; location: str; city: str; contact: Optional[str] = None
    screens: List[ScreenOut] = []
    model_config = {"from_attributes": True}

# ── Review ──────────────────────────────────────────
class ReviewCreate(BaseModel):
    rating: int; comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: int; user_id: int; rating: int; comment: Optional[str] = None
    username: str = ""; created_at: datetime
    model_config = {"from_attributes": True}

class PaginatedReviews(BaseModel):
    items: List[ReviewOut]; total: int; page: int; limit: int; total_pages: int

# ── Booking ─────────────────────────────────────────
class BookingRequest(BaseModel):
    show_timing_id: int; seat_ids: List[int]; coupon_code: Optional[str] = None

class BookingResponse(BaseModel):
    booking_reference: str; total_amount: float; discount_amount: float = 0
    seats: List[str]; movie_title: str; show_time: datetime
    hall_name: str; screen_name: str = ""; status: str
    user_name: str = ""; user_email: str = ""

class BookingHistoryItem(BaseModel):
    booking_reference: str; movie_title: str; show_time: datetime
    hall_name: str; seats: List[str]; total_amount: float; status: str
    booking_time: datetime

class PaginatedBookings(BaseModel):
    items: List[BookingHistoryItem]; total: int; page: int; limit: int; total_pages: int

# ── Coupon ──────────────────────────────────────────
class CouponValidateRequest(BaseModel):
    code: str; order_amount: float

class CouponValidateResponse(BaseModel):
    valid: bool; discount_percent: float = 0; discount_amount: float = 0
    final_amount: float = 0; message: str = ""

class CouponOut(BaseModel):
    id: int; code: str; discount_percent: float; max_uses: int
    used_count: int; is_active: bool; min_order_amount: float
    expires_at: str
    model_config = {"from_attributes": True}

# ── Payment ─────────────────────────────────────────
class PaymentCreateRequest(BaseModel):
    booking_id: Optional[int] = None; amount: float
    show_timing_id: int; seat_ids: List[int]; coupon_code: Optional[str] = None

class PaymentOrderResponse(BaseModel):
    order_id: str; amount: int; currency: str = "INR"; key_id: str

class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str; razorpay_payment_id: str
    razorpay_signature: str; show_timing_id: int
    seat_ids: List[int]; coupon_code: Optional[str] = None

# ── Admin ───────────────────────────────────────────
class AdminStats(BaseModel):
    total_bookings: int; total_revenue: float; total_users: int
    today_bookings: int; today_revenue: float; occupancy_rate: float

class RevenueDataPoint(BaseModel):
    date: str; revenue: float; bookings: int

class OccupancyDataPoint(BaseModel):
    show_label: str; occupancy: float

class PopularMovie(BaseModel):
    movie_id: int; title: str; booking_count: int

class AdminDashboardResponse(BaseModel):
    stats: AdminStats; revenue_trend: List[RevenueDataPoint]
    occupancy_data: List[OccupancyDataPoint]; popular_movies: List[PopularMovie]
