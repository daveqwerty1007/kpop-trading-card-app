from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..crud import create_cart_item, get_cart_item_by_id, update_cart_item, delete_cart_item, get_cart_items, get_card_by_id
from ..schemas import CartItemSchema, CardSchema

bp = Blueprint('cart_items', __name__, url_prefix='/cart_items')

@bp.route('/', methods=['POST'])
@jwt_required()
def create():
    cart_item_data = request.json
    user_id = get_jwt_identity()
    cart_item_data['user_id'] = user_id
    cart_item = create_cart_item(cart_item_data)
    return jsonify(CartItemSchema.from_orm(cart_item).dict()), 201

@bp.route('/<int:cart_item_id>', methods=['GET'])
@jwt_required()
def get(cart_item_id):
    cart_item = get_cart_item_by_id(cart_item_id)
    if cart_item is None:
        return jsonify({'message': 'Cart item not found'}), 404
    return jsonify(CartItemSchema.from_orm(cart_item).dict())

@bp.route('/<int:cart_item_id>', methods=['PUT'])
@jwt_required()
def update(cart_item_id):
    cart_item_data = request.json
    cart_item = update_cart_item(cart_item_id, cart_item_data)
    return jsonify(CartItemSchema.from_orm(cart_item).dict())

@bp.route('/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def delete(cart_item_id):
    delete_cart_item(cart_item_id)
    return '', 204

@bp.route('/', methods=['GET'])
@jwt_required()
def list_cart_items():
    user_id = get_jwt_identity()
    cart_items = get_cart_items(user_id)
    detailed_cart_items = []

    for item in cart_items:
        card = get_card_by_id(item.card_id)  # Ensure card details are included
        item_data = CartItemSchema.from_orm(item).dict()
        item_data['card'] = CardSchema.from_orm(card).dict()
        detailed_cart_items.append(item_data)

    return jsonify(detailed_cart_items), 200
