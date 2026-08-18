import os
from flask import Flask, jsonify, request, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SQLITE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'kpop_trading.db')
from flask_cors import CORS 
from .database import init_db, db
from .routers import users, cards, orders, payments, inventory, admin, order_items, cart_items
from flask_login import LoginManager, current_user
from .models import User
from flask_jwt_extended import JWTManager, create_access_token


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, 
         supports_credentials=True,
         resources={r"/*": {"origins": "*"}},
         origins=["http://localhost:3000"])
    
    jwt = JWTManager(app)

    # Database configuration
    if os.environ.get("TESTING") == "1":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        # Defaults to a local SQLite file. Set DATABASE_URL to point at a
        # real MySQL/Postgres server instead, e.g.:
        # mysql+mysqlconnector://user:password@host/dbname
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', DEFAULT_SQLITE_URI)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    init_db(app)

    # Falls back to a fixed dev key so local/test runs don't need setup, but
    # any real deployment should set SECRET_KEY explicitly.
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-insecure-secret-key')

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('user-'):
            return User.query.get(int(user_id.split('-')[1]))
        return None
        
    # Register blueprints (routers)
    app.register_blueprint(users.bp)
    app.register_blueprint(cards.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(cart_items.bp)
    app.register_blueprint(order_items.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/check_login_status', methods=['GET'])
    def check_login_status():
        if current_user.is_authenticated:
            return jsonify({"logged_in": True, "user": current_user.name}), 200
        else:
            return jsonify({"logged_in": False}), 401
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app
