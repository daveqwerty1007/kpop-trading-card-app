from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..crud import create_order_item, get_order_item_by_id, update_order_item, delete_order_item, get_order_items
from ..schemas import OrderItem

bp = Blueprint('order_items', __name__, url_prefix='/order_items')

@bp.route('/', methods=['POST'])
def create():
    order_item_data = request.json
    order_item = create_order_item(order_item_data)
    return jsonify(OrderItem.from_orm(order_item).dict()), 201

@bp.route('/<int:order_item_id>', methods=['GET'])
def get(order_item_id):
    order_item = get_order_item_by_id(order_item_id)
    if order_item is None:
        return jsonify({'message': 'Order item not found'}), 404
    return jsonify(OrderItem.from_orm(order_item).dict())

@bp.route('/<int:order_item_id>', methods=['PUT'])
def update(order_item_id):
    order_item_data = request.json
    order_item = update_order_item(order_item_id, order_item_data)
    return jsonify(OrderItem.from_orm(order_item).dict())

@bp.route('/<int:order_item_id>', methods=['DELETE'])
def delete(order_item_id):
    delete_order_item(order_item_id)
    return jsonify({'message': 'Order item deleted'}), 204

@bp.route('/', methods=['GET'])
def list_order_items():
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 100)
    order_items = get_order_items(skip=skip, limit=limit)
    return jsonify([OrderItem.from_orm(item).dict() for item in order_items])
