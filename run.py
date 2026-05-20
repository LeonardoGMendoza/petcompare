import uvicorn
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8001))
    
    print(f"🚀 Iniciando servidor PetCompare em http://{host}:{port}")
    
    # Inicia o servidor uvicorn apontando para a aplicação FastAPI
    # Nota: a aplicação real estará em api/main.py
    uvicorn.run("api.main:app", host=host, port=port, reload=True)
