from flask import Flask, request, jsonify
import math
from datetime import datetime, timedelta
from rules import check_rules

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/detect_suspicious_activity', methods=['POST'])
def detect_suspicious_activity():
    transaction_data = request.get_json()
    output = check_rules(transaction_data)
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)