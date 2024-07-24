from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from ..crud import create_user, get_user_by_id, update_user, delete_user
from ..models import User, Admin
from ..schemas import UserSchema, AdminSchema
from ..utils import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

@bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        admin_email = current_user.email
        logout_user()
        print("Admin logged out:", admin_email)  # Debugging statement
    return redirect(url_for('admin.login'))

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    users = User.query.all()  # Fetch all users from the database
    return render_template('admin_dashboard.html', admin=current_user, users=users)

@bp.route('/create_user', methods=['POST'])
@login_required
@admin_required
def create_user_route():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        user = UserSchema(**user_data)
        new_user = create_user(user.dict())
        flash(f'User {new_user.name} created successfully.', 'success')
    except ValidationError as e:
        flash(f'Error: {e.errors()}', 'danger')
    return redirect(url_for('admin.dashboard'))

@bp.route('/update_user', methods=['POST'])
@login_required
@admin_required
def update_user_route():
    try:
        user_id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form.get('password')
        user_data = {
            'name': name,
            'email': email
        }
        if password:
            user_data['password'] = generate_password_hash(password, method='pbkdf2:sha256')
        update_user(user_id, user_data)
        flash(f'User {user_id} updated successfully.', 'success')
    except ValidationError as e:
        flash(f'Error: {e.errors()}', 'danger')
    return redirect(url_for('admin.dashboard'))

@bp.route('/delete_user', methods=['POST'])
@login_required
@admin_required
def delete_user_route():
    try:
        user_id = request.form['id']
        delete_user(user_id)
        flash(f'User ID {user_id} deleted successfully.', 'success')
    except ValidationError as e:
        flash(f'Error: {e.errors()}', 'danger')
    return redirect(url_for('admin.dashboard'))
