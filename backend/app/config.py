import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/lawai")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-prod")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    CORPUS_DIR = os.getenv("CORPUS_DIR", "./data/corpus")
    JWT_ACCESS_TOKEN_EXPIRES = 86400
