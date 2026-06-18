import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from services.user import UserServies, get_user_servies
from shemes.users import UserRegistrationSheme

logger = logging.getLogger(__name__)

router_user = APIRouter(prefix="/user", tags=["User"])


@router_user.post("/signup")
async def registration(
    user: UserRegistrationSheme, servies: UserServies = Depends(get_user_servies)
):
    try:
        return await servies.registration(user)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to sign up")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sign up",
        ) from exc


@router_user.post("/signin")
async def login(
    user: OAuth2PasswordRequestForm = Depends(),
    servies: UserServies = Depends(get_user_servies),
):
    try:
        return await servies.login(user)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to sign in")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sign in",
        ) from exc
