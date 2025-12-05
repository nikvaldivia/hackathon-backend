"""
Rutas para la funcionalidad de API de cursos
"""
from fastapi import APIRouter
from app.courses_api.routes import courses

# Crear el router principal
router = APIRouter()

# Incluir los sub-routers
router.include_router(courses.router, prefix="/cursos", tags=["cursos"])

__all__ = ["router"]
