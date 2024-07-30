from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..crud import create_payment, get_payment_by_id, update_payment, delete_payment
from ..schemas import PaymentSchema

bp = Blueprint('payments', __name__, url_prefix='/payments')

@bp.route('/', methods=['POST'])
@jwt_required()
def create():
    payment_data = request.json
    payment = create_payment(payment_data)
    return jsonify(PaymentSchema.from_orm(payment).dict()), 201

@bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment is None:
        return jsonify({'message': 'Payment not found'}), 404
    return jsonify(PaymentSchema.from_orm(payment).dict())

@bp.route('/<int:payment_id>', methods=['PUT'])
@jwt_required()
def update(payment_id):
    payment_data = request.json
    payment = update_payment(payment_id, payment_data)
    return jsonify(PaymentSchema.from_orm(payment).dict())

@bp.route('/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete(payment_id):
    delete_payment(payment_id)
    return jsonify({'message': 'Payment deleted'}), 204
