from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    JWT_SECRET_KEY: str


@lru_cache
def get_auth_settings() -> AuthSettings:
    return AuthSettings()


auth_settings = get_auth_settings()
