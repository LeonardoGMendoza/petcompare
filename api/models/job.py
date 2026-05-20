from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from api.database import Base

class Job(Base):
    """Modelo para rastrear as execuções dos robôs de scraping/RPA"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    bot_name = Column(String(100), nullable=False, index=True) # Ex: 'doghero_scraper', 'google_maps_scraper'
    status = Column(String(50), default="pending") # pending, running, completed, failed
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    
    items_collected = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    # Pode armazenar parâmetros usados para a busca (ex: cidade='São Paulo')
    parameters = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
