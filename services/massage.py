from datetime import datetime

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.massag import Massage
from models.user import User
from settings.db import get_db
from shemes.massages import MassageSchemePut, MassageShemeUpdate


class MassageServies:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_massages(self):
        massages = await self.db.scalars(
            select(Massage).options(selectinload(Massage.user))
        )

        return [
            {
                "id": massage.id,
                "username": massage.user.username,
                "text": massage.text,
                "date": massage.date,
                "path": massage.path,
            }
            for massage in massages.all()
        ]

    async def send_massages(self, massage: MassageSchemePut, path: str | None):
        user_id = 1
        user = await self.db.scalar(select(User).where(User.id == user_id))
        self.db.add(
            Massage(text=massage.text, date=datetime.now(), user=user, path=path)
        )
        return {"ok": True}

    async def update_massage(self, massage: MassageShemeUpdate, path: str | None):
        user_id = 1
        await self.db.execute(
            update(Massage)
            .where(Massage.id == massage.id, Massage.user_id == user_id)
            .values(text=massage.text, path=path)
        )
        return {"ok": True}

    async def remove_massage(self, id: int):
        user_id = 1
        await self.db.execute(
            delete(Massage).where(Massage.id == id, Massage.user_id == user_id)
        )
        return {"ok": True}


async def get_massage_servies(db: AsyncSession = Depends(get_db)):
    return MassageServies(db)
