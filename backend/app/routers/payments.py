from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..crud import create_payment, get_payment_by_id, update_payment, delete_payment
from ..schemas import PaymentSchema
from ..models import Order
from ..utils import is_admin_identity

bp = Blueprint('payments', __name__, url_prefix='/payments')

def _can_access_payment(payment, identity):
    order = Order.query.get(payment.order_id)
    return (order is not None and order.user_id == identity) or is_admin_identity(identity)

@bp.route('/', methods=['POST'])
@jwt_required()
def create():
    payment_data = request.json
    identity = get_jwt_identity()
    order = Order.query.get(payment_data.get('order_id'))
    if order is None:
        return jsonify({'message': 'Order not found'}), 404
    if order.user_id != identity and not is_admin_identity(identity):
        return jsonify({'message': 'Forbidden'}), 403
    payment = create_payment(payment_data)
    return jsonify(PaymentSchema.from_orm(payment).dict()), 201

@bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment is None:
        return jsonify({'message': 'Payment not found'}), 404
    if not _can_access_payment(payment, get_jwt_identity()):
        return jsonify({'message': 'Forbidden'}), 403
    return jsonify(PaymentSchema.from_orm(payment).dict())

@bp.route('/<int:payment_id>', methods=['PUT'])
@jwt_required()
def update(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment is None:
        return jsonify({'message': 'Payment not found'}), 404
    if not _can_access_payment(payment, get_jwt_identity()):
        return jsonify({'message': 'Forbidden'}), 403
    payment = update_payment(payment_id, request.json)
    return jsonify(PaymentSchema.from_orm(payment).dict())

@bp.route('/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment is None:
        return jsonify({'message': 'Payment not found'}), 404
    if not _can_access_payment(payment, get_jwt_identity()):
        return jsonify({'message': 'Forbidden'}), 403
    delete_payment(payment_id)
    return '', 204
