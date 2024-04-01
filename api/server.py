import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from model import generate_summary

app = Flask(__name__)
CORS(app)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route("/members")
def get_members():
    # Your logic to fetch members
    members = ["Alice", "Bob", "Charlie"]
    return jsonify(members)

@app.route('/')
def home():
    return "Text Summarizer @ HSM - Backend", 200

@app.route('/summary', methods=['POST'])
def your_route_function():
    if not request.json:
        return jsonify({"error": "Request body must be in JSON format"}), 400

    url = request.json.get('url')
    percentage_str = request.json.get('percentage')

    if percentage_str is None:
        return jsonify({"error": "Percentage not provided"}), 400

    try:
        percentage = int(percentage_str)
    except ValueError:
        return jsonify({"error": "Percentage must be an integer"}), 400

    summary, lenarticle, lensummary = generate_summary(url, percentage)

    # Return the summary
    return jsonify({"summary": summary, "lengthA" : lenarticle, "lengthS" : lensummary})

#  flask --app server run --debug 