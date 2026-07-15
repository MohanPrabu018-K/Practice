from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ShowTimingOut(BaseModel):
    id: int; movie_id: int; screen_id: int; show_time: datetime; base_price: float
    screen_name: str = ""; hall_name: str = ""
    model_config = {"from_attributes": True}

class MovieOut(BaseModel):
    id: int; title: str; description: Optional[str] = None
    poster_url: Optional[str] = None; genre: Optional[str] = None
    duration: Optional[int] = None; language: Optional[str] = None
    release_date: Optional[datetime] = None; is_upcoming: bool = False
    average_rating: float = 0.0; total_reviews: int = 0
    model_config = {"from_attributes": True}

class MovieDetailOut(MovieOut):
    show_timings: List[ShowTimingOut] = []

class ReviewOut(BaseModel):
    id: int; user_id: int; rating: int; comment: Optional[str] = None
    username: str = ""; created_at: datetime
    model_config = {"from_attributes": True}

class ReviewCreate(BaseModel):
    rating: int; comment: Optional[str] = None

class PaginatedMovies(BaseModel):
    items: List[MovieOut]; total: int; page: int; limit: int; total_pages: int

class PaginatedReviews(BaseModel):
    items: List[ReviewOut]; total: int; page: int; limit: int; total_pages: int
