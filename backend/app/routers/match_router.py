from fastapi import APIRouter, HTTPException
from app.db.mongodb import db
from app.models.match import Match
from bson import ObjectId

# Match Router
match_router = APIRouter()
match_collection = db.matches

@match_router.post("/", response_model=Match)
async def create_match(match: Match):
    data = match.dict(by_alias=True, exclude={"id"})
    result = await match_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return Match(**data)

@match_router.get("/", response_model=list[Match])
async def get_matches():
    matches = []
    async for doc in match_collection.find():
        doc["_id"] = str(doc["_id"])  # convert to str if your Match model uses _id as str
        matches.append(Match(**doc))  # no duplicate _id
    return matches

@match_router.get("/{id}", response_model=Match)
async def get_match(id: str):
    doc = await match_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Match not found")
    return Match(**doc, _id=str(doc["_id"]))

@match_router.put("/{id}", response_model=Match)
async def update_match(id: str, match: Match):
    data = match.dict(by_alias=True, exclude={"id"})
    result = await match_collection.replace_one({"_id": ObjectId(id)}, data)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")
    data["_id"] = id
    return Match(**data)

@match_router.delete("/{id}")
async def delete_match(id: str):
    result = await match_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"detail": "Deleted successfully"}
