"""Debug step 3: add app.config import."""
import sys
import os

_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_root)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
CORS(app)
JWTManager(app)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "step": 3, "jwt_key_set": bool(app.config.get("JWT_SECRET_KEY"))})
