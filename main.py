from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.base import Usuario
from models.conectar_sql import SessionLocal
from repo.encarregado_repo import criar_tabela
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tabela = criar_tabela()
    return templates.TemplateResponse("entrar.html", {"request": request, "tabela": tabela})

@app.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
   
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/form")
async def create_form(request: Request,db: Session = Depends(get_db) ,usuario: str = Form(...), senha: str = Form(...)):
    remetente = db.query(Usuario).filter(Usuario.usuario == usuario, Usuario.senha == senha).first()
    if not remetente:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    return templates.TemplateResponse("inicial.html", {"request": request})   
     




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
