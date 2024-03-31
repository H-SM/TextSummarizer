import time
from flask import Flask, jsonify
from flask_cors import CORS

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
def home_page():
    return {"page": "this is server"}

#  flask --app server run --debug 