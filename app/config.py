import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = os.environ.get("DATABASE_HOSTNAME")
    database_port: str = os.environ.get("DATABASE_PORT")
    database_password: str = os.environ.get("DATABASE_PASSWORD")
    database_name: str = os.environ.get("DATABASE_NAME")
    database_username: str = os.environ.get("DATABASE_USERNAME")
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = int(
        os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    )  # convert to int


class Config:
    env_file = ".env"


settings = Settings()
