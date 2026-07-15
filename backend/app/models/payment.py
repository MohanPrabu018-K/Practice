"""Payment & Refund models for Razorpay transactions."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, unique=True)
    razorpay_order_id = Column(String(100), unique=True, nullable=False)
    razorpay_payment_id = Column(String(100), unique=True, nullable=True)
    razorpay_signature = Column(String(500), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(String(30), default="created")  # created, paid, failed
    created_at = Column(DateTime, server_default=func.now())

    booking = relationship("Booking", back_populates="payment")


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, unique=True)
    razorpay_refund_id = Column(String(100), unique=True, nullable=True)
    amount = Column(Float, nullable=False)
    reason = Column(String(500))
    status = Column(String(30), default="initiated")
    created_at = Column(DateTime, server_default=func.now())

    booking = relationship("Booking", back_populates="refund")
