"""Import all models so Alembic and Base.metadata can discover them."""
from app.models.user import User
from app.models.movie import Movie
from app.models.theatre import Theatre
from app.models.screen import Screen
from app.models.show import ShowTiming
from app.models.seat import Seat, SeatCategory
from app.models.booking import Booking, BookingSeat
from app.models.review import Review
from app.models.coupon import Coupon
from app.models.payment import Payment, Refund
from app.models.refresh_token import RefreshToken

__all__ = [
    "User", "Movie", "Theatre", "Screen", "ShowTiming",
    "Seat", "SeatCategory", "Booking", "BookingSeat",
    "Review", "Coupon", "Payment", "Refund", "RefreshToken",
]
