"""Vercel Python serverless entry point."""
import sys
import os
import traceback
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Use 'application' internally; Vercel looks for 'app'
_flask = Flask(__name__)
_boot_errors = []

try:
    from app.config import Config  # noqa — 'app' here is the module, not Flask instance

    def _origin_allowed(origin):
        if not origin:
            return False
        if re.match(r'https://.*\.vercel\.app$', origin):
            return True
        if origin.startswith("http://localhost"):
            return True
        return False

    _flask.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    _flask.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
    _flask.config["PROPAGATE_EXCEPTIONS"] = True
    CORS(_flask, origins=_origin_allowed, supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    JWTManager(_flask)
except Exception:
    _boot_errors.append(("core", traceback.format_exc()))

_blueprints = [
    ("auth", "app.routes.auth", "auth_bp", "/api/auth"),
    ("chat", "app.routes.chat", "chat_bp", "/api/chat"),
    ("expert", "app.routes.expert", "expert_bp", "/api/experts"),
    ("docs", "app.routes.docs", "docs_bp", "/api/docs"),
    ("upload", "app.routes.upload", "upload_bp", "/api/docs"),
    ("generate", "app.routes.generate", "generate_bp", "/api/generate"),
]
for _name, _module, _attr, _prefix in _blueprints:
    try:
        import importlib as _il
        _mod = _il.import_module(_module)
        _bp = getattr(_mod, _attr)
        _flask.register_blueprint(_bp, url_prefix=_prefix)
    except Exception:
        _boot_errors.append((_name, traceback.format_exc()))


@_flask.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "LAWAI Backend is running"})


@_flask.route("/api/debug/boot")
def boot_debug():
    if _boot_errors:
        return jsonify({"status": "partial", "errors": {k: v[-2000:] for k, v in _boot_errors}}), 500
    return jsonify({"status": "full"})


@_flask.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e), "type": type(e).__name__,
                    "trace": traceback.format_exc()[-1000:]}), 500


# Vercel uses `app` as the WSGI callable
app = _flask
