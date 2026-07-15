from pydantic import BaseModel
from typing import List, Optional

class ScreenOut(BaseModel):
    id: int; theatre_id: int; name: str; total_rows: int; total_cols: int
    model_config = {"from_attributes": True}

class TheatreOut(BaseModel):
    id: int; name: str; location: str; city: str; contact: Optional[str] = None
    screens: List[ScreenOut] = []
    model_config = {"from_attributes": True}
