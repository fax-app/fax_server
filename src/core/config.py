from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX_STR: str = "/api/v1"
    SECRET_KEY: str
    PROJECT_NAME: str = "fax_server"

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # AWS values
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    USERS_OPEN_REGISTRATION: bool

    class Config:
        env_file = ".env"


settings = Settings()
