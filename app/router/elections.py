from fastapi import APIRouter, HTTPException, Request, Depends
from app.services import elections as elections_service

from sqlalchemy.orm import Session
from contextvars import ContextVar
from app.dependencies import get_db, db_session

router = APIRouter(prefix="/elections", tags=["/elections"])

@router.post("/")
async def create_election(request: Request, db: Session = Depends(get_db)):
    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameter 'seats' on request body or its imcomplete")

    if not (request_json and 'seats' in request_json and request_json['seats']):
        raise HTTPException(status_code=422, detail="Missing parameter 'seats' on request body or its imcomplete")

    number_of_seats = request_json['seats']

    return elections_service.create_election_in_db(number_of_seats)
    
@router.get("/{election_id}")
def get_number_of_seats(election_id: int, db: Session = Depends(get_db)):
    db_session.set(db)
    return elections_service.get_number_of_seats_from_db(election_id)

@router.put("/{election_id}")
def update_number_of_seats(election_id: int, request: Request, db: Session = Depends(get_db)):

    db_session.set(db)

    request_json = request.json()
    if not (request_json and 'seats' in request_json and request_json['seats']):
        raise HTTPException(status_code=422, detail="Missing parameter 'seats' on request body or its imcomplete")

    return elections_service.update_number_of_seats_in_db(seats)

#@router.put("/{seats}")
#def update_number_of_seats(seats: int, db: Session = Depends(get_db)):
#
#    db_session.set(db)
#    return elections_service.update_number_of_seats_in_db(seats)

#@router.delete("/{isbn}")
#def delete_book_db(isbn: str, db: Session = Depends(get_db)):
#    if not validate_isbn(isbn):
#        raise HTTPException(status_code=422, detail="the isbn must be a digit of 10 or 12 characters length")
#
#    db_session.set(db)
#    return books_service.delete_book_in_db(isbn)
