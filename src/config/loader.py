from pydantic_settings import BaseSettings
from pydantic import ValidationError
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    app_name: str

    class Config:
        env_prefix = ""
        fields = {
            "app_name": {"env": "APP_NAME"}
        }

def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        raise RuntimeError(f"Config validation failed: {e}")
