from fastapi import APIRouter, HTTPException
from app.schemas.requests import TextRequest, TranslationRequest
from app.schemas.responses import (
    SentimentResponse,
    NERResponse,
    EntityResponse,
    TranslationResponse,
    EmbeddingResponse,
)
from app.models.hf_loader import (
    get_sentiment_model,
    get_ner_model,
    get_translation_model,
    get_embeddings_model,
)

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

@router.post("/ner", response_model=NERResponse)
def extract_entities(body: TextRequest):
    try:
        model = get_ner_model()
        results = model(body.text)
        entities = [
            EntityResponse(
                word=r["word"],
                entity=r["entity_group"],
                score=round(r["score"], 4),
                start=r["start"],
                end=r["end"],
            )
            for r in results
        ]
        return NERResponse(text=body.text, entities=entities)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/translate", response_model=TranslationResponse)
def translate_text(body: TranslationRequest):
    try:
        model = get_translation_model()
        result = model(body.text)[0]
        return TranslationResponse(
            original=body.text,
            translated=result["translation_text"],
            source="en",
            target="pt",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embeddings", response_model=EmbeddingResponse)
def generate_embeddings(body: TextRequest):
    try:
        model = get_embeddings_model()
        vector = model.encode(body.text).tolist()
        return EmbeddingResponse(
            text=body.text,
            embedding=vector,
            dimensions=len(vector),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))