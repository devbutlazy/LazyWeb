from fastapi import APIRouter

from database.database import new_session
from database.models import CounterORM

router = APIRouter()


@router.get("/visits")
async def get_visits() -> dict:
    """
    Get visits counter

    :return: visits counter
    """
    async with new_session() as session:
        counter = await session.get(CounterORM, 1)
        return {"status": 200, "visits": counter.counter or 0}


@router.post("/increment_visits")
async def increment_visits() -> dict:
    """
    Increment visits counter

    :return: success message
    """
    async with new_session() as session:
        counter = await session.get(CounterORM, 1)
        if counter:
            counter.counter += 1
        else:
            counter = CounterORM(id=1, counter=1)
            session.add(counter)
        await session.commit()

    return {"status": 200, "message": "Incremented visits"}
