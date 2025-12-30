from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Organization, Category
from app.schemas import OrganizationResponse, CategoryResponse

router = APIRouter(prefix="/api", tags=["Public"])

@router.get("/organizations", response_model=List[OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return organizations

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
