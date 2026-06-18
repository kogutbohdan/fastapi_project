import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from services.files import add_file
from services.massage import MassageServies, get_massage_servies
from services.user import UserServies
from shemes.massages import MassageSchemePut, MassageShemeRead, MassageShemeUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/massage", tags=["Massages"])


@router.post("/")
async def send_massage(
    massage: MassageSchemePut = Depends(),
    file: UploadFile | None = File(None),
    user_id: int = Depends(UserServies.get_current_user_id),
    servies: MassageServies = Depends(get_massage_servies),
):
    try:
        return await servies.send_massages(user_id, massage, await add_file(file))
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
    user_id: int = Depends(UserServies.get_current_user_id),
    servies: MassageServies = Depends(get_massage_servies),
):
    try:
        return await servies.update_massage(user_id, massage, await add_file(file))
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
    id: int,
    user_id: int = Depends(UserServies.get_current_user_id),
    servies: MassageServies = Depends(get_massage_servies),
):
    try:
        return await servies.remove_massage(user_id, id)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to remove massage")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove massage",
        ) from exc
