"""
Carpeta compartida para utilidades y recursos comunes
entre todas las funcionalidades del proyecto.

Nota: La configuración y la base de datos están en app/config.py y app/database.py
"""
# Re-exportar desde los nuevos lugares para mantener compatibilidad
from app.config import settings
from app.database import (
    mongodb,
    connect_to_mongo,
    close_mongo_connection,
    get_database
)

__all__ = [
    "settings",
    "mongodb",
    "connect_to_mongo",
    "close_mongo_connection",
    "get_database"
]

