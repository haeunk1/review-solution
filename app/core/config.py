import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env 파일 로드
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Review AI Solution"
    
    # DB 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # OpenAI 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # Google Gemini 설정
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # JWT 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()