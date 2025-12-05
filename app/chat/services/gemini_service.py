"""
Servicio para interactuar con la API de Gemini
"""
import google.generativeai as genai
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Configurar Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Servicio para manejar interacciones con Gemini API"""
    
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    async def classify_relevant_courses(
        self,
        conversation: list[dict],
        available_courses: list[list[str]]
    ) -> list[str]:
        """
        Clasifica qué cursos son relevantes para la conversación.
        
        Args:
            conversation: Lista de mensajes de la conversación
            available_courses: Lista de cursos disponibles en formato [nombre, sigla1, sigla2, ...]
            
        Returns:
            Lista de siglas de cursos relevantes
        """
        try:
            # Formatear la conversación
            conversation_text = self._format_conversation(conversation)
            
            # Formatear la lista de cursos
            courses_text = self._format_courses_list(available_courses)
            
            # Crear el prompt para clasificación
            prompt = f"""Analiza esta conversación y identifica qué cursos son relevantes para responder al usuario.

CONVERSACIÓN:
{conversation_text}

CURSOS DISPONIBLES:
{courses_text}

INSTRUCCIONES:
- Identifica cursos mencionados explícitamente o relacionados con el tema de la conversación
- Responde SOLO con siglas separadas por comas, sin espacios
- Si no hay cursos relevantes, responde con una cadena vacía
- NO incluyas explicaciones, puntos, ni texto adicional
- NO uses espacios entre las siglas

Ejemplo de formato correcto: ICS1113,IIC2233,FIS1533

SIGLAS:"""

            # Generar respuesta
            response = await self._generate_text(prompt)
            
            # Procesar respuesta para extraer siglas
            siglas = self._extract_siglas(response, available_courses)
            
            logger.info(f"Cursos relevantes identificados: {siglas}")
            return siglas
            
        except Exception as e:
            logger.error(f"Error al clasificar cursos relevantes: {e}", exc_info=True)
            raise
    
    async def generate_response(
        self,
        conversation: list[dict],
        courses_context: list[dict]
    ) -> str:
        """
        Genera una respuesta al último mensaje del usuario usando el contexto de cursos.
        
        Args:
            conversation: Lista de mensajes de la conversación
            courses_context: Información de los cursos relevantes de la base de datos
            
        Returns:
            Respuesta generada por el modelo
        """
        try:
            # Formatear la conversación
            conversation_text = self._format_conversation(conversation)
            
            # Formatear el contexto de cursos
            courses_context_text = self._format_courses_context(courses_context)
            
            # Obtener el último mensaje del usuario
            last_user_message = ""
            for msg in reversed(conversation):
                if msg.get("role") == "user":
                    last_user_message = msg.get("content", "")
                    break
            
            # Crear el prompt para generar respuesta (RAG)
            prompt = f"""Eres un asistente académico que responde preguntas sobre cursos universitarios usando SOLO la información proporcionada.

INFORMACIÓN DE CURSOS DISPONIBLE:
{courses_context_text}

ÚLTIMA PREGUNTA DEL USUARIO:
{last_user_message}

INSTRUCCIONES CRÍTICAS:
- Responde SOLO usando la información de cursos proporcionada arriba
- Si la información no está en el contexto, di "No tengo esa información específica disponible"
- Sé BREVE: máximo 3-4 oraciones
- Responde directamente la pregunta, sin introducciones largas
- Usa datos concretos del contexto (nombres, siglas, ratings, etc.)
- Responde en el mismo idioma del usuario

