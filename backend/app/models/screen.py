"""Screen model belonging to a theatre."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Screen 1", "IMAX"
    total_rows = Column(Integer, default=6)
    total_cols = Column(Integer, default=10)

    theatre = relationship("Theatre", back_populates="screens")
    show_timings = relationship("ShowTiming", back_populates="screen")
