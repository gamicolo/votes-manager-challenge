from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.dbbase import Base

class Lists(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Columnd(String, unique=True, index=True)
