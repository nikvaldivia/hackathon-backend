"""
Funciones para consultar MongoDB

Este módulo trabaja EXCLUSIVAMENTE con la colección cursos_filtrados.
"""
# Exportar funciones de queries para fácil acceso
from app.database.queries import (
    # Funciones genéricas
    get_collection,
    find_one,
    find_many,
    count_documents,
    # Funciones nuevas (recomendadas)
    get_course_by_id,
    get_course_by_nrc,
    get_courses_by_course_code,
    get_courses_by_course_name,
    get_courses_by_professor,
    get_courses_by_course_rating,
    get_courses_by_professor_rating,
    get_courses_by_workload,
    get_courses_by_difficulty_level,
    get_all_courses,
    search_courses,
    # Funciones de compatibilidad (nombres antiguos)
    get_curso_filtrado_by_id,
    get_curso_filtrado_by_nrc,
    get_cursos_filtrados_by_sigla,
    get_cursos_filtrados_by_nombre,
    get_cursos_filtrados_by_profesor,
    get_cursos_filtrados_by_rating_curso,
    get_cursos_filtrados_by_rating_profesor,
    get_cursos_filtrados_by_carga_academica,
    get_all_cursos_filtrados,
    search_cursos_filtrados,
    # Funciones para profesores (extraídas de cursos_filtrados)
    get_profesor_by_id,
    get_profesor_by_nombre,
    get_all_profesores,
)
