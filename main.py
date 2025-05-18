from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.get_db import get_db
from models.base import Usuario
from models.prisioneiro import Remetente
from repo.encarregado_repo import criar_tabela_encarregado
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import repo.prisioneiro_repo
from datetime import datetime, date


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tabela = criar_tabela_encarregado()
    return templates.TemplateResponse("entrar.html", {"request": request, "tabela": tabela})

@app.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
   
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/formlogin")
async def create_form(request: Request,db: Session = Depends(get_db) ,usuario: str = Form(...), senha: str = Form(...)):
    remetente = db.query(Usuario).filter(Usuario.usuario == usuario, Usuario.senha == senha).first()
    if not remetente:
        return templates.TemplateResponse("login.html", {"request": request, "erro": "Usuario ou senha incorretos"})
    else:
        return templates.TemplateResponse("inicial.html", {"request": request})   
     
@app.get("/inicial", response_class=HTMLResponse)
async def inicial(request: Request):
    return templates.TemplateResponse("inicial.html", {"request": request})

@app.get("/ponto", response_class=HTMLResponse)
async def ponto(request: Request):
    return templates.TemplateResponse("ponto.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro(request: Request):
    tabela_prisioneiro = repo.prisioneiro_repo.criar_tabela_remetente()
    return templates.TemplateResponse("cadastro.html", {"request": request, "tabela_prisioneiro": tabela_prisioneiro})

@app.post("/formcadastro")
def cadastrar_remetente(
    request: Request,
    prisioneiro: str = Form(...),
    data_nascimento: str = Form(...),
    crime: str = Form(...),
    tempo_sentenca: int = Form(...),
    cela: str = Form(...),
    comportamento: str = Form(...)
):
    try:
        # Converte a string de data para datetime.date
        data_formatada = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

        # Cria o objeto Remetente (sem ID ainda)
        remetente = Remetente(
            id=0,  # será preenchido dentro da função com lastrowid
            prisioneiro=prisioneiro,
            data_nascimento=data_formatada,
            crime=crime,
            tempo_sentenca=tempo_sentenca,
            cela=cela,
            comportamento=comportamento
        )

        # Insere no banco
        remetente = repo.prisioneiro_repo.inserir_prisioneiro(remetente)

        return {"cadastro.html",{"request": request,"sucesso":"Remetente cadastrado com sucesso!", "id": remetente.id}}

    except Exception as e:
        return {"erro": str(e)}

@app.get("/relatorio", response_class=HTMLResponse)
async def relatorio(request: Request):
    return templates.TemplateResponse("relatorio.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
