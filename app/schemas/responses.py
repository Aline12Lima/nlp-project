from pydantic import BaseModel
from typing import List

class SentimentResponse(BaseModel):
    text: str
    label: str
    score: float

class EntityResponse(BaseModel):
    word: str
    entity: str
    score: float
    start: int
    end: int

class NERResponse(BaseModel):
    text: str
    entities: List[EntityResponse]

class TranslationResponse(BaseModel):
    original: str
    translated: str
    source: str
    target: str

class EmbeddingResponse(BaseModel):
    text: str
    embedding: List[float]
    dimensions: int