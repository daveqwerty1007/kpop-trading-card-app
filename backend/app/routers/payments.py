from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from ..crud import create_payment, get_payment_by_id, update_payment, delete_payment
from ..schemas import PaymentSchema, PaymentCreateSchema, PaymentUpdateSchema
from ..models import Order
from ..utils import admin_required, current_user_id, owns_or_admin

bp = Blueprint('payments', __name__, url_prefix='/payments')

def _can_access_payment(payment, identity):
    order = Order.query.get(payment.order_id)
    return owns_or_admin(order.user_id if order else None, identity)

# Payment records are written by checkout; only admins may create, change or
# delete them directly (owners could otherwise mark their own orders paid).
@bp.route('/', methods=['POST'])
@admin_required
def create():
    try:
        payment_data = PaymentCreateSchema(**request.json).dict()
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    if Order.query.get(payment_data.get('order_id')) is None:
        return jsonify({'message': 'Order not found'}), 404
    payment = create_payment(payment_data)
    return jsonify(PaymentSchema.from_orm(payment).dict()), 201

@bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment is None:
        return jsonify({'message': 'Payment not found'}), 404
    if not _can_access_payment(payment, current_user_id()):
        return jsonify({'message': 'Forbidden'}), 403
    return jsonify(PaymentSchema.from_orm(payment).dict())

@bp.route('/<int:payment_id>', methods=['PUT'])
@admin_required
def update(payment_id):
    if get_payment_by_id(payment_id) is None:
        return jsonify({'message': 'Payment not found'}), 404
    try:
        updates = PaymentUpdateSchema(**request.json).dict(exclude_unset=True)
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    if 'order_id' in updates and Order.query.get(updates['order_id']) is None:
        return jsonify({'message': 'Order not found'}), 404
    payment = update_payment(payment_id, updates)
    return jsonify(PaymentSchema.from_orm(payment).dict())

@bp.route('/<int:payment_id>', methods=['DELETE'])
@admin_required
def delete(payment_id):
    if get_payment_by_id(payment_id) is None:
        return jsonify({'message': 'Payment not found'}), 404
    delete_payment(payment_id)
    return '', 204
