from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as api_router
from .database import engine, Base

# Cria as tabelas no banco de dados se elas não existirem
# (Útil para desenvolvimento local e primeiro deploy)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare System API")

# Configuração de CORS para permitir que o frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, trocaremos pelo link do Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Healthcare System", "status": "online"}
