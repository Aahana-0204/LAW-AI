"""Vercel Python serverless entry point."""
import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify

app = Flask(__name__)

# Always available health endpoint
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "LAWAI Backend is running"})

# Try to load the full app
_boot_errors = []

try:
    import re
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    from app.config import Config

    def _origin_allowed(origin):
        if not origin:
            return False
        if re.match(r'https://.*\.vercel\.app$', origin):
            return True
        if origin.startswith("http://localhost"):
            return True
        return False

    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
    app.config["PROPAGATE_EXCEPTIONS"] = True
    CORS(app, origins=_origin_allowed, supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    JWTManager(app)
except Exception as _e:
    _boot_errors.append(("core", traceback.format_exc()))

# Register blueprints one by one to isolate failures
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
        app.register_blueprint(_bp, url_prefix=_prefix)
    except Exception as _e:
        _boot_errors.append((_name, traceback.format_exc()))


@app.route("/api/debug/boot")
def boot_debug():
    if _boot_errors:
        return jsonify({"status": "partial", "errors": {k: v[-2000:] for k, v in _boot_errors}}), 500
    return jsonify({"status": "full"})


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e), "type": type(e).__name__,
                    "trace": traceback.format_exc()[-1000:]}), 500
