"""
Punto de entrada principal de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection, mongodb, is_connected

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("🚀 Iniciando aplicación...")
    await connect_to_mongo()
    # Actualizar la instancia global después de la conexión
    global db
    db = mongodb.database
    yield
    # Shutdown
    logger.info("🛑 Cerrando aplicación...")
    await close_mongo_connection()


# Instancia global de la base de datos
# Se puede usar en cualquier parte de la aplicación importando: from app.main import db
# Nota: Se inicializa después de la conexión en el lifespan
# Alternativamente, puedes usar: from app.database import get_database
db = None


def get_db():
    """
    Función helper para obtener la instancia de la base de datos.
    Siempre devuelve la instancia actual de MongoDB.
    
    Uso:
        from app.main import get_db
        db = get_db()
    """
    return mongodb.database


# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API para Hackathon con FastAPI, MongoDB y Gemini",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar y registrar las rutas de cada funcionalidad
# Las rutas se agregarán aquí cuando cada funcionalidad esté lista
# Ejemplo:
# from app.database.routes import router as database_router
# from app.courses_api.routes import router as courses_api_router
# from app.chat.routes import router as chat_router
#
# app.include_router(database_router, prefix="/api/database", tags=["database"])
# app.include_router(courses_api_router, prefix="/api/courses", tags=["courses"])
# app.include_router(chat_router, prefix="/api/chat", tags=["chat"])


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a Hackathon Backend API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    try:
        db_status = "connected" if is_connected() else "disconnected"
        # Si está conectado, hacer un ping para verificar que la conexión sigue activa
        if db_status == "connected":
            try:
                await mongodb.client.admin.command('ping')
            except Exception:
                db_status = "disconnected"
        
        return {
            "status": "healthy" if db_status == "connected" else "degraded",
            "database": db_status
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }

