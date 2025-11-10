from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/convert')
def convert():
    return jsonify({'message': 'Converter service is working!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)

