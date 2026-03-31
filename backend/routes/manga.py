from fastapi import APIRouter, Depends
from services.manga_service import search_and_cache
from db.mongodb import get_db

router = APIRouter()

@router.get("/search")
async def search(
    query: str, 
    page: int = 1,
    limit: int = 10,
    db=Depends(get_db)
):
    result = await search_and_cache(query, db, page, limit)
    return result