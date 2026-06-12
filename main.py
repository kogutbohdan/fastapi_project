import logging

from fastapi import Depends, FastAPI, HTTPException, status

from services.massage import MassageServies, get_massage_servies
from settings.db import *
from shemes.shemes import MassageSchemePut, MassageShemeRead

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def home():
    return {"massage": "Hellow World"}


@app.post("/massage")
async def send_massage(
    massage: MassageSchemePut, servies: MassageServies = Depends(get_massage_servies)
):
    try:
        return await servies.send_massages(massage)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to send massage")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send massage",
        ) from exc


@app.get("/massage", response_model=list[MassageShemeRead])
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


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}
