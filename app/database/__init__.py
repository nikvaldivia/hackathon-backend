"""
Configuración y conexión a MongoDB
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MongoDB:
    """Clase para manejar la conexión a MongoDB"""
    
    client: Optional[AsyncIOMotorClient] = None
    database = None


# Instancia global de MongoDB
mongodb = MongoDB()


async def connect_to_mongo():
    """
    Conectar a MongoDB con configuración optimizada.
    
    Raises:
        Exception: Si no se puede establecer la conexión
    """
    try:
        # Validar que la URL de MongoDB esté configurada
        if not settings.MONGODB_URL:
            raise ValueError("MONGODB_URL no está configurada en las variables de entorno")
        
        if not settings.MONGODB_DB_NAME:
            raise ValueError("MONGODB_DB_NAME no está configurada en las variables de entorno")
        
        logger.info(f"🔌 Intentando conectar a MongoDB: {settings.MONGODB_URL.split('@')[-1] if '@' in settings.MONGODB_URL else 'URL oculta'}")
        
        # Configurar opciones de conexión
        connection_options = {
            "serverSelectionTimeoutMS": 5000,  # Timeout de 5 segundos para selección de servidor
            "connectTimeoutMS": 10000,  # Timeout de 10 segundos para conexión
            "socketTimeoutMS": 20000,  # Timeout de 20 segundos para operaciones
            "retryWrites": True,  # Reintentar escrituras fallidas
            "retryReads": True,  # Reintentar lecturas fallidas
            "maxPoolSize": 50,  # Tamaño máximo del pool de conexiones
            "minPoolSize": 10,  # Tamaño mínimo del pool de conexiones
        }
        
        # Crear cliente de MongoDB
        mongodb.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            **connection_options
        )
        
        # Obtener referencia a la base de datos
        mongodb.database = mongodb.client[settings.MONGODB_DB_NAME]
        
        # Verificar conexión con un ping
        await mongodb.client.admin.command('ping')
        
        # Obtener información del servidor para confirmar conexión
        server_info = await mongodb.client.server_info()
        logger.info(f"✅ Conectado a MongoDB exitosamente")
        logger.info(f"   Base de datos: {settings.MONGODB_DB_NAME}")
        logger.info(f"   Versión del servidor: {server_info.get('version', 'desconocida')}")
        
    except Exception as e:
        logger.error(f"❌ Error al conectar a MongoDB: {e}")
        logger.error(f"   URL: {settings.MONGODB_URL.split('@')[-1] if '@' in settings.MONGODB_URL else 'URL oculta'}")
        # Cerrar cliente si se creó pero falló la conexión
        if mongodb.client:
            mongodb.client.close()
            mongodb.client = None
        raise


async def close_mongo_connection():
    """
    Cerrar conexión a MongoDB de forma segura.
    """
    if mongodb.client:
        try:
            mongodb.client.close()
            mongodb.client = None
            mongodb.database = None
            logger.info("🔌 Conexión a MongoDB cerrada correctamente")
        except Exception as e:
            logger.error(f"❌ Error al cerrar conexión a MongoDB: {e}")


async def get_database():
    """
    Obtener instancia de la base de datos.
    
    Returns:
        Database: Instancia de la base de datos MongoDB
        
    Raises:
        RuntimeError: Si la base de datos no está conectada
    """
    if mongodb.database is None:
        raise RuntimeError("La base de datos no está conectada. Llama a connect_to_mongo() primero.")
    return mongodb.database


def is_connected() -> bool:
    """
    Verificar si hay una conexión activa a MongoDB.
    
    Returns:
        bool: True si está conectado, False en caso contrario
    """
    return mongodb.client is not None and mongodb.database is not None
