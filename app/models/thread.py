from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)