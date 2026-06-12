from datetime import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.massag import Massage
from models.user import User
from settings.db import get_db
from shemes.shemes import MassageSchemePut


class MassageServies:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_massages(self):
        massages = [
            {
                "username": massage.user.username,
                "text": massage.text,
                "date": massage.date,
            }
            for massage in await self.db.scalars(select(Massage)).all()
        ]
        return massages

    async def send_massages(self, massage: MassageSchemePut):
        user_id = 1
        user = await self.db.scalar(select(User).where(User.id == user_id))
        self.db.add(Massage(text=massage.text, date=datetime.now(), user=user))
        return {"ok": True}


async def get_massage_servies(db: AsyncSession = Depends(get_db)):
    return MassageServies(db)
