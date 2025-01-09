from fastapi import APIRouter, Depends

from core.database.repositories.visit import VisitRepository
from core.api.dependencies.depends import get_visit_repository

router = APIRouter()


@router.get("/get_visits")
async def get_visits(
    repository: VisitRepository = Depends(get_visit_repository),
) -> dict:
    """
    Get visits counter

    :return: visits counter
    """

    visits = await repository.get_one()
    return {"status": 200, "visits": visits.counter or 0}


@router.post("/increment_visits")
async def increment_visits(
    repository: VisitRepository = Depends(get_visit_repository),
) -> dict:
    """
    Increment visits counter

    :return: success message
    """

    await repository.add_one()
    return {"status": 200, "message": "Incremented visits"}
