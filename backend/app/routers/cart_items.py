from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..crud import create_cart_item, get_cart_item_by_id, update_cart_item, delete_cart_item, get_cart_items, get_card_by_id
from ..schemas import CartItemSchema, CardSchema

bp = Blueprint('cart_items', __name__, url_prefix='/cart_items')

@bp.route('/', methods=['POST'])
@login_required
def create():
    cart_item_data = request.json
    cart_item_data['user_id'] = current_user.id
    cart_item = create_cart_item(cart_item_data)
    return jsonify(CartItemSchema.from_orm(cart_item).dict()), 201

@bp.route('/<int:cart_item_id>', methods=['GET'])
@login_required
def get(cart_item_id):
    cart_item = get_cart_item_by_id(cart_item_id)
    if cart_item is None:
        return jsonify({'message': 'Cart item not found'}), 404
    return jsonify(CartItemSchema.from_orm(cart_item).dict())

@bp.route('/<int:cart_item_id>', methods=['PUT'])
@login_required
def update(cart_item_id):
    cart_item_data = request.json
    cart_item = update_cart_item(cart_item_id, cart_item_data)
    return jsonify(CartItemSchema.from_orm(cart_item).dict())

@bp.route('/<int:cart_item_id>', methods=['DELETE'])
@login_required
def delete(cart_item_id):
    delete_cart_item(cart_item_id)
    return '', 204

@bp.route('/', methods=['GET'])
@login_required
def list_cart_items():
    cart_items = get_cart_items(current_user.id)
    for item in cart_items:
        item.card = get_card_by_id(item.card_id)  # Ensure card details are included
    return render_template('cart_item.html', cart_items=cart_items)
