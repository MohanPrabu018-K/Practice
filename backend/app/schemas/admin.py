from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.movie import MovieOut
from app.schemas.theatre import TheatreOut, ScreenOut

class PaymentCreateRequest(BaseModel):
    booking_id: int | None = None; amount: float
    show_timing_id: int; seat_ids: List[int]
    coupon_code: Optional[str] = None

class PaymentOrderResponse(BaseModel):
    order_id: str; amount: int; currency: str = "INR"; key_id: str

class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str; razorpay_payment_id: str
    razorpay_signature: str; show_timing_id: int
    seat_ids: List[int]; coupon_code: str | None = None

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
    stats: AdminStats
    revenue_trend: List[RevenueDataPoint]
    occupancy_data: List[OccupancyDataPoint]
    popular_movies: List[PopularMovie]
