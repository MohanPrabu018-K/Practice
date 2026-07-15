"""Seat model with category-based pricing."""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class SeatCategory(Base):
    __tablename__ = "seat_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # Silver, Gold, Platinum
    price_multiplier = Column(Float, nullable=False, default=1.0)  # 1.0, 1.5, 2.0
    color = Column(String(20), default="#1b5e20")  # hex color for UI


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    show_timing_id = Column(Integer, ForeignKey("show_timings.id"), nullable=False)
    row_label = Column(String(5), nullable=False)
    seat_number = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("seat_categories.id"), nullable=True)
    is_booked = Column(Boolean, default=False)
    locked_until = Column(DateTime, nullable=True)  # real-time lock expiry
    locked_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # who locked it

    show_timing = relationship("ShowTiming", back_populates="seats")
    category = relationship("SeatCategory")
