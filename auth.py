from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas import UserCreate, UserLogin, Token
from utils import hash_password, verify_password, create_access_token
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import jwt

class User(BaseModel):
    email: EmailStr
    hashed_password: str

"""Mongo-connection"""
load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

if MONGO_USERNAME and MONGO_PASSWORD:
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD)
else:
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    print("Mongo Connection successful")

db = client['mutual_fund']
users_collection = db['user']

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return {"email": email, "exception": True}
        return {"email": email, "exception": False}
    except Exception:
        return {"exception": True}

@router.post("/register")
async def register(user: UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    user_obj = User(email=user.email, hashed_password=hashed)
    users_collection.insert_one(user_obj.dict())
    return {"message": "User registered successfully"}



@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user =  users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

