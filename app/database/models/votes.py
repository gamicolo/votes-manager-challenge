from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.dbbase import Base

class Votes(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"))
    list_name = Column(Integer, ForeignKey("lists.name"))
    votes = Column(Integer)
