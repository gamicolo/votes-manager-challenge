from fastapi import HTTPException

from app.database.crud.votes import votes_crud
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

def create_list_votes_in_db(election_id: int, list_name: str, votes: int):

    try:
        #the create method of list_crud instance validates the existance of the election_id and list_name before create the list
        list_votes_created = votes_crud.create(election_id, list_name, votes)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The list with the name {list_name} for the election with id {election_id} already exist on the system")

    return list_votes_created

def get_all_votes_from_db(election_id: int):

    try:
        votes_in_db = votes_crud.get_all_votes(election_id)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=404, detail=f"No votes for the id {election_id} were found on the system")

    return votes_in_db

#TODO evalur si quitar esta funcion (no se realizaran actualizaciones de votos)
def update_votes_in_db(election_id: int, list_name: str, votes: int):

    try:
        list_votes_updated = votes_crud.update(election_id, list_name, votes)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The list with the name {list_name} for the election with id {election_id} already exist on the system")

    return list_votes_updated
