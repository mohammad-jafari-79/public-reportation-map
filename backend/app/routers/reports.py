from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Report, Vote, User, ReportImage
from app.schemas import ReportCreate, ReportResponse, ReportListResponse, VoteCreate
from app.auth import get_current_active_user, get_current_user
import os
from app.utils import save_and_compress_image

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/my-reports", response_model=List[ReportListResponse])
def get_my_reports(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """گزارشات خود کاربر (همه وضعیت‌ها)"""
    reports = db.query(Report).filter(Report.user_id == current_user.id).order_by(Report.created_at.desc()).all()
    return reports

@router.get("/", response_model=List[ReportListResponse])
def get_reports(
    status: Optional[str] = None,
    organization_id: Optional[int] = None,
    category_id: Optional[int] = None,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Report)
    
    # برای ادمین: همه گزارشات با فیلتر
    if current_user and current_user.role == "admin":
        if status:
            query = query.filter(Report.status == status)
    # برای کاربران لاگین شده: تایید شده‌ها + گزارشات خودشون
    elif current_user:
        if status:
            # اگر فیلتر status داره، فقط گزارشات خودش با اون status + تایید شده‌های دیگران
            from sqlalchemy import or_, and_
            query = query.filter(
                or_(
                    and_(Report.user_id == current_user.id, Report.status == status),
                    and_(Report.user_id != current_user.id, Report.status == "approved")
                )
            )
        else:
            # بدون فیلتر: همه گزارشات خودش + تایید شده‌های دیگران
            from sqlalchemy import or_
            query = query.filter(
                or_(
                    Report.user_id == current_user.id,
                    Report.status == "approved"
                )
            )
    # برای کاربران غیرلاگین: فقط تایید شده‌ها
    else:
        query = query.filter(Report.status == "approved")
    
    if organization_id:
        query = query.filter(Report.organization_id == organization_id)
    if category_id:
        query = query.filter(Report.category_id == category_id)
    
    reports = query.order_by(Report.created_at.desc()).all()
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    title: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    address: Optional[str] = Form(None),
    organization_id: int = Form(...),
    category_id: int = Form(...),
    images: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Create report
    new_report = Report(
        title=title,
        description=description,
        latitude=latitude,
        longitude=longitude,
        address=address,
        organization_id=organization_id,
        category_id=category_id,
        user_id=current_user.id
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    # Save images if provided
    if images:
        for image in images:
            if image.filename:
                image_path = await save_and_compress_image(image, new_report.id)
                report_image = ReportImage(report_id=new_report.id, image_path=image_path)
                db.add(report_image)
        db.commit()
        db.refresh(new_report)
    
    return new_report

@router.post("/{report_id}/vote", status_code=status.HTTP_201_CREATED)
def vote_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if report exists
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check if user already voted
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.report_id == report_id
    ).first()
    
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already voted for this report"
        )
    
    # Create vote
    new_vote = Vote(user_id=current_user.id, report_id=report_id)
    db.add(new_vote)
    
    # Update votes count
    report.votes_count += 1
    
    db.commit()
    db.refresh(report)
    return {"message": "Vote recorded successfully", "votes_count": report.votes_count}

@router.delete("/{report_id}/vote", status_code=status.HTTP_200_OK)
def unvote_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if vote exists
    vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.report_id == report_id
    ).first()
    
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found"
        )
    
    # Get report and decrease vote count
    report = db.query(Report).filter(Report.id == report_id).first()
    if report:
        report.votes_count -= 1
    
    db.delete(vote)
    db.commit()
    if report:
        db.refresh(report)
        return {"message": "Vote removed successfully", "votes_count": report.votes_count}
    return {"message": "Vote removed successfully"}
