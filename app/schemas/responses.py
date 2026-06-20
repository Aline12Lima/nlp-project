from pydantic import BaseModel

class SentimentResponse(BaseModel):
    text: str
    label: str
    score: float