from fastapi import APIRouter, Depends
from db.mongodb import get_db
from utils.dependencies import get_current_user
from bson import ObjectId
from models.schemas import AddToLibrary, UpdateLibrary
from datetime import datetime, UTC


# TO BE IMPLEMENTED
# from pymongo.errors import DuplicateKeyError
# try:
#     await db.user_manga.update_one(...)
# except DuplicateKeyError:
#     return {"message": "Already exists (race condition handled)"}

router = APIRouter()

@router.post("/add")
async def add_to_library(
    payload: AddToLibrary, 
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    user_id = current_user["user_id"]
    manga_id = ObjectId(payload.manga_id)

    update_doc = {
        "$set": {
            "status": payload.status,
            "current_chapter": payload.current_chapter,
            "rating": payload.rating,
            "updated_at": datetime.now(UTC)
        },
        "$setOnInsert": {
            "user_id": user_id,
            "manga_id": manga_id,
            "created_at": datetime.now(UTC)
        }
    }
    await db.user_manga.update_one(
        {
            "user_id": user_id,
            "manga_id": manga_id
        },
        update_doc,
        upsert=True
    )
    return {"message": "Added to library"}


@router.put("/update/{manga_id}")
async def update_library(
    manga_id: str,
    payload: UpdateLibrary,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    user_id = current_user["user_id"]

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}

    await db.user_manga.update_one(
        {
            "user_id": ObjectId(user_id),
            "manga_id": ObjectId(manga_id)
        },
        {"$set": update_data}
    )

    return {"message": "Updated successfully"}


@router.get("/my-list")
async def get_user_list(
    page: int = 1,
    limit: int = 10,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    user_id = current_user["user_id"]
    skip = (page - 1)*limit

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$lookup": {
                "from": "manga",
                "localField": "manga_id",
                "foreignField": "_id",
                "as": "manga_info"
            }
        },
        {"$unwind": "$manga_info"},
        {"$skip": skip},
        {"$limit": limit}
    ]

    results = await db.user_manga.aggregate(pipeline).to_list(limit)

    # Clean response
    formatted = []
    for item in results:
        formatted.append({
            "_id": str(item["_id"]),
            "manga_id": str(item["manga_id"]),
            "title": item["manga_info"]["title"],
            "cover_image": item["manga_info"]["cover_image"],
            "total_chapters": item["manga_info"].get("total_chapters"),
            "status": item["status"],
            "current_chapter": item["current_chapter"],
            "rating": item.get("rating")
        })

    total = await db.user_manga.count_documents({"user_id": user_id})
    return {"data": formatted, "total": total}
    # data = await db.user_manga.find({
    #     "user_id": ObjectId(user_id)
    # }).to_list(100)

    # for item in data:
    #     item["_id"] = str(item["_id"])
    #     item["user_id"] = str(item["user_id"])
    #     item["manga_id"] = str(item["manga_id"])

    # return data