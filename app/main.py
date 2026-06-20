from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import health, nlp
from app.config import settings
from app.models.hf_loader import get_sentiment_model
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pré-carrega o modelo ao subir a API
    get_sentiment_model()
    yield

app = FastAPI(
    title="NLP Portfolio API",
    description="Pipeline de NLP com modelos HuggingFace",
    version=settings.APP_VERSION,
    docs_url="/docs",
    lifespan=lifespan,
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(nlp.router, prefix="/nlp", tags=["nlp"])

@app.get("/")
def root():
    return {"message": "NLP Portfolio API", "version": settings.APP_VERSION}