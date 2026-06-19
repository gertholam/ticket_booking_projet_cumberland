from flask import Flask
from flask_bcrypt import Bcrypt
from app.models import db
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    # CRET KEY (IMPORTANT)
    app.secret_key = "super_secret_key"

    # INIT EXTENSIONS
    db.init_app(app)
    bcrypt.init_app(app)

    # JWT
    app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
    jwt.init_app(app)

    # IMPORTS DANS LA FONCTION (IMPORTANT 🔥)
    from app.routes.auth_routes import auth_bp
    from app.routes.view_routes import view_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(view_bp)

    return app