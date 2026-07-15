from pydantic import BaseModel

class RecommendedSeatsRequest(BaseModel):
    count: int = 2; preference: str = "best_view"
