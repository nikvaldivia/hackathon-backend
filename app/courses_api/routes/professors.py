"""
Rutas para endpoints de profesores
"""
from fastapi import APIRouter, HTTPException
from app.courses_api.services.professor_service import ProfessorService
from app.courses_api.schemas.course import CourseListResponse, CourseResponse
from app.courses_api.schemas.professor import ProfessorResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
professor_service = ProfessorService()


@router.get("/{nombre_profesor}/courses", response_model=CourseListResponse)
async def get_professor_courses(nombre_profesor: str):
    """
    Obtener todos los cursos dictados por un profesor.
    
    Args:
        nombre_profesor: Nombre del profesor
        
    Returns:
        Lista de cursos dictados por el profesor
    """
    try:
        courses = await professor_service.get_courses_by_professor(nombre_profesor)
        return CourseListResponse(
            courses=[CourseResponse(**course) for course in courses],
            count=len(courses)
        )
    except Exception as e:
        logger.error(f"Error en get_professor_courses: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener cursos del profesor: {str(e)}"
        )


@router.get("/{nombre_profesor}", response_model=ProfessorResponse)
async def get_professor_info(nombre_profesor: str):
    """
    Obtener información de un profesor.
    
    Args:
        nombre_profesor: Nombre del profesor
        
    Returns:
        Información del profesor
    """
    try:
        professor = await professor_service.get_professor_info(nombre_profesor)
        if not professor:
            raise HTTPException(
                status_code=404,
                detail=f"Profesor {nombre_profesor} no encontrado"
            )
        return ProfessorResponse(**professor)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_professor_info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener información del profesor: {str(e)}"
        )

