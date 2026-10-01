from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError

from ..utils import admin_required, current_user_id, owns_or_admin
from ..crud import (
    CheckoutError, checkout_cart, get_all_orders, get_order_by_id, get_order_filter_options, search_orders,
    update_order, delete_order, get_cart_items, calculate_cart_total
)
from ..schemas import OrderSchema

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/cart', methods=['GET'])
@jwt_required()
def cart():
    user_id = current_user_id()
    cart_items = get_cart_items(user_id)
    total_amount = calculate_cart_total(cart_items)
    return jsonify({"cart_items": [item.to_dict() for item in cart_items], "total_amount": total_amount}), 200

@bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    payment_method = (request.json or {}).get('payment_method')
    if not payment_method:
        return jsonify({'message': 'Please choose a payment method'}), 400
    try:
        order = checkout_cart(current_user_id(), payment_method)
    except CheckoutError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    return jsonify({'message': 'Checkout successful', 'order_id': order.id}), 200

@bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def detail(order_id):
    try:
        order = get_order_by_id(order_id)
        if order is None:
            return jsonify({'message': 'Order not found'}), 404
        identity = current_user_id()
        if not owns_or_admin(order.user_id, identity):
            return jsonify({'message': 'Forbidden'}), 403
        return jsonify(OrderSchema.from_orm(order).dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['PUT'])
@admin_required
def update(order_id):
    try:
        order_data = request.json
        order = update_order(order_id, order_data)
        if order is None:
            return jsonify({'message': 'Order not found'}), 404
        return jsonify(OrderSchema.from_orm(order).dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['DELETE'])
@admin_required
def delete(order_id):
    try:
        order = delete_order(order_id)
        if order is None:
            return jsonify({'message': 'Order not found'}), 404
        return '', 204
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/list', methods=['GET'])
@admin_required
def list_orders():
    user_id = request.args.get('user_id', type=int)
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    min_total = request.args.get('min_total', type=float)
    max_total = request.args.get('max_total', type=float)
    sort_by = request.args.get('sort_by')

    try:
        orders = get_all_orders(user_id=user_id, min_date=min_date, max_date=max_date, min_total=min_total, max_total=max_total, sort_by=sort_by)
        return jsonify([OrderSchema.from_orm(order).dict() for order in orders])
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/filter-options', methods=['GET'])
@admin_required
def order_filter_options():
    try:
        options = get_order_filter_options()
        return jsonify(options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
@admin_required
def search_orders_route():
    query = request.args.get('q')
    if not query:
        return jsonify([]), 200

    try:
        results = search_orders(query)
        return jsonify([OrderSchema.from_orm(order).dict() for order in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
