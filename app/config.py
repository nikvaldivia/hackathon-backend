"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Hackathon Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Configuración de MongoDB
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "hackathon_db"
    
    # Configuración de Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"
    
    # Configuración de CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Instancia global de configuración
settings = Settings()

