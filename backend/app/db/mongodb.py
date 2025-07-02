# db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[3] / '.env'  # adjust based on depth
load_dotenv(dotenv_path=env_path)
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)

db = client["MatchNet"]
