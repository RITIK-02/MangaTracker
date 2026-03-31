from services.anilist import search_manga
from datetime import datetime, UTC

def normalize_manga(anilist_manga):
    return {
        "anilist_id": anilist_manga["id"],
        "title": anilist_manga["title"]["romaji"],
        "title_lower": anilist_manga["title"]["romaji"].lower(),
        "cover_image": anilist_manga["coverImage"]["large"],
        "total_chapters": anilist_manga.get("chapters"),
    }


async def search_and_cache(query: str, db, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    db_query = {
        "title_lower": {"$regex": f".*{query.lower()}.*"}
    }

    cached = await db.manga.find(db_query).skip(skip).limit(limit).to_list(limit)

    total = await db.manga.count_documents(db_query)

    if total > 0:
        for item in cached:
            item["_id"] = str(item["_id"])
        return {
            "source": "cache",
            "page": page,
            "limit": limit,
            "total": total,
            "data": cached
        }

    api_data = await search_manga(query)
    manga_list = api_data["data"]["Page"]["media"]

    results = []
    for m in manga_list:
        doc = normalize_manga(m)
        doc["updated_at"] = datetime.now(UTC)

        await db.manga.update_one(
            {"anilist_id": doc["anilist_id"]},
            {"$set": doc},
            upsert=True
        )

        results.append(doc)

    return {
        "source": "api",
        "page": page,
        "limit": limit,
        "total": len(results),
        "data": results[skip: skip + limit]
    }
