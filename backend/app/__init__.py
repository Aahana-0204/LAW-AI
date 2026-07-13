import os
import re

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

jwt = JWTManager()


def _origin_allowed(origin):
    if not origin:
        return False
    if re.match(r'https://.*\.vercel\.app$', origin):
        return True
    if origin.startswith("http://localhost"):
        return True
    return False


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES
    app.config["PROPAGATE_EXCEPTIONS"] = True

    CORS(
        app,
        origins=_origin_allowed,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.chat import chat_bp
    from .routes.expert import expert_bp
    from .routes.docs import docs_bp
    from .routes.upload import upload_bp
    from .routes.generate import generate_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(expert_bp, url_prefix="/api/experts")
    app.register_blueprint(docs_bp, url_prefix="/api/docs")
    app.register_blueprint(upload_bp, url_prefix="/api/docs")
    app.register_blueprint(generate_bp, url_prefix="/api/generate")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "message": "LAWAI Backend is running"})

    @app.route("/api/debug/db")
    def debug_db():
        """Check MongoDB connection and list databases."""
        import traceback
        try:
            from pymongo import MongoClient
            uri = Config.MONGO_URI
            client = MongoClient(uri, serverSelectionTimeoutMS=8000)
            # Force connection
            dbs = client.list_database_names()
            db = client["lawai"]
            cols = db.list_collection_names()
            user_count = db["users"].count_documents({})
            return jsonify({
                "status": "connected",
                "databases": dbs,
                "lawai_collections": cols,
                "user_count": user_count,
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e),
                "trace": traceback.format_exc()
            }), 500

    # Global error handler — return JSON instead of HTML 500 pages
    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        return jsonify({
            "error": str(e),
            "type": type(e).__name__,
            "trace": traceback.format_exc()[-1000:]
        }), 500

    return app
