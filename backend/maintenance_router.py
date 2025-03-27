from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import Maintenance
from datetime import datetime
router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

# ---------------------
# Pydantic Schemas
# ---------------------

class MaintenanceCreate(BaseModel):
    device: str
    event: str
    changedBy: str
    notes: Optional[str] = None
    status: Optional[str] = "pending"

class MaintenanceOut(MaintenanceCreate):
    id: int
    time: datetime

    class Config:
        orm_mode = True

# ---------------------
# Routes
# ---------------------

@router.get("/", response_model=List[MaintenanceOut])
def get_all_maintenance(db: Session = Depends(get_db)):
    return db.query(Maintenance).order_by(Maintenance.time.desc()).all()

@router.get("/{maintenance_id}", response_model=MaintenanceOut)
def get_maintenance_by_id(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance

@router.post("/", response_model=MaintenanceOut)
def create_maintenance(entry: MaintenanceCreate, db: Session = Depends(get_db)):
    new_entry = Maintenance(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{maintenance_id}", response_model=MaintenanceOut)
def update_maintenance(maintenance_id: int, entry: MaintenanceCreate, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    
    for key, value in entry.dict().items():
        setattr(maintenance, key, value)

    db.commit()
    db.refresh(maintenance)
    return maintenance

@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    
    db.delete(maintenance)
    db.commit()
    return {"detail": "Deleted successfully"}
