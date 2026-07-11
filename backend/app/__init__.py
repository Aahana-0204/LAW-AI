from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES

    CORS(
        app,
        origins=["http://localhost:5173", "http://localhost:3000"],
        supports_credentials=True,
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
        return {"status": "ok", "message": "LAWAI Backend is running"}

    return app
