from fastapi import APIRouter
from db.mongodb import db
import subprocess
import pandas as pd
import os
from bson import ObjectId
import math
import ast
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dateutil import tz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from model.prediction import prediction
from betting.expected_value import compute_ev_and_suggestion_with_bookmaker

pipeline_router = APIRouter()

# Load .env from root (adjust path as needed)
# Step 1: Dynamically determine the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # Assumes this script is in `backend/scraping/` or similar

# Step 2: Load .env from root
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# Step 3: Resolve all env vars to absolute paths
def resolve_path(var_name):
    relative_path = os.getenv(var_name)
    if not relative_path:
        raise ValueError(f"{var_name} not found in .env")
    return PROJECT_ROOT / relative_path

# Step 4: Get paths
players_path = resolve_path("PLAYERS_CSV")
player_stats_path = resolve_path("PLAYER_STATS_CSV")
matches_path = resolve_path("MATCHES_CSV")
pipeline_path = resolve_path("PIPELINE_PATH")
BET_SIZE = 10

def to_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0  # or some default

def clean_nan_values(stat: dict):
    return {
        k: (None if isinstance(v, float) and math.isnan(v) else v)
        for k, v in stat.items()
    }

@pipeline_router.post("/")
async def trigger_pipeline():
    """
    This route is triggered hourly from the frontend.
    It runs the pipeline.py script, then reads generated CSVs to update the database.
    """
    try:
        # Run pipeline.py as a subprocess and wait for it to finish
        result = subprocess.run(["python", pipeline_path], capture_output=True, text=True)

        print(result)
        
        if result.returncode != 0:
            raise RuntimeError(f"Pipeline failed: {result.stderr}")
        
        # Load and process player stats csv
        player_stats_collection = db.player_stats
        if os.path.exists(player_stats_path):
            df = pd.read_csv(player_stats_path)
            df['rank_points'] = df['rank_points'].apply(
                lambda x: int(str(x).replace(',', '')) if pd.notna(x) else None
            )
            for _, row in df.iterrows():
                stat = clean_nan_values(row.to_dict())
                existing = await player_stats_collection.find_one({"name": stat["name"]})

                if existing:
                    # Ensure last_updated is a proper datetime object and UTC-aware
                    last_updated_raw = existing.get("last_updated")
                    now = datetime.now(timezone.utc)

                    last_updated = None
                    if isinstance(last_updated_raw, str):
                        try:
                            # Attempt to parse from ISO string
                            last_updated = datetime.fromisoformat(last_updated_raw)
                            # If the parsed datetime is naive, assume it's UTC
                            if last_updated.tzinfo is None:
                                last_updated = last_updated.replace(tzinfo=timezone.utc)
                        except ValueError:
                            pass
                    elif isinstance(last_updated_raw, datetime):
                        last_updated = last_updated_raw
                        # If it's naive, assume it's UTC
                        if last_updated.tzinfo is None:
                            last_updated = last_updated.replace(tzinfo=timezone.utc)

                    if last_updated and (now - last_updated >= timedelta(days=7)):
                        fields_to_update = {
                            "atp_rank": stat.get("atp_rank"),
                            "age": stat.get("age"),
                            "elo": stat.get("elo"),
                            "elo_rank": stat.get("elo_rank"),
                            "hElo": stat.get("hElo"),
                            "hElo_rank": stat.get("hElo_rank"),
                            "chElo": stat.get("cElo"),
                            "cElo_rank": stat.get("cElo_rank"),
                            "gElo": stat.get("gElo"),
                            "gElo_rank": stat.get("gElo_rank"),
                            "peak_elo": stat.get("peak_elo"),
                            "peak_month": stat.get("peak_month"),
                            "rank_points": stat.get("rank_points"),
                            "last_updated": now
                        }
                        await player_stats_collection.update_one(
                            {"_id": existing["_id"]},
                            {"$set": fields_to_update}
                        )
                else:
                    stat["last_updated"] = datetime.now(timezone.utc)
                    await player_stats_collection.insert_one(stat)

        # Load and process player csv
        player_collection = db.players
        if os.path.exists(players_path):
            df = pd.read_csv(players_path)
            for _, row in df.iterrows():
                stat = row.to_dict()
                existing = await player_collection.find_one({"name": stat["name"]})
                if existing:
                    # Ensure last_updated is a proper datetime object and UTC-aware
                    last_updated_raw = existing.get("last_updated")
                    now = datetime.now(timezone.utc)

                    last_updated = None
                    if isinstance(last_updated_raw, str):
                        try:
                            # Attempt to parse from ISO string
                            last_updated = datetime.fromisoformat(last_updated_raw)
                            # If the parsed datetime is naive, assume it's UTC
                            if last_updated.tzinfo is None:
                                last_updated = last_updated.replace(tzinfo=timezone.utc)
                        except ValueError:
                            pass
                    elif isinstance(last_updated_raw, datetime):
                        last_updated = last_updated_raw
                        # If it's naive, assume it's UTC
                        if last_updated.tzinfo is None:
                            last_updated = last_updated.replace(tzinfo=timezone.utc)

                    if last_updated and (now - last_updated >= timedelta(days=7)):
                        fields_to_update = {
                            "rank": stat.get("rank"),
                            "rank_points": stat.get("rank_points"),
                        }
                        await player_collection.update_one(
                            {"_id": existing["_id"]}, 
                            {"$set": fields_to_update}
                        )
                else:
                    stat["last_updated"] = datetime.now(timezone.utc)
                    await player_collection.insert_one(stat)

        # Load and process matches csv
        match_collection = db.matches
        if os.path.exists(matches_path):
            df = pd.read_csv(matches_path)

            for _, row in df.iterrows():
                stat = row.to_dict()

                # 🧼 Clean status2
                status2 = stat.get("status2")
                stat["status2"] = status2 if isinstance(status2, str) else ""

                # Fix odds fields if they're stringified lists
                for field in ["player1_odds", "player2_odds"]:
                    val = stat.get(field)
                    if isinstance(val, str) and val.startswith("[") and val.endswith("]"):
                        try:
                            stat[field] = ast.literal_eval(val)
                        except Exception:
                            stat[field] = []  # fallback if malformed

                # 🗃️ De-duplicate based on player names and match date
                existing = await match_collection.find_one({
                    "player1_name": stat["player1_name"],
                    "player2_name": stat["player2_name"],
                    "date": stat["date"]
                })

                if not existing:
                    # 🟢 Insert new match
                    await match_collection.insert_one(stat)
                else:
                    # 🛑 Skip update if match already finished or canceled
                    if existing.get("match_status") not in ["FINISHED", "CANCELED"]:
                        # Only update selected fields
                        fields_to_update = {
                            "status1": stat.get("status1"),
                            "status2": stat.get("status2"),
                            "match_status": stat.get("match_status"),
                            "player1_odds": stat.get("player1_odds"),
                            "player2_odds": stat.get("player2_odds"),
                            "player1_score": stat.get("player1_score"),
                            "player2_score": stat.get("player2_score")
                        }

                        await match_collection.update_one(
                            {"_id": existing["_id"]},
                            {"$set": fields_to_update}
                        )

        # Generate match feature dataset for ML
        scheduled_matches_cursor = await match_collection.find({"match_status": "SCHEDULED"}).to_list(length=None)

        data_for_model = []
        for match in scheduled_matches_cursor:
            player1_name = match.get("player1_name")
            player2_name = match.get("player2_name")
            surface = match.get("surface").lower()

            player1 = await player_collection.find_one({"name": player1_name})
            player2 = await player_collection.find_one({"name": player2_name})

            if not player1 or not player2:
                continue

            rank_diff = to_int(player1.get("rank")) - to_int(player2.get("rank"))
            points_diff = to_int(player1.get("rank_points")) - to_int(player2.get("rank_points"))

            surfaceMap = {"carpet": 0, "clay": 1, "grass": 2, "hard": 3}

            data_for_model.append({
                "player0_rank": to_int(player1.get("rank")),
                "player0_rank_points": to_int(player1.get("rank_points")),
                "player1_rank": to_int(player2.get("rank")),
                "player1_rank_points": to_int(player2.get("rank_points")),
                "surface": surfaceMap.get(surface),
                "rank_diff": rank_diff,
                "rank_points_diff": points_diff
            })

        model_input_df = pd.DataFrame(data_for_model)

        # Pass model_input_df to model for predictions
        predictions = prediction(model_input_df)

        print(predictions)

        # Create new data frame for betting insights
        insight_data = []
        insights_collection = db.insights

        for i, match in enumerate(scheduled_matches_cursor):
            player1_name = match.get("player1_name")
            player2_name = match.get("player2_name")
            player1 = await player_collection.find_one({"name": player1_name})
            player2 = await player_collection.find_one({"name": player2_name})
            player1_rank = player1.get("rank")
            player2_rank = player2.get("rank")

            prob1 = float(predictions[i][0])
            prob2 = 1.0 - prob1

            best_odds1, book1, ev1, bet1 = compute_ev_and_suggestion_with_bookmaker(
                BET_SIZE, match.get("player1_odds", []), prob2
            )
            best_odds2, book2, ev2, bet2 = compute_ev_and_suggestion_with_bookmaker(
                BET_SIZE, match.get("player2_odds", []), prob1
            )

            # Date/time formatting
            match_date = match.get("date", "")
            match_time = match.get("status2", "")

            insight_dict = {
                "player1_name": player1_name,
                "player2_name": player2_name,
                "player1_rank": to_int(player1_rank),
                "player2_rank": to_int(player2_rank),
                "probability_player1": round(prob2, 3),
                "probability_player2": round(prob1, 3),
                "ev_player1": round(ev1, 3) if ev1 is not None else None,
                "ev_player2": round(ev2, 3) if ev2 is not None else None,
                "bet_on_player1": bet1,
                "bet_on_player2": bet2,
                "best_line_player1": best_odds1,
                "best_line_player2": best_odds2,
                "best_book_player1": book1, 
                "best_book_player2": book2, 
                "date": match_date,
                "time": match_time
            }

            existing_insight = await insights_collection.find_one({
                "player1_name": player1_name,
                "player2_name": player2_name,
                "date": match_date
            })

            if existing_insight:
                await insights_collection.update_one(
                    {"_id": existing_insight["_id"]},
                    {"$set": {
                        "probability_player1": insight_dict["probability_player1"],
                        "probability_player2": insight_dict["probability_player2"],
                        "ev_player1": insight_dict["ev_player1"],
                        "ev_player2": insight_dict["ev_player2"],
                        "bet_on_player1": insight_dict["bet_on_player1"],
                        "bet_on_player2": insight_dict["bet_on_player2"],
                        "best_line_player1": insight_dict["best_line_player1"],
                        "best_line_player2": insight_dict["best_line_player2"],
                        "best_book_player1": insight_dict["best_book_player1"],
                        "best_book_player2": insight_dict["best_book_player2"],
                        "time": insight_dict["time"]
                    }}
                )
            else:
                await insights_collection.insert_one(insight_dict)

            insight_data.append(insight_dict)

        return {"detail": "Pipeline executed, CSVs processed, DB updated, features generated."}

    except Exception as e:
        return {"error": str(e)}
