from datetime import datetime

from pydantic import BaseModel, Field


class MassageSchemePut(BaseModel):
    text: str


class MassageShemeRead(BaseModel):
    text: str
    user_name: str
    date: datetime
