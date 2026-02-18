"""
emotion_detection.py

This module contains functions for detecting emotions based on input data.
It includes methods for processing input, analyzing emotion patterns, and
returning results.

The user is using Cloud IDE Kubernetes tools to complete the Developing AI Applications with Python and Flask course.
"""

import requests
from flask import Flask, request, jsonify, render_template_string
import requestsy

app=Flask (__name__)

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

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    response = requests.post(url, headers=headers, json=input_json)
    response.raise_for_status()
    data = response.json()

    emotions = data["document"]["emotion"]

    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion
    }

