from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.infra.sqlite.sqlite import Sqlite, get_sqlite
from src.services.health import HealthService, get_health_service

router = APIRouter()


@router.get("/health")
async def health(
        service: HealthService = Depends(get_health_service),
        sqlite: Sqlite = Depends(get_sqlite),
):
    res = await service.check_service_health([
        sqlite
    ])

    if len(res) > 0:
        return JSONResponse(status_code=500, content='\n'.join(res))

    return JSONResponse(status_code=200, content="all dependencies are ok")


@router.get("/ready")
async def ready():
    return JSONResponse(status_code=200, content="user-experience is up")
