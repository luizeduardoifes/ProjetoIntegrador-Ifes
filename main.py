from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from encarregado_repo import criar_tabela

from models import Encarregado
from databaseEncarregado import get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("entrar.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
    tabela = criar_tabela()
    return templates.TemplateResponse("login.html", {"request": request, "tabela": tabela})

@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    usuario: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(Encarregado).filter(
        Encarregado.usuario == usuario,
        Encarregado.senha == senha
    ).first()

    if user:
        return templates.TemplateResponse("inicial.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Usuário ou senha inválidos."
        })

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
