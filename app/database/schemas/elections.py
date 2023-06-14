from pydantic import BaseModel

class Elections(BaseModel):
    id: int
    seats: int
    seats_distribution: dict
    
    class Config:
        orm_mode = True
