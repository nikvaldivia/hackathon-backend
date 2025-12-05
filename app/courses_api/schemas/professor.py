"""
Schemas para profesores
"""
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class ProfessorResponse(BaseModel):
    """Schema para la respuesta de un profesor"""
    
    id: Optional[str] = Field(None, alias="_id", description="ID del profesor")
    nombre: Optional[str] = Field(None, description="Nombre del profesor")
    email: Optional[str] = Field(None, description="Email del profesor")
    departamento: Optional[str] = Field(None, description="Departamento")
    rating_promedio: Optional[float] = Field(None, description="Rating promedio del profesor")
    total_cursos: Optional[int] = Field(None, description="Total de cursos dictados")
    
    # Campos adicionales que pueden existir
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "nombre": "Juan Pérez",
                "email": "juan.perez@universidad.cl",
                "departamento": "Ingeniería",
                "rating_promedio": 4.5,
                "total_cursos": 10
            }
        }


class ProfessorListResponse(BaseModel):
    """Schema para la respuesta de una lista de profesores"""
    
    professors: List[ProfessorResponse] = Field(default_factory=list, description="Lista de profesores")
    count: int = Field(0, description="Número total de profesores")
    
    class Config:
        json_schema_extra = {
            "example": {
                "professors": [
                    {
                        "_id": "507f1f77bcf86cd799439011",
                        "nombre": "Juan Pérez",
                        "email": "juan.perez@universidad.cl",
                        "departamento": "Ingeniería",
                        "rating_promedio": 4.5,
                        "total_cursos": 10
                    }
                ],
                "count": 1
            }
        }

