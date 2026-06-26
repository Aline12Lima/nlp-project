from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"

    # Modelos HuggingFace
    HF_MODEL_SENTIMENT: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    HF_MODEL_NER: str = "dbmdz/bert-large-cased-finetuned-conll03-english"
    HF_MODEL_TRANSLATION: str = "Helsinki-NLP/opus-mt-tc-big-en-pt"
    HF_MODEL_EMBEDDINGS: str = "sentence-transformers/all-MiniLM-L6-v2"
    HF_CACHE_DIR: str = "./models"

    class Config:
        env_file = ".env"


settings = Settings()