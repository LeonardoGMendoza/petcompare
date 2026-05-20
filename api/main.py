from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import settings
from api.routes import services, jobs

# Inicializa a aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para o PetCompare - Comparador de Serviços para Pets",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as Rotas
app.include_router(services.router)
app.include_router(jobs.router)

@app.get("/")
async def root():
    return {
        "message": f"Bem-vindo à API do {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
