from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "running" in response.json()["message"]


def test_prediction():
    payload = {
        "age": 24,
        "gender": "Male",
        "location": "USA",
        "game_genre": "Action",
        "game_difficulty": "Medium",
        "sessions_per_week": 12,
        "avg_session_duration_minutes": 70,
        "player_level": 25,
        "achievements_unlocked": 30,
        "total_events": 1500,
        "days_since_last_seen": 3,
        "account_age_days": 120
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "purchase_prediction" in data
    assert "purchase_probability" in data
    assert data["purchase_prediction"] in [0, 1]
    assert 0 <= data["purchase_probability"] <= 1


def test_invalid_age():
    payload = {
        "age": "invalid",
        "gender": "Male",
        "location": "USA",
        "game_genre": "Action",
        "game_difficulty": "Medium",
        "sessions_per_week": 12,
        "avg_session_duration_minutes": 70,
        "player_level": 25,
        "achievements_unlocked": 30,
        "total_events": 1500,
        "days_since_last_seen": 3,
        "account_age_days": 120
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422