from unittest.mock import patch

import pytest
import requests

from emotion_detection import EmotionServiceError, emotion_detector, emotion_predictor
from server import app


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("I love this project", "joy"),
        ("I am really mad", "anger"),
        ("That is gross", "disgust"),
        ("I feel sad", "sadness"),
        ("I am afraid", "fear"),
    ],
)
def test_explicit_heuristic_backend(text, expected):
    result = emotion_predictor(emotion_detector(text, backend="heuristic"))
    assert result["dominant_emotion"] == expected


def test_network_failure_is_not_silently_replaced():
    with patch("emotion_detection.requests.post", side_effect=requests.ConnectionError):
        with pytest.raises(EmotionServiceError, match="unavailable"):
            emotion_detector("I am happy", backend="watson")


def test_flask_route_in_explicit_demo_mode(monkeypatch):
    monkeypatch.setenv("EMOTION_BACKEND", "heuristic")
    response = app.test_client().get("/emotionDetector", query_string={"textToAnalyze": "I am glad"})
    assert response.status_code == 200
    assert response.get_json()["dominant_emotion"] == "joy"


def test_empty_input_returns_400(monkeypatch):
    monkeypatch.setenv("EMOTION_BACKEND", "heuristic")
    response = app.test_client().get("/emotionDetector", query_string={"textToAnalyze": ""})
    assert response.status_code == 400
