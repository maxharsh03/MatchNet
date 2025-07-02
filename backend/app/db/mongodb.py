# db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

env_path = Path(__file__).resolve().parents[3] / '.env'  # adjust based on depth
load_dotenv(dotenv_path=env_path)
# Now you can use the variables
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)

'''
#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI="mongodb+srv://maxharshberger03:wBYyVGCgaTjKLXLj@cluster0.wizcten.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
'''

db = client["MatchNet"]
