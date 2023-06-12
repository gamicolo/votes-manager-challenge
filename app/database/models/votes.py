from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.dbbase import Base

class Votes(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    votes = Column(Integer)
    list_id = Column(Integer, ForeignKey("list.id"))
    election_id = Column(Integer, ForeignKey("elections.id"))
