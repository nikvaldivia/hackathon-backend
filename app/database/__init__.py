"""
Funciones para consultar MongoDB
"""
# Exportar funciones de queries para fácil acceso
from app.database.queries import (
    # Funciones genéricas
    get_collection,
    find_one,
    find_many,
    count_documents,
    # Funciones para cursos_filtrados (PRINCIPAL)
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
    # Funciones para cursos_scrapeados
    get_curso_scrapeado_by_id,
    get_curso_scrapeado_by_nrc,
    get_cursos_scrapeados_by_sigla,
    get_all_cursos_scrapeados,
    # Funciones para programas_cursos
    get_programa_by_id,
    get_programa_by_sigla,
    get_programa_by_nrc,
    get_all_programas,
    # Funciones para comentarios_cursos
    get_comentario_by_id,
    get_comentarios_by_sigla,
    get_comentarios_by_nrc,
    get_comentarios_by_profesor,
    get_all_comentarios,
    # Funciones para profesores
    get_profesor_by_id,
    get_profesor_by_nombre,
    get_all_profesores,
)
