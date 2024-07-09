import pandas as pd
from sqlalchemy import create_engine

db_user = 'root'
db_password = ''
db_host = 'localhost'
db_port = '3306'
db_name = 'kpop_trading_card'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

def load_csv_to_db(file_path, table_name):
    df = pd.read_csv(file_path)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f'Data from {file_path} has been loaded into {table_name} table.')


load_csv_to_db('Data/SampleData/Sample_Inventory_New.csv', 'Inventory')
load_csv_to_db('Data/SampleData/Sample_Payments_New.csv', 'Payment')
load_csv_to_db('Data/SampleData/Sample_Orders_New.csv', 'Order')
load_csv_to_db('Data/SampleData/Sample_Cards_New.csv', 'Card')
load_csv_to_db('Data/SampleData/Sample_Order_Items_New.csv', 'OrderItem')
load_csv_to_db('Data/SampleData/Sample_Cart_Items_New.csv', 'CartItem')
load_csv_to_db('Data/SampleData/Sample_Users_New.csv', 'User')
load_csv_to_db('Data/SampleData/Sample_Admins_New.csv', 'Admin')





