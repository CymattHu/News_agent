import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "zh")
    db_url: str = os.getenv("DB_URL", "sqlite:///news_agent.db")
    user_agent: str = os.getenv("USER_AGENT", "news-agent-bot/1.0")

settings = Settings()
