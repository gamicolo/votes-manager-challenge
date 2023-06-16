from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing_extensions import Annotated

from app.database.models.login import User as UserModel
from app.database.schemas.login import TokenData, User, UserInDB

from app.config import settings
from app.dependencies import pwd_context, oauth2_scheme

from sqlalchemy.orm import Session

def verify_password(plain_password: str, hashed_password: str):
    """
    Verify the password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """
    Get the hashed password
    """
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    """
    Get the user from the DB
    """

    user_from_db = db.query(UserModel).filter(UserModel.username == username).first()

    if user_from_db:
        return UserInDB(**user_from_db)

    return None

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#def create_list_votes_in_db(election_id: int, list_name: str, votes: int):
#
#    try:
#        #the create method of list_crud instance validates the existance of the election_id and list_name before create the list
#        list_votes_created = votes_crud.create(election_id, list_name, votes)
#    except AlreadyExistsOnDBException as error:
#        raise HTTPException(status_code=409, detail=f"The list with the name {list_name} for the election with id {election_id} already exist on the system")
#
#    return list_votes_created
#
#def get_all_votes_from_db(election_id: int):
#
#    try:
#        votes_in_db = votes_crud.get_all_votes(election_id)
#    except NotFoundOnDBException as error:
#        raise HTTPException(status_code=404, detail=f"No votes for the id {election_id} were found on the system")
#
#    return votes_in_db
#
##TODO evalur si quitar esta funcion (no se realizaran actualizaciones de votos)
#def update_votes_in_db(election_id: int, list_name: str, votes: int):
#
#    try:
#        list_votes_updated = votes_crud.update(election_id, list_name, votes)
#    except AlreadyExistsOnDBException as error:
#        raise HTTPException(status_code=409, detail=f"The list with the name {list_name} for the election with id {election_id} already exist on the system")
#
#    return list_votes_updated
#
#
