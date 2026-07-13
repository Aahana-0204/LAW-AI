"""Vercel Python serverless entry point."""
import sys
import os
import re
import traceback

# Ensure backend root is in path for our app package
_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_root not in sys.path:
    sys.path.insert(0, _backend_root)

# --- Bootstrap Flask first (always available) ---
from flask import Flask, jsonify

_flask = Flask(__name__)
_boot_errors = []


def _origin_allowed(origin):
    if not origin:
        return False
    if re.match(r'https://.*\.vercel\.app$', origin):
        return True
    if origin.startswith("http://localhost"):
        return True
    return False


# --- CORS + JWT (optional — fail gracefully) ---
try:
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    from app.config import Config

    _flask.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    _flask.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
    _flask.config["PROPAGATE_EXCEPTIONS"] = True
    CORS(_flask, origins=_origin_allowed, supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    JWTManager(_flask)
except Exception:
    _boot_errors.append(("core", traceback.format_exc()))

# --- Blueprints (fail per-module) ---
for _name, _module, _attr, _prefix in [
    ("auth", "app.routes.auth", "auth_bp", "/api/auth"),
    ("chat", "app.routes.chat", "chat_bp", "/api/chat"),
    ("expert", "app.routes.expert", "expert_bp", "/api/experts"),
    ("docs", "app.routes.docs", "docs_bp", "/api/docs"),
    ("upload", "app.routes.upload", "upload_bp", "/api/docs"),
    ("generate", "app.routes.generate", "generate_bp", "/api/generate"),
]:
    try:
        import importlib as _il
        _mod = _il.import_module(_module)
        _flask.register_blueprint(getattr(_mod, _attr), url_prefix=_prefix)
    except Exception:
        _boot_errors.append((_name, traceback.format_exc()))


@_flask.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "LAWAI Backend is running",
                    "boot_ok": len(_boot_errors) == 0})


@_flask.route("/api/debug/boot")
def boot_debug():
    if _boot_errors:
        return jsonify({"status": "partial", "errors": {k: v[-2000:] for k, v in _boot_errors}}), 500
    return jsonify({"status": "full"})


@_flask.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e), "type": type(e).__name__,
                    "trace": traceback.format_exc()[-1000:]}), 500


app = _flask
