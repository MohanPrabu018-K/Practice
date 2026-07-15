"""Movie model with ratings, trending, and upcoming support."""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    poster_url = Column(String(500))
    genre = Column(String(100))
    duration = Column(Integer)  # minutes
    language = Column(String(100))
    release_date = Column(DateTime)
    is_upcoming = Column(Boolean, default=False)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)

    show_timings = relationship("ShowTiming", back_populates="movie")
    reviews = relationship("Review", back_populates="movie")
