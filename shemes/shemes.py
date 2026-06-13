from datetime import datetime

from pydantic import BaseModel, Field


class MassageSchemePut(BaseModel):
    text: str


class MassageShemeRead(BaseModel):
    id: int
    text: str
    username: str = Field(..., max_length=100)
    date: datetime


class MassageShemeUpdate(BaseModel):
    id: int
    text: str
