"""
Servicio para manejar la lógica de negocio de cursos
"""
from typing import List, Optional, Dict, Any
from app.database import (
    get_cursos_filtrados_by_sigla,
    get_curso_filtrado_by_nrc,
    get_cursos_filtrados_by_nombre,
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
            sigla: Sigla del curso (ej: "IIC2233")
            
        Returns:
            Lista de secciones del curso
        """
        try:
            courses = await get_cursos_filtrados_by_sigla(sigla)
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
            course = await get_curso_filtrado_by_nrc(nrc)
            return course
        except Exception as e:
            logger.error(f"Error al obtener curso por NRC {nrc}: {e}")
            raise
    
    @staticmethod
    async def search_courses_by_name(nombre: str) -> List[Dict[str, Any]]:
        """
        Buscar cursos por nombre del curso.
        
        Args:
            nombre: Nombre del curso a buscar (búsqueda parcial)
            
        Returns:
            Lista de cursos que coinciden con el nombre
        """
        try:
            courses = await get_cursos_filtrados_by_nombre(nombre, exact_match=False)
            return courses
        except Exception as e:
            logger.error(f"Error al buscar cursos por nombre {nombre}: {e}")
            raise

