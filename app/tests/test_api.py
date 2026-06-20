import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_health():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sentiment_positive():
    mock_result = [{"label": "positive", "score": 0.98}]
    with patch("app.routers.nlp.get_sentiment_model") as mock_model:
        mock_model.return_value = MagicMock(return_value=mock_result)
        response = client.post(
            "/nlp/sentiment",
            json={"text": "I love this!"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "positive"
    assert data["score"] == 0.98


def test_sentiment_negative():
    mock_result = [{"label": "negative", "score": 0.94}]
    with patch("app.routers.nlp.get_sentiment_model") as mock_model:
        mock_model.return_value = MagicMock(return_value=mock_result)
        response = client.post(
            "/nlp/sentiment",
            json={"text": "I hate this!"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "negative"


def test_sentiment_empty_text():
    mock_result = [{"label": "neutral", "score": 0.5}]
    with patch("app.routers.nlp.get_sentiment_model") as mock_model:
        mock_model.return_value = MagicMock(return_value=mock_result)
        response = client.post(
            "/nlp/sentiment",
            json={"text": ""}
        )
    assert response.status_code == 200


def test_sentiment_missing_field():
    response = client.post("/nlp/sentiment", json={})
    assert response.status_code == 422