from database import engine, Base  # ✅ Import Base here
from models import User, Maintenance
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_default_admin():
    db: Session = SessionLocal()
    if not db.query(User).filter(User.username == "admin").first():
        hashed = pwd_context.hash("password")
        db.add(User(username="admin", hashed_password=hashed, role="admin"))
        db.commit()
        print("Admin user created")
    db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    create_default_admin()
