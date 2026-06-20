from fastapi import APIRouter, HTTPException
from app.schemas.requests import TextRequest
from app.schemas.responses import SentimentResponse
from app.models.hf_loader import get_sentiment_model

router = APIRouter()

@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(body: TextRequest):
    try:
        model = get_sentiment_model()
        result = model(body.text)[0]
        return SentimentResponse(
            text=body.text,
            label=result["label"],
            score=round(result["score"], 4),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))