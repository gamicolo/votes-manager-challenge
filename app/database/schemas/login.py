from pydantic import BaseModel
from typing import Union

#class Votes(BaseModel):
#    id: int
#    election_id: int
#    list_id: int
#    votes: int
#
#    class Config:
#        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str,None] = None
    full_name: Union[str,None] = None
    disable: Union[bool,None] = None

class UserInDB(User):
    hashed_password: str
