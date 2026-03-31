import httpx

ANILIST_URL = "https://graphql.anilist.co"

async def search_manga(query: str):
    graphql_query = """
    query ($search: String) {
      Page {
        media(search: $search, type: MANGA) {
          id
          title { romaji }
          coverImage { large }
          chapters
        }
      }
    }
    """

    async with httpx.AsyncClient() as client:
        res = await client.post(
            ANILIST_URL,
            json={"query": graphql_query, "variables": {"search": query}}
        )
        return res.json()