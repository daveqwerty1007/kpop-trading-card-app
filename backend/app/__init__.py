import os
from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from .database import init_db, db
from .routers import users, cards, orders, payments, inventory, admin, order_items, cart_items
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .models import User, Admin
from .schemas import UserSchema, AdminSchema
from werkzeug.security import check_password_hash

def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

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

    app.secret_key = 'myapp'
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Check if the ID belongs to an admin or a user
        admin_user = Admin.query.get(int(user_id))
        if admin_user:
            return admin_user
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user_type = request.form['user_type']

            user = None
            if user_type == 'admin':
                user = Admin.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    login_user(user)
                    print("Login successful for admin:", email)  # Debugging statement
                    return redirect(url_for('admin.dashboard'))
            else:
                user = User.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    login_user(user)
                    print("Login successful for user:", email)  # Debugging statement
                    return redirect(url_for('users.profile'))

            print("Invalid credentials for user:", email)  # Debugging statement
            flash('Invalid credentials', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('login'))

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
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app
