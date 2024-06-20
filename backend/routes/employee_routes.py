from flask import Blueprint, request, jsonify
import mysql.connector
from backend.config import DB_CONFIG

employee_bp = Blueprint('employee_bp', __name__)

def connect_to_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user= DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        database= DB_CONFIG['database']
    )

@employee_bp.route('/', methods=['GET'])
def get_employees():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    conn.close()
    return jsonify(employees)

@employee_bp.route('/', methods=['POST'])
def add_employee():
    new_employee = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Employee (Name, KPI, Warehouse) VALUES (%s, %s, %s)"
    cursor.execute(sql, (new_employee['Name'], new_employee['KPI'], new_employee['Warehouse']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee added successfully!"}), 201
