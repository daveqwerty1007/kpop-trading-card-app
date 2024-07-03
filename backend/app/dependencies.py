from flask import current_app
from .models import db

def get_db():
    return db
