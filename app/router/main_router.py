from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.router import elections, lists

router = APIRouter(prefix="")

# Add all rotuers
router.include_router(elections.router)
router.include_router(lists.router)

@router.get("/")
def root():
    return RedirectResponse(url=("/docs"))
