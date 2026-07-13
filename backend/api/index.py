"""Debug step 2: flask_cors + flask_jwt_extended imports."""
import sys
import os

_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_root)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
JWTManager(app)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "step": 2})
