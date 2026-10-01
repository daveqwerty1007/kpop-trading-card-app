from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        if get_jwt().get('role') != 'admin':
            return jsonify({"message": "Admins only: Access denied"}), 403

        return f(*args, **kwargs)
    return decorated_function

def current_user_id():
    """The current request's user id as an int.

    Tokens carry the id as a string (PyJWT >= 2.10 rejects non-string
    'sub' claims), so convert it back before comparing with integer
    columns. int() also accepts tokens issued before this change.
    """
    return int(get_jwt_identity())

def is_current_admin():
    """Whether the current request's JWT belongs to an admin.

    Reads the 'role' claim set at login time rather than re-deriving role
    from the raw identity, so this stays correct however roles end up
    being modeled.
    """
    return get_jwt().get('role') == 'admin'

def owns_or_admin(owner_id, identity):
    """Whether the current caller either owns a resource or is an admin.

    owner_id may be None (e.g. resource's parent record is missing) —
    admins still pass in that case, matching each call site's original
    "admins always bypass ownership" behavior.
    """
    return is_current_admin() or owner_id == identity

def current_profile(model):
    """Return {id, email, name} for the model row matching the current JWT identity, or None."""
    entity = model.query.get(current_user_id())
    if entity:
        return {"id": entity.id, "email": entity.email, "name": entity.name}
    return None
