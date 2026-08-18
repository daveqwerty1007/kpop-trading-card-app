from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..crud import create_order_item, get_order_item_by_id, update_order_item, delete_order_item, get_order_items
from ..schemas import OrderItem
from ..models import Order
from ..utils import admin_required, owns_or_admin

bp = Blueprint('order_items', __name__, url_prefix='/order_items')

@bp.route('/', methods=['POST'])
@admin_required
def create():
    order_item_data = request.json
    order_item = create_order_item(order_item_data)
    return jsonify(OrderItem.from_orm(order_item).dict()), 201

@bp.route('/<int:order_item_id>', methods=['GET'])
@jwt_required()
def get(order_item_id):
    order_item = get_order_item_by_id(order_item_id)
    if order_item is None:
        return jsonify({'message': 'Order item not found'}), 404
    identity = get_jwt_identity()
    order = Order.query.get(order_item.order_id)
    if not owns_or_admin(order.user_id if order else None, identity):
        return jsonify({'message': 'Forbidden'}), 403
    return jsonify(OrderItem.from_orm(order_item).dict())

@bp.route('/<int:order_item_id>', methods=['PUT'])
@admin_required
def update(order_item_id):
    order_item = update_order_item(order_item_id, request.json)
    if order_item is None:
        return jsonify({'message': 'Order item not found'}), 404
    return jsonify(OrderItem.from_orm(order_item).dict())

@bp.route('/<int:order_item_id>', methods=['DELETE'])
@admin_required
def delete(order_item_id):
    order_item = delete_order_item(order_item_id)
    if order_item is None:
        return jsonify({'message': 'Order item not found'}), 404
    return '', 204

@bp.route('/', methods=['GET'])
@admin_required
def list_order_items():
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    order_items = get_order_items(skip=skip, limit=limit)
    return jsonify([OrderItem.from_orm(item).dict() for item in order_items])
