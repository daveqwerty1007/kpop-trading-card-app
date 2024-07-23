from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..crud import create_card, get_card_by_id, update_card, delete_card, get_all_cards
from ..schemas import CardSchema

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/', methods=['POST'])
def create():
    try:
        card_data = request.json
        card = CardSchema(**card_data)
        new_card = create_card(card.dict())
        return jsonify(CardSchema.from_orm(new_card).dict()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:card_id>', methods=['GET'])
def detail(card_id):
    try:
        card = get_card_by_id(card_id)
        if card is None:
            return jsonify({'message': 'Card not found'}), 404
        return jsonify(CardSchema.from_orm(card).dict())
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:card_id>', methods=['PUT'])
def update(card_id):
    try:
        card_data = request.json
        card = CardSchema(**card_data)
        updated_card = update_card(card_id, card.dict())
        return jsonify(CardSchema.from_orm(updated_card).dict())
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:card_id>', methods=['DELETE'])
def delete(card_id):
    try:
        card = get_card_by_id(card_id)
        if card is None:
            return jsonify({'message': 'Card not found'}), 404
        delete_card(card_id)
        return '', 204
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/', methods=['GET'])
def list_all():
    try:
        cards = get_all_cards()
        return jsonify([CardSchema.from_orm(card).dict() for card in cards])
    except ValidationError as e:
        return jsonify(e.errors()), 400
