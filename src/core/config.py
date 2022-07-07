from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX_STR: str = "/api/v1"
    SECRET_KEY: str
    PROJECT_NAME: str = "fax_server"

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # postgres values
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool

    class Config:
        env_file = ".env"


settings = Settings()
