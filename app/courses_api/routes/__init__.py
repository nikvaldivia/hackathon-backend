"""
Rutas para la funcionalidad de API de cursos
"""
from fastapi import APIRouter
from app.courses_api.routes import courses
from app.courses_api.routes import professors

# Crear el router principal
router = APIRouter()

# Incluir los sub-routers
router.include_router(courses.router, prefix="/courses", tags=["courses"])
router.include_router(professors.router, prefix="/professors", tags=["professors"])

__all__ = ["router"]
