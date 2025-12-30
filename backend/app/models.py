from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reports = relationship("Report", back_populates="user")
    votes = relationship("Vote", back_populates="user")

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_fa = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    reports = relationship("Report", back_populates="organization")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_fa = Column(String(100), nullable=False)
    icon = Column(String(50), nullable=True)
    
    reports = relationship("Report", back_populates="category")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500), nullable=True)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    votes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="reports")
    organization = relationship("Organization", back_populates="reports")
    category = relationship("Category", back_populates="reports")
    images = relationship("ReportImage", back_populates="report", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="report", cascade="all, delete-orphan")

class ReportImage(Base):
    __tablename__ = "report_images"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    image_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    report = relationship("Report", back_populates="images")

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="votes")
    report = relationship("Report", back_populates="votes")
