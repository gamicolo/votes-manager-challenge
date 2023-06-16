from sqlalchemy import Column, Integer, String, Boolean 
from app.database.dbbase import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    disable = Column(Boolean,default=True)
