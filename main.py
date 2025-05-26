from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.get_db import get_db
from models.base import Usuario
from models.remetente import Remetente
from repo.encarregado_repo import criar_tabela_encarregado
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import repo.remetente_repo
from datetime import datetime


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tabela = criar_tabela_encarregado()
    tabela_remetente = repo.remetente_repo.criar_tabela_remetente()
    return templates.TemplateResponse("entrar.html", {"request": request, "tabela": tabela, "tabela_remetente": tabela_remetente})

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
    consultas = repo.remetente_repo.obter_remetentes_por_pagina(12, 0)
    return templates.TemplateResponse("ponto.html", {"request": request, "consultas": consultas})


@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro(request: Request):
    
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.post("/formcadastro", response_class=HTMLResponse)
def cadastrar_remetente(
    request: Request,
    remetente: str = Form(...),
    data_nascimento: str = Form(...),
    crime: str = Form(...),
    tempo_sentenca: int = Form(...),
    cela: str = Form(...),
    comportamento: str = Form(...)
):
    try:
        # Converte a string para data no formato yyyy-mm-dd
        data_formatada = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

        # Cria o objeto remetente
        remetente = Remetente(
            id=0,  # será atribuído após inserção
            remetente=remetente,
            data_nascimento=data_formatada,
            crime=crime,
            tempo_sentenca=tempo_sentenca,
            cela=cela,
            comportamento=comportamento
        )

        # Insere no banco e recupera com ID
        remetente = repo.remetente_repo.inserir_remetente(remetente)

        # Retorna o template com confirmação
        return templates.TemplateResponse("cadastro.html",{"request": request,"sucesso": "remetente cadastrado com sucesso!","remetente": remetente})

    except Exception as e:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": f"Erro ao cadastrar: {str(e)}"
            }
        )

@app.get("/relatorio", response_class=HTMLResponse)
async def relatorio(request: Request):
    return templates.TemplateResponse("relatorio.html", {"request": request})

@app.get("/consulta", response_class=HTMLResponse)
async def consulta_get(request: Request):
    consultas = repo.remetente_repo.listar_remetentes()
    return templates.TemplateResponse("consulta.html", {
        "request": request,
        "consultas": consultas,
        "modo_edicao": None
    })


@app.get("/alterar_dados/{id}", response_class=HTMLResponse)
async def editar_dados(request: Request):
    # Aqui você buscaria os dados do remetente no banco
    remetentes = repo.remetente_repo.obter_remetente_por_id(1)  # Sua função personalizada
    return templates.TemplateResponse("alterar_dados.html", {"request": request, "remetentes": remetentes})








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
    

