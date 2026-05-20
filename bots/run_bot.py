import asyncio
import sys
import os

# Adiciona a raiz do projeto no path do Python para conseguir importar a pasta api e bots
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from sqlalchemy import select

from api.database import AsyncSessionLocal, engine, Base
from api.models.pet_service import PetService
from api.models.price import Price
from bots.scraping.doghero_scraper import DogHeroScraper

async def init_db():
    """Garante que as tabelas existem antes de rodar"""
    async with engine.begin() as conn:
        # Em produção ideal usar Alembic, mas aqui forçamos a criação para testes
        await conn.run_sync(Base.metadata.create_all)

async def run_and_save(city: str, state: str):
    """Executa o bot e salva os dados no banco"""
    logger.info("=" * 50)
    logger.info(f"🐶 Iniciando rotina de Scraping: {city}/{state}")
    logger.info("=" * 50)
    
    # 1. Garante que o DB está pronto
    await init_db()
    
    # 2. Executa o Robô
    bot = DogHeroScraper(headless=True)
    try:
        results = bot.search_hotels(city=city, state=state)
    except Exception as e:
        logger.error(f"Falha ao executar o bot: {e}")
        return

    if not results:
        logger.warning("Nenhum dado retornado pelo robô.")
        return

    # 3. Salva no Banco de Dados
    async with AsyncSessionLocal() as session:
        for data in results:
            # Verifica se o anfitrião já existe
            stmt = select(PetService).where(
                PetService.name == data["name"],
                PetService.city == data["city"]
            )
            result = await session.execute(stmt)
            service_obj = result.scalars().first()
            
            if service_obj:
                logger.info(f"🔄 Atualizando anfitrião existente: {data['name']}")
                # Atualiza os dados
                service_obj.rating_avg = data["rating"]
                service_obj.rating_count = data["reviews"]
                service_obj.source_url = data["url"]
            else:
                logger.info(f"✨ Criando novo anfitrião: {data['name']}")
                # Cria novo
                service_obj = PetService(
                    name=data["name"],
                    service_type="hotel",
                    city=data["city"],
                    state=data["state"],
                    source_url=data["url"],
                    source_platform=data["source"],
                    rating_avg=data["rating"],
                    rating_count=data["reviews"]
                )
                session.add(service_obj)
                
            # Faz um flush para gerar o ID caso seja novo
            await session.flush()
            
            # 4. Adiciona o preço encontrado (mantendo o histórico)
            logger.info(f"   -> Salvando preço: R$ {data['price_per_night']}/noite")
            new_price = Price(
                service_id=service_obj.id,
                amount=data["price_per_night"],
                pricing_type="per_night"
            )
            session.add(new_price)
            
        # Confirma as transações
        await session.commit()
        logger.success(f"✅ Sucesso! {len(results)} anfitriões foram salvos no Banco de Dados.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rodar Bot do PetCompare")
    parser.add_argument("--city", type=str, default="Guarulhos", help="Cidade para buscar")
    parser.add_argument("--state", type=str, default="SP", help="Estado (sigla) para buscar")
    args = parser.parse_args()
    
    # Roda o fluxo assíncrono
    asyncio.run(run_and_save(args.city, args.state))
