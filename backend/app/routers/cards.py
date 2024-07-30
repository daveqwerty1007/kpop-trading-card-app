from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from ..crud import create_card, get_card_by_id, get_filter_options, search_cards, update_card, delete_card, get_all_cards
from ..schemas import CardSchema
from ..models import Card

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/', methods=['POST'])
@jwt_required()
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
        return jsonify({'errors': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:card_id>', methods=['PUT'])
@jwt_required()
def update(card_id):
    try:
        card_data = request.json
        card = CardSchema(**card_data)
        updated_card = update_card(card_id, card.dict())
        return jsonify(CardSchema.from_orm(updated_card).dict())
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
def delete(card_id):
    try:
        card = get_card_by_id(card_id)
        if card is None:
            return jsonify({'message': 'Card not found'}), 404
        delete_card(card_id)
        return '', 204
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/list', methods=['GET'])
def list_cards():
    artist = request.args.get('artist')
    group = request.args.get('group')
    album = request.args.get('album')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by')

    try:
        cards = get_all_cards(artist=artist, group=group, album=album, min_price=min_price, max_price=max_price, sort_by=sort_by)
        return jsonify([CardSchema.from_orm(card).dict() for card in cards])
    except ValidationError as e:
        return jsonify(e.errors()), 400

@bp.route('/filter-options', methods=['GET'])
def filter_options():
    try:
        options = get_filter_options()
        return jsonify(options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify([]), 200

    try:
        results = search_cards(query)
        return jsonify([CardSchema.from_orm(card).dict() for card in results])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
