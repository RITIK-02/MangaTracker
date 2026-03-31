from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from db.mongodb import get_db
from utils.auth import create_access_token
from models.schemas import UserSignup, UserLogin

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup")
async def signup(user: UserSignup, db=Depends(get_db)):
    hashed = pwd_context.hash(user["password"])
    user_doc = {
        "email": user["email"],
        "password_hash": hashed
    }
    await db.users.insert_one(user_doc)
    return {"message": "User created"}



@router.post("/login")
async def login(user: UserLogin, db=Depends(get_db)):
    db_user = await db.users.find_one({"email": user["email"]})

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(user["password"], db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {"access_token": token, "token_type": "bearer"}