from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from .models import Admin

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request() 
        user_id = get_jwt_identity()
        user = Admin.query.get(user_id)
        
        if not user or not getattr(user, 'is_admin', False):
            return jsonify({"message": "Admins only: Access denied"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def is_admin_identity(identity):
    return Admin.query.get(identity) is not None

def current_profile(model):
    """Return {id, email, name} for the model row matching the current JWT identity, or None."""
    entity = model.query.get(get_jwt_identity())
    if entity:
        return {"id": entity.id, "email": entity.email, "name": entity.name}
    return None
