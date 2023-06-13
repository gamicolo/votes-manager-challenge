from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.dbbase import Base

class Lists(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)#TODO el nombre puede repetirse, lo que no se puede repetir es el id de la lista
    election_id = Column(Integer, ForeignKey("elections.id"))
