from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import health, nlp, rag, history, cache
from app.config import settings
from app.models.hf_loader import (
    get_sentiment_model,
    get_ner_model,
    get_translation_model,
    get_embeddings_model,
)
from app.services.chroma_service import get_chroma_client
from app.services.redis_service import get_redis_client
from app.database.connection import engine
from app.database.models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Criando tabelas no PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas prontas.")

    get_sentiment_model()
    get_ner_model()
    get_translation_model()
    get_embeddings_model()
    get_chroma_client()
    get_redis_client()
    yield


app = FastAPI(
    title="NLP Portfolio API",
    description="Pipeline de NLP com modelos HuggingFace + RAG + cache Redis",
    version=settings.APP_VERSION,
    docs_url="/docs",
    lifespan=lifespan,
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(nlp.router, prefix="/nlp", tags=["nlp"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(history.router, prefix="/history", tags=["history"])
app.include_router(cache.router, prefix="/cache", tags=["cache"])


@app.get("/")
def root():
    return {"message": "NLP Portfolio API", "version": settings.APP_VERSION}