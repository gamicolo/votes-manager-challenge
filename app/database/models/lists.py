from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.dbbase import Base

class Lists(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"))
