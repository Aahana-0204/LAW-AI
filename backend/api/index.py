"""
Vercel Python serverless entry point.
"""
import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify

app = Flask(__name__)

# ---- minimal health ping (no heavy imports) ----
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "LAWAI Backend is running"})


# ---- try to load the real app blueprints ----
_load_error = None
try:
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.expert import expert_bp
    from app.routes.docs import docs_bp
    from app.routes.upload import upload_bp
    from app.routes.generate import generate_bp
    from app.config import Config
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    import re

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

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(expert_bp, url_prefix="/api/experts")
    app.register_blueprint(docs_bp, url_prefix="/api/docs")
    app.register_blueprint(upload_bp, url_prefix="/api/docs")
    app.register_blueprint(generate_bp, url_prefix="/api/generate")

except Exception as _e:
    _load_error = traceback.format_exc()


@app.route("/api/debug/boot")
def boot_debug():
    if _load_error:
        return jsonify({"status": "partial", "error": _load_error[-3000:]}), 500
    return jsonify({"status": "full"})


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e), "type": type(e).__name__,
                    "trace": traceback.format_exc()[-1000:]}), 500
