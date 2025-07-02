from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Insight(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    player1_name: Optional[str]
    player2_name: Optional[str]
    player1_rank: Optional[int]
    player2_rank: Optional[int]
    probability_player1: Optional[float]
    probability_player2: Optional[float]
    ev_player1: Optional[float]
    ev_player2: Optional[float]
    bet_on_player1: Optional[bool]
    bet_on_player2: Optional[bool]
    best_line_player1: Optional[float]
    best_line_player2: Optional[float]
    best_book_player1: Optional[str]
    best_book_player2: Optional[str]
    date: Optional[str]
    time: Optional[str]
    match_id: Optional[str] = None  # Optional reference to Match _id

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
