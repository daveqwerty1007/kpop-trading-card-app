import pytest
from app import create_app, db
from app.models import User, Card, Order, Payment, Inventory, Admin  # Import all models

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests
    with flask_app.app_context():
        # Create the database and the database table(s)
        db.create_all()

        # Insert initial test data if necessary
        # user = User(name='Test User', email='test@example.com', password='password')
        # db.session.add(user)
        # db.session.commit()

        yield testing_client  # This is where the testing happens!

        # Drop all tables after tests
        db.drop_all()
