from pydantic import BaseModel, EmailStr


class UserRegistrationSheme(BaseModel):
    username: str
    password: str
    email: EmailStr
