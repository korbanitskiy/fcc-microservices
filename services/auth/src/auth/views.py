from fastapi import APIRouter

router = APIRouter()


@router.get("/health-check")
async def health_check():
    return {"status": "ok"}


@router.post("/login")
async def login():
    pass
