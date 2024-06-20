from flask import Blueprint, request, jsonify
import mysql.connector
from backend.config import DB_CONFIG

delivery_bp = Blueprint('delivery_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@delivery_bp.route('/', methods=['GET'])
def get_deliveries():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Delivery")
    deliveries = cursor.fetchall()
    conn.close()
    return jsonify(deliveries)

@delivery_bp.route('/', methods=['POST'])
def add_delivery():
    new_delivery = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Delivery (DeliveryMethod, Cost) VALUES (%s, %s)"
    cursor.execute(sql, (new_delivery['DeliveryMethod'], new_delivery['Cost']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Delivery added successfully!"}), 201
