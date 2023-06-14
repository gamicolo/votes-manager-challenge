from fastapi import HTTPException

from app.database.crud.elections import elections_crud
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

def create_election_in_db(number_of_seats: int):
    """
    Create election and store the number of seats to be distributed
    """
    try:
        election_created = elections_crud.create(number_of_seats)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail="The number of seats for the election with id {election_id} already exist on the system")

    return election_created

def get_number_of_seats_from_db(election_id: int):
    """
    Get the number of seats to be distributed for a specific election
    """
    
    try:
        num_of_seats_in_db = elections_crud.get_number_of_seats(election_id)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=404, detail=f"No seats assigned for the election with id {election_id} were found on the system")

    return num_of_seats_in_db

def update_number_of_seats_in_db(election_id: int, seats: int):
    """
    Modify the number of seats to be distributed for a specific election
    """
    try: 
        num_of_seats_updated = elections_crud.update_seats(election_id, seats)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The election with id {election_id} does not exists on the system")

    return num_of_seats_updated

def get_elections_result(election_id: int):
    """
    Get the seats distribution for a specific election
    """
    try:
        elections_result_stored = elections_crud.get_elections_result(election_id)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail=f"No elections result for the election with id {election_id} were found on the system")

    return elections_result_stored

def store_elections_result_in_db(election_id: int, seats_distribution: dict):
    """
    Store the seats distribution for a specific election
    """

    try:
        elections_result_stored = elections_crud.update_seats_distribution(election_id, seats_distribution)
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail=f"The elections result for the election with id {election_id} already exist on the system")

    return elections_result_stored

