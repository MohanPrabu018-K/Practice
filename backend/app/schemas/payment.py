from pydantic import BaseModel
from typing import List, Optional

class CouponOut(BaseModel):
    id: int; code: str; discount_percent: float; max_uses: int
    used_count: int; is_active: bool; min_order_amount: float
    expires_at: str
    model_config = {"from_attributes": True}

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
