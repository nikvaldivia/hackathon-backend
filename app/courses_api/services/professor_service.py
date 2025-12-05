"""
Servicio para manejar la lógica de negocio de profesores
"""
from typing import List, Optional, Dict, Any
from app.database import (
    get_cursos_filtrados_by_profesor,
    get_profesor_by_nombre,
)
import logging

logger = logging.getLogger(__name__)


class ProfessorService:
    """Servicio para operaciones relacionadas con profesores"""
    
    @staticmethod
    async def get_courses_by_professor(nombre_profesor: str) -> List[Dict[str, Any]]:
        """
        Obtener todos los cursos dictados por un profesor.
        
        Args:
            nombre_profesor: Nombre del profesor
            
        Returns:
            Lista de cursos dictados por el profesor
        """
        try:
            courses = await get_cursos_filtrados_by_profesor(
                nombre_profesor,
                exact_match=False
            )
            return courses
        except Exception as e:
            logger.error(f"Error al obtener cursos del profesor {nombre_profesor}: {e}")
            raise
    
    @staticmethod
    async def get_professor_info(nombre_profesor: str) -> Optional[Dict[str, Any]]:
        """
        Obtener información de un profesor.
        
        Args:
            nombre_profesor: Nombre del profesor
            
        Returns:
            Información del profesor o None si no se encuentra
        """
        try:
            professor = await get_profesor_by_nombre(nombre_profesor, exact_match=False)
            return professor
        except Exception as e:
            logger.error(f"Error al obtener información del profesor {nombre_profesor}: {e}")
            raise

