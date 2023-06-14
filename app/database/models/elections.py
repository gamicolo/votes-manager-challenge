from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import relationship
from app.database.dbbase import Base

class Elections(Base):
    __tablename__ = "elections"
    id = Column(Integer, primary_key=True, index=True)
    seats = Column(Integer)
    seats_distribution = Column(JSON)
