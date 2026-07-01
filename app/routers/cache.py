from fastapi import APIRouter, HTTPException

from app.services.redis_service import clear_cache, get_stats

router = APIRouter()


@router.get(
    "/stats",
    summary="Estatísticas do cache Redis",
    responses={
        200: {"description": "Métricas do cache"},
        500: {"description": "Erro ao acessar o Redis"},
    },
)
def cache_stats():
    """
    Retorna métricas em tempo real do cache Redis.

    ### Campos retornados
    - `total_keys`: quantidade de chaves atualmente armazenadas
    - `cache_hits`: total de acertos (respostas servidas do cache)
    - `cache_misses`: total de misses (chamadas que rodaram o modelo)
    - `hit_rate`: percentual de acertos (0 a 100)

    ### Interpretação
    Uma **hit rate alta** (>70%) indica bom aproveitamento do cache.
    Uma taxa baixa pode significar textos muito variados ou TTL curto demais.
    """
    try:
        return get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete(
    "/clear",
    summary="Limpa todo o cache",
    responses={
        200: {"description": "Cache limpo com sucesso"},
        500: {"description": "Erro ao limpar o cache"},
    },
)
def cache_clear():
    """
    Remove **todas as chaves** de cache do Redis (padrão `cache:*`).

    ### Quando usar
    - Após atualizar um modelo (invalidar respostas antigas)
    - Em testes para garantir estado limpo
    - Para forçar recomputação em desenvolvimento

    ### Retorno
    Quantidade de chaves apagadas.
    """
    try:
        deleted = clear_cache()
        return {"deleted_keys": deleted, "status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
