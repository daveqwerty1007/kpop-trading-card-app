from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from datetime import datetime

from ..utils import admin_required, is_admin_identity
from ..crud import (
    create_order, get_all_orders, get_order_by_id, get_order_filter_options, search_orders, update_order, delete_order,
    get_cart_items, clear_cart, create_payment, calculate_cart_total
)
from ..schemas import OrderSchema
from ..models import Card

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/cart', methods=['GET'])
@jwt_required()
def cart():
    user_id = get_jwt_identity()
    cart_items = get_cart_items(user_id)
    total_amount = calculate_cart_total(cart_items)
    return jsonify({"cart_items": [item.to_dict() for item in cart_items], "total_amount": total_amount}), 200

@bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = get_jwt_identity()
        cart_items = get_cart_items(user_id)
        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 400

        total_amount = calculate_cart_total(cart_items)
        order_data = {
            'user_id': user_id,
            'order_date': datetime.utcnow(),
            'total_amount': total_amount
        }
        order = create_order(order_data)
        payment_data = {
            'order_id': order.id,
            'payment_date': datetime.utcnow(),
            'payment_method': request.json.get('payment_method'),
            'payment_status': 'Completed'
        }
        create_payment(payment_data)
        clear_cart(user_id)
        return jsonify({'message': 'Checkout successful', 'order_id': order.id}), 200

    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def detail(order_id):
    try:
        order = get_order_by_id(order_id)
        if order is None:
            return jsonify({'message': 'Order not found'}), 404
        identity = get_jwt_identity()
        if order.user_id != identity and not is_admin_identity(identity):
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
def order_filter_options():
    try:
        options = get_order_filter_options()
        return jsonify(options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_orders_route():
    query = request.args.get('q')
    if not query:
        return jsonify([]), 200

    try:
        results = search_orders(query)
        return jsonify([OrderSchema.from_orm(order).dict() for order in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
