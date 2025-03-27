from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read DB settings from .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Updated table: monitoring
class Monitoring(Base):
    __tablename__ = "monitoring"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Schema
class MonitoringCreate(BaseModel):
    name: str
    status: str

# Router
router = APIRouter(prefix="/db", tags=["Database Manager"])

@router.post("/create-monitoring")
def create_monitoring(entry: MonitoringCreate):
    db = SessionLocal()
    new_entry = Monitoring(name=entry.name, status=entry.status)
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
        return {"message": "Entry created", "data": {"id": new_entry.id, "name": new_entry.name, "status": new_entry.status}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
