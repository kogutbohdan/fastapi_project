from authx.exceptions import TokenExpiredError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from settings.db import get_db
from settings.utils.security import hash_password, security, verify_password
from shemes.users import UserRegistrationSheme


class UserServies:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users_for_report(self):
        users = (await self.db.scalars(select(User))).all()
        return [f"username:{user.username} | email:{user.email}" for user in users]

    async def registration(self, user: UserRegistrationSheme):
        exist_user = await self.db.scalar(
            select(User).where(
                or_(User.username == user.username, User.email == user.email)
            )
        )
        if not exist_user:
            print(user.password)
            user = User(
                username=user.username,
                email=user.email,
                password=hash_password(user.password),
            )
            self.db.add(user)
            await self.db.flush()
            access_token = security.create_access_token(uid=str(user.id))
            return {"access_token": access_token, "token_type": "bearer"}
        if exist_user.username == user.username and exist_user.email == user.email:
            raise HTTPException(
                status_code=400,
                detail=[
                    {"failed": "username", "massage": "Вже є такий email і username"}
                ],
            )
        if exist_user.username == user.username:
            raise HTTPException(
                status_code=400,
                detail=[{"failed": "username", "massage": "Вже є такий username"}],
            )
        if exist_user.email == user.email:
            raise HTTPException(
                status_code=400,
                detail=[{"failed": "email", "massage": "Вже є такий email"}],
            )

    async def login(self, user: OAuth2PasswordRequestForm):
        model_user = await self.db.scalar(
            select(User).where(User.username == user.username)
        )

        if not model_user or not verify_password(user.password, model_user.password):
            raise HTTPException(
                status_code=401,
                detail="Ви неправильно ввели імя користувача або пароль",
            )

        access_token = security.create_access_token(uid=str(model_user.id))
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_current_user_id(payload=Depends(security.access_token_required)):
        user_id = payload.sub

        if not user_id:
            raise HTTPException(status_code=401, detail="Невалідний токен")

        return int(user_id)


def get_user_servies(db: AsyncSession = Depends(get_db)):
    return UserServies(db)
