"""Vercel Python serverless entry point for LAWAI."""
import sys
import os
import re
import traceback

_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _backend_root)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

CORS(app, supports_credentials=True, origins="*",
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
JWTManager(app)

# Register blueprints
_boot_errors = {}
for _name, _module, _attr, _prefix in [
    ("auth",     "app.routes.auth",     "auth_bp",     "/api/auth"),
    ("chat",     "app.routes.chat",     "chat_bp",     "/api/chat"),
    ("expert",   "app.routes.expert",   "expert_bp",   "/api/experts"),
    ("docs",     "app.routes.docs",     "docs_bp",     "/api/docs"),
    ("upload",   "app.routes.upload",   "upload_bp",   "/api/docs"),
    ("generate", "app.routes.generate", "generate_bp", "/api/generate"),
]:
    try:
        import importlib as _il
        _mod = _il.import_module(_module)
        app.register_blueprint(getattr(_mod, _attr), url_prefix=_prefix)
    except Exception:
        _boot_errors[_name] = traceback.format_exc()[-400:]


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "LAWAI Backend is running",
        "version": "2.0.0",
    })


@app.route("/api/debug/db")
def debug_db():
    try:
        from pymongo import MongoClient
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=8000,
                             tls=True, tlsAllowInvalidCertificates=True)
        db = client["lawai"]
        cols = db.list_collection_names()
        counts = {c: db[c].count_documents({}) for c in cols}
        return jsonify({"status": "connected", "collections": cols, "counts": counts})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e), "type": type(e).__name__,
                    "trace": traceback.format_exc()[-800:]}), 500
