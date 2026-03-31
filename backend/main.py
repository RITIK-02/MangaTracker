from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.mongodb import db

# Import routers
from routes import auth, manga, library


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await db.user_manga.create_index(
        [("user_id", 1), ("manga_id", 1)],
        unique=True
    )
    await db.manga.create_index("title_lower")
    await db.manga.create_index("anilist_id", unique=True)

    print("DB indexes created")

    yield  # app runs here

    #Shutdown logic goes here
    print("App shutting down")


app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://v3rc.vercel.app/"],  # later restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(manga.router)
app.include_router(library.router)


# Root route (health check)
@app.get("/")
def home():
    return {"message": "MangaTracker API running"}