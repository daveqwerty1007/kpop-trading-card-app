from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from ..crud import create_payment, get_payment_by_id, update_payment, delete_payment
from ..schemas import PaymentSchema, PaymentCreateSchema, PaymentUpdateSchema
from ..models import Order
from ..utils import owns_or_admin

bp = Blueprint('payments', __name__, url_prefix='/payments')

def _can_access_payment(payment, identity):
    order = Order.query.get(payment.order_id)
    return owns_or_admin(order.user_id if order else None, identity)

@bp.route('/', methods=['POST'])
@jwt_required()
def create():
    try:
        payment_data = PaymentCreateSchema(**request.json).dict()
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    identity = get_jwt_identity()
    order = Order.query.get(payment_data.get('order_id'))
    if order is None:
        return jsonify({'message': 'Order not found'}), 404
    if not owns_or_admin(order.user_id, identity):
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
    try:
        updates = PaymentUpdateSchema(**request.json).dict(exclude_unset=True)
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    payment = update_payment(payment_id, updates)
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
