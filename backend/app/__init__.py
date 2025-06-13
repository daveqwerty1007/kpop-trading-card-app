import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS 
from .database import init_db, db
from .routers import users, cards, orders, payments, inventory, admin, order_items, cart_items
from flask_login import LoginManager, current_user
from .models import User, Admin
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
        DB_CONFIG = {
            'host': 'database-1.cbko6om64nur.us-east-1.rds.amazonaws.com',
            'user': 'admin',
            'password': 'nCbx9SyJPoUXXT8zcw4d',
            'database': 'kpop_trading'
        }
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    init_db(app)

    app.secret_key = 'myapp'
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('user-'):
            return User.query.get(int(user_id.split('-')[1]))
        elif user_id.startswith('admin-'):
            return Admin.query.get(int(user_id.split('-')[1]))
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
