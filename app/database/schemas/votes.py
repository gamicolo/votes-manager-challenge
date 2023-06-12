from pydantic import BaseModel
#from datetime import datetime
#from app.schemas.elections import Elections
#from app.schemas.lists import Lists

class Votes(BaseModel):
    id: int
    election_id: int
    list_id: int
    votes: int

    class Config:
        orm_mode = True
