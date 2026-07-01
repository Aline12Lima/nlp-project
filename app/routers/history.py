from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.services.history_service import get_history

router = APIRouter()


@router.get(
    "/",
    summary="Lista o histórico de operações NLP",
    responses={200: {"description": "Histórico retornado com sucesso"}},
)
def list_history(
    limit: int = Query(10, ge=1, le=100, description="Quantidade de registros (1 a 100)"),
    operation: Optional[str] = Query(
        None,
        description="Filtra por tipo de operação (sentiment, ner, translate, embeddings)"
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna as últimas operações NLP realizadas, em ordem cronológica reversa
    (mais recentes primeiro).

    ### Casos de uso
    - Auditoria: rastrear o que foi processado e quando
    - Debug: identificar chamadas problemáticas
    - Análise: entender padrões de uso da API
    - Compliance: manter registro para regulamentações

    ### Estrutura de cada registro
    - `id`: identificador único auto-incrementado
    - `operation`: tipo da operação (sentiment/ner/translate/embeddings)
    - `input_text`: texto processado
    - `result`: resultado completo em JSON
    - `created_at`: timestamp com timezone
    """
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