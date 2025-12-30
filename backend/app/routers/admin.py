from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import Report, User, Organization
from app.schemas import ReportResponse, ReportUpdate, StatsResponse
from app.auth import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/reports", response_model=List[ReportResponse])
def get_all_reports(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return reports

@router.patch("/reports/{report_id}", response_model=ReportResponse)
def update_report_status(
    report_id: int,
    report_update: ReportUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    report.status = report_update.status
    db.commit()
    db.refresh(report)
    return report

@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    db.delete(report)
    db.commit()
    return None

@router.get("/stats", response_model=StatsResponse)
def get_statistics(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    total_reports = db.query(Report).count()
    pending_reports = db.query(Report).filter(Report.status == "pending").count()
    approved_reports = db.query(Report).filter(Report.status == "approved").count()
    rejected_reports = db.query(Report).filter(Report.status == "rejected").count()
    total_users = db.query(User).count()
    
    # Reports by organization
    org_stats = db.query(
        Organization.name_fa,
        func.count(Report.id).label('count')
    ).join(Report).group_by(Organization.id, Organization.name_fa).all()
    
    reports_by_organization = {org: count for org, count in org_stats}
    
    return {
        "total_reports": total_reports,
        "pending_reports": pending_reports,
        "approved_reports": approved_reports,
        "rejected_reports": rejected_reports,
        "total_users": total_users,
        "reports_by_organization": reports_by_organization
    }
