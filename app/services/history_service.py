from sqlalchemy.orm import Session

from app.database.models import NLPHistory


def save_history(db: Session, operation: str, input_text: str, result: dict) -> NLPHistory:
    entry = NLPHistory(
        operation=operation,
        input_text=input_text,
        result=result,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_history(db: Session, limit: int = 10, operation: str = None):
    query = db.query(NLPHistory)
    if operation:
        query = query.filter(NLPHistory.operation == operation)
    return query.order_by(NLPHistory.created_at.desc()).limit(limit).all()
