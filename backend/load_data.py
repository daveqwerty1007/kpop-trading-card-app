import mysql.connector
import csv
import os

def connect_to_rds():
    connection = mysql.connector.connect(
        host='database-1.cbko6om64nur.us-east-1.rds.amazonaws.com',
        user='admin',
        password='nCbx9SyJPoUXXT8zcw4d',
        database='kpop_trading'
    )
    return connection

def load_csv_to_db(table_name, csv_file_path, columns):
    connection = connect_to_rds()
    cursor = connection.cursor()

    with open(csv_file_path, 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip the header row
        for row in csv_data:
            placeholders = ', '.join(['%s'] * len(row))
            columns_str = ', '.join([f"`{col}`" if col.lower() in ['from', 'to'] else col for col in columns])
            sql = f"INSERT IGNORE INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(row))
    
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data loaded into {table_name} from {csv_file_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    sample_data_dir = os.path.join(base_dir, '../sample_data')
    
    # Load data into tables that do not have foreign key dependencies first
    load_csv_to_db('KpopGroup', os.path.join(sample_data_dir, 'KpopGroup.csv'), 
                   ['GroupID', 'GroupName'])
    load_csv_to_db('Delivery', os.path.join(sample_data_dir, 'Delivery.csv'), 
                   ['DeliveryID', 'DeliveryMethod', 'Cost'])
    load_csv_to_db('Branch', os.path.join(sample_data_dir, 'Branch.csv'), 
                   ['BranchID'])
    load_csv_to_db('Warehouse', os.path.join(sample_data_dir, 'Warehouse.csv'), 
                   ['WarehouseID', 'WarehouseLocation', 'ProductName', 'NumberInStock'])
    load_csv_to_db('Customer', os.path.join(sample_data_dir, 'Customer.csv'), 
                   ['CustomerID', 'Name', 'Email', 'PhoneNumber', 'Address'])
    load_csv_to_db('Employee', os.path.join(sample_data_dir, 'Employee.csv'), 
                   ['EmployeeID', 'Name', 'KPI', 'Warehouse'])

    # Load data into tables with foreign key dependencies
    load_csv_to_db('Product', os.path.join(sample_data_dir, 'Product.csv'), 
                   ['ProductID', 'ProductName', 'SellingPrice', 'GroupID'])
    load_csv_to_db('`Order`', os.path.join(sample_data_dir, 'Order.csv'), 
                   ['OrderID', 'OrderNumber', 'ProductID', 'NumberOfItems', 'Price', 
                    'Branch', 'Date', 'Time', 'EmployeeID', 'CustomerID', 'Status'])
    load_csv_to_db('Shipping', os.path.join(sample_data_dir, 'Shipping.csv'), 
                   ['ShippingNumber', 'OrderID', 'ProductID', 'NumberOfItems', '`From`', 
                    '`To`', 'EmployeeID', 'CustomerID', 'Status'])
