from pydantic import BaseModel

class CouponValidateRequest(BaseModel):
    code: str; order_amount: float

class CouponValidateResponse(BaseModel):
    valid: bool; discount_percent: float = 0; discount_amount: float = 0
    final_amount: float = 0; message: str = ""
