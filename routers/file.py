import logging

from fastapi import APIRouter, Depends, HTTPException, status

from services.files import generate_simple_report
from services.massage import MassageServies, get_massage_servies
from services.user import UserServies, get_user_servies

logger = logging.getLogger(__name__)

router_files = APIRouter(prefix="/files", tags=["Files"])


@router_files.get("/users")
async def get_users(servies: UserServies = Depends(get_user_servies)):
    try:
        return generate_simple_report(
            "user_report.pdf",
            "Report about users",
            await servies.get_all_users_for_report(),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to gnerate report about users")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to gnerate report about users",
        ) from exc


@router_files.get("/massages")
async def get_users(servies: MassageServies = Depends(get_massage_servies)):
    try:
        return generate_simple_report(
            "massage_report.pdf",
            "Report about massages",
            await servies.get_all_massages_for_report(),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to gnerate report about massages")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to gnerate report about massages",
        ) from exc
