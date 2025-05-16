import aiohttp
import os
from fastapi import APIRouter, HTTPException, Query, Depends
from dotenv import load_dotenv
from auth import users_collection, get_current_user

router = APIRouter()
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

BASE_URL = f"https://{RAPIDAPI_HOST}"
url = f"{BASE_URL}/master"
HEADERS = {"X-RapidAPI-Host": RAPIDAPI_HOST,
           "X-RapidAPI-Key": RAPIDAPI_KEY}


@router.get("/funds")
async def get_open_ended_funds(rta_agent_code: str = Query(..., description="e.g. CAMS, KARVY"),
                               current_user: dict = Depends(get_current_user)):

    params = {"RTA_Agent_Code": rta_agent_code}
    email = current_user['email']

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS, params=params) as response:
            status = response.status
            response_text = await response.text()

            if status != 200:
                raise HTTPException(status_code=500, detail=f"Failed to fetch fund data: {status} - {response_text}")

            data = await response.json()
            users_collection.update_one({"email": email}, {"$set": {"portfolio":data}}, upsert=True)

    open_ended = [
        fund for fund in data
        if fund.get("Scheme_Type") == "Open Ended"
    ]

    return {"count": len(open_ended), "funds": open_ended}
