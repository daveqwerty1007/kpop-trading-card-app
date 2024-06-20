from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

branch_bp = Blueprint('branch_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@branch_bp.route('/', methods=['GET'])
def get_branches():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Branch")
    branches = cursor.fetchall()
    conn.close()
    return jsonify(branches)

@branch_bp.route('/', methods=['POST'])
def add_branch():
    new_branch = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Branch () VALUES ()"
    cursor.execute(sql, ())
    conn.commit()
    conn.close()
    return jsonify({"message": "Branch added successfully!"}), 201
