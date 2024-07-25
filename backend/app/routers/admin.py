from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import ValidationError
from ..crud import create_user, detect_fraudulent_orders, get_old_inventory, get_order_count, get_product_count, get_restock_list, get_sales_data_last_week, get_top_spending_users, get_total_sales, get_user_by_id, get_user_count, update_user, delete_user
from ..models import User, Admin
from ..schemas import UserSchema, AdminSchema
from ..utils import admin_required, user_or_admin_required
import logging

logging.basicConfig(level=logging.DEBUG)  # Set the level to DEBUG or INFO as needed

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            logging.info(f"Admin {admin.email} logged in.")
            return jsonify({"message": "Admin login successful", "admin_id": admin.id}), 200
        else:
            logging.warning(f"Failed login attempt for {email}")
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        logging.error(f"Error during admin login: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500

@bp.route('/logout', methods=['POST'])
# @admin_required
def logout():
    if current_user.is_authenticated and current_user.is_admin:
        admin_email = current_user.email
        logout_user()
        print("Admin logged out:", admin_email)  # Debugging statement
        return jsonify({"message": "Logout successful"}), 200
    return jsonify({"message": "Unauthorized"}), 401

@bp.route('/create_user', methods=['POST'])
# @admin_required
def create_user_route():
    try:
        data = request.json
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserSchema(**data)
        new_user = create_user(user_schema.dict())
        return jsonify({"message": f"User {new_user.name} created successfully.", "user_id": new_user.id}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/update_user', methods=['PUT'])
#@admin_required
def update_user_route():
    try:
        user_id = request.json.get('id')
        data = request.json
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
        user_schema = UserSchema(**data)
        updated_user = update_user(user_id, user_schema.dict())
        if updated_user:
            return jsonify({"message": f"User {user_id} updated successfully."}), 200
        return jsonify({"message": "User not found"}), 404
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.route('/delete_user', methods=['DELETE'])
#@admin_required
def delete_user_route():
    user_id = request.json.get('id')
    user = delete_user(user_id)
    if user:
        return jsonify({"message": f"User ID {user_id} deleted successfully."}), 204
    return jsonify({"message": "User not found"}), 404

@bp.route('/dashboard', methods=['GET'])
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