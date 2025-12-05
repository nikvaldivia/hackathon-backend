"""
Funciones para consultar y obtener datos de MongoDB

Colecciones disponibles:
- cursos_filtrados: Información limpia filtrada por IA (PRINCIPAL)
- cursos_scrapeados: Información scrapeada de los cursos
- programas_cursos: Programa de los cursos
- comentarios_cursos: Comentarios scrapeados sobre los cursos
"""
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from app.db_config import get_database
import logging

logger = logging.getLogger(__name__)


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
# FUNCIONES ESPECÍFICAS PARA CURSOS_FILTRADOS (COLECCIÓN PRINCIPAL)
# ============================================================================

async def get_curso_filtrado_by_id(curso_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtener un curso filtrado por su ID.
    
    Args:
        curso_id: ID del curso
        
    Returns:
        Dict con la información del curso filtrado o None
    """
    return await find_one("cursos_filtrados", {"_id": curso_id})


async def get_curso_filtrado_by_nrc(nrc: str) -> Optional[Dict[str, Any]]:
    """
    Obtener un curso filtrado por su NRC.
    
    Args:
        nrc: NRC del curso (código específico por sección)
        
    Returns:
        Dict con la información del curso filtrado o None
    """
    return await find_one("cursos_filtrados", {"nrc": nrc})


async def get_cursos_filtrados_by_sigla(
    sigla: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener todos los cursos filtrados por sigla.
    
    Args:
        sigla: Sigla del curso (ej: "IIC2233")
        sort: Ordenamiento opcional
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados con esa sigla
    """
    return await find_many("cursos_filtrados", {"sigla": sigla}, sort=sort, limit=limit)


async def get_cursos_filtrados_by_nombre(
    nombre: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener cursos filtrados por nombre.
    
    Args:
        nombre: Nombre del curso a buscar
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial (case-insensitive)
        sort: Ordenamiento opcional
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados que coinciden con el nombre
    """
    if exact_match:
        filter_query = {"nombre": nombre}
    else:
        filter_query = {"nombre": {"$regex": nombre, "$options": "i"}}
    
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit)


async def get_cursos_filtrados_by_profesor(
    nombre_profesor: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener cursos filtrados por nombre del profesor.
    
    Args:
        nombre_profesor: Nombre del profesor a buscar
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial (case-insensitive)
        sort: Ordenamiento opcional
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados del profesor
    """
    if exact_match:
        filter_query = {"profesor": nombre_profesor}
    else:
        filter_query = {"profesor": {"$regex": nombre_profesor, "$options": "i"}}
    
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit)


async def get_cursos_filtrados_by_rating_curso(
    rating_minimo: float,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener cursos filtrados con rating del curso mayor o igual al especificado.
    
    Args:
        rating_minimo: Rating mínimo del curso (ej: 4.0)
        sort: Ordenamiento opcional (recomendado: [("rating_curso", -1)] para mayor a menor)
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados con rating >= rating_minimo
    """
    filter_query = {"rating_curso": {"$gte": rating_minimo}}
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit)


async def get_cursos_filtrados_by_rating_profesor(
    rating_minimo: float,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener cursos filtrados con rating del profesor mayor o igual al especificado.
    
    Args:
        rating_minimo: Rating mínimo del profesor (ej: 4.0)
        sort: Ordenamiento opcional (recomendado: [("rating_profesor", -1)] para mayor a menor)
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados con rating del profesor >= rating_minimo
    """
    filter_query = {"rating_profesor": {"$gte": rating_minimo}}
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit)


async def get_cursos_filtrados_by_carga_academica(
    carga_academica: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener cursos filtrados por carga académica.
    
    Args:
        carga_academica: Carga académica del curso (ej: "Baja", "Media", "Alta")
        sort: Ordenamiento opcional
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados con esa carga académica
    """
    filter_query = {"carga_academica": carga_academica}
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit)


async def get_all_cursos_filtrados(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener todos los cursos filtrados (o con filtros personalizados).
    
    Args:
        filter_query: Filtros opcionales personalizados
        sort: Ordenamiento (ej: [("rating_curso", -1)])
        limit: Límite de resultados
        skip: Número de documentos a saltar (útil para paginación)
        
    Returns:
        Lista de cursos filtrados
    """
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit, skip=skip)


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
    """
    Búsqueda avanzada de cursos filtrados con múltiples criterios.
    
    Args:
        sigla: Sigla del curso
        nombre: Nombre del curso (búsqueda parcial)
        nombre_profesor: Nombre del profesor (búsqueda parcial)
        nrc: NRC específico del curso
        rating_curso_min: Rating mínimo del curso
        rating_profesor_min: Rating mínimo del profesor
        carga_academica: Carga académica
        sort: Ordenamiento opcional
        limit: Límite de resultados
        
    Returns:
        Lista de cursos filtrados que cumplen con todos los criterios especificados
    """
    filter_query = {}
    
    if sigla:
        filter_query["sigla"] = sigla
    if nombre:
        filter_query["nombre"] = {"$regex": nombre, "$options": "i"}
    if nombre_profesor:
        filter_query["profesor"] = {"$regex": nombre_profesor, "$options": "i"}
    if nrc:
        filter_query["nrc"] = nrc
    if rating_curso_min is not None:
        filter_query["rating_curso"] = {"$gte": rating_curso_min}
    if rating_profesor_min is not None:
        filter_query["rating_profesor"] = {"$gte": rating_profesor_min}
    if carga_academica:
        filter_query["carga_academica"] = carga_academica
    
    return await find_many("cursos_filtrados", filter_query, sort=sort, limit=limit)


# ============================================================================
# FUNCIONES PARA CURSOS_SCRAPEADOS
# ============================================================================

async def get_curso_scrapeado_by_id(curso_id: str) -> Optional[Dict[str, Any]]:
    """Obtener un curso scrapeado por su ID."""
    return await find_one("cursos_scrapeados", {"_id": curso_id})


async def get_curso_scrapeado_by_nrc(nrc: str) -> Optional[Dict[str, Any]]:
    """Obtener un curso scrapeado por su NRC."""
    return await find_one("cursos_scrapeados", {"nrc": nrc})


async def get_cursos_scrapeados_by_sigla(
    sigla: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener todos los cursos scrapeados por sigla."""
    return await find_many("cursos_scrapeados", {"sigla": sigla}, sort=sort, limit=limit)


async def get_all_cursos_scrapeados(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener todos los cursos scrapeados (o con filtros personalizados)."""
    return await find_many("cursos_scrapeados", filter_query, sort=sort, limit=limit)


# ============================================================================
# FUNCIONES PARA PROGRAMAS_CURSOS
# ============================================================================

async def get_programa_by_id(programa_id: str) -> Optional[Dict[str, Any]]:
    """Obtener un programa de curso por su ID."""
    return await find_one("programas_cursos", {"_id": programa_id})


async def get_programa_by_sigla(
    sigla: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener programas de cursos por sigla."""
    return await find_many("programas_cursos", {"sigla": sigla}, sort=sort, limit=limit)


async def get_programa_by_nrc(nrc: str) -> Optional[Dict[str, Any]]:
    """Obtener un programa de curso por NRC."""
    return await find_one("programas_cursos", {"nrc": nrc})


async def get_all_programas(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener todos los programas de cursos (o con filtros personalizados)."""
    return await find_many("programas_cursos", filter_query, sort=sort, limit=limit)


# ============================================================================
# FUNCIONES PARA COMENTARIOS_CURSOS
# ============================================================================

async def get_comentario_by_id(comentario_id: str) -> Optional[Dict[str, Any]]:
    """Obtener un comentario por su ID."""
    return await find_one("comentarios_cursos", {"_id": comentario_id})


async def get_comentarios_by_sigla(
    sigla: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener comentarios de cursos por sigla."""
    return await find_many("comentarios_cursos", {"sigla": sigla}, sort=sort, limit=limit)


async def get_comentarios_by_nrc(
    nrc: str,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener comentarios de un curso específico por NRC."""
    return await find_many("comentarios_cursos", {"nrc": nrc}, sort=sort, limit=limit)


async def get_comentarios_by_profesor(
    nombre_profesor: str,
    exact_match: bool = False,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener comentarios de cursos por nombre del profesor.
    
    Args:
        nombre_profesor: Nombre del profesor
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial
        sort: Ordenamiento opcional
        limit: Límite de resultados
    """
    if exact_match:
        filter_query = {"profesor": nombre_profesor}
    else:
        filter_query = {"profesor": {"$regex": nombre_profesor, "$options": "i"}}
    
    return await find_many("comentarios_cursos", filter_query, sort=sort, limit=limit)


async def get_all_comentarios(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Obtener todos los comentarios (o con filtros personalizados)."""
    return await find_many("comentarios_cursos", filter_query, sort=sort, limit=limit)


# ============================================================================
# FUNCIONES PARA PROFESORES
# ============================================================================

async def get_profesor_by_id(profesor_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtener un profesor por su ID.
    
    Args:
        profesor_id: ID del profesor
        
    Returns:
        Dict con la información del profesor o None
    """
    return await find_one("profesores", {"_id": profesor_id})


async def get_profesor_by_nombre(
    nombre: str,
    exact_match: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Obtener un profesor por su nombre.
    
    Args:
        nombre: Nombre del profesor
        exact_match: Si True, busca coincidencia exacta; si False, busca parcial (case-insensitive)
        
    Returns:
        Dict con la información del profesor o None
    """
    if exact_match:
        filter_query = {"nombre": nombre}
    else:
        filter_query = {"nombre": {"$regex": nombre, "$options": "i"}}
    
    return await find_one("profesores", filter_query)


async def get_all_profesores(
    filter_query: Optional[Dict[str, Any]] = None,
    sort: Optional[List[tuple]] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtener todos los profesores (o con filtros personalizados).
    
    Args:
        filter_query: Filtros opcionales personalizados
        sort: Ordenamiento opcional
        limit: Límite de resultados
        
    Returns:
        Lista de profesores
    """
    return await find_many("profesores", filter_query, sort=sort, limit=limit)
