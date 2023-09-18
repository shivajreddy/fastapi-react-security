from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str

    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str

    class Config:
        env_file = "./.env"


settings = Settings()
