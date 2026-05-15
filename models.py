from sqlalchemy import Column, Integer,String
from database import Base
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(String, nullable=False)