from flask import Blueprint, request, jsonify
import mysql.connector
from backend.config import DB_CONFIG

kpopgroup_bp = Blueprint('kpopgroup_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@kpopgroup_bp.route('/', methods=['GET'])
def get_kpopgroups():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM KpopGroup")
    kpopgroups = cursor.fetchall()
    conn.close()
    return jsonify(kpopgroups)

@kpopgroup_bp.route('/', methods=['POST'])
def add_kpopgroup():
    new_kpopgroup = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO KpopGroup (GroupName) VALUES (%s)"
    cursor.execute(sql, (new_kpopgroup['GroupName'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "KpopGroup added successfully!"}), 201
