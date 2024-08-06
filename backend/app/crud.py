from datetime import datetime, timedelta, timezone
from sqlalchemy import and_, func, or_
from .models import db, User, Card, Order, Payment, Inventory, Admin, CartItem, OrderItem
from . import database
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload


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
def excuteSql(sql):
    db.session.execute(sql)
    db.session.commit()
    return True
def get_all_users(name=None, email=None, sort_by=None):
    query = User.query

    if name:
        name_filters = name.split(',')
        query = query.filter(or_(*[User.name.ilike(f"%{n}%") for n in name_filters]))
    if email:
        email_filters = email.split(',')
        query = query.filter(or_(*[User.email.ilike(f"%{e}%") for e in email_filters]))

    if sort_by == 'name_asc':
        query = query.order_by(User.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(User.name.desc())
    elif sort_by == 'email_asc':
        query = query.order_by(User.email.asc())
    elif sort_by == 'email_desc':
        query = query.order_by(User.email.desc())

    return query.all()

def get_user_filter_options():
    try:
        names = db.session.query(User.name).distinct().all()
        emails = db.session.query(User.email).distinct().all()

        # Extract values from the tuples
        names = [name[0] for name in names]
        emails = [email[0] for email in emails]

        return {
            'names': names,
            'emails': emails,
        }
    except Exception as e:
        raise RuntimeError(f"Error fetching filter options: {str(e)}")

def search_users(query_string):
    query_string = f"%{query_string}%"
    search_conditions = [
        User.name.ilike(query_string),
        User.email.ilike(query_string),
    ]
    results = User.query.filter(or_(*search_conditions)).all()
    return results

def get_user_orders(user_id):
    orders = db.session.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.card)
    ).filter(Order.user_id == user_id).all()
    
    order_list = []
    for order in orders:
        order_dict = {
            'order_id': order.id,
            'order_date': order.order_date,
            'total_amount': order.total_amount,
            'items': [
                {
                    'item_id': item.id,
                    'card_name': item.card.card_name,
                    'artist': item.card.artist,
                    'group': item.card.group,
                    'album': item.card.album,
                    'quantity': item.quantity,
                    'price': item.card.price
                } for item in order.items
            ]
        }
        order_list.append(order_dict)
    
    return order_list


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

def get_all_cards(artist=None, group=None, album=None, min_price=None, max_price=None, sort_by=None):
    query = Card.query

    if artist:
        artist_filters = artist.split(',')
        query = query.filter(or_(*[Card.artist.ilike(f"%{a}%") for a in artist_filters]))
    if group:
        group_filters = group.split(',')
        query = query.filter(or_(*[Card.group.ilike(f"%{g}%") for g in group_filters]))
    if album:
        album_filters = album.split(',')
        query = query.filter(or_(*[Card.album.ilike(f"%{a}%") for a in album_filters]))
    if min_price is not None:
        query = query.filter(Card.price >= min_price)
    if max_price is not None:
        query = query.filter(Card.price <= max_price)

    if sort_by == 'price_asc':
        query = query.order_by(Card.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Card.price.desc())
    elif sort_by == 'latest':
        query = query.order_by(Card.id.desc())
    elif sort_by == 'recommended':
        query = (query
                 .join(OrderItem, OrderItem.card_id == Card.id)
                 .join(Order, Order.id == OrderItem.order_id)
                 .filter(Order.order_date >= (datetime.now(timezone.utc) - timedelta(days=90)))
                 .group_by(Card.id)
                 .order_by(db.func.sum(OrderItem.quantity).desc(), db.func.max(Order.order_date).desc()))

    return query.all()

def get_filter_options():
    try:
        artists = db.session.query(Card.artist).distinct().all()
        albums = db.session.query(Card.album).distinct().all()
        groups = db.session.query(Card.group).distinct().all()

        # Extract values from the tuples
        artists = [artist[0] for artist in artists]
        albums = [album[0] for album in albums]
        groups = [group[0] for group in groups]

        return {
            'artists': artists,
            'albums': albums,
            'groups': groups
        }
    except Exception as e:
        raise RuntimeError(f"Error fetching filter options: {str(e)}")

def search_cards(query_string):
    query_string = f"%{query_string}%"
    search_conditions = [
        Card.card_name.ilike(query_string),
        Card.artist.ilike(query_string),
        Card.album.ilike(query_string),
        Card.group.ilike(query_string)
    ]
    results = Card.query.filter(or_(*search_conditions)).all()
    return results

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

def get_all_orders(user_id=None, min_date=None, max_date=None, min_total=None, max_total=None, sort_by=None):
    query = Order.query

    if user_id:
        query = query.filter(Order.user_id == user_id)
    if min_date:
        query = query.filter(Order.order_date >= min_date)
    if max_date:
        query = query.filter(Order.order_date <= max_date)
    if min_total is not None:
        query = query.filter(Order.total_amount >= min_total)
    if max_total is not None:
        query = query.filter(Order.total_amount <= max_total)

    if sort_by == 'total_asc':
        query = query.order_by(Order.total_amount.asc())
    elif sort_by == 'total_desc':
        query = query.order_by(Order.total_amount.desc())
    elif sort_by == 'latest':
        query = query.order_by(Order.order_date.desc())

    return query.all()

def get_order_filter_options():
    try:
        users = db.session.query(User.id, User.name).join(Order, User.id == Order.user_id).distinct().all()
        date_range = db.session.query(func.min(Order.order_date), func.max(Order.order_date)).one()
        
        # Extract values
        users = [{'id': user[0], 'name': user[1]} for user in users]
        min_date, max_date = date_range

        return {
            'users': users,
            'min_date': min_date,
            'max_date': max_date
        }
    except Exception as e:
        raise RuntimeError(f"Error fetching filter options: {str(e)}")
    
def search_orders(query_string):
    query_string = f"%{query_string}%"
    search_conditions = [
        User.name.ilike(query_string),
        # Add other search conditions if there are other searchable fields in Order
    ]
    results = Order.query.join(User, User.id == Order.user_id).filter(or_(*search_conditions)).all()
    return results



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

def get_user_count():
    return User.query.count()

def get_order_count():
    return Order.query.count()

def get_product_count():
    return Card.query.count()

def get_total_sales():
    total_sales = round(db.session.query(func.sum(Order.total_amount)).scalar(),2)
    return total_sales or 0  # Return 0 if total_sales is None

def get_sales_data_last_week():
    one_week_ago = datetime.utcnow() - timedelta(days=30)
    sales_data = db.session.query(
        func.date(Order.order_date).label('date'),
        func.sum(Order.total_amount).label('sales')
    ).filter(Order.order_date >= one_week_ago).group_by(func.date(Order.order_date)).all()
    
    return [{"date": str(data.date), "sales": float(data.sales)} for data in sales_data]

def rows_to_dict_list(rows):
    return [row._asdict() for row in rows]

def detect_fraudulent_orders():
    seven_days_ago = datetime.now() - timedelta(days=7)
    results = db.session.query(
        User.name.label('customer_name'),
        User.email.label('customer_email'),
        Order.id.label('order_id'),
        Order.order_date,
        Payment.payment_status
    ).join(Order, User.id == Order.user_id) \
     .outerjoin(Payment, Order.id == Payment.order_id) \
     .filter(and_(
         Order.order_date <= seven_days_ago,
         (Payment.payment_status == None) | (Payment.payment_status != 'Completed')
     )).all()

    # Convert results to list of dicts
    return rows_to_dict_list(results)

def get_top_spending_users():
    results = db.session.query(
        User.id,
        User.name,
        User.email,
        func.sum(Order.total_amount).label('total_spent')
    ).join(Order, User.id == Order.user_id) \
     .group_by(User.id, User.name, User.email) \
     .order_by(func.sum(Order.total_amount).desc()) \
     .limit(5).all()
    
    # Convert results to list of dicts
    return rows_to_dict_list(results)

def get_old_inventory():
    three_months_ago = datetime.now() - timedelta(days=90)
    results = db.session.query(
        Card.card_name,
        Card.artist,
        Card.group,
        Card.album,
        func.coalesce(func.sum(OrderItem.quantity), 0).label('total_quantity_sold'),
        func.max(Order.order_date).label('last_sold_date'),
        Inventory.quantity_available
    ).outerjoin(OrderItem, OrderItem.card_id == Card.id) \
     .outerjoin(Order, and_(Order.id == OrderItem.order_id, Order.order_date >= three_months_ago)) \
     .join(Inventory, Inventory.card_id == Card.id) \
     .group_by(Card.card_name, Card.artist, Card.group, Card.album, Inventory.quantity_available) \
     .order_by('total_quantity_sold', 'last_sold_date') \
     .limit(5).all()
    
    # Convert results to list of dicts
    return rows_to_dict_list(results)

def get_restock_list():
    three_months_ago = datetime.now() - timedelta(days=90)
    results = db.session.query(
        Card.card_name,
        Card.artist,
        Card.group,
        Card.album,
        func.sum(OrderItem.quantity).label('total_quantity_sold'),
        func.max(Order.order_date).label('last_sold_date'),
        Inventory.quantity_available
    ).join(OrderItem, OrderItem.card_id == Card.id) \
     .join(Order, Order.id == OrderItem.order_id) \
     .join(Inventory, Inventory.card_id == Card.id) \
     .filter(Order.order_date >= three_months_ago) \
     .group_by(Card.card_name, Card.artist, Card.group, Card.album, Inventory.quantity_available) \
     .having(Inventory.quantity_available < 2) \
     .order_by('total_quantity_sold', 'last_sold_date') \
     .limit(10).all()
    
    # Convert results to list of dicts
    return rows_to_dict_list(results)


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
