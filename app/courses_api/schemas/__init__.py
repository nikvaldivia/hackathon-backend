"""
Schemas para la funcionalidad de API de cursos
"""
from app.courses_api.schemas.course import (
    CourseResponse,
    CourseListResponse,
    ScheduleItem,
    ProfessorRating,
)

__all__ = [
    "CourseResponse",
    "CourseListResponse",
    "ScheduleItem",
    "ProfessorRating",
]
