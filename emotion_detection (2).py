"""
emotion_detection.py

This module contains functions for detecting emotions based on input data.
It includes methods for processing input, analyzing emotion patterns, and
returning results.
"""

import requests
from flask import Flask, request, jsonify


app = Flask(__name__)


def emotion_detector(text_to_analyse):
    """
    Detects emotions from the given text input using Watson NLP service.

    Args:
        text_to_analyse (str): The text to analyze for emotions.

    Returns:
        dict: A dictionary containing emotion scores and dominant emotion.
    """
    if not text_to_analyse:
        return {
            'anger': 0,
            'disgust': 0,
            'fear': 0,
            'joy': 0,
            'sadness': 0,
            'dominant_emotion': None
        }

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
    "grpc-metadata-mm-model-id": (
        "emotion_aggregated-workflow_lang_en_stock"
    ),
    "Content-Type": "application/json"
}

    input_json = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=input_json,
        timeout=10  # timeout in seconds
        )
    response.raise_for_status()
    data = response.json()

    emotions = data["document"]["emotion"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions.get("anger", 0),
        "disgust": emotions.get("disgust", 0),
        "fear": emotions.get("fear", 0),
        "joy": emotions.get("joy", 0),
        "sadness": emotions.get("sadness", 0),
        "dominant_emotion": dominant_emotion
    }


@app.route('/')
def home():
    return (
    "Emotion Detector is running. Send POST requests to /detect_emotion "
    "with JSON {'text': 'your text'}."
)


@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]
    try:
        result = emotion_detector(text)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify(
            {
                "error": "Failed to get emotion data",
                "details": str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
