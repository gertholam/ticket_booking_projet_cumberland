from flask import Flask
from flask_bcrypt import Bcrypt
from app.models import db   # IMPORTANT
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    db.init_app(app)   # Lien entre Flask et DB
    bcrypt.init_app(app)
    
    #INIT JWT
    app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
    jwt.init_app(app)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app