from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database.connection import Base


class NLPHistory(Base):
    __tablename__ = "nlp_history"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String(50), nullable=False, index=True)
    input_text = Column(Text, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())