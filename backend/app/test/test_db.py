# tests/test_db.py
from sqlalchemy import text

def test_database_connection(init_database):
    # Try to connect to the database and perform a simple query
    connection = init_database.engine.connect()
    result = connection.execute(text("SELECT 1"))
    assert result.fetchone()[0] == 1
    connection.close()

def test_database_initialization(init_database):
    # Check if the tables are created
    inspector = init_database.inspect(init_database.engine)
    tables = inspector.get_table_names()
    assert 'user' in tables
    assert 'card' in tables
    assert 'order' in tables
    assert 'payment' in tables
    assert 'inventory' in tables
