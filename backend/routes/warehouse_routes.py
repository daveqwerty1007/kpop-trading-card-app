from flask import Blueprint, request, jsonify
import mysql.connector
from backend.config import DB_CONFIG

warehouse_bp = Blueprint('warehouse_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@warehouse_bp.route('/', methods=['GET'])
def get_warehouses():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Warehouse")
    warehouses = cursor.fetchall()
    conn.close()
    return jsonify(warehouses)

@warehouse_bp.route('/', methods=['POST'])
def add_warehouse():
    new_warehouse = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Warehouse (WarehouseLocation, ProductName, NumberInStock) VALUES (%s, %s, %s)"
    cursor.execute(sql, (new_warehouse['WarehouseLocation'], new_warehouse['ProductName'], new_warehouse['NumberInStock']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Warehouse added successfully!"}), 201
