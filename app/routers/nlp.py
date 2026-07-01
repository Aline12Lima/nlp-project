from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
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
from app.database.connection import get_db
from app.services.history_service import save_history
from app.services.redis_service import get_cached, set_cached

router = APIRouter()


@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(body: TextRequest, db: Session = Depends(get_db)):
    try:
        # Tenta cache primeiro
        cached = get_cached("sentiment", body.text)
        if cached:
            return SentimentResponse(**cached)

        model = get_sentiment_model()
        result = model(body.text)[0]
        response = SentimentResponse(
            text=body.text,
            label=result["label"],
            score=round(result["score"], 4),
        )

        # Salva em cache e no histórico
        set_cached("sentiment", body.text, response.model_dump())
        save_history(db, "sentiment", body.text, response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ner", response_model=NERResponse)
def extract_entities(body: TextRequest, db: Session = Depends(get_db)):
    try:
        cached = get_cached("ner", body.text)
        if cached:
            return NERResponse(**cached)

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
        response = NERResponse(text=body.text, entities=entities)

        set_cached("ner", body.text, response.model_dump())
        save_history(db, "ner", body.text, response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslationResponse)
def translate_text(body: TranslationRequest, db: Session = Depends(get_db)):
    try:
        cached = get_cached("translate", body.text)
        if cached:
            return TranslationResponse(**cached)

        model = get_translation_model()
        result = model(body.text)[0]
        response = TranslationResponse(
            original=body.text,
            translated=result["translation_text"],
            source="en",
            target="pt",
        )

        set_cached("translate", body.text, response.model_dump())
        save_history(db, "translate", body.text, response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings", response_model=EmbeddingResponse)
def generate_embeddings(body: TextRequest, db: Session = Depends(get_db)):
    try:
        # Embeddings não usam cache (vetor é grande e pouco reutilizado)
        model = get_embeddings_model()
        vector = model.encode(body.text).tolist()
        response = EmbeddingResponse(
            text=body.text,
            embedding=vector,
            dimensions=len(vector),
        )
        save_history(db, "embeddings", body.text, {"dimensions": len(vector)})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))