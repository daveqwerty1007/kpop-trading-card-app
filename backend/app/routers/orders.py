from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..crud import create_order, get_order_by_id, update_order, delete_order, add_to_cart, remove_from_cart, get_cart_items, clear_cart, create_payment
from ..schemas import OrderSchema, PaymentSchema
from datetime import datetime

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/cart', methods=['GET'])
@login_required
def cart():
    cart_items = get_cart_items(current_user.id)
    total_amount = sum(item.card.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Retrieve cart items
        cart_items = get_cart_items(current_user.id)
        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 400
        
        # Calculate total amount
        total_amount = sum(item.card.price * item.quantity for item in cart_items)
        
        # Create order
        order_data = {
            'user_id': current_user.id,
            'order_date': datetime.utcnow(),
            'total_amount': total_amount
        }
        order = create_order(order_data)
        
        # Create payment (assuming payment is successful for this example)
        payment_data = {
            'order_id': order.id,
            'payment_date': datetime.utcnow(),
            'payment_method': request.form['payment_method'],
            'payment_status': 'Completed'
        }
        create_payment(payment_data)
        
        # Clear the cart
        clear_cart(current_user.id)
        
        return jsonify({'message': 'Checkout successful'}), 200

    return render_template('checkout.html')

@bp.route('/add_to_cart/<int:card_id>', methods=['POST'])
@login_required
def add_to_cart_route(card_id):
    add_to_cart(current_user.id, card_id)
    return redirect(url_for('orders.cart'))

@bp.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart_route(item_id):
    remove_from_cart(current_user.id, item_id)
    return redirect(url_for('orders.cart'))

@bp.route('/', methods=['POST'])
def create():
    order_data = request.json
    order = create_order(order_data)
    return jsonify(OrderSchema.from_orm(order).dict()), 201

@bp.route('/<int:order_id>', methods=['GET'])
def get(order_id):
    order = get_order_by_id(order_id)
    if order is None:
        return jsonify({'message': 'Order not found'}), 404
    return jsonify(OrderSchema.from_orm(order).dict())

@bp.route('/<int:order_id>', methods=['PUT'])
def update(order_id):
    order_data = request.json
    order = update_order(order_id, order_data)
    return jsonify(OrderSchema.from_orm(order).dict())

@bp.route('/<int:order_id>', methods=['DELETE'])
def delete(order_id):
    delete_order(order_id)
    return jsonify({'message': 'Order deleted'}), 204