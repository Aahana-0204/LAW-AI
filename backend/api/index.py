"""Debug: sys.path.insert + Flask only (step 1 diagnosis)."""
import sys
import os

_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_root)

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "backend_root": _backend_root, "sys_path_0": sys.path[0]})
