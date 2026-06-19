import flask
from app.models.user import User
from app.models import db
from app import bcrypt

#  JWT (optionnel si tu veux garder)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = flask.Blueprint('auth', __name__)


#  REGISTER (HTML)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = flask.request.form

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    #  validation
    if not username or not email or not password:
        return "Champs manquants ❌"

    #  vérifie si user existe
    if User.query.filter_by(email=email).first():
        return "Utilisateur existe déjà ❌"

    #  hash
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role="client"
    )

    db.session.add(new_user)
    db.session.commit()

    #  redirection HTML (IMPORTANT)
    return flask.redirect("/")


#  LOGIN (SESSION) 
@auth_bp.route('/login', methods=['POST'])
def login():
    data = flask.request.form

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return "Champs manquants ❌"

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):

        #  SESSION
        flask.session["user_id"] = user.id
        flask.session["username"] = user.username
        flask.session["role"] = user.role

        #  redirection selon rôle
        if user.role == "admin":
            return flask.redirect("/admin/events")
        else:
            return flask.redirect("/events")

    return "Login incorrect ❌"


#  PROTECTED ROUTE (JWT - optionnel)
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return flask.jsonify({
        "message": f"Bonjour {user.username}, vous êtes connecté !"
    })


# CHECK ADMIN
def is_admin():
    return flask.session.get("role") == "admin"
