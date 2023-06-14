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
async def update_number_of_seats(election_id: int, request: Request, db: Session = Depends(get_db)):

    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameters on request body or its imcomplete")

    if not (request_json and 'seats' in request_json and request_json['seats']):
        raise HTTPException(status_code=422, detail="Missing parameter 'seats' on request body or its imcomplete")
    seats = request_json['seats']

    return elections_service.update_number_of_seats_in_db(election_id, seats)

@router.get("/{election_id}/results")
def get_elections_result(election_id: int, db: Session = Depends(get_db)):

    db_session.set(db)

    return elections_service.get_elections_result(election_id)

@router.put("/{election_id}/results")
async def store_elections_result(request: Request, election_id: int, db: Session = Depends(get_db)):
    
    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameters on request body or its imcomplete")

    if not (request_json and 'seats_distribution' in request_json and request_json['seats_distribution']):
        raise HTTPException(status_code=422, detail="Missing parameter 'seats_distribution' on request body or its imcomplete")
    seats_distribution = request_json['seats_distribution']

    return elections_service.store_elections_result_in_db(election_id, seats_distribution)
