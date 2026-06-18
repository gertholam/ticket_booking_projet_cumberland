import flask
from app.models.user import User
from app.models import db
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = flask.Blueprint('auth', __name__)

# TEST
#@auth_bp.route('/')
#def home():
#    return "API Ticket Booking fonctionne"

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    #data = request.get_json(force=True)
    data = flask.request.form
    
    #if not data:
    #   return jsonify({"error": "JSON invalide"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return flask.jsonify({"error": "Utilisateur existe deja"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role="client"
    )

    db.session.add(new_user)
    db.session.commit()

    return flask.jsonify({"message": "Utilisateur cree avec succes !"})
    return flask.redirect("/login")



# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    #data = request.get_json()
    data = flask.request.form
    
    username = data.get("username")
    password = data.get("password")
    
    
    #if not data:
    #   return jsonify({"error": "JSON invalide"}), 400

    #email = data.get("email")
    #password = data.get("password")

    #if not email or not password:
    #    return jsonify({"error": "Champs manquants"}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        if user.role == "admin":
            return flask.redirect("/admin/events")
        else:
            return flask.redirect("/events")
        
    return "login incorrect!"
    
    
#        #creation du token JWT
#        token = create_access_token(identity=str(user.id))
#        
#        return flask.jsonify({
#            "message": "Connexion réussie !",
#            "user": user.username,
#            "access_token": token
#        })
#    else:
#        return flask.jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    
    
    
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return flask.jsonify({"message": f"Bonjour {user.username}, vous êtes connecté !"})