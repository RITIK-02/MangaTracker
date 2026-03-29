from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
assert SECRET_KEY == "68c944be3fc88edcba3a5472e1b67ac78ca7eb478fb3fd9aea7d15822c47fee6"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)