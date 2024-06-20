from flask import Blueprint, request, jsonify
import mysql.connector
from backend.config import DB_CONFIG

customer_bp = Blueprint('customer_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

@customer_bp.route('/', methods=['GET'])
def get_customers():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    conn.close()
    return jsonify(customers)

@customer_bp.route('/', methods=['POST'])
def add_customer():
    new_customer = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Customer (Name, Email, PhoneNumber, Address) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (new_customer['Name'], new_customer['Email'], new_customer['PhoneNumber'], new_customer['Address']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer added successfully!"}), 201
