from fastapi import APIRouter, HTTPException
from app.db.mongodb import db
from app.models.player import Player
from bson import ObjectId

# Player Router
player_router = APIRouter()
player_collection = db.players

@player_router.post("/", response_model=Player)
async def create_player(player: Player):
    data = player.dict(by_alias=True, exclude={"id"})
    result = await player_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return Player(**data)

@player_router.get("/", response_model=list[Player])
async def get_players():
    return [Player(**doc, _id=str(doc["_id"])) async for doc in player_collection.find()]

@player_router.get("/{id}", response_model=Player)
async def get_player(id: str):
    doc = await player_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Player not found")
    return Player(**doc, _id=str(doc["_id"]))

@player_router.put("/{id}", response_model=Player)
async def update_player(id: str, player: Player):
    data = player.dict(by_alias=True, exclude={"id"})
    result = await player_collection.replace_one({"_id": ObjectId(id)}, data)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    data["_id"] = id
    return Player(**data)

@player_router.delete("/{id}")
async def delete_player(id: str):
    result = await player_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"detail": "Deleted successfully"}
