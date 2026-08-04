from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class UserBase(BaseModel):
    username: str
    email: str
    role: str = 'operator'

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class WasteBatchBase(BaseModel):
    batch_id: str
    fabric_type: str
    source: str
    quantity_kg: float
    color: str
    condition: str
    waste_category: str
    recyclability_score: float
    contamination_level: str = 'None'
    damage_level: str = 'None'
    notes: Optional[str] = None

class WasteBatchCreate(WasteBatchBase):
    pass

class WasteBatchResponse(WasteBatchBase):
    id: int
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_batches: int
    total_weight: float
    material_distribution: Dict[str, float]
    category_distribution: Dict[str, int]
    condition_distribution: Dict[str, int]
    avg_recyclability: float
