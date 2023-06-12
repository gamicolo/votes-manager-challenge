from pydantic import BaseModel

class Elections(BaseModel):
    id: int
    seats: int
    
    class Config:
        orm_mode = True
