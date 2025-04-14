from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.user import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id['id'] if isinstance(current_user_id, dict) else current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Accès administrateur requis"}), 403
        return fn(*args, **kwargs)
    return wrapper