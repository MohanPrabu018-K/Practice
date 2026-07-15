from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class BookingRequest(BaseModel):
    show_timing_id: int; seat_ids: List[int]
    coupon_code: Optional[str] = None

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

class CancelResponse(BaseModel):
    message: str; refund_amount: float
