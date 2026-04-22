from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Copywriting API is running"}


def test_generate_copywriting_endpoint() -> None:
    response = client.post(
        "/api/v1/copywriting/generate",
        json={
            "platform": "xiaohongshu",
            "topic": "春季护肤",
            "tone": "natural",
            "keywords": ["保湿", "敏感肌"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "xiaohongshu"
    assert "小红书风格" in data["content"]


def test_generate_copywriting_unsupported_platform() -> None:
    response = client.post(
        "/api/v1/copywriting/generate",
        json={
            "platform": "other",
            "topic": "春季护肤",
            "tone": "natural",
            "keywords": ["保湿"],
        },
    )
    assert response.status_code == 422
