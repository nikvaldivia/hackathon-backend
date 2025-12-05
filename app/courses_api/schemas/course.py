"""
Schemas para cursos basados en el esquema real de la base de datos
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ScheduleItem(BaseModel):
    """Schema para un item del horario"""
    type: str = Field(..., description="Tipo de clase (CLAS, AYU, TAL, etc.)")
    day: str = Field(..., description="Día de la semana (L, M, W, J, V, S)")
    module: int = Field(..., description="Módulo/hora de la clase")
    room: str = Field(..., description="Sala donde se imparte la clase")
    
    class Config:
        extra = "ignore"


class ProfessorRating(BaseModel):
    """Schema para el rating de un profesor"""
    name: str = Field(..., description="Nombre del profesor")
    overall: Optional[float] = Field(None, description="Rating general del profesor")
    summary: Optional[str] = Field(None, description="Resumen de comentarios sobre el profesor")
    
    class Config:
        extra = "ignore"


class CourseResponse(BaseModel):
    """Schema para la respuesta de un curso"""
    
    nrc: str = Field(..., description="NRC (código único por sección)")
    course_code: str = Field(..., description="Sigla del curso (ej: ICS1113)")
    course_name: str = Field(..., description="Nombre del curso")
    section: Optional[int] = Field(None, description="Número de sección")
    professor: str = Field(..., description="Nombre del profesor")
    campus: Optional[str] = Field(None, description="Campus donde se imparte")
    format: Optional[str] = Field(None, description="Formato (Presencial, Online, etc.)")
    credits: Optional[int] = Field(None, description="Créditos del curso")
    total_slots: Optional[int] = Field(None, description="Total de cupos disponibles")
    available_slots: Optional[int] = Field(None, description="Cupos disponibles")
    schedule: List[ScheduleItem] = Field(default_factory=list, description="Horario del curso")
    requirements: List[str] = Field(default_factory=list, description="Requisitos del curso")
    semester: Optional[str] = Field(None, description="Semestre")
    professor_ratings: List[ProfessorRating] = Field(default_factory=list, description="Ratings del profesor")
    difficulty_level: Optional[str] = Field(None, description="Nivel de dificultad (baja, media, alta)")
    workload_score: Optional[int] = Field(None, description="Score de carga académica (1-10)")
    workload: Optional[str] = Field(None, description="Carga académica (baja, media, intensa, alta)")
    exam_dates: List[str] = Field(default_factory=list, description="Fechas de exámenes")
    pros: List[str] = Field(default_factory=list, description="Aspectos positivos del curso")
    cons: List[str] = Field(default_factory=list, description="Aspectos negativos del curso")
    overall_summary: Optional[str] = Field(None, description="Resumen general del curso")
    representative_comments: List[str] = Field(default_factory=list, description="Comentarios representativos")
    last_updated: Optional[str] = Field(None, description="Fecha de última actualización")
    
    class Config:
        populate_by_name = True
        # Permitir campos extra del documento que no estén en el schema
        extra = "ignore"
        json_schema_extra = {
            "example": {
                "nrc": "12489",
                "course_code": "ICS1113",
                "course_name": "Optimización",
                "section": 1,
                "professor": "Klapp Mathias",
                "campus": "San Joaquín",
                "format": "Presencial",
                "credits": 10,
                "total_slots": 141,
                "available_slots": 6,
                "schedule": [
                    {
                        "type": "CLAS",
                        "day": "L",
                        "module": 3,
                        "room": "K203"
                    }
                ],
                "requirements": [],
                "semester": "",
                "professor_ratings": [
                    {
                        "name": "Klapp Mathias",
                        "overall": None,
                        "summary": "Los comentarios indican que el profesor Klapp explica muy bien..."
                    }
                ],
                "difficulty_level": "media",
                "workload_score": 7,
                "workload": "intensa",
                "exam_dates": [],
                "pros": ["El profesor explica muy bien los conceptos"],
                "cons": [],
                "overall_summary": "El curso de Optimización...",
                "representative_comments": ["Klapp explica muy bien"],
                "last_updated": "2025-12-05T13:51:27.729342"
            }
        }


class CourseListResponse(BaseModel):
    """Schema para la respuesta de una lista de cursos"""
    
    courses: List[CourseResponse] = Field(default_factory=list, description="Lista de cursos")
    count: int = Field(0, description="Número total de cursos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "courses": [],
                "count": 0
            }
        }
