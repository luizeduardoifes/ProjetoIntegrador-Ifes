import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.models import SessionLocal
from repo.encarregado_repo import criar_tabela
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import *
from sqlalchemy import Engine, Table, MetaData
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # ou especifique seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema de entrada
class LoginData(BaseModel):
    usuario: str
    senha: str

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

@app.post("/login")
async def verificar_login(request: Request, usuario: str = Form(...), senha: str = Form(...)):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return RedirectResponse(url="/inicial", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "erro": "Usuário ou senha inválidos."})



@app.get("/inicial", response_class=HTMLResponse)
async def inicial(request: Request):
    return templates.TemplateResponse("inicial.html", {"request": request})

@app.get("/ponto", response_class=HTMLResponse)
async def ponto(request: Request):
    return templates.TemplateResponse("ponto.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.get("/relatorio", response_class=HTMLResponse)
async def relatorio(request: Request):
    return templates.TemplateResponse("relatorio.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
