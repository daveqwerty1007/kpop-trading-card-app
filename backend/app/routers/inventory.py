from flask import Blueprint, request, jsonify
from ..crud import create_inventory, get_inventory_by_id, update_inventory, delete_inventory, get_all_inventory
from ..schemas import InventorySchema
from pydantic import ValidationError

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@bp.route('/', methods=['POST'])
def create():
    try:
        inventory_data = request.json
        inventory = create_inventory(inventory_data)
        return jsonify(InventorySchema.from_orm(inventory).dict()), 201
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/', methods=['GET'])
def list_inventory():
    try:
        inventory_list = get_all_inventory()
        return jsonify([InventorySchema.from_orm(inventory).dict() for inventory in inventory_list])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:inventory_id>', methods=['GET'])
def get(inventory_id):
    try:
        inventory = get_inventory_by_id(inventory_id)
        if inventory is None:
            return jsonify({'message': 'Inventory item not found'}), 404
        return jsonify(InventorySchema.from_orm(inventory).dict())
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:inventory_id>', methods=['PUT'])
def update(inventory_id):
    try:
        inventory_data = request.json
        inventory = update_inventory(inventory_id, inventory_data)
        return jsonify(InventorySchema.from_orm(inventory).dict())
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete(inventory_id):
    try:
        delete_inventory(inventory_id)
        return '', 204
    except Exception as e:
        return jsonify({'message': str(e)}), 500
