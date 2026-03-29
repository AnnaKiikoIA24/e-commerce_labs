from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    day = Column(String)
    lesson = Column(String)
    time = Column(String)