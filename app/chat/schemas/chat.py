"""
Schemas para el chat
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class Message(BaseModel):
    """Schema para un mensaje en la conversación"""
    role: str = Field(..., description="Rol del mensaje: 'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")


class ChatRequest(BaseModel):
    """Schema para el request del endpoint de chat"""
    messages: List[Message] = Field(..., description="Lista de mensajes de la conversación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "¿Qué cursos de optimización hay disponibles?"},
                    {"role": "assistant", "content": "Hay varios cursos relacionados con optimización..."},
                    {"role": "user", "content": "¿Cuál tiene mejor rating?"}
                ]
            }
        }


class ChatResponse(BaseModel):
    """Schema para la respuesta del endpoint de chat"""
    response: str = Field(..., description="Respuesta breve del chatbot")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "El curso ICS1113 (Optimización) tiene una carga académica intensa y es dictado por el profesor Klapp Mathias en el campus San Joaquín."
            }
        }

