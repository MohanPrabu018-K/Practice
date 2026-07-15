from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ReviewOut(BaseModel):
    id: int; user_id: int; rating: int; comment: Optional[str] = None
    username: str = ""; created_at: datetime
    model_config = {"from_attributes": True}

class ReviewCreate(BaseModel):
    rating: int; comment: Optional[str] = None

class PaginatedReviews(BaseModel):
    items: List[ReviewOut]; total: int; page: int; limit: int; total_pages: int
