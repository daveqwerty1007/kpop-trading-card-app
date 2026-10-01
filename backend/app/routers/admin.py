from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from ..crud import create_user, detect_fraudulent_orders, get_old_inventory, get_order_count, get_product_count, get_restock_list, get_sales_data_last_week, get_top_spending_users, get_total_sales, get_user_count, update_user, delete_user
from ..models import User
from ..schemas import UserSchema, UserUpdateSchema, UserRegisterSchema
from ..utils import admin_required, current_profile
import logging

logging.basicConfig(level=logging.DEBUG)  # Set the level to DEBUG or INFO as needed

bp = Blueprint('admin', __name__, url_prefix='/admin')
@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    admin_data = current_profile(User)
    if admin_data:
        return jsonify(admin_data), 200
    return jsonify({"message": "User not found"}), 404
@bp.route('/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        admin = User.query.filter_by(email=email, role='admin').first()
        if admin and check_password_hash(admin.password, password):
            access_token = create_access_token(identity=str(admin.id), additional_claims={'role': 'admin'})
            logging.info(f"Admin {admin.email} logged in.")
            return jsonify({"message": "Admin login successful", "access_token": access_token, "admin_id": admin.id}), 200
        else:
            logging.warning(f"Failed login attempt for {email}")
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        logging.error(f"Error during admin login: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    # Invalidate the token on the client side or implement token blacklisting
    return jsonify({"message": "Logout successful"}), 200

@bp.route('/create_user', methods=['POST'])
@admin_required
def create_user_route():
    try:
        data = request.json
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserRegisterSchema(**data)
        new_user = create_user(user_schema.dict())
        return jsonify({"message": f"User {new_user.name} created successfully.", "user_id": new_user.id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/update_user', methods=['PUT'])
@admin_required
def update_user_route():
    try:
        user_id = request.json.get('id')
        data = request.json
        user_schema = None
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
            user_schema = UserSchema(**data)
        else:
            user_schema = UserUpdateSchema(**data)
        updated_user = update_user(user_id, user_schema.dict())
        if updated_user:
            return jsonify({"message": f"User {user_id} updated successfully."}), 200
        return jsonify({"message": "User not found"}), 404
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/delete_user', methods=['DELETE'])
@admin_required
def delete_user_route():
    user_id = request.json.get('id')
    user = delete_user(user_id)
    if user:
        return '', 204
    return jsonify({"message": "User not found"}), 404

@bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    try:
        response = {
            "user_count": get_user_count(),
            "order_count": get_order_count(),
            "product_count": get_product_count(),
            "total_sales": get_total_sales(),
            "sales_data_last_week": get_sales_data_last_week(),  # Ensure this is serializable
            "fraudulent_orders": detect_fraudulent_orders(),
            "top_spending_users": get_top_spending_users(),
            "old_inventory": get_old_inventory(),
            "restock_list": get_restock_list(),
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
