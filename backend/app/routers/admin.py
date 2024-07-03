from flask import Blueprint, request, jsonify
from ..crud import create_admin, get_admin_by_id, update_admin, delete_admin
from ..schemas import AdminSchema

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', methods=['POST'])
def create():
    admin_data = request.json
    admin = create_admin(admin_data)
    return jsonify(AdminSchema.from_orm(admin).dict()), 201

@bp.route('/<int:admin_id>', methods=['GET'])
def get(admin_id):
    admin = get_admin_by_id(admin_id)
    return jsonify(AdminSchema.from_orm(admin).dict())

@bp.route('/<int:admin_id>', methods=['PUT'])
def update(admin_id):
    admin_data = request.json
    admin = update_admin(admin_id, admin_data)
    return jsonify(AdminSchema.from_orm(admin).dict())

@bp.route('/<int:admin_id>', methods=['DELETE'])
def delete(admin_id):
    delete_admin(admin_id)
    return '', 204
