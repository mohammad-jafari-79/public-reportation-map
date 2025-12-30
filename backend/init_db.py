# این فایل یک اسکریپت برای ایجاد داده‌های اولیه است
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Organization, Category, User
from app.auth import get_password_hash

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Organization).first():
            print("Database already initialized!")
            return
        
        # Create organizations
        organizations = [
            Organization(name="municipality", name_fa="شهرداری", description="سازمان شهرداری"),
            Organization(name="fire_department", name_fa="آتش‌نشانی", description="سازمان آتش‌نشانی"),
            Organization(name="electricity", name_fa="اداره برق", description="اداره برق"),
            Organization(name="water", name_fa="اداره آب", description="اداره آب"),
            Organization(name="road", name_fa="راه و شهرسازی", description="سازمان راه و شهرسازی"),
        ]
        
        for org in organizations:
            db.add(org)
        
        # Create categories
        categories = [
            Category(name="asphalt", name_fa="آسفالت و خیابان", icon="road"),
            Category(name="lighting", name_fa="روشنایی معابر", icon="lightbulb"),
            Category(name="trees", name_fa="درخت و فضای سبز", icon="tree"),
            Category(name="traffic", name_fa="ترافیک", icon="traffic"),
            Category(name="garbage", name_fa="زباله و نظافت", icon="trash"),
            Category(name="other", name_fa="سایر موارد", icon="ellipsis"),
        ]
        
        for cat in categories:
            db.add(cat)
        
        # Create admin user
        admin_user = User(
            name="Admin",
            email="admin@cityreports.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        
        db.commit()
        print("Database initialized successfully!")
        print("Admin credentials: admin@cityreports.com / admin123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
