from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models import db
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

# TEST
@auth_bp.route('/')
def home():
    return "API Ticket Booking fonctionne"

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)   

    if not data:
        return jsonify({"error": "JSON invalide"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Utilisateur existe deja"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role="client"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur cree avec succes !"})



# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON invalide"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Champs manquants"}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        
        #creation du token JWT
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "message": "Connexion réussie !",
            "user": user.username,
            "access_token": token
        })
    else:
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401
    
    
    
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"message": f"Bonjour {user.username}, vous êtes connecté !"})