from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime

class JobBase(BaseModel):
    bot_name: str
    parameters: Optional[Dict[str, Any]] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    status: str
    items_collected: Optional[int] = None
    error_message: Optional[str] = None
    finished_at: Optional[datetime] = None

class JobResponse(JobBase):
    id: int
    status: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    items_collected: int
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
