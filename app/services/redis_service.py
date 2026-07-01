import redis
import json
import hashlib
from app.config import settings
import logging

logger = logging.getLogger(__name__)

_redis_client = None


def get_redis_client():
    """Retorna cliente Redis singleton."""
    global _redis_client
    if _redis_client is None:
        logger.info("Conectando ao Redis...")
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
        _redis_client.ping()
        logger.info("Redis conectado.")
    return _redis_client


def _make_cache_key(operation: str, text: str) -> str:
    """Gera chave de cache baseada em operação e hash do texto."""
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
    return f"cache:{operation}:{text_hash}"


def get_cached(operation: str, text: str):
    """Busca resultado em cache. Retorna None se não existir."""
    client = get_redis_client()
    key = _make_cache_key(operation, text)
    cached = client.get(key)
    if cached:
        logger.info(f"Cache HIT: {key}")
        return json.loads(cached)
    logger.info(f"Cache MISS: {key}")
    return None


def set_cached(operation: str, text: str, result: dict, ttl_seconds: int = 3600):
    """Salva resultado em cache com tempo de expiração (padrão: 1 hora)."""
    client = get_redis_client()
    key = _make_cache_key(operation, text)
    client.setex(key, ttl_seconds, json.dumps(result))


def get_stats() -> dict:
    """Retorna estatísticas do cache."""
    client = get_redis_client()
    info = client.info("stats")
    keys_count = client.dbsize()
    return {
        "total_keys": keys_count,
        "cache_hits": info.get("keyspace_hits", 0),
        "cache_misses": info.get("keyspace_misses", 0),
        "hit_rate": round(
            info.get("keyspace_hits", 0) / max(1, info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0)) * 100,
            2
        ),
    }


def clear_cache() -> int:
    """Limpa todo o cache. Retorna quantidade de chaves apagadas."""
    client = get_redis_client()
    keys = client.keys("cache:*")
    if keys:
        client.delete(*keys)
    return len(keys)