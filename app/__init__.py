from flask import Flask, g, session
from flask_bcrypt import Bcrypt
from app.models import db
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.security import generate_csrf_token
import logging

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    # SECRET KEY
    app.secret_key = Config.SECRET_KEY

    # INIT EXTENSIONS
    db.init_app(app)
    bcrypt.init_app(app)

    # JWT
    app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
    jwt.init_app(app)

    # SECURITY HEADERS
    Talisman(app, content_security_policy=None)

    # RATE LIMITING
    limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
    limiter.init_app(app)

    # LOGGING
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    @app.context_processor
    def inject_csrf_token():
        return {"csrf_token": generate_csrf_token()}

    @app.before_request
    def set_request_context():
        g.user_id = session.get("user_id")
        g.user_role = session.get("role")

    # IMPORTS DANS LA FONCTION (IMPORTANT 🔥)
    from app.routes.auth_routes import auth_bp
    from app.routes.view_routes import view_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(view_bp)

    return app