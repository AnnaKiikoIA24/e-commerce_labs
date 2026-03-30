from sqlalchemy import Column, Integer, String
from app.db import Base

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    day = Column(String)
    lesson = Column(String)
    time = Column(String)