"""Debug step 4: add all blueprints."""
import sys
import os
import traceback

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

_errors = {}
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
        app.register_blueprint(getattr(_mod, _attr), url_prefix=_prefix)
    except Exception:
        _errors[_name] = traceback.format_exc()[-800:]


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "step": 4, "blueprint_errors": _errors})
