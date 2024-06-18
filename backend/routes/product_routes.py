# backend/routes/product_routes.py

from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

product_bp = Blueprint('product_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

@product_bp.route('/', methods=['GET'])
def get_products():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@product_bp.route('/', methods=['POST'])
def add_product():
    new_product = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Product (ProductName, SellingPrice, GroupID) VALUES (%s, %s, %s)"
    cursor.execute(sql, (new_product['ProductName'], new_product['SellingPrice'], new_product['GroupID']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product added successfully!"}), 201
