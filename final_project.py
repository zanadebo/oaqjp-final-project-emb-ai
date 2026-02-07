from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/emotion', methods=['POST'])
def emotion_detector():
    data = request.get_json()
    text_to_analyse = data.get('text', '')

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = {"raw_document": {"text": text_to_analyse}}

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get emotion prediction"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)