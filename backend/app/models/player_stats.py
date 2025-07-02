from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PlayerStats(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    atp_rank: Optional[int]
    age: Optional[float] = None
    elo: Optional[float] = None
    elo_rank: Optional[int] = None
    hElo: Optional[float] = None
    hElo_rank: Optional[int] = None
    cElo: Optional[float] = None
    cElo_rank: Optional[int] = None
    gElo: Optional[float] = None
    gElo_rank: Optional[int] = None
    peak_elo: Optional[float] = None
    peak_month: Optional[str] = None  # Format: YYYY-MM
    rank_points: Optional[int]
    last_updated: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
