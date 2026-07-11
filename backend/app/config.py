import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/lawai")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-prod")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    CORPUS_DIR = os.getenv("CORPUS_DIR", "./data/corpus")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    JWT_ACCESS_TOKEN_EXPIRES = 86400
