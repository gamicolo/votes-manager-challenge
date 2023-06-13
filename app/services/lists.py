from fastapi import HTTPException

from app.database.crud.lists import lists_crud
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

def create_list_in_db(election_id: int, list_name: str):

    try:
        #the create method of list_crud instance validates the existance of the election_id before create the list
        list_created = lists_crud.create(election_id, list_name)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The list with the name {list_name} for the election with id {election_id} already exist on the system")

    return list_created

def get_all_lists_from_db(election_id: int):

    try:
        lists_in_db = lists_crud.get_all_lists(election_id)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=404, detail=f"No lists for the id {election_id} were found on the system")

    return lists_in_db

def get_list_by_id_from_db(election_id: int, list_id):

    try:
        list_in_db = lists_crud.get_list(election_id)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=404, detail=f"No list for the election id {election_id} with the id {list_id} were found on the system")

    return list_in_db

def update_name_in_db(election_id: int, list_name: int):

    try: 
        name_updated = lists_crud.update(election_id, list_name)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The election with id {election_id} does not exists on the system")

    return name_updated

