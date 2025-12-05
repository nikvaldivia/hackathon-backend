"""
Funciones para consultar y obtener datos de MongoDB

Esta colección trabaja EXCLUSIVAMENTE con la colección cursos_filtrados,
que contiene información limpia y filtrada por IA consolidada a partir
de otras colecciones de la base de datos.
"""
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from app.db_config import get_database
import logging

logger = logging.getLogger(__name__)

# Nombre de la colección principal
COLLECTION_NAME = "cursos_filtrados"


# ============================================================================
# FUNCIONES GENÉRICAS
# ============================================================================

async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    """
    Obtener una colección de MongoDB.
    
    Args:
        collection_name: Nombre de la colección
        
    Returns:
        AsyncIOMotorCollection: Colección de MongoDB
    """
    db = await get_database()
    return db[collection_name]


async def find_one(
    collection_name: str,
    filter_query: Dict[str, Any],
    projection: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Buscar un documento en una colección.
    
    Args:
        collection_name: Nombre de la colección
        filter_query: Query de filtro (ej: {"_id": "123"})
        projection: Campos a retornar (ej: {"nombre": 1, "email": 1})
        
    Returns:
        Dict con el documento encontrado o None
    """
    try:
        collection = await get_collection(collection_name)
        result = await collection.find_one(filter_query, projection)
        return result
    except Exception as e:
        logger.error(f"Error al buscar documento en {collection_name}: {e}")
        raise


async def find_many(
    collection_name: str,
    filter_query: Optional[Dict[str, Any]] = None,
    projection: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Buscar múltiples documentos en una colección.
    
    Args:
        collection_name: Nombre de la colección
        filter_query: Query de filtro (ej: {"status": "active"})
        projection: Campos a retornar
        sort: Lista de tuplas para ordenar (ej: [("fecha", -1)])
        limit: Límite de documentos a retornar
        skip: Número de documentos a saltar
        
    Returns:
        Lista de documentos encontrados
    """
    try:
        collection = await get_collection(collection_name)
        cursor = collection.find(filter_query or {}, projection)
        
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
            
        results = await cursor.to_list(length=limit or 1000)
        return results
    except Exception as e:
        logger.error(f"Error al buscar documentos en {collection_name}: {e}")
        raise


async def count_documents(
    collection_name: str,
    filter_query: Optional[Dict[str, Any]] = None
) -> int:
    """
    Contar documentos en una colección.
    
    Args:
        collection_name: Nombre de la colección
        filter_query: Query de filtro
        
    Returns:
        Número de documentos que coinciden con el filtro
    """
    try:
        collection = await get_collection(collection_name)
        count = await collection.count_documents(filter_query or {})
        return count
    except Exception as e:
        logger.error(f"Error al contar documentos en {collection_name}: {e}")
        raise


# ============================================================================
# FUNCIONES ESPECÍFICAS PARA CURSOS_FILTRADOS
# ============================================================================

async def get_course_by_id(course_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtener un curso por su ID.
    
    Args:
        course_id: ID del curso
        
    Returns:
        Dict con la información del curso o None
    """
    return await find_one(COLLECTION_NAME, {"_id": course_id})


async def get_course_by_nrc(nrc: str) -> Optional[Dict[str, Any]]:
    """
    Obtener un curso por su NRC.
    
    Args:
        nrc: NRC del curso (código específico por sección)
        
    Returns:
        Dict con la información del curso o None
    """
    return await find_one(COLLECTION_NAME, {"nrc": nrc})


async def get_courses_by_course_code(
    course_code: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener todos los cursos por sigla (course_code).
    
    Args:
        course_code: Sigla del curso (ej: "ICS1113", "IIC2233")
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos con esa sigla
    """
    return await find_many(COLLECTION_NAME, {"course_code": course_code}, sort=sort, limit=limit)


async def get_courses_by_course_name(
    course_name: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener cursos por nombre del curso.
    
    Args:
        course_name: Nombre del curso a buscar
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial (case-insensitive)
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos que coinciden con el nombre
    """
    if exact_match:
        filter_query = {"course_name": course_name}
    else:
        filter_query = {"course_name": {"$regex": course_name, "$options": "i"}}
    
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


async def get_courses_by_professor(
    professor_name: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener cursos por nombre del profesor.
    
    Args:
        professor_name: Nombre del profesor a buscar
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial (case-insensitive)
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos del profesor
    """
    if exact_match:
        filter_query = {"professor": professor_name}
    else:
        filter_query = {"professor": {"$regex": professor_name, "$options": "i"}}
    
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


async def get_courses_by_course_rating(
    min_rating: float,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener cursos con rating del curso mayor o igual al especificado.
    
    NOTA: Este campo no existe en el esquema actual. Esta función busca en professor_ratings.overall
    como alternativa. Considerar eliminar o ajustar según necesidades.
    
    Args:
        min_rating: Rating mínimo del curso (ej: 4.0)
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos con rating >= min_rating (basado en professor_ratings.overall)
    """
    # El esquema no tiene course_rating, usamos professor_ratings.overall como alternativa
    filter_query = {
        "professor_ratings": {
            "$elemMatch": {
                "overall": {"$gte": min_rating, "$ne": None}
            }
        }
    }
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


async def get_courses_by_professor_rating(
    min_rating: float,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener cursos con rating del profesor mayor o igual al especificado.
    
    Args:
        min_rating: Rating mínimo del profesor (ej: 4.0)
        sort: Ordenamiento opcional (recomendado: [("professor_ratings.overall", -1)] para mayor a menor)
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos con rating del profesor >= min_rating
    """
    filter_query = {
        "professor_ratings": {
            "$elemMatch": {
                "overall": {"$gte": min_rating, "$ne": None}
            }
        }
    }
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


async def get_courses_by_workload(
    workload_label: Optional[str] = None,
    min_workload_score: Optional[float] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener cursos por carga académica (workload).
    
    Args:
        workload_label: Etiqueta de carga académica (ej: "baja", "media", "intensa", "alta")
        min_workload_score: Score mínimo de carga académica (ej: 1-10)
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos que cumplen con los criterios de carga académica
    """
    filter_query = {}
    
    if workload_label:
        filter_query["workload"] = workload_label
    
    if min_workload_score is not None:
        filter_query["workload_score"] = {"$gte": min_workload_score}
    
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


async def get_courses_by_difficulty_level(
    difficulty_level: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Obtener cursos por nivel de dificultad.
    
    Args:
        difficulty_level: Nivel de dificultad (ej: "baja", "media", "alta")
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos con ese nivel de dificultad
    """
    filter_query = {"difficulty_level": difficulty_level}
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


async def get_all_courses(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener todos los cursos (o con filtros personalizados).
    
    Args:
        filter_query: Filtros opcionales personalizados
        sort: Ordenamiento (ej: [("course_rating", -1)])
        limit: Límite de resultados
        skip: Número de documentos a saltar (útil para paginación)
        
    Returns:
        Lista de cursos
    """
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit, skip=skip)


async def search_courses(
    course_code: Optional[str] = None,
    course_name: Optional[str] = None,
    professor_name: Optional[str] = None,
    nrc: Optional[str] = None,
    min_course_rating: Optional[float] = None,
    min_professor_rating: Optional[float] = None,
    workload_label: Optional[str] = None,
    min_workload_score: Optional[float] = None,
    difficulty_level: Optional[str] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = 50
) -> List[Dict[str, Any]]:
    """
    Búsqueda avanzada de cursos con múltiples criterios.
    
    Args:
        course_code: Sigla del curso
        course_name: Nombre del curso (búsqueda parcial)
        professor_name: Nombre del profesor (búsqueda parcial)
        nrc: NRC específico del curso
        min_course_rating: Rating mínimo del curso (usa professor_ratings.overall como alternativa)
        min_professor_rating: Rating mínimo del profesor
        workload_label: Etiqueta de carga académica
        min_workload_score: Score mínimo de carga académica
        difficulty_level: Nivel de dificultad
        sort: Ordenamiento opcional
        limit: Límite de resultados (default: 50)
        
    Returns:
        Lista de cursos que cumplen con todos los criterios especificados
    """
    filter_query = {}
    
    if course_code:
        filter_query["course_code"] = course_code
    if course_name:
        filter_query["course_name"] = {"$regex": course_name, "$options": "i"}
    if professor_name:
        filter_query["professor"] = {"$regex": professor_name, "$options": "i"}
    if nrc:
        filter_query["nrc"] = nrc
    # Manejar ratings: si ambos están especificados, usar el mayor
    if min_course_rating is not None or min_professor_rating is not None:
        min_rating = max(
            min_course_rating or 0,
            min_professor_rating or 0
        )
        filter_query["professor_ratings"] = {
            "$elemMatch": {
                "overall": {"$gte": min_rating, "$ne": None}
            }
        }
    if workload_label:
        filter_query["workload"] = workload_label
    if min_workload_score is not None:
        filter_query["workload_score"] = {"$gte": min_workload_score}
    if difficulty_level:
        filter_query["difficulty_level"] = difficulty_level
    
    return await find_many(COLLECTION_NAME, filter_query, sort=sort, limit=limit)


# ============================================================================
# FUNCIONES DE COMPATIBILIDAD (nombres antiguos para mantener compatibilidad)
# ============================================================================

async def get_curso_filtrado_by_id(curso_id: str) -> Optional[Dict[str, Any]]:
    """Compatibilidad: Usar get_course_by_id en su lugar."""
    return await get_course_by_id(curso_id)


async def get_curso_filtrado_by_nrc(nrc: str) -> Optional[Dict[str, Any]]:
    """Compatibilidad: Usar get_course_by_nrc en su lugar."""
    return await get_course_by_nrc(nrc)


async def get_cursos_filtrados_by_sigla(
    sigla: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_courses_by_course_code en su lugar."""
    return await get_courses_by_course_code(sigla, sort=sort, limit=limit or 50)


async def get_cursos_filtrados_by_nombre(
    nombre: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_courses_by_course_name en su lugar."""
    return await get_courses_by_course_name(nombre, exact_match=exact_match, sort=sort, limit=limit or 50)


async def get_cursos_filtrados_by_profesor(
    nombre_profesor: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_courses_by_professor en su lugar."""
    return await get_courses_by_professor(nombre_profesor, exact_match=exact_match, sort=sort, limit=limit or 50)


async def get_cursos_filtrados_by_rating_curso(
    rating_minimo: float,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_courses_by_course_rating en su lugar."""
    return await get_courses_by_course_rating(rating_minimo, sort=sort, limit=limit or 50)


async def get_cursos_filtrados_by_rating_profesor(
    rating_minimo: float,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_courses_by_professor_rating en su lugar."""
    return await get_courses_by_professor_rating(rating_minimo, sort=sort, limit=limit or 50)


async def get_cursos_filtrados_by_carga_academica(
    carga_academica: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_courses_by_workload en su lugar."""
    return await get_courses_by_workload(workload_label=carga_academica, sort=sort, limit=limit or 50)


async def get_all_cursos_filtrados(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar get_all_courses en su lugar."""
    return await get_all_courses(filter_query=filter_query, sort=sort, limit=limit, skip=skip)


async def search_cursos_filtrados(
    sigla: Optional[str] = None,
    nombre: Optional[str] = None,
    nombre_profesor: Optional[str] = None,
    nrc: Optional[str] = None,
    rating_curso_min: Optional[float] = None,
    rating_profesor_min: Optional[float] = None,
    carga_academica: Optional[str] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Compatibilidad: Usar search_courses en su lugar."""
    return await search_courses(
        course_code=sigla,
        course_name=nombre,
        professor_name=nombre_profesor,
        nrc=nrc,
        min_course_rating=rating_curso_min,
        min_professor_rating=rating_profesor_min,
        workload_label=carga_academica,
        sort=sort,
        limit=limit or 50
    )


# ============================================================================
# FUNCIONES PARA PROFESORES (extraídas de cursos_filtrados)
# ============================================================================

async def get_profesor_by_nombre(
    nombre: str,
    exact_match: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Obtener información de un profesor desde los cursos.
    
    NOTA: No hay una colección separada de profesores. Esta función busca
    el primer curso del profesor y extrae su información desde professor_ratings.
    
    Args:
        nombre: Nombre del profesor
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial (case-insensitive)
        
    Returns:
        Dict con información del profesor o None si no se encuentra
    """
    # Buscar un curso del profesor
    courses = await get_courses_by_professor(nombre, exact_match=exact_match, limit=1)
    
    if not courses:
        return None
    
    # Extraer información del profesor del primer curso
    course = courses[0]
    professor_name = course.get("professor")
    professor_ratings = course.get("professor_ratings", [])
    
    # Buscar el rating del profesor en professor_ratings
    professor_rating = None
    for rating in professor_ratings:
        if rating.get("name") == professor_name and rating.get("overall") is not None:
            professor_rating = rating.get("overall")
            break
    
    # Contar total de cursos del profesor
    all_courses = await get_courses_by_professor(nombre, exact_match=exact_match)
    total_cursos = len(all_courses)
    
    return {
        "_id": None,  # No hay ID único para profesores
        "nombre": professor_name,
        "rating_promedio": professor_rating,
        "total_cursos": total_cursos,
        "professor_ratings": professor_ratings
    }


async def get_profesor_by_id(profesor_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtener un profesor por su ID.
    
    NOTA: No hay una colección separada de profesores. Esta función retorna None.
    
    Args:
        profesor_id: ID del profesor
        
    Returns:
        None (no hay colección de profesores)
    """
    return None


async def get_all_profesores(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener todos los profesores.
    
    NOTA: No hay una colección separada de profesores. Esta función retorna una lista vacía.
    
    Args:
        filter_query: Filtros opcionales (no aplica)
        sort: Ordenamiento opcional (no aplica)
        limit: Límite de resultados (no aplica)
        
    Returns:
        Lista vacía (no hay colección de profesores)
    """
    return []


