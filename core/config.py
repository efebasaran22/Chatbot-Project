"""Application configuration using Pydantic Settings."""
from typing import List
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings
    SettingsConfigDict = None
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "MSKÜ ChatBot API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "LLM Tabanlı Üniversite Bilgi Asistanı"
    
    # LLM Configuration
    LLM_PROVIDER: str = "groq"  # "groq" or "ollama"
    
    # Groq Settings
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    GROQ_TEMPERATURE: float = 0.3
    GROQ_MAX_TOKENS: int = 500
    
    # Ollama Settings (fallback)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = "paraphrase-multilingual-mpnet-base-v2"
    
    # Vector Database
    CHROMA_DB_PATH: str = "./app/data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "msku_documents"
    
    # Security
    MAX_QUESTION_LENGTH: int = 500
    RATE_LIMIT_PER_MINUTE: int = 30
    RATE_LIMIT_PER_HOUR: int = 500
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    if SettingsConfigDict is not None:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=True
        )
    else:
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = True
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


# Global settings instance
settings = Settings()
