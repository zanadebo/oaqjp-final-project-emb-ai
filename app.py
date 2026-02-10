from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/emotion', methods=['POST'])
def emotion_detector():
    data = request.get_json()
    text_to_analyse = data.get('text', '')

    if not text_to_analyse:
        return jsonify({"error": "No text provided"}), 400

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, headers=headers, json=input_json, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract emotions and dominant emotion from response
        emotions = data.get('document', {}).get('emotion', {})
        if not emotions:
            return jsonify({"error": "No emotion data found"}), 500

        anger = emotions.get('anger', 0)
        disgust = emotions.get('disgust', 0)
        fear = emotions.get('fear', 0)
        joy = emotions.get('joy', 0)
        sadness = emotions.get('sadness', 0)
        dominant_emotion = max(emotions, key=emotions.get)

        return jsonify({
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': dominant_emotion
        })

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get emotion prediction: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
