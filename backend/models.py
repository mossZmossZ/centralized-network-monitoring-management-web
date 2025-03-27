from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(20), default="user")

class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime(timezone=True), default=func.now())
    device = Column(String(100), nullable=False)
    event = Column(String(100), nullable=False)
    changedBy = Column(String(50), nullable=False)
    notes = Column(Text)
