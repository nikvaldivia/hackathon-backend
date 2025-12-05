"""
Rutas para endpoints de cursos
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.courses_api.services.course_service import CourseService
from app.courses_api.schemas.course import CourseResponse, CourseListResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
course_service = CourseService()


@router.get("/by-sigla/{sigla}", response_model=CourseListResponse)
async def get_courses_by_sigla(sigla: str):
    """
    Obtener todas las secciones de un curso por su sigla.
    
    Args:
        sigla: Sigla del curso (ej: "IIC2233")
        
    Returns:
        Lista de todas las secciones del curso
    """
    try:
        courses = await course_service.get_courses_by_sigla(sigla)
        return CourseListResponse(
            courses=[CourseResponse(**course) for course in courses],
            count=len(courses)
        )
    except Exception as e:
        logger.error(f"Error en get_courses_by_sigla: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener cursos por sigla: {str(e)}")


@router.get("/by-nrc/{nrc}", response_model=CourseResponse)
async def get_course_by_nrc(nrc: str):
    """
    Obtener una sección específica de un curso por su NRC.
    
    Args:
        nrc: NRC del curso (código único por sección)
        
    Returns:
        Información de la sección del curso
    """
    try:
        course = await course_service.get_course_by_nrc(nrc)
        if not course:
            raise HTTPException(status_code=404, detail=f"Curso con NRC {nrc} no encontrado")
        return CourseResponse(**course)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_course_by_nrc: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener curso por NRC: {str(e)}")


@router.get("/search", response_model=CourseListResponse)
async def search_courses_by_name(
    nombre: str = Query(..., description="Nombre del curso a buscar")
):
    """
    Buscar cursos por nombre del curso.
    
    Args:
        nombre: Nombre del curso a buscar (búsqueda parcial, case-insensitive)
        
    Returns:
        Lista de cursos que coinciden con el nombre
    """
    try:
        courses = await course_service.search_courses_by_name(nombre)
        return CourseListResponse(
            courses=[CourseResponse(**course) for course in courses],
            count=len(courses)
        )
    except Exception as e:
        logger.error(f"Error en search_courses_by_name: {e}")
        raise HTTPException(status_code=500, detail=f"Error al buscar cursos por nombre: {str(e)}")

