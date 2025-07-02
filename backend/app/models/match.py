from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Match(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    player1_name: str
    player2_name: str
    surface: str
    date: str  # Format: YYYY-MM-DD
    tournament: str
    status1: Optional[str] = None
    status2: Optional[str] = None
    match_status: str  # LIVE, FINISHED, CANCELED, SCHEDULED
    player1_odds: Optional[List[str]] = None
    player2_odds: Optional[List[str]] = None
    player1_score: Optional[str] = None
    player2_score: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
