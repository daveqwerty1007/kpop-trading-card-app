from flask import Blueprint, flash, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from ..crud import create_user, get_user_by_id, update_user, delete_user
from ..models import User, Admin
from ..schemas import UserSchema, AdminSchema
from ..utils import admin_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        try:
            user = UserSchema(**user_data)
            new_user = create_user(user.dict())
            return redirect(url_for('users.login'))
        except ValidationError as e:
            return jsonify(e.errors()), 400
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('users.profile'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('user_profile.html', user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@bp.route('/', methods=['POST'])
def create():
    try:
        user_data = request.json
        user_data['password'] = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
        user = UserSchema(**user_data)
        new_user = create_user(user.dict())
        print("User created:", new_user.email)  # Debugging statement
        return jsonify(UserSchema.from_orm(new_user).dict()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    try:
        user = get_user_by_id(user_id)
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(UserSchema.from_orm(user).dict())
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    try:
        user_data = request.json
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
        user = UserSchema(**user_data)
        updated_user = update_user(user_id, user.dict())
        return jsonify(UserSchema.from_orm(updated_user).dict())
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    try:
        delete_user(user_id)
        return '', 204
    except ValidationError as e:
        return jsonify(e.errors()), 400
