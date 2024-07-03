from flask import Blueprint, request, jsonify
from ..crud import create_inventory, get_inventory_by_id, update_inventory, delete_inventory
from ..schemas import InventorySchema

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@bp.route('/', methods=['POST'])
def create():
    inventory_data = request.json
    inventory = create_inventory(inventory_data)
    return jsonify(InventorySchema.from_orm(inventory).dict()), 201

@bp.route('/<int:inventory_id>', methods=['GET'])
def get(inventory_id):
    inventory = get_inventory_by_id(inventory_id)
    if inventory is None:
        return jsonify({'message': 'Inventory item not found'}), 404
    return jsonify(InventorySchema.from_orm(inventory).dict())

@bp.route('/<int:inventory_id>', methods=['PUT'])
def update(inventory_id):
    inventory_data = request.json
    inventory = update_inventory(inventory_id, inventory_data)
    return jsonify(InventorySchema.from_orm(inventory).dict())

@bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete(inventory_id):
    delete_inventory(inventory_id)
    return '', 204
