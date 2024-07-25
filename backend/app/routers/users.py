from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from ..crud import create_user, get_all_users, get_user_by_id, get_user_filter_options, get_user_orders, search_users, update_user, delete_user
from ..models import User
from ..schemas import UserSchema
import logging 

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserSchema(**data)
        new_user = create_user(user_schema.dict())
        return jsonify({"message": "Registration successful", "user_id": new_user.id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password, data.get('password')):
        login_user(user)
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/profile', methods=['GET'])
#@login_required
def profile():
    user_data = {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }
    return jsonify(user_data), 200

@bp.route('/logout', methods=['POST'])
#@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@bp.route('/', methods=['POST'])
def create():
    try:
        data = request.json
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserSchema(**data)
        new_user = create_user(user_schema.dict())
        return jsonify(UserSchema.from_orm(new_user).dict()), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/<int:user_id>', methods=['GET'])
#@login_required
def get(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(UserSchema.from_orm(user).dict()), 200
    return jsonify({"message": "User not found"}), 404

@bp.route('/<int:user_id>', methods=['PUT'])
#@login_required
def update(user_id):
    try:
        data = request.json
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserSchema(**data)
        updated_user = update_user(user_id, user_schema.dict())
        return jsonify(UserSchema.from_orm(updated_user).dict()), 200
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/<int:user_id>', methods=['DELETE'])
#@login_required
def delete(user_id):
    user = delete_user(user_id)
    if user:
        return jsonify({"message": "User deleted successfully"}), 204
    return jsonify({"message": "User not found"}), 404


@bp.route('/list', methods=['GET'])
def list_users():
    name = request.args.get('name')
    email = request.args.get('email')
    sort_by = request.args.get('sort_by')

    try:
        users = get_all_users(name=name, email=email, sort_by=sort_by)
        return jsonify([UserSchema.from_orm(user).dict() for user in users])
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
@bp.route('/filter-options', methods=['GET'])
def user_filter_options():
    try:
        options = get_user_filter_options()
        return jsonify(options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/search', methods=['GET'])
def search_users_route():
    query = request.args.get('q')
    if not query:
        return jsonify([]), 200

    try:
        results = search_users(query)
        return jsonify([UserSchema.from_orm(user).dict() for user in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/current', methods=['GET'])
@login_required 
def get_current_user():
    try:
        if current_user.is_authenticated:
            user_data = UserSchema.from_orm(current_user).dict()
            return jsonify(user_data), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/orders', methods=['GET'])
@login_required 
def current_user_orders():
    try:
        user_id = current_user.id
        orders = get_user_orders(user_id)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500