from fastapi import APIRouter

from source.database import get_count, increment_count

router = APIRouter()


@router.get("/visits")
async def get_visits():
    return {"status": 200, "visits": await get_count()}


@router.post("/increment_visits")
async def increment_visits():
    await increment_count()
    return {"status": 200, "message": "Incremented visits"}
