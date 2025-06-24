import json
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.get_db import get_db
from models.base import Usuario
from models.registro_ponto import RegistroPonto
from models.remetente import Remetente
from repo.encarregado_repo import criar_tabela_encarregado
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import repo.remetente_repo
from datetime import datetime
import repo.registro_ponto_repo
from pdf import *

criar_tabela_encarregado()
repo.remetente_repo.criar_tabela_remetente()
repo.registro_ponto_repo.criar_tabela_registro_ponto()




app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
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
    consultas = repo.remetente_repo.listar_remetentes()
    return templates.TemplateResponse("ponto.html", {"request": request, "consultas": consultas})

def calcular_dias_remidos(entrada, entrada_intervalo, saida_intervalo, saida, jornada_padrao=8):
        formato = "%H:%M"
        entrada = datetime.strptime(entrada, formato)
        entrada_intervalo = datetime.strptime(entrada_intervalo, formato)
        saida_intervalo = datetime.strptime(saida_intervalo, formato)
        saida = datetime.strptime(saida, formato)

        periodo1 = entrada_intervalo - entrada
        periodo2 = saida - saida_intervalo

        total_trabalhado = periodo1 + periodo2
        total_horas = total_trabalhado.total_seconds() / 3600

        dias_remidos = total_horas / jornada_padrao
        return round(dias_remidos, 2)


@app.post("/salvar_todos")
def salvar_todos_registros(registros: str = Form(...)):
    
        registros_lista = json.loads(registros)
        
       
        for registro in registros_lista:
            
            # Converte a string de data para objeto datetime
           
            
            # Cria o objeto RegistroPonto
            registro_ponto = RegistroPonto(
                id=0,  # ID será 0 se não existir
                data=registro["data"],  # Data já deve estar no formato correto
                remetente=registro["remetente"],
                entrada=registro["entrada"],
                entrada_intervalo=registro["entrada_intervalo"],
                saida_intervalo=registro["saida_intervalo"],
                saida=registro["saida"],
                dias_remidos=calcular_dias_remidos(
                    registro["entrada"],
                    registro["entrada_intervalo"],
                    registro["saida_intervalo"],
                    registro["saida"]
                )

            )
            
            # Insere ou atualiza o registro no banco de dados
            registro = repo.registro_ponto_repo.inserir_registro_ponto(registro_ponto)
            
            
            

        return RedirectResponse(url="/ponto", status_code=303)
    
@app.post("/salvarpdf")
def salvar_pdf(request: Request):
    try:
        # Gera os PDFs com os registros de ponto
        inserir_dados_ponto()
        
        # Retorna a página de relatório com os links dos PDFs
        return RedirectResponse(url="/ponto", status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            "ponto.html",
            {
                "request": request,
                "erro": f"Erro ao gerar PDF: {str(e)}"
            }
        )
            

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
async def index(request: Request):
    files = os.listdir(PDF_DIR)
    links = [f"/static/pdfs/{f}" for f in files]
    return templates.TemplateResponse("relatorio.html", {"request": request, "pdf_links": links})

@app.post("/limpar_pdfs")
async def limpar_pdfs():
    """Limpa todos os PDFs do diretório."""
    files = os.listdir(PDF_DIR)
    for file in files:
        file_path = os.path.join(PDF_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        repo.registro_ponto_repo.excluir_registro_ponto()
    return RedirectResponse(url="/relatorio", status_code=303)


@app.get("/consulta", response_class=HTMLResponse)
async def consulta_get(request: Request):
    consultas = repo.remetente_repo.obter_remetentes_por_pagina(12, 0)
    return templates.TemplateResponse("consulta.html", {
        "request": request,
        "consultas": consultas,
        "modo_edicao": None
    })

@app.post("/atualizar")
async def atualizar_remetente(
    id: int = Form(...),
    remetente: str = Form(...),
    data_nascimento: str = Form(...),
    crime: str = Form(...),
    tempo_sentenca: str = Form(...),
    cela: str = Form(...),
    comportamento: str = Form(...),
):
    # Crie seu objeto remetente com esses dados
    remetente_obj = Remetente(
        id=id,
        remetente=remetente,
        data_nascimento=datetime.strptime(data_nascimento, "%Y-%m-%d").date(),
        crime=crime,
        tempo_sentenca=tempo_sentenca,
        cela=cela,
        comportamento=comportamento
    )
   
    repo.remetente_repo.atualizar_remetente(remetente_obj)

    return RedirectResponse(url="/consulta", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
    

