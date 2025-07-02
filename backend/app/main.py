from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import player_stats_router as player_stats, player_router as player, insight_router as insight, match_router as match, trigger_pipeline_router as pipeline

app = FastAPI()

# Allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(player_stats.player_stats_router, prefix="/api/player-stats")
app.include_router(player.player_router, prefix="/api/players")
app.include_router(match.match_router, prefix="/api/matches")
app.include_router(insight.insight_router, prefix="/api/insights")
app.include_router(pipeline.pipeline_router, prefix="/api/trigger-pipeline")