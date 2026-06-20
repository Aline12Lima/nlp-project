from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    HF_MODEL_SENTIMENT: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    HF_CACHE_DIR: str = "./models"

    class Config:
        env_file = ".env"

settings = Settings()