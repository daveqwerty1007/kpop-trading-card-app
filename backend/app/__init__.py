from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from .database import init_db,db
from .routers import users, cards, orders, payments, inventory, admin, order_items, cart_items
from flask_login import LoginManager
from .models import *

def create_app():
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
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints (routers)
    app.register_blueprint(users.bp)
    app.register_blueprint(cards.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(cart_items.bp) 
    app.register_blueprint(order_items.bp)
    

if __name__ == '__main__':
    app.run(debug=True)