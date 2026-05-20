from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class PetService(Base):
    __tablename__ = "pet_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    service_type = Column(String(100), nullable=False) # Ex: 'hotel', 'creche', 'pet_sitter'
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Metadata from scraping
    source_url = Column(String(500), nullable=True)
    source_platform = Column(String(100), nullable=True) # Ex: 'doghero', 'google_maps'
    rating_avg = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    prices = relationship("Price", back_populates="service", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="service", cascade="all, delete-orphan")
