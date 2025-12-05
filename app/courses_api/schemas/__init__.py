"""
Schemas para la funcionalidad de API de cursos
"""
from app.courses_api.schemas.course import CourseResponse, CourseListResponse
from app.courses_api.schemas.professor import ProfessorResponse, ProfessorListResponse

__all__ = [
    "CourseResponse",
    "CourseListResponse",
    "ProfessorResponse",
    "ProfessorListResponse",
]
