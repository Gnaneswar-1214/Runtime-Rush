from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/runtime_rush"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev-secret-key"
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
