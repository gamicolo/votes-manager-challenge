from fastapi import HTTPException

from app.database.crud.elections import elections_crud
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

#TODO es necesario un try/except?
def create_election_in_db(number_of_seats: int):
    try:
        election_created = elections_crud.create(number_of_seats)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail="The XXXX it's already exist on the system")

    return election_created

def get_number_of_seats_from_db(election_id: int):
    num_of_seats_in_db = elections_crud.get_number_of_seats(election_id)
    if not num_of_seats_in_db:
        raise HTTPException(status_code=404, detail=f"No elections whit the id {election_id} were found on the system")
    return num_of_seats_in_db

def update_number_of_seats_in_db(election_id: int, seats: int):
    try: 
        num_of_seats_updated = elections_crud.update(election_id, seats)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The election with id {election_id} does not exists on the system")

    return num_of_seats_updated
