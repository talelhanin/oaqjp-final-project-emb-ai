"""Flask entry point for the emotion-detection course project."""

from flask import Flask, render_template, request

from emotion_detection import EmotionServiceError, emotion_detector, emotion_predictor

app = Flask(__name__)


@app.get("/emotionDetector")
def sent_detector():
    text = request.args.get("textToAnalyze", "")
    try:
        result = emotion_predictor(emotion_detector(text))
    except EmotionServiceError as exc:
        return {"error": str(exc)}, 503
    if result["dominant_emotion"] is None:
        return {"error": "Text input is required and must contain a supported signal."}, 400
    return {
        "scores": {emotion: result[emotion] for emotion in ("anger", "disgust", "fear", "joy", "sadness")},
        "dominant_emotion": result["dominant_emotion"],
    }


@app.get("/")
def render_index_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
