from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api.config import settings
from api.routes import services, jobs
import os

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

# Inclui as Rotas da API
app.include_router(services.router)
app.include_router(jobs.router)

# Monta os arquivos estáticos do dashboard (CSS, JS)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dashboard_dir = os.path.join(BASE_DIR, "dashboard")
app.mount("/css", StaticFiles(directory=os.path.join(dashboard_dir, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(dashboard_dir, "js")), name="js")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a página principal do PetCompare"""
    index_path = os.path.join(dashboard_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/api/status")
async def api_status():
    return {
        "message": f"Bem-vindo à API do {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
