from fastapi import APIRouter, HTTPException, Request, Depends
from app.services import lists as lists_service

from sqlalchemy.orm import Session
from contextvars import ContextVar
from app.dependencies import get_db, db_session

router = APIRouter(prefix="/lists", tags=["/lists"])

@router.post("/")
async def create_list(request: Request, db: Session = Depends(get_db)):
    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameters on request body or its imcomplete")

    if not (request_json and 'name' in request_json and request_json['name']):
        raise HTTPException(status_code=422, detail="Missing parameter 'name' on request body or its imcomplete")
    list_name = request_json['name']

    if not (request_json and 'election_id' in request_json and request_json['election_id']):
        raise HTTPException(status_code=422, detail="Missing parameter 'election_id' on request body or its imcomplete")
    election_id = request_json['election_id']

    return lists_service.create_list_in_db(election_id, list_name)
    
@router.get("/{election_id}")
def get_all_lists(election_id: int, db: Session = Depends(get_db)):

    db_session.set(db)

    return lists_service.get_all_lists_from_db(election_id)

@router.put("/{election_id}")
def update_(election_id: int, request: Request, db: Session = Depends(get_db)):

    db_session.set(db)
    try:
        request_json = request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameters on request body or its imcomplete")

    if not (request_json and 'name' in request_json and request_json['name']):
        raise HTTPException(status_code=422, detail="Missing parameter 'name' on request body or its imcomplete")
    list_name = request_json['name']

#    if not (request_json and 'election_id' in request_json and request_json['election_id']):
#        raise HTTPException(status_code=422, detail="Missing parameter 'election_id' on request body or its imcomplete")
#    election_id = request_json['election_id']

    return lists_service.update_name_in_db(election_id, list_name)
