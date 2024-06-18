from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

order_bp = Blueprint('order_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@order_bp.route('/', methods=['GET'])
def get_orders():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `Order`")
    orders = cursor.fetchall()
    conn.close()
    return jsonify(orders)

@order_bp.route('/', methods=['POST'])
def add_order():
    new_order = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO `Order` (OrderNumber, ProductID, NumberOfItems, Price, Branch, Date, Time, EmployeeID, CustomerID, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (new_order['OrderNumber'], new_order['ProductID'], new_order['NumberOfItems'], new_order['Price'], new_order['Branch'], new_order['Date'], new_order['Time'], new_order['EmployeeID'], new_order['CustomerID'], new_order['Status']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order added successfully!"}), 201
