from fastapi import FastAPI
import uvicorn
import auth
from funds import router as fund_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.include_router(auth.router)
app.include_router(fund_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_index():
    return FileResponse('static/index.html')

if "__main__" == __name__:
    uvicorn.run(app, host="0.0.0.0", port=8000)