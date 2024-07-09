from .models import db, User, Card, Order, Payment, Inventory, Admin, CartItem, OrderItem
from . import database
from werkzeug.security import generate_password_hash

# User CRUD operations
def create_user(user_data):
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id):
    return db.session.get(User, user_id)

def update_user(user_id, user_data):
    user = db.session.get(User, user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
    return user

def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

# Card CRUD operations
def create_card(card_data):
    card = Card(**card_data)
    db.session.add(card)
    db.session.commit()
    return card

def get_card_by_id(card_id):
    return db.session.get(Card, card_id)

def update_card(card_id, card_data):
    card = db.session.get(Card, card_id)
    if card:
        for key, value in card_data.items():
            setattr(card, key, value)
        db.session.commit()
    return card

def delete_card(card_id):
    card = db.session.get(Card, card_id)
    if card:
        db.session.delete(card)
        db.session.commit()
    return card

# Order CRUD operations
def create_order(order_data):
    order = Order(**order_data)
    db.session.add(order)
    db.session.commit()
    return order

def get_order_by_id(order_id):
    return Order.query.get(order_id)

def update_order(order_id, order_data):
    order = Order.query.get(order_id)
    for key, value in order_data.items():
        setattr(order, key, value)
    db.session.commit()
    return order

def delete_order(order_id):
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()

# Payment CRUD operations
def get_payment_by_id(payment_id):
    return Payment.query.get(payment_id)

def create_payment(payment_data):
    payment = Payment(**payment_data)
    db.session.add(payment)
    db.session.commit()
    return payment

def update_payment(payment_id, payment_data):
    payment = Payment.query.get(payment_id)
    for key, value in payment_data.items():
        setattr(payment, key, value)
    db.session.commit()
    return payment

def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    db.session.delete(payment)
    db.session.commit()

# Inventory CRUD operations
def create_inventory(inventory_data):
    inventory = Inventory(**inventory_data)
    db.session.add(inventory)
    db.session.commit()
    return inventory

def get_inventory_by_id(inventory_id):
    return Inventory.query.get(inventory_id)

def update_inventory(inventory_id, inventory_data):
    inventory = Inventory.query.get(inventory_id)
    for key, value in inventory_data.items():
        setattr(inventory, key, value)
    db.session.commit()
    return inventory

def delete_inventory(inventory_id):
    inventory = Inventory.query.get(inventory_id)
    db.session.delete(inventory)
    db.session.commit()

def get_all_inventory():
    return Inventory.query.all()

# Admin CRUD operations
def create_admin(admin_data):
    admin = Admin(**admin_data)
    db.session.add(admin)
    db.session.commit()
    return admin

def get_admin_by_id(admin_id):
    return db.session.get(Admin, admin_id)

def update_admin(admin_id, admin_data):
    admin = db.session.get(Admin, admin_id)
    if admin:
        for key, value in admin_data.items():
            setattr(admin, key, value)
        db.session.commit()
    return admin

def delete_admin(admin_id):
    admin = db.session.get(Admin, admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
    return admin

# Cart CRUD operations

def create_cart_item(cart_item_data):
    cart_item = CartItem(**cart_item_data)
    db.session.add(cart_item)
    db.session.commit()
    return cart_item

def get_cart_item_by_id(cart_item_id):
    return db.session.get(CartItem, cart_item_id)

def update_cart_item(cart_item_id, cart_item_data):
    cart_item = db.session.get(CartItem, cart_item_id)
    if cart_item:
        for key, value in cart_item_data.items():
            setattr(cart_item, key, value)
        db.session.commit()
    return cart_item

def delete_cart_item(cart_item_id):
    cart_item = db.session.get(CartItem, cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return cart_item

def get_cart_items(user_id):
    return CartItem.query.filter_by(user_id=user_id).all()

def clear_cart(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

# OrderItem CRUD operations
def create_order_item(order_item_data):
    order_item = OrderItem(**order_item_data)
    db.session.add(order_item)
    db.session.commit()
    return order_item

def get_order_item_by_id(order_item_id):
    return db.session.get(OrderItem, order_item_id)

def update_order_item(order_item_id, order_item_data):
    order_item = db.session.get(OrderItem, order_item_id)
    if order_item:
        for key, value in order_item_data.items():
            setattr(order_item, key, value)
        db.session.commit()
    return order_item

def delete_order_item(order_item_id):
    order_item = db.session.get(OrderItem, order_item_id)
    if order_item:
        db.session.delete(order_item)
        db.session.commit()
    return order_item

def get_order_items(skip: int = 0, limit: int = 100):
    return OrderItem.query.offset(skip).limit(limit).all()
