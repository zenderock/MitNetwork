from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,  # Ajout de cette importation
    get_jwt_identity
)
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 200

@auth.route('/me', methods=['GET'])
@jwt_required()  # Maintenant correctement défini
def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
        
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    }), 200

@auth.route('/login-admin', methods=['POST'])
def login_admin():
    # Ajoutez ce bloc AU DÉBUT de la fonction
    if not User.query.first():  # Si aucun utilisateur
        admin = User(username="admin", email="admin@admin.com", is_admin=True)
        admin.set_password("iamadmin")
        db.session.add(admin)
        db.session.commit()