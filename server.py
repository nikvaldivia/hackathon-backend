"""
Archivo para iniciar el servidor FastAPI
Carga las variables de entorno y ejecuta uvicorn
"""
import uvicorn
from app.config import settings

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )

