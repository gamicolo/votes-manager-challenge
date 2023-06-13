from fastapi import APIRouter, HTTPException, Request, Depends
from app.services import votes as votes_service

from sqlalchemy.orm import Session
from contextvars import ContextVar
from app.dependencies import get_db, db_session

router = APIRouter(prefix="/votes", tags=["/votes"])

@router.post("/")
async def load_lists_votes(request: Request, db: Session = Depends(get_db)):
    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameters on request body or its imcomplete")

    if not (request_json and 'election_id' in request_json and request_json['election_id']):
        raise HTTPException(status_code=422, detail="Missing parameter 'election_id' on request body or its imcomplete")
    election_id = request_json['election_id']

    if not (request_json and 'list_name' in request_json and request_json['list_name']):
        raise HTTPException(status_code=422, detail="Missing parameter 'list_name' on request body or its imcomplete")
    list_name = request_json['list_name']

    if not (request_json and 'votes' in request_json and request_json['votes']):
        raise HTTPException(status_code=422, detail="Missing parameter 'votes' on request body or its imcomplete")
    votes = request_json['votes']

    return votes_service.create_list_votes_in_db(election_id, list_name, votes)
    
@router.get("/{election_id}")
def get_all_votes_lists(election_id: int, db: Session = Depends(get_db)):

    db_session.set(db)

    return votes_service.get_all_votes_from_db(election_id)

@router.put("/{election_id}")
def update_lists_votes(election_id: int, request: Request, db: Session = Depends(get_db)):

    db_session.set(db)
    try:
        request_json = request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameters on request body or its imcomplete")

    if not (request_json and 'list_name' in request_json and request_json['list_name']):
        raise HTTPException(status_code=422, detail="Missing parameter 'list_name' on request body or its imcomplete")
    list_name = request_json['list_name']

    if not (request_json and 'votes' in request_json and request_json['votes']):
        raise HTTPException(status_code=422, detail="Missing parameter 'votes' on request body or its imcomplete")
    votes = request_json['votes']

    return votes_service.update_votes_in_db(election_id, list_name, votes)
