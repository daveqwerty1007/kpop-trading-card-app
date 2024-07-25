from functools import wraps
from flask import jsonify, redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def user_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return f(*args, **kwargs)
            # Check if the user has the right permissions (custom logic)
            if current_user.has_permission('view_order'):
                return f(*args, **kwargs)
        return jsonify({"message": "Unauthorized"}), 401
    return decorated_function