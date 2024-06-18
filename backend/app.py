##########connect server and set tables##########
import mysql.connector
import os
from flask import Flask
from routes import branch_bp, customer_bp, delivery_bp, employee_bp, kpopgroup_bp, order_bp, product_bp, shipping_bp, warehouse_bp

def connect_to_rds():
    connection = mysql.connector.connect(
        host='database-1.cbko6om64nur.us-east-1.rds.amazonaws.com',
        user='admin',
        password='nCbx9SyJPoUXXT8zcw4d'
    )
    return connection

def create_database():
    connection = connect_to_rds()
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS kpop_trading")
    cursor.close()
    connection.close()

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r') as sql_file:
        result_iterator = cursor.execute(sql_file.read(), multi=True)
        for res in result_iterator:
            print("Running query: ", res)
            print(f"Affected {res.rowcount} rows" if res.rowcount >= 0 else "")

def create_tables():
    connection = mysql.connector.connect(
        host='database-1.cbko6om64nur.us-east-1.rds.amazonaws.com',
        user='admin',
        password='nCbx9SyJPoUXXT8zcw4d',
        database='kpop_trading'  # Ensure the database is selected
    )
    cursor = connection.cursor()
    
    # Get the absolute path of the Setup.sql file
    setup_sql_path = os.path.join(os.path.dirname(__file__), 'Setup.sql')
    
    # Execute the SQL file
    execute_sql_file(cursor, setup_sql_path)
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_database()  # Create the database first
    create_tables()    # Then create tables
    print("Database and tables created successfully")

##########Set up API with flask##########
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(customer_bp, url_prefix='/api/customers')
app.register_blueprint(order_bp, url_prefix='/api/orders')
app.register_blueprint(employee_bp, url_prefix='/api/employees')
app.register_blueprint(shipping_bp, url_prefix='/api/shippings')
app.register_blueprint(warehouse_bp, url_prefix='/api/warehouses')
app.register_blueprint(branch_bp, url_prefix='/api/branches')
app.register_blueprint(delivery_bp, url_prefix='/api/deliveries')
app.register_blueprint(kpopgroup_bp, url_prefix='/api/kpopgroups')

if __name__ == '__main__':
    app.run(debug=True)
