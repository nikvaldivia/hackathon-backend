"""
Schemas para cursos
"""
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class CourseResponse(BaseModel):
    """Schema para la respuesta de un curso"""
    
    id: Optional[str] = Field(None, alias="_id", description="ID del curso")
    sigla: Optional[str] = Field(None, description="Sigla del curso")
    nombre: Optional[str] = Field(None, description="Nombre del curso")
    nrc: Optional[str] = Field(None, description="NRC (código único por sección)")
    profesor: Optional[str] = Field(None, description="Nombre del profesor")
    rating_curso: Optional[float] = Field(None, description="Rating del curso")
    rating_profesor: Optional[float] = Field(None, description="Rating del profesor")
    carga_academica: Optional[str] = Field(None, description="Carga académica")
    
    # Campos adicionales que pueden existir
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "sigla": "IIC2233",
                "nombre": "Programación Avanzada",
                "nrc": "12345",
                "profesor": "Juan Pérez",
                "rating_curso": 4.5,
                "rating_profesor": 4.8,
                "carga_academica": "Media"
            }
        }


class CourseListResponse(BaseModel):
    """Schema para la respuesta de una lista de cursos"""
    
    courses: List[CourseResponse] = Field(default_factory=list, description="Lista de cursos")
    count: int = Field(0, description="Número total de cursos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "courses": [
                    {
                        "_id": "507f1f77bcf86cd799439011",
                        "sigla": "IIC2233",
                        "nombre": "Programación Avanzada",
                        "nrc": "12345",
                        "profesor": "Juan Pérez",
                        "rating_curso": 4.5,
                        "rating_profesor": 4.8,
                        "carga_academica": "Media"
                    }
                ],
                "count": 1
            }
        }

