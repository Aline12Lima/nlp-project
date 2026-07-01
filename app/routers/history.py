from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.services.history_service import get_history

router = APIRouter()


@router.get("/")
def list_history(
    limit: int = Query(10, ge=1, le=100),
    operation: Optional[str] = None,
    db: Session = Depends(get_db),
):
    entries = get_history(db, limit=limit, operation=operation)
    return [
        {
            "id": e.id,
            "operation": e.operation,
            "input_text": e.input_text,
            "result": e.result,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in entries
    ]