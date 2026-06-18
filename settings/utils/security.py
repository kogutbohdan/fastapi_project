from authx import AuthX, AuthXConfig
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from ..configs.auth import auth_settings

config = AuthXConfig()
config.JWT_SECRET_KEY = auth_settings.JWT_SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = "my_token"
config.JWT_TOKEN_LOCATION = ["headers"]

security = AuthX(config=config)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hash):
    return pwd_context.verify(password, hash)


def hash_password(password):
    return pwd_context.hash(password)
