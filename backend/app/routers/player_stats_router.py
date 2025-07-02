from fastapi import APIRouter, HTTPException
from db.mongodb import db
from models.player_stats import PlayerStats
from bson import ObjectId

player_stats_router = APIRouter()
collection = db.player_stats

@player_stats_router.post("/", response_model=PlayerStats)
async def create_stat(stat: PlayerStats):
    stat_dict = stat.dict(by_alias=True, exclude={"id"})
    result = await collection.insert_one(stat_dict)
    stat_dict["_id"] = str(result.inserted_id)
    return PlayerStats(**stat_dict)

@player_stats_router.get("/", response_model=list[PlayerStats])
async def get_all_stats():
    '''
    cursor = collection.find({})
    stats = [PlayerStats(**doc, _id=str(doc["_id"])) async for doc in cursor]
    return stats
    '''
    stats = []
    cursor = collection.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        stats.append(PlayerStats(**doc))
    return stats

@player_stats_router.get("/{id}", response_model=PlayerStats)
async def get_stat(id: str):
    doc = await collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Stat not found")
    return PlayerStats(**doc, _id=str(doc["_id"]))

@player_stats_router.put("/{id}", response_model=PlayerStats)
async def update_stat(id: str, stat: PlayerStats):
    stat_dict = stat.dict(by_alias=True, exclude={"id"})
    result = await collection.replace_one({"_id": ObjectId(id)}, stat_dict)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Stat not found")
    stat_dict["_id"] = id
    return PlayerStats(**stat_dict)

@player_stats_router.delete("/{id}")
async def delete_stat(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Stat not found")
    return {"detail": "Deleted successfully"}
