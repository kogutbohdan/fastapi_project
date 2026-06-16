from pydantic import BaseModel, EmailStr


class UserSheme(BaseModel):
    username: str
    password: str
    email: EmailStr
