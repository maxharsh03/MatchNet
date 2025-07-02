from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Player(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    rank: int
    rank_points: int
    last_updated: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
