from flask import Blueprint

bp = Blueprint('main', __name__)

from . import users, cards, orders, payments, inventory, admin
