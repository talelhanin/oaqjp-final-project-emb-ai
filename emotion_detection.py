"""Emotion-analysis service used by the Flask course project."""

from __future__ import annotations

import os
from typing import Any

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
API_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


class EmotionServiceError(RuntimeError):
    """Raised when the configured emotion backend cannot return a result."""


def _empty_result() -> dict[str, None]:
    return {**{emotion: None for emotion in EMOTIONS}, "dominant_emotion": None}


def _heuristic_backend(text: str) -> dict[str, Any]:
    """Explicit offline demo backend; this is not a trained NLP model."""
    keywords = {
        "joy": ("glad", "happy", "joy", "pleased", "love", "enjoy", "great", "fun"),
        "anger": ("mad", "angry", "furious", "hate"),
        "disgust": ("disgust", "disgusted", "gross"),
        "sadness": ("sad", "sorrow", "unhappy"),
        "fear": ("afraid", "scared", "fear"),
    }
    normalized = text.lower()
    for emotion, tokens in keywords.items():
        if any(token in normalized for token in tokens):
            scores = {name: (0.95 if name == emotion else 0.01) for name in EMOTIONS}
            return {"emotionPredictions": [{"emotion": scores}]}
    return _empty_result()


def emotion_detector(text_to_analyze: str, *, backend: str | None = None) -> dict[str, Any]:
    """Return the configured backend response without silently changing models."""
    text = (text_to_analyze or "").strip()
    if not text:
        return _empty_result()

    selected_backend = (backend or os.getenv("EMOTION_BACKEND", "watson")).lower()
    if selected_backend == "heuristic":
        return _heuristic_backend(text)
    if selected_backend != "watson":
        raise EmotionServiceError(f"Unsupported EMOTION_BACKEND: {selected_backend}")

    try:
        response = requests.post(
            API_URL,
            json={"raw_document": {"text": text}},
            headers=API_HEADERS,
            timeout=10,
        )
    except requests.RequestException as exc:
        raise EmotionServiceError("Watson emotion service is unavailable") from exc

    if response.status_code == 400:
        return _empty_result()
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as exc:
        raise EmotionServiceError("Watson emotion service returned an invalid response") from exc


def emotion_predictor(detected_text: dict[str, Any]) -> dict[str, float | str | None]:
    """Normalize a backend response and select the highest-scoring emotion."""
    if "emotionPredictions" not in detected_text and all(
        detected_text.get(emotion) is None for emotion in EMOTIONS
    ):
        return _empty_result()
    predictions = detected_text.get("emotionPredictions")
    if not predictions:
        raise EmotionServiceError("Emotion response contains no predictions")
    scores = predictions[0].get("emotion", {})
    if any(emotion not in scores for emotion in EMOTIONS):
        raise EmotionServiceError("Emotion response is missing required scores")
    dominant = max(EMOTIONS, key=lambda emotion: scores[emotion])
    return {**{emotion: scores[emotion] for emotion in EMOTIONS}, "dominant_emotion": dominant}
