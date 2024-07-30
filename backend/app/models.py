from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    @property
    def is_admin(self):
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True 

    @property
    def is_anonymous(self):
        return False
    
    def user_type(self):
        return 'user'

    def get_id(self):
        return f"user-{self.id}"

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
    items = db.relationship('OrderItem', back_populates='order') 

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_date": self.order_date,
            "total_amount": self.total_amount,
            "items": [item.to_dict() for item in self.items]  
        }


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

    card = db.relationship('Card', backref=db.backref('inventory_items', lazy=True))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    @property
    def is_admin(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def user_type(self):
        return 'admin'
    
    def get_id(self):
        return f"admin-{self.id}"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    card = db.relationship('Card', backref=db.backref('cart_items', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "card_id": self.card_id,
            "quantity": self.quantity,
            "card_name": self.card.card_name,
            "price": self.card.price  
        }
    
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    quantity = db.Column(db.Integer, nullable=False)
    
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    card = db.relationship('Card', backref=db.backref('order_items', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "card_id": self.card_id,
            "quantity": self.quantity,
            "card_name": self.card.card_name,  # Assuming card_name exists in Card model
            "price": self.card.price  # Assuming price exists in Card model
        }
