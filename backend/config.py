from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "4M1N Bilişim Teknolojileri - Teklif Hazırlama Platformu"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./4m1n_bilisim.db"
    
    ALLOWED_HOSTS: list = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()