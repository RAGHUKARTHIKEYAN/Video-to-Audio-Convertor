from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
CONVERTER_URL = os.getenv("CONVERTER_URL", "http://converter-service:10000")

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    response = requests.post(f"{CONVERTER_URL}/convert", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/')
def home():
    return jsonify({"message": "Gateway Service Running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
