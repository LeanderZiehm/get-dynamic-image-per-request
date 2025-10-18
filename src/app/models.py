from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class TimeView(Base):
    __tablename__ = "time_views"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
