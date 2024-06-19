from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG
from datetime import timedelta

order_bp = Blueprint('order_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

def convert_timedelta_to_string(obj):
    if isinstance(obj, timedelta):
        return str(obj)
    return obj

@order_bp.route('/', methods=['GET'])
def get_orders():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM OrderDetail")
    orders = cursor.fetchall()
    conn.close()

    # Convert timedelta objects to strings
    for order in orders:
        for key, value in order.items():
            order[key] = convert_timedelta_to_string(value)

    return jsonify(orders)

@order_bp.route('/', methods=['POST'])
def add_order():
    new_order = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO OrderDetail (OrderID, ProductID, NumberOfItems, Origin, Destination, EmployeeID, CustomerID, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (new_order['OrderID'], new_order['ProductID'], new_order['NumberOfItems'], new_order['Origin'], new_order['Destination'], new_order['EmployeeID'], new_order['CustomerID'], new_order['Status']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order added successfully!"}), 201
