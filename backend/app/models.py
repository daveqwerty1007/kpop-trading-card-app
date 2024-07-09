from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    group = db.Column(db.String(150), nullable=False)
    album = db.Column(db.String(150), nullable=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user = db.relationship('User', backref=db.backref('cart_item', lazy=True))
    card = db.relationship('Card', backref=db.backref('cart_item', lazy=True))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    quantity = db.Column(db.Integer, nullable=False)
    
    order = db.relationship("Order", back_populates="order_item")
    card = db.relationship("Card", back_populates="order_item")