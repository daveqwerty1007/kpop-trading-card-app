from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

shipping_bp = Blueprint('shipping_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@shipping_bp.route('/', methods=['GET'])
def get_shippings():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Shipping")
    shippings = cursor.fetchall()
    conn.close()
    return jsonify(shippings)

@shipping_bp.route('/', methods=['POST'])
def add_shipping():
    new_shipping = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Shipping (OrderID, ProductID, NumberOfItems, Origin, Destination, EmployeeID, CustomerID, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (new_shipping['OrderID'], new_shipping['ProductID'], new_shipping['NumberOfItems'], new_shipping['From'], new_shipping['To'], new_shipping['EmployeeID'], new_shipping['CustomerID'], new_shipping['Status']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Shipping added successfully!"}), 201
