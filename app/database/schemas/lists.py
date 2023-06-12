from pydantic import BaseModel

class Lists(BaseModel):
    id: int
    name: str
    election_id: int
    
    class Config:
        orm_mode = True
