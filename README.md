# Emotion Detection Flask Course Project

[![CI](https://github.com/Harryphan72007/Coursera-Developing-AI-Applications-with-Python-and-Flask-Final-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryphan72007/Coursera-Developing-AI-Applications-with-Python-and-Flask-Final-Project/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-0F766E.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)

An educational Flask application from IBM's *Developing AI Applications with Python and Flask* course. The application analyzes English text, returns five emotion scores, and identifies the dominant emotion.

The default backend calls the course-hosted Watson NLP endpoint. A separate keyword heuristic is available for offline interface and test demonstrations; it must be selected explicitly and never silently replaces a failed network model.

## Features

- Flask interface and JSON endpoint
- Normalized scores for anger, disgust, fear, joy, and sadness
- Dominant-emotion selection
- Explicit Watson and offline-demo backend modes
- Clear `400` responses for invalid input
- Clear `503` responses when the configured network service is unavailable
- pytest coverage for every demo emotion, route behavior, invalid input, and network failure
- GitHub Actions continuous integration

## Architecture

```text
Browser or API client
        │
        ▼
Flask application (`server.py`)
        │
        ▼
Emotion service (`emotion_detection.py`)
        ├── Watson course endpoint
        └── explicit offline heuristic
```

`emotion_detector` calls the selected backend without silently changing models. `emotion_predictor` validates the response, normalizes the five required scores, and selects the highest-scoring emotion.

## Quick start

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Start the application with the course-hosted Watson endpoint:

```bash
python server.py
```

For an explicit offline interface demonstration:

```bash
EMOTION_BACKEND=heuristic python server.py
```

On Windows PowerShell:

```powershell
$env:EMOTION_BACKEND = "heuristic"
python server.py
```

Open `http://127.0.0.1:5000`.

## API

Send text to:

```text
GET /emotionDetector?textToAnalyze=I%20love%20this%20project
```

Example:

```bash
curl --get \
  --data-urlencode "textToAnalyze=I love this project" \
  http://127.0.0.1:5000/emotionDetector
```

Successful responses contain:

- `scores`: anger, disgust, fear, joy, and sadness
- `dominant_emotion`: the emotion with the highest score

The offline heuristic is deterministic test/demo behavior, not a trained NLP model.

## Test

```bash
pytest
```

The test suite verifies:

- All five explicit heuristic outcomes
- Network failures are not silently replaced
- Flask route behavior in demo mode
- Empty input returns `400`

The same suite runs in GitHub Actions on pushes to `main` and pull requests.

## Project structure

```text
server.py                  Flask entry point and HTTP routes
emotion_detection.py       backend selection, validation, and prediction logic
test_emotion_detection.py  service and route regression tests
templates/                 browser interface
static/                    interface assets
requirements.txt           pinned runtime and test dependencies
```

## Attribution and scope

The starter structure is based on IBM Skills Network's `oaqjp-final-project-emb-ai` course repository.

This repository is:

- A learning exercise
- Not an original emotion-classification model
- Not a production or high-availability service
- Dependent on a course-hosted endpoint when using the default backend

The repository retains its existing [Apache-2.0 license](LICENSE).
