"""ShowTiming model — links movie to a theatre screen at a specific time."""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class ShowTiming(Base):
    __tablename__ = "show_timings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    show_time = Column(DateTime, nullable=False)
    base_price = Column(Float, nullable=False)

    movie = relationship("Movie", back_populates="show_timings")
    screen = relationship("Screen", back_populates="show_timings")
    seats = relationship("Seat", back_populates="show_timing", cascade="all, delete-orphan")
