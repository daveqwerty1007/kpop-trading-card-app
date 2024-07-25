from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from pydantic import ValidationError
from datetime import datetime

from ..utils import admin_required, user_or_admin_required
from ..crud import (
    create_order, get_all_orders, get_order_by_id, get_order_filter_options, get_user_orders, search_orders, update_order, delete_order,
    update_cart_item, delete_cart_item, get_cart_items, clear_cart, create_payment
)
from ..schemas import OrderSchema, PaymentSchema

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/cart', methods=['GET'])
#@login_required
def cart():
    cart_items = get_cart_items(current_user.id)
    total_amount = sum(item.card.price * item.quantity for item in cart_items)
    return jsonify({"cart_items": [item.to_dict() for item in cart_items], "total_amount": total_amount}), 200

@bp.route('/checkout', methods=['POST'])
#@login_required
def checkout():
    try:
        cart_items = get_cart_items(current_user.id)
        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 400
        
        total_amount = sum(item.card.price * item.quantity for item in cart_items)
        order_data = {
            'user_id': current_user.id,
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
        clear_cart(current_user.id)
        return jsonify({'message': 'Checkout successful', 'order_id': order.id}), 200

    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/update_cart_item/<int:card_id>', methods=['PUT'])
#@login_required
def update_cart_item_route(card_id):
    try:
        quantity = request.json['quantity']
        update_cart_item(current_user.id, card_id, quantity)
        return jsonify({'message': 'Cart item updated'}), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/delete_cart_item/<int:card_id>', methods=['DELETE'])
#@login_required
def delete_cart_item_route(card_id):
    try:
        delete_cart_item(current_user.id, card_id)
        return jsonify({'message': 'Cart item deleted'}), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['GET'])
#@user_or_admin_required
def detail(order_id):
    try:
        order = get_order_by_id(order_id)
        if order is None:
            return jsonify({'message': 'Order not found'}), 404
        return jsonify(OrderSchema.from_orm(order).dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['PUT'])
#@login_required
#@admin_required
def update(order_id):
    try:
        order_data = request.json
        order = update_order(order_id, order_data)
        return jsonify(OrderSchema.from_orm(order).dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:order_id>', methods=['DELETE'])
#@login_required
#@admin_required
def delete(order_id):
    try:
        delete_order(order_id)
        return jsonify({'message': 'Order deleted'}), 204
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