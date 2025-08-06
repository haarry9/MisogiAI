from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    database_ssl_mode: str = "require"
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    secret_key: str
    debug: bool = False
    environment: str = "production"
    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    aws_region: str = None
    maps_api_key: str = None
    email_api_key: str = None

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()