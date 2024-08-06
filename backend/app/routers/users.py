from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from ..crud import create_user, get_all_users, get_user_by_id, get_user_filter_options, get_user_orders, search_users, update_user, delete_user
from ..models import User
from ..schemas import UserSchema,UserRegisterSchema
from ..database import db
import logging

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"message": "Name, email, and password are required."}), 400
        data['id'] = None
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')

        user_schema = UserRegisterSchema(**data)
        
        new_user_data = user_schema.dict()
        new_user = create_user(new_user_data)  # The create_user function will handle adding and committing
        access_token = create_access_token(identity=new_user.id)
        return jsonify({"message": "Login successful", "access_token": access_token, "user_id": new_user.id}), 200

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@bp.route('/update_user', methods=['POST'])
def update_name_and_email():
    try:

        data = request.json
        if not data.get('name') or not data.get('email') or not  data.get('id'):
            return jsonify({"message": "Name, emailare,id required."}), 400
        update_user(data.get('id'), data)
        user = User.query.get(data.get('id'))
        if user:
            user_data = UserSchema.from_orm(user).dict()
            return jsonify(user_data), 200
        return jsonify({"message": "User not found"}), 404
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": access_token, "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
        return jsonify(user_data), 200
    return jsonify({"message": "User not found"}), 404

@bp.route('/logout', methods=['POST'])
def logout():
    # Logout functionality for JWT (if using refresh tokens, handle them here)
    return jsonify({"message": "Logout successful"}), 200

@bp.route('/', methods=['POST'])
def create():
    try:
        data = request.json
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserSchema(**data)
        new_user = create_user(user_schema.dict())
        return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == user_id:  # Prevent users from deleting themselves
        return jsonify({"message": "Cannot delete own account"}), 403
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
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        user_data = UserSchema.from_orm(user).dict()
        return jsonify(user_data), 200
    return jsonify({"message": "User not found"}), 404

@bp.route('/orders', methods=['GET'])
@jwt_required()
def current_user_orders():
    current_user_id = get_jwt_identity()
    try:
        orders = get_user_orders(current_user_id)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
