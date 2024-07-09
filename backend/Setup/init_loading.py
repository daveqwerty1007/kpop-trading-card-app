import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, inspect
import os

DB_CONFIG = {
    'host': 'database-1.cbko6om64nur.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'nCbx9SyJPoUXXT8zcw4d',
    'database': 'kpop_trading'
}

DATABASE_URI = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Define the path to the ProductionData directory
production_data_dir = os.path.join(os.path.dirname(__file__), 'ProductionData')

# Check the contents of the ProductionData directory to list all CSV files
production_data_files = [file for file in os.listdir(production_data_dir) if file.endswith('.csv')]

# Function to map pandas dtypes to SQLAlchemy types with default VARCHAR length
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer
    elif pd.api.types.is_float_dtype(dtype):
        return Float
    else:
        return String(255)  # Default length for VARCHAR

# Function to create a table from a dataframe
def create_table_from_dataframe(table_name, df, metadata, engine):
    columns = []
    for col_name, col_dtype in zip(df.columns, df.dtypes):
        col_type = map_dtype(col_dtype)
        columns.append(Column(col_name, col_type))
    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine, tables=[table])
    return table

# Loop through all CSV files in the ProductionData directory
for csv_file in production_data_files:
    table_name = csv_file.split('.')[0].lower()  # Use the filename (without extension) as the table name
    csv_path = os.path.join(production_data_dir, csv_file)
    df = pd.read_csv(csv_path)

    # Check if table exists; if not, create it
    if not inspect(engine).has_table(table_name):
        table = create_table_from_dataframe(table_name, df, metadata, engine)
    else:
        table = Table(table_name, metadata, autoload_with=engine)

    # Insert data into the table
    with engine.connect() as connection:
        for index, row in df.iterrows():
            insert_stmt = table.insert().values(**row.to_dict())
            connection.execute(insert_stmt)

print("All data successfully imported into the database.")
