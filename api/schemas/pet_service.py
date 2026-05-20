from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Prices ---
class PriceBase(BaseModel):
    amount: float
    currency: str = "BRL"
    pricing_type: str
    pet_size: Optional[str] = None
    is_promotional: bool = False

class PriceCreate(PriceBase):
    pass

class PriceResponse(PriceBase):
    id: int
    service_id: int
    collected_at: datetime
    
    class Config:
        from_attributes = True

# --- Reviews ---
class ReviewBase(BaseModel):
    author_name: Optional[str] = None
    rating: float
    comment: Optional[str] = None
    review_date: Optional[datetime] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    service_id: int
    collected_at: datetime
    
    class Config:
        from_attributes = True

# --- Pet Services ---
class PetServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    service_type: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source_url: Optional[str] = None
    source_platform: Optional[str] = None
    rating_avg: float = 0.0
    rating_count: int = 0
    is_active: bool = True

class PetServiceCreate(PetServiceBase):
    prices: Optional[List[PriceCreate]] = []
    reviews: Optional[List[ReviewCreate]] = []

class PetServiceResponse(PetServiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    prices: List[PriceResponse] = []
    
    class Config:
        from_attributes = True

class PetServiceDetailResponse(PetServiceResponse):
    reviews: List[ReviewResponse] = []
