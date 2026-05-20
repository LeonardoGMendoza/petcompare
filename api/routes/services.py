from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from api.database import get_db
from api.models.pet_service import PetService
from api.schemas.pet_service import PetServiceResponse, PetServiceDetailResponse

router = APIRouter(prefix="/services", tags=["Pet Services"])

@router.get("/", response_model=List[PetServiceResponse])
async def list_services(
    city: Optional[str] = None,
    service_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Retorna a lista de serviços para pets disponíveis, com filtros opcionais"""
    query = select(PetService).options(selectinload(PetService.prices))
    
    if city:
        query = query.filter(PetService.city.ilike(f"%{city}%"))
    if service_type:
        query = query.filter(PetService.service_type == service_type)
        
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    services = result.scalars().all()
    
    return services

@router.get("/{service_id}", response_model=PetServiceDetailResponse)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    """Retorna detalhes completos de um serviço, incluindo avaliações e preços"""
    query = select(PetService).options(
        selectinload(PetService.prices),
        selectinload(PetService.reviews)
    ).filter(PetService.id == service_id)
    
    result = await db.execute(query)
    service = result.scalars().first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
    return service
