from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..crud import create_user, get_user_by_id, update_user, delete_user
from ..models import User
from ..schemas import UserSchema

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('users.profile'))
        return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('user_profile.html', user=current_user)

@bp.route('/', methods=['POST'])
def create():
    user_data = request.json
    user = create_user(user_data)
    return jsonify(UserSchema.from_orm(user).dict()), 201

@bp.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(UserSchema.from_orm(user).dict())

@bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    user_data = request.json
    user = update_user(user_id, user_data)
    return jsonify(UserSchema.from_orm(user).dict())

@bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    delete_user(user_id)
    return '', 204
