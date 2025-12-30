from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, ReportStatus

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Organization Schemas
class OrganizationBase(BaseModel):
    name: str
    name_fa: str
    description: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: int
    
    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    name_fa: str
    icon: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Report Schemas
class ReportImageResponse(BaseModel):
    id: int
    image_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    latitude: float = Field(..., ge=35.0, le=37.0)  # Mashhad coordinates range
    longitude: float = Field(..., ge=58.0, le=60.0)
    address: Optional[str] = None
    organization_id: int
    category_id: int

class ReportUpdate(BaseModel):
    status: ReportStatus

class ReportResponse(BaseModel):
    id: int
    title: str
    description: str
    latitude: float
    longitude: float
    address: Optional[str]
    status: ReportStatus
    user_id: int
    organization_id: int
    category_id: int
    votes_count: int
    created_at: datetime
    updated_at: datetime
    user: UserResponse
    organization: OrganizationResponse
    category: CategoryResponse
    images: List[ReportImageResponse]
    
    class Config:
        from_attributes = True

class ReportListResponse(BaseModel):
    id: int
    title: str
    latitude: float
    longitude: float
    status: ReportStatus
    votes_count: int
    created_at: datetime
    organization: OrganizationResponse
    category: CategoryResponse
    
    class Config:
        from_attributes = True

# Vote Schema
class VoteCreate(BaseModel):
    report_id: int

class VoteResponse(BaseModel):
    id: int
    user_id: int
    report_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Stats Schema
class StatsResponse(BaseModel):
    total_reports: int
    pending_reports: int
    approved_reports: int
    rejected_reports: int
    total_users: int
    reports_by_organization: dict
