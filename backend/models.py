from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    poster_url = Column(String(500))
    genre = Column(String(100))
    duration = Column(Integer)  # minutes
    language = Column(String(100))

    show_timings = relationship("ShowTiming", back_populates="movie")


class ShowTiming(Base):
    __tablename__ = "show_timings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    hall_name = Column(String(100), nullable=False)
    show_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)

    movie = relationship("Movie", back_populates="show_timings")
    seats = relationship("Seat", back_populates="show_timing")


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    show_timing_id = Column(Integer, ForeignKey("show_timings.id"), nullable=False)
    row_label = Column(String(5), nullable=False)
    seat_number = Column(Integer, nullable=False)
    is_booked = Column(Boolean, default=False)

    show_timing = relationship("ShowTiming", back_populates="seats")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    booking_reference = Column(String(20), unique=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    booking_time = Column(DateTime, server_default=func.now())

    seats = relationship("Seat", secondary="booking_seats", backref="bookings")


class BookingSeat(Base):
    __tablename__ = "booking_seats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("booking_id", "seat_id", name="uq_booking_seat"),
    )
