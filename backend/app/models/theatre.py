"""Theatre model with multiple screens."""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Theatre(Base):
    __tablename__ = "theatres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    contact = Column(String(20))

    screens = relationship("Screen", back_populates="theatre", cascade="all, delete-orphan")
