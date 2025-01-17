import os
from pydantic_settings import BaseSettings, SettingsConfigDict

_env_file_path = os.path.join(os.path.dirname(__file__), ".env")
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=_env_file_path, extra="ignore")
    SECRET_JWT: str
    PASSWORD: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
config = Config()
