from fastapi import APIRouter, HTTPException
from app.services.redis_service import get_stats, clear_cache

router = APIRouter()


@router.get("/stats")
def cache_stats():
    try:
        return get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
def cache_clear():
    try:
        deleted = clear_cache()
        return {"deleted_keys": deleted, "status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))