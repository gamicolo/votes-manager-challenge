from pydantic import BaseModel

class Lists(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
