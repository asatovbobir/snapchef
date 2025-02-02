from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    openai_api_key: str
    pexels_api_key: str
    api_port: int = 8000
    temp_image_dir: Path = Path("static/temp_images")
    default_image_url: str = "https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_1280.jpg"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()