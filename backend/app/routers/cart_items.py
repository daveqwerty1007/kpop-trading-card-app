from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from ..crud import add_to_cart, get_cart_item_by_id, update_cart_item, delete_cart_item, get_cart_items, get_card_by_id
from ..schemas import CartItemAddSchema, CartItemQuantitySchema, CartItemSchema, CardSchema
from ..utils import current_user_id

bp = Blueprint('cart_items', __name__, url_prefix='/cart_items')

@bp.route('/', methods=['POST'])
@jwt_required()
def create():
    try:
        data = CartItemAddSchema(**(request.json or {}))
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    if get_card_by_id(data.card_id) is None:
        return jsonify({'message': 'Card not found'}), 404
    cart_item = add_to_cart(current_user_id(), data.card_id, data.quantity)
    return jsonify(CartItemSchema.from_orm(cart_item).dict()), 201

@bp.route('/<int:cart_item_id>', methods=['GET'])
@jwt_required()
def get(cart_item_id):
    cart_item = get_cart_item_by_id(cart_item_id)
    if cart_item is None:
        return jsonify({'message': 'Cart item not found'}), 404
    if cart_item.user_id != current_user_id():
        return jsonify({'message': 'Forbidden'}), 403
    return jsonify(CartItemSchema.from_orm(cart_item).dict())

@bp.route('/<int:cart_item_id>', methods=['PUT'])
@jwt_required()
def update(cart_item_id):
    cart_item = get_cart_item_by_id(cart_item_id)
    if cart_item is None:
        return jsonify({'message': 'Cart item not found'}), 404
    if cart_item.user_id != current_user_id():
        return jsonify({'message': 'Forbidden'}), 403
    try:
        data = CartItemQuantitySchema(**(request.json or {}))
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    cart_item = update_cart_item(cart_item_id, {'quantity': data.quantity})
    return jsonify(CartItemSchema.from_orm(cart_item).dict())

@bp.route('/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def delete(cart_item_id):
    cart_item = get_cart_item_by_id(cart_item_id)
    if cart_item is None:
        return jsonify({'message': 'Cart item not found'}), 404
    if cart_item.user_id != current_user_id():
        return jsonify({'message': 'Forbidden'}), 403
    delete_cart_item(cart_item_id)
    return '', 204

@bp.route('/', methods=['GET'])
@jwt_required()
def list_cart_items():
    user_id = current_user_id()
    cart_items = get_cart_items(user_id)
    detailed_cart_items = []

    for item in cart_items:
        card = get_card_by_id(item.card_id)  # Ensure card details are included
        item_data = CartItemSchema.from_orm(item).dict()
        item_data['card'] = CardSchema.from_orm(card).dict()
        detailed_cart_items.append(item_data)

    return jsonify(detailed_cart_items), 200
