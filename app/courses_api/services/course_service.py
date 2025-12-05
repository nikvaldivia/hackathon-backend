"""
Servicio para manejar la lógica de negocio de cursos
"""
from typing import List, Optional, Dict, Any
from app.database import (
    get_courses_by_course_code as db_get_courses_by_course_code,
    get_course_by_nrc as db_get_course_by_nrc,
    search_courses as db_search_courses,
)
import logging

logger = logging.getLogger(__name__)


class CourseService:
    """Servicio para operaciones relacionadas con cursos"""
    
    @staticmethod
    async def get_courses_by_sigla(sigla: str) -> List[Dict[str, Any]]:
        """
        Obtener todas las secciones de un curso por su sigla.
        
        Args:
            sigla: Sigla del curso (ej: "ICS1113", "IIC2233")
            
        Returns:
            Lista de secciones del curso
        """
        try:
            courses = await db_get_courses_by_course_code(sigla)
            return courses
        except Exception as e:
            logger.error(f"Error al obtener cursos por sigla {sigla}: {e}")
            raise
    
    @staticmethod
    async def get_course_by_nrc(nrc: str) -> Optional[Dict[str, Any]]:
        """
        Obtener una sección específica de un curso por su NRC.
        
        Args:
            nrc: NRC del curso (código único por sección)
            
        Returns:
            Información del curso o None si no se encuentra
        """
        try:
            course = await db_get_course_by_nrc(nrc)
            return course
        except Exception as e:
            logger.error(f"Error al obtener curso por NRC {nrc}: {e}")
            raise
    
    @staticmethod
    async def search_courses(
        course_name: Optional[str] = None,
        course_code: Optional[str] = None,
        professor_name: Optional[str] = None,
        nrc: Optional[str] = None,
        min_professor_rating: Optional[float] = None,
        workload_label: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        limit: Optional[int] = 50
    ) -> List[Dict[str, Any]]:
        """
        Buscar cursos con múltiples criterios.
        
        Args:
            course_name: Nombre del curso a buscar (búsqueda parcial)
            course_code: Sigla del curso
            professor_name: Nombre del profesor
            nrc: NRC específico
            min_professor_rating: Rating mínimo del profesor
            workload_label: Carga académica (baja, media, intensa, alta)
            difficulty_level: Nivel de dificultad (baja, media, alta)
            limit: Límite de resultados
            
        Returns:
            Lista de cursos que cumplen con los criterios
        """
        try:
            courses = await db_search_courses(
                course_code=course_code,
                course_name=course_name,
                professor_name=professor_name,
                nrc=nrc,
                min_professor_rating=min_professor_rating,
                workload_label=workload_label,
                difficulty_level=difficulty_level,
                limit=limit
            )
            return courses
        except Exception as e:
            logger.error(f"Error al buscar cursos: {e}")
            raise

