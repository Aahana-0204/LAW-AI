"""
Vercel Python serverless entry point.
"""
import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from main import app as _flask_app
    # Vercel uses `app` as the WSGI callable for Python functions
    app = _flask_app
except Exception as _boot_err:
    _tb = traceback.format_exc()
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def boot_error(path):
        return jsonify({"error": "Boot failed", "detail": str(_boot_err), "trace": _tb[-2000:]}), 500
