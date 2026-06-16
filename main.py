import logging

from fastapi import APIRouter, Depends, FastAPI, File, HTTPException, UploadFile, status

from services.files import add_file
from services.massage import MassageServies, get_massage_servies
from settings.db import *
from shemes.massages import MassageSchemePut, MassageShemeRead, MassageShemeUpdate

logger = logging.getLogger(__name__)

app = FastAPI()

router = APIRouter(prefix="/massage", tags=["Massages"])
router_files = APIRouter(prefix="/files", tags=["Files"])


@app.get("/")
def home():
    return {"massage": "Hellow World"}


@router.post("/")
async def send_massage(
    massage: MassageSchemePut = Depends(),
    file: UploadFile | None = File(None),
    servies: MassageServies = Depends(get_massage_servies),
):
    try:
        return await servies.send_massages(massage, await add_file(file))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to send massage")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send massage",
        ) from exc


@router.get("/", response_model=list[MassageShemeRead])
async def get_massage(servies: MassageServies = Depends(get_massage_servies)):
    try:
        return await servies.get_massages()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get massage")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get massage",
        ) from exc


@router.put("/")
async def update_massage(
    massage: MassageShemeUpdate = Depends(),
    file: UploadFile | None = File(None),
    servies: MassageServies = Depends(get_massage_servies),
):
    try:
        return await servies.update_massage(massage, await add_file(file))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update massage")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update massage",
        ) from exc


@router.delete("/{id}")
async def remove_massage(
    id: int, servies: MassageServies = Depends(get_massage_servies)
):
    try:
        return await servies.remove_massage(id)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to remove massage")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove massage",
        ) from exc


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}


app.include_router(router)
app.include_router(router_files)
