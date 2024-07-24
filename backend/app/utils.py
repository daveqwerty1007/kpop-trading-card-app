from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function
