import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/inicial", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("inicial.html", {"request": request})

@app.get("/ponto", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("ponto.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
