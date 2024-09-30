from pydantic import (
    BaseSettings
)


class Settings(BaseSettings, extra="ignore"):
    """
    use this http://127.0.0.1:8000/api/v1 for local testing
    """
    VULAVULA_BASE_URL: str = "https://vulavula-services.lelapa.ai/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = 'ignore'


settings = Settings()
