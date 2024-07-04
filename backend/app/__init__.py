from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .database import init_db,db
from .routers import users, cards, orders, payments, inventory, admin
from flask_login import LoginManager
from .models import User

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

        # Define a route for the root URL
    @app.route('/')
    def index():
        return render_template('index.html')  # Ensure you have an index.html in your templates folder
    
    @app.route('/admin_panel')
    def admin_panel():
        return render_template('admin_panel.html')

    @app.route('/card_detail')
    def card_detail():
        return render_template('card_detail.html')

    @app.route('/card_list')
    def card_list():
        return render_template('card_list.html')

    @app.route('/cart')
    def cart():
        return render_template('cart.html')

    @app.route('/checkout')
    def checkout():
        return render_template('checkout.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/user_profile')
    def user_profile():
        return render_template('user_profile.html')


    return app
