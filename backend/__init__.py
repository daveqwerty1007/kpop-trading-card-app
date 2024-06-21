import mysql.connector
import os

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
    setup_sql_path = os.path.join(os.path.dirname(__file__), '..', 'Setup.sql')
    
    # Execute the SQL file
    execute_sql_file(cursor, setup_sql_path)
    
    connection.commit()
    cursor.close()
    connection.close()
