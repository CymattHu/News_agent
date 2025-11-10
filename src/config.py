import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "zh")
    db_url: str = os.getenv("DB_URL", "sqlite:///news_agent.db")
    user_agent: str = os.getenv("USER_AGENT", "news-agent-bot/1.0")

settings = Settings()
