"""
Rutas para la funcionalidad de chat
"""
from fastapi import APIRouter
from app.chat.routes import chat

# Crear el router principal
router = APIRouter()

# Incluir los sub-routers
router.include_router(chat.router, tags=["chat"])

__all__ = ["router"]
