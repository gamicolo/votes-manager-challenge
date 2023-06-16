from pydantic import BaseModel

class Votes(BaseModel):
    id: int
    election_id: int
    list_id: int
    votes: int

    class Config:
        orm_mode = True