RESPUESTA BREVE:"""

            # Generar respuesta
            response = await self._generate_text(prompt)
            
            logger.info("Respuesta generada exitosamente")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}", exc_info=True)
            raise
    
    def _format_conversation(self, conversation: list[dict]) -> str:
        """Formatea la conversación para el prompt"""
        formatted = []
        for msg in conversation:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.upper()}: {content}")
        return "\n".join(formatted)
    
    def _format_courses_list(self, courses: list[list[str]]) -> str:
        """Formatea la lista de cursos para el prompt"""
        formatted = []
        for course in courses:
            name = course[0] if course else ""
            siglas = ", ".join(course[1:]) if len(course) > 1 else ""
            formatted.append(f"- {name} ({siglas})")
        return "\n".join(formatted)
    
    def _format_courses_context(self, courses: list[dict]) -> str:
        """Formatea el contexto de cursos de la base de datos de forma concisa"""
        if not courses:
            return "No hay información de cursos disponible."
        
        formatted = []
        for course in courses:
            # Información básica
            course_info = f"{course.get('course_name', 'N/A')} ({course.get('course_code', 'N/A')})"
            course_info += f" - Profesor: {course.get('professor', 'N/A')}"
            
            # Rating del profesor si está disponible
            if course.get('professor_ratings'):
                ratings = course.get('professor_ratings', [])
                if ratings and len(ratings) > 0 and ratings[0].get('overall'):
                    course_info += f" - Rating: {ratings[0].get('overall')}"
            
            # Información adicional importante
            if course.get('workload'):
                course_info += f" - Carga: {course.get('workload')}"
            if course.get('difficulty_level'):
                course_info += f" - Dificultad: {course.get('difficulty_level')}"
            if course.get('campus'):
                course_info += f" - Campus: {course.get('campus')}"
            if course.get('available_slots') is not None and course.get('total_slots') is not None:
                course_info += f" - Cupos: {course.get('available_slots')}/{course.get('total_slots')}"
            
            # Resumen si está disponible
            if course.get('overall_summary'):
                course_info += f"\n  Resumen: {course.get('overall_summary')}"
            
            # Pros y cons si están disponibles
            if course.get('pros'):
                course_info += f"\n  Pros: {', '.join(course.get('pros', [])[:3])}"  # Máximo 3 pros
            if course.get('cons'):
                course_info += f"\n  Contras: {', '.join(course.get('cons', [])[:3])}"  # Máximo 3 contras
            
            formatted.append(course_info)
        
        return "\n\n".join(formatted)
    
    def _extract_siglas(self, response: str, available_courses: list[list[str]]) -> list[str]:
        """Extrae las siglas válidas de la respuesta del modelo"""
        if not response:
            return []
        
        # Limpiar la respuesta
        response = response.strip().upper()
        
        # Extraer todas las siglas posibles de la lista de cursos
        all_siglas = set()
        for course in available_courses:
            if len(course) > 1:
                all_siglas.update([sigla.upper() for sigla in course[1:]])
        
        if not all_siglas:
            return []
        
        found_siglas = []
        
        # Primero intentar parsear directamente por comas (formato esperado)
        if "," in response:
            potential_siglas = [s.strip().upper() for s in response.split(",")]
            for sigla in potential_siglas:
                # Limpiar cualquier carácter extra
                sigla = sigla.strip().replace(".", "").replace(" ", "")
                if sigla in all_siglas:
                    found_siglas.append(sigla)
        
        # Si no se encontraron por comas, buscar siglas en el texto
        if not found_siglas:
            # Buscar siglas que aparezcan como palabras completas
            import re
            # Crear un patrón regex para buscar siglas
            for sigla in all_siglas:
                # Buscar la sigla como palabra completa (con límites de palabra)
                pattern = r'\b' + re.escape(sigla) + r'\b'
                if re.search(pattern, response):
                    found_siglas.append(sigla)
        
        # Eliminar duplicados y retornar
        return list(set(found_siglas))
    
    async def _generate_text(self, prompt: str) -> str:
        """Genera texto usando Gemini"""
        try:
            # La API de Gemini es síncrona, pero la envolvemos en async
            import asyncio
            
            def _sync_generate():
                """Función síncrona para generar contenido"""
                response = self.model.generate_content(prompt)
                # Manejar diferentes formatos de respuesta
                if hasattr(response, 'text'):
                    return response.text
                elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                    return response.candidates[0].content.parts[0].text
                else:
                    raise ValueError("Formato de respuesta inesperado de Gemini")
            
            # Usar to_thread si está disponible (Python 3.9+), sino usar executor
            try:
                response_text = await asyncio.to_thread(_sync_generate)
            except AttributeError:
                # Fallback para Python < 3.9
                loop = asyncio.get_event_loop()
                response_text = await loop.run_in_executor(None, _sync_generate)
            
            if not response_text or not response_text.strip():
                raise ValueError("Respuesta vacía de Gemini")
            
            return response_text.strip()
        except Exception as e:
            logger.error(f"Error al generar texto con Gemini: {e}", exc_info=True)
            raise

