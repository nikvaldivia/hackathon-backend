"""
Servicio para manejar la lógica del chat
"""
from typing import List, Dict, Any
from app.chat.services.gemini_service import GeminiService
from app.database import get_courses_by_course_code
import logging

logger = logging.getLogger(__name__)

# Lista de cursos disponibles (hardcodeada según el requerimiento)
AVAILABLE_COURSES = [
    ['Calculo 2', 'MAT1620'],
    ['Optimización', 'ICS1113'],
    ['Electricidad y Magnetismo', 'FIS1533'],
    ['Termodinamica', 'FIS1523', 'IIQ1003'],
    ['Programacion Avanzada', 'IIC2233'],
    ['Probabilidades y Estadistica', 'EYP1113'],
    ['Analisis Forense', 'QIM122'],
    ['Biologia de la Celula', 'BIO141C'],
    ['Introduccion a la Argumentacion', 'FIL2006'],
    ['Tenis 1', 'DPT6500'],
    ['Dinamica', 'FIS0154', 'ICE1514'],
    ['Introduccion a la Programacion', 'IIC1103'],
    ['Calculo 3', 'MAT1630'],
    ['Ecuaciones Diferenciales', 'MAT1640'],
    ['Busqueda Religiosa y Cristianismo', 'TTF202'],
    ['Introduccion a la Economia', 'ICS1513'],
    ['Etica para Ingenieria', 'ETI188'],
    ['Modelos Estocasticos', 'ICS2123'],
    ['Investigacion, Innovacion y Emprendimiento', 'ING2030']
]


class ChatService:
    """Servicio para operaciones relacionadas con el chat"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def process_chat(
        self,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Procesa una conversación de chat:
        1. Clasifica cursos relevantes usando Gemini
        2. Busca información de esos cursos en la BD
        3. Genera respuesta usando el contexto
        
        Args:
            messages: Lista de mensajes de la conversación
            
        Returns:
            Dict con la respuesta y los cursos relevantes
        """
        try:
            # Paso 1: Clasificar cursos relevantes
            logger.info("Clasificando cursos relevantes...")
            relevant_siglas = await self.gemini_service.classify_relevant_courses(
                conversation=messages,
                available_courses=AVAILABLE_COURSES
            )
            
            logger.info(f"Cursos relevantes identificados: {relevant_siglas}")
            
            # Paso 2: Buscar información de los cursos en la base de datos
            courses_context = []
            if relevant_siglas:
                logger.info("Buscando información de cursos en la base de datos...")
                for sigla in relevant_siglas:
                    try:
                        courses = await get_courses_by_course_code(sigla, limit=5)
                        courses_context.extend(courses)
                    except Exception as e:
                        logger.warning(f"Error al buscar curso {sigla}: {e}")
                        continue
            
            logger.info(f"Información de {len(courses_context)} cursos encontrada")
            
            # Paso 3: Generar respuesta con el contexto (RAG)
            logger.info("Generando respuesta con contexto (RAG)...")
            if not courses_context:
                # Si no hay contexto, generar respuesta indicando que no hay información
                response = "No tengo información específica sobre los cursos mencionados en la base de datos."
            else:
                response = await self.gemini_service.generate_response(
                    conversation=messages,
                    courses_context=courses_context
                )
            
            return {
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error al procesar chat: {e}", exc_info=True)
            raise

