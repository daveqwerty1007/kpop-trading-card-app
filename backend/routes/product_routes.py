from flask import Blueprint, request, jsonify
from models import db, Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'ProductID': product.ProductID,
        'ProductName': product.ProductName,
        'SellingPrice': product.SellingPrice,
        'GroupID': product.GroupID
    } for product in products])

@product_bp.route('/', methods=['POST'])
def add_product():
    new_product = request.json
    product = Product(
        ProductName=new_product['ProductName'],
        SellingPrice=new_product['SellingPrice'],
        GroupID=new_product['GroupID']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201
