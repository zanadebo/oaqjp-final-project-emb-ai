"""Flask server for the Emotion Detection web application."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/")
def render_index_page():
    """Render the home page."""
    return render_template("emotion_detection.html")


@app.route("/emotionDetector", methods=["GET"])
def sent_analyzer():
    """Analyze text and return formatted emotion response."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
