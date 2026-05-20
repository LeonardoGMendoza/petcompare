from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("pet_services.id", ondelete="CASCADE"), nullable=False)
    
    author_name = Column(String(255), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    review_date = Column(DateTime, nullable=True)
    
    collected_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    service = relationship("PetService", back_populates="reviews")
