from fastapi import APIRouter, HTTPException
from db.mongodb import db
from models.insight import Insight
from bson import ObjectId

# Prediction Router
insight_router = APIRouter()
insight_collection = db.insights

@insight_router.post("/", response_model=Insight)
async def create_insight(pred: Insight):
    data = pred.dict(by_alias=True, exclude={"id"})
    result = await insight_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return Insight(**data)

@insight_router.get("/", response_model=list[Insight])
async def get_insights():
    insights = []
    async for doc in insight_collection.find():
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        insights.append(Insight(**doc))
    return insights

@insight_router.get("/{id}", response_model=Insight)
async def get_insight(id: str):
    doc = await insight_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return Insight(**doc, _id=str(doc["_id"]))

@insight_router.put("/{id}", response_model=Insight)
async def update_insight(id: str, pred: Insight):
    data = pred.dict(by_alias=True, exclude={"id"})
    result = await insight_collection.replace_one({"_id": ObjectId(id)}, data)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
    data["_id"] = id
    return Insight(**data)

@insight_router.delete("/{id}")
async def delete_insight(id: str):
    result = await insight_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"detail": "Deleted successfully"}
