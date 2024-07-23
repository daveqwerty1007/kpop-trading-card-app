import os
from sqlite3 import IntegrityError
import sys
import json
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(backend_dir)

from app.models import User, Card, Order, Payment, Inventory, CartItem, OrderItem, Admin
from app.database import db, init_db

app = Flask(__name__)
# Database configuration
DB_CONFIG = {
    'host': 'database-1.cbko6om64nur.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'nCbx9SyJPoUXXT8zcw4d',
    'database': 'kpop_trading'
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
init_db(app)

# Database setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db.Model.metadata.create_all(bind=engine)

def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def insert_data(session, data):
    # Insert Users
    for user_data in data['users']:
        if not session.query(User).filter_by(id=user_data['id']).first():
            hashed_password = generate_password_hash(user_data['password'], method='pbkdf2:sha256')
            user = User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=hashed_password
            )
            session.add(user)
    session.commit()

    # Insert Admins
    for admin_data in data['admins']:
        if not session.query(Admin).filter_by(id=admin_data['id']).first():
            hashed_password = generate_password_hash(admin_data['password'], method='pbkdf2:sha256')
            admin = Admin(
                id=admin_data['id'],
                name=admin_data['name'],
                email=admin_data['email'],
                password=hashed_password
            )
            session.add(admin)
    session.commit()

    # Insert Cards
    for card_data in data['cards']:
        if not session.query(Card).filter_by(id=card_data['id']).first():
            card = Card(
                id=card_data['id'],
                card_name=card_data['card_name'],
                artist=card_data['artist'],
                group=card_data['group'],
                album=card_data['album'],
                price=card_data['price'],
                description=card_data['description'],
                image_url=card_data['image_url']
            )
            session.add(card)
    session.commit()

    # Insert Orders
    for order_data in data['orders']:
        if not session.query(Order).filter_by(id=order_data['id']).first():
            order = Order(
                id=order_data['id'],
                user_id=order_data['user_id'],
                order_date=order_data['order_date'],
                total_amount=order_data['total_amount']
            )
            session.add(order)
    session.commit()

    # Insert Payments
    for payment_data in data['payments']:
        if not session.query(Payment).filter_by(id=payment_data['id']).first():
            payment = Payment(
                id=payment_data['id'],
                order_id=payment_data['order_id'],
                payment_date=payment_data['payment_date'],
                payment_method=payment_data['payment_method'],
                payment_status=payment_data['payment_status']
            )
            session.add(payment)
    session.commit()

    # Insert Inventory
    for inventory_data in data['inventory']:
        if not session.query(Inventory).filter_by(id=inventory_data['id']).first():
            inventory = Inventory(
                id=inventory_data['id'],
                card_id=inventory_data['card_id'],
                quantity_available=inventory_data['quantity_available']
            )
            session.add(inventory)
    session.commit()

    # Insert Cart Items
    for cart_item_data in data['cart_items']:
        if not session.query(CartItem).filter_by(id=cart_item_data['id']).first():
            cart_item = CartItem(
                id=cart_item_data['id'],
                user_id=cart_item_data['user_id'],
                card_id=cart_item_data['card_id'],
                quantity=cart_item_data['quantity']
            )
            session.add(cart_item)
    session.commit()

    # Insert Order Items
    for order_item_data in data['order_items']:
        if not session.query(OrderItem).filter_by(id=order_item_data['id']).first():
            order_item = OrderItem(
                id=order_item_data['id'],
                order_id=order_item_data['order_id'],
                card_id=order_item_data['card_id'],
                quantity=order_item_data['quantity']
            )
            session.add(order_item)
    session.commit()

def main():
    with app.app_context():
        session = SessionLocal()
        try:
            data_file_path = os.path.join(current_dir, 'data.json')
            data = load_data(data_file_path)
            insert_data(session, data)
        except IntegrityError as e:
            print(f"Integrity error occurred: {e}")
            session.rollback()
        finally:
            session.close()

if __name__ == "__main__":
    main()
