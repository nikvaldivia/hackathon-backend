"""
Rutas para el endpoint de chat
"""
from fastapi import APIRouter, HTTPException
from app.chat.services.chat_service import ChatService
from app.chat.schemas.chat import ChatRequest, ChatResponse, Message
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint para chatear con el bot sobre cursos (RAG).
    
    El usuario envía los últimos mensajes de la conversación. El sistema:
    1. Usa Gemini para identificar qué cursos son relevantes para el contexto
    2. Busca información de esos cursos en la base de datos
    3. Genera una respuesta breve usando el contexto de los cursos (RAG)
    
    Args:
        request: Request con los mensajes de la conversación
        
    Returns:
        Respuesta breve del chatbot basada en el contexto de cursos
    """
    try:
        # Validar que hay mensajes
        if not request.messages:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar al menos un mensaje en la conversación"
            )
        
        # Validar que el último mensaje es del usuario
        last_message = request.messages[-1]
        if last_message.role != "user":
            raise HTTPException(
                status_code=400,
                detail="El último mensaje debe ser del usuario"
            )
        
        # Convertir mensajes a formato dict
        messages_dict = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Procesar el chat
        result = await chat_service.process_chat(messages_dict)
        
        return ChatResponse(
            response=result["response"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint /chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el chat: {str(e)}"
        )

