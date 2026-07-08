import logging

from sentence_transformers import SentenceTransformer
from transformers import pipeline

from app.config import settings

logger = logging.getLogger(__name__)

_models: dict = {}


def get_sentiment_model():
    if "sentiment" not in _models:
        logger.info("Carregando modelo de sentimento...")
        _models["sentiment"] = pipeline(
            "sentiment-analysis",
            model=settings.HF_MODEL_SENTIMENT,
        )
        logger.info("Sentimento carregado.")
    return _models["sentiment"]


def get_ner_model():
    if "ner" not in _models:
        logger.info("Carregando modelo NER...")
        _models["ner"] = pipeline(
            "ner",
            model=settings.HF_MODEL_NER,
            aggregation_strategy="simple",
        )
        logger.info("NER carregado.")
    return _models["ner"]


def get_translation_model():
    if "translation" not in _models:
        logger.info("Carregando modelo de tradução...")
        _models["translation"] = pipeline(
            "translation",
            model=settings.HF_MODEL_TRANSLATION,
        )
        logger.info("Tradução carregada.")
    return _models["translation"]


def get_embeddings_model():
    if "embeddings" not in _models:
        logger.info("Carregando modelo de embeddings...")
        _models["embeddings"] = SentenceTransformer(
            settings.HF_MODEL_EMBEDDINGS,
        )
        logger.info("Embeddings carregado.")
    return _models["embeddings"]
