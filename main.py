import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from encarregado_repo import criar_tabela



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def verificar_login(usuario: str, senha: str) -> bool:
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND senha = ?", (usuario, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tabela = criar_tabela()
    return templates.TemplateResponse("entrar.html", {"request": request, "tabela": tabela})

@app.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
   
    return templates.TemplateResponse("login.html", {"request": request})



@app.get("/inicial", response_class=HTMLResponse)
async def inicial(request: Request):
    return templates.TemplateResponse("inicial.html", {"request": request})

@app.get("/ponto", response_class=HTMLResponse)
async def ponto(request: Request):
    return templates.TemplateResponse("ponto.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
