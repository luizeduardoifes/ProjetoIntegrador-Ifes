from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("entrar.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def processar_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "123456":
        mensagem = "Login bem-sucedido!"
    else:
        mensagem = "Login inválido."

    return templates.TemplateResponse("login.html", {
        "request": request,
        "mensagem": mensagem,
        "username": username
    })




@app.get("/inicial", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("inicial.html", {"request": request})

@app.get("/ponto", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("ponto.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
