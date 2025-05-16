import traceback
import aiohttp
import os
from fastapi import APIRouter, HTTPException,Request
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

router = APIRouter()
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

BASE_URL = f"https://{RAPIDAPI_HOST}"
url = f"{BASE_URL}/master"
HEADERS = {"X-RapidAPI-Host": RAPIDAPI_HOST,
           "X-RapidAPI-Key": RAPIDAPI_KEY}
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, rta_agent_code: str):
    try:
        df = await get_portfolio_df(rta_agent_code)
        table_html = df.to_html(classes="dataframe", index=False)

        return templates.TemplateResponse("dashboard.html", {"request": request,
                                                             "table": table_html,
                                                             "rta_agent_code": rta_agent_code})

    except Exception as e:
        traceback.print_exc()
        return str(e)


async def get_portfolio_df(rta_agent_code: str) -> pd.DataFrame:
    try:
        params = {"RTA_Agent_Code": rta_agent_code}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=HEADERS, params=params) as response:
                status = response.status
                response_text = await response.text()

                if status != 200:
                    raise HTTPException(status_code=500,
                                        detail=f"Failed to fetch fund data: {status} - {response_text}")

                data = await response.json()
        form_data = []
        for fund in data:
            if fund['RTA_Agent_Code'] == rta_agent_code:
                form_data.append({"RTA AGENT CODE": fund['RTA_Agent_Code'],
                                  "AMC SCHEME CODE": fund['AMC_Scheme_Code'],
                                  "MINIMUM PURCHASE AMOUNT": fund['Minimum_Purchase_Amount']})
        return pd.DataFrame(form_data)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))