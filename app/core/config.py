from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

# .env 파일 로드
load_dotenv()

# 환경 변수 설정
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEFAULT_LLM_MODEL = os.getenv("LLM_MODEL", "llama3-70b-8192")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")

def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 

class Settings(BaseSettings):
    # Groq API 설정
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192")
    
    # HuggingFace 설정
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    # PostgreSQL 설정
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    
    # Naver API 설정
    NAVER_CLIENT_ID: str = os.getenv("NAVER_CLIENT_ID", "")
    NAVER_CLIENT_SECRET: str = os.getenv("NAVER_CLIENT_SECRET", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 