from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("pet_services.id", ondelete="CASCADE"), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="BRL")
    pricing_type = Column(String(50), nullable=False) # Ex: 'per_night', 'per_hour', 'per_day'
    pet_size = Column(String(50), nullable=True) # Ex: 'small', 'medium', 'large'
    
    is_promotional = Column(Boolean, default=False)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    service = relationship("PetService", back_populates="prices")
