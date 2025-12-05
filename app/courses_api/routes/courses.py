"""
Rutas para endpoints de cursos
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.courses_api.services.course_service import CourseService
from app.courses_api.schemas.course import CourseResponse, CourseListResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
course_service = CourseService()


@router.get("/sigla/{sigla}", response_model=CourseListResponse)
async def get_courses_by_sigla(sigla: str):
    """
    Obtener todas las secciones de un curso por su sigla.
    
    Args:
        sigla: Sigla del curso (ej: "ICS1113", "IIC2233")
        
    Returns:
        Lista de todas las secciones del curso
    """
    try:
        courses = await course_service.get_courses_by_sigla(sigla)
        # Convertir cada curso al schema, manejando posibles errores de validación
        course_responses = []
        for course in courses:
            try:
                course_responses.append(CourseResponse(**course))
            except Exception as e:
                logger.warning(f"Error al validar curso {course.get('nrc', 'unknown')}: {e}")
                # Continuar con el siguiente curso si hay un error de validación
                continue
        
        return CourseListResponse(
            courses=course_responses,
            count=len(course_responses)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_courses_by_sigla: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al obtener cursos por sigla: {str(e)}")


@router.get("/nrc/{nrc}", response_model=CourseResponse)
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
        
        try:
            return CourseResponse(**course)
        except Exception as validation_error:
            logger.error(f"Error de validación al procesar curso NRC {nrc}: {validation_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar datos del curso: {str(validation_error)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en get_course_by_nrc: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al obtener curso por NRC: {str(e)}")


@router.get("/search", response_model=CourseListResponse)
async def search_courses(
    course_name: Optional[str] = Query(None, description="Nombre del curso a buscar (búsqueda parcial)"),
    course_code: Optional[str] = Query(None, description="Sigla del curso"),
    professor_name: Optional[str] = Query(None, description="Nombre del profesor"),
    nrc: Optional[str] = Query(None, description="NRC específico"),
    min_professor_rating: Optional[float] = Query(None, description="Rating mínimo del profesor"),
    workload_label: Optional[str] = Query(None, description="Carga académica (baja, media, intensa, alta)"),
    difficulty_level: Optional[str] = Query(None, description="Nivel de dificultad (baja, media, alta)"),
    limit: Optional[int] = Query(50, description="Límite de resultados")
):
    """
    Buscar cursos con múltiples criterios de búsqueda.
    
    Principalmente se usa para buscar por nombre del curso, pero también permite
    filtrar por otros criterios como profesor, rating, carga académica, etc.
    
    Args:
        course_name: Nombre del curso a buscar (búsqueda parcial, case-insensitive)
        course_code: Sigla del curso
        professor_name: Nombre del profesor
        nrc: NRC específico
        min_professor_rating: Rating mínimo del profesor
        workload_label: Carga académica
        difficulty_level: Nivel de dificultad
        limit: Límite de resultados
        
    Returns:
        Lista de cursos que cumplen con los criterios especificados
    """
    try:
        # Validar que al menos un parámetro de búsqueda esté presente
        if not any([course_name, course_code, professor_name, nrc, min_professor_rating, workload_label, difficulty_level]):
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar al menos un criterio de búsqueda"
            )
        
        courses = await course_service.search_courses(
            course_name=course_name,
            course_code=course_code,
            professor_name=professor_name,
            nrc=nrc,
            min_professor_rating=min_professor_rating,
            workload_label=workload_label,
            difficulty_level=difficulty_level,
            limit=limit
        )
        
        # Convertir cada curso al schema, manejando posibles errores de validación
        course_responses = []
        for course in courses:
            try:
                course_responses.append(CourseResponse(**course))
            except Exception as e:
                logger.warning(f"Error al validar curso {course.get('nrc', 'unknown')}: {e}")
                # Continuar con el siguiente curso si hay un error de validación
                continue
        
        return CourseListResponse(
            courses=course_responses,
            count=len(course_responses)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en search_courses: {e}")
        raise HTTPException(status_code=500, detail=f"Error al buscar cursos: {str(e)}")
