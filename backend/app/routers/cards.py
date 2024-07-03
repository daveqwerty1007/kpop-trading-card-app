from flask import Blueprint, request, jsonify
from ..crud import create_card, get_card_by_id, update_card, delete_card
from ..schemas import CardSchema

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/', methods=['POST'])
def create():
    card_data = request.json
    card = create_card(card_data)
    return jsonify(CardSchema.from_orm(card).dict()), 201

@bp.route('/<int:card_id>', methods=['GET'])
def detail(card_id):
    card = get_card_by_id(card_id)
    return jsonify(CardSchema.from_orm(card).dict())

@bp.route('/<int:card_id>', methods=['PUT'])
def update(card_id):
    card_data = request.json
    card = update_card(card_id, card_data)
    return jsonify(CardSchema.from_orm(card).dict())

@bp.route('/<int:card_id>', methods=['DELETE'])
def delete(card_id):
    delete_card(card_id)
    return '', 204
