from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.player_stats_router import player_stats_router as player_stats
from app.routers.player_router import player_router as player
from app.routers.insight_router import insight_router as insight
from app.routers.match_router import match_router as match
from app.routers.trigger_pipeline_router import pipeline_router as pipeline

app = FastAPI()

# Allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(player_stats, prefix="/api/player-stats")
app.include_router(player, prefix="/api/players")
app.include_router(match, prefix="/api/matches")
app.include_router(insight, prefix="/api/insights")
app.include_router(pipeline, prefix="/api/trigger-pipeline")
