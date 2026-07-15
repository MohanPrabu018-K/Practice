"""Booking model with status tracking, coupon, and payment link."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_reference = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled, refunded
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    booking_time = Column(DateTime, server_default=func.now())
    cancelled_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="bookings")
    seats = relationship("Seat", secondary="booking_seats", backref="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)
    refund = relationship("Refund", back_populates="booking", uselist=False)


class BookingSeat(Base):
    __tablename__ = "booking_seats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)

    __table_args__ = (UniqueConstraint("booking_id", "seat_id", name="uq_booking_seat"),)
