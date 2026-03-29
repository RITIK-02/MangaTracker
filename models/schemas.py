from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Manga(BaseModel):
    anilist_id: int
    title: str
    cover_image: Optional[str]
    total_chapters: Optional[int]



class AddToLibrary(BaseModel):
    manga_id: str
    status: str = Field(pattern="^(reading|completed|plan)$")
    current_chapter: int = 0
    rating: Optional[int] = Field(default=None, ge=1, le=10)


class UpdateLibrary(BaseModel):
    status: Optional[str] = Field(default=None, pattern="^(reading|completed|plan)$")
    current_chapter: Optional[int]
    rating: Optional[int] = Field(default=None, ge=1, le=10)