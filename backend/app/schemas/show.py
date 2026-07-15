from pydantic import BaseModel
from datetime import datetime
from typing import List

class SeatOut(BaseModel):
    id: int; show_timing_id: int; row_label: str; seat_number: int
    is_booked: bool; category_id: int | None = None
    category_name: str = ""; price: float = 0.0
    model_config = {"from_attributes": True}

class ShowTimingSeatsOut(BaseModel):
    show_timing_id: int; show_time: datetime; base_price: float
    screen_name: str; hall_name: str; seats: List[SeatOut]

class RecommendedSeatsRequest(BaseModel):
    count: int = 2; preference: str = "best_view"
