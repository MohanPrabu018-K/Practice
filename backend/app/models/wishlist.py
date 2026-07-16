"""Wishlist (favorites) model."""
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    movie = relationship("Movie")
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="uq_user_movie_wishlist"),)
