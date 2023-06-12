from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.dbbase import Base

class Results(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"))
    list_id = Column(Integer, ForeignKey("list.id"))
    seats_assigned = Column(Integer)
