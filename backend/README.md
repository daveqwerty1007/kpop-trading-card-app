
# K-pop Trading Card Selling Application

## Features

- User authentication and profile management
- Browse and search for trading cards
- Add trading cards to cart and checkout
- Admin panel for managing users, cards, orders, and inventory

## Prerequisites

- Docker

## Setup

### Running the Application with Docker

Run these from the repository root.

1. **Build the Docker image:**

   ```bash
   docker build -t kpop-trading-app ./backend
   ```

2. **Run the Docker container:**

   ```bash
   docker run -d --name kpop -p 5001:5000 -e SECRET_KEY=<long random string> kpop-trading-app
   ```

   Without `SECRET_KEY` the server uses a random key on each start, so
   everyone is logged out whenever the container restarts.

3. **Load the sample data** (the container starts with an empty database):

   ```bash
   docker exec kpop python data/loaddata.py
   ```

The API is now on `http://localhost:5001`. Run the frontend (see the root
README) to use the app.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py       # create_app(): config, auth, blueprints
│   ├── main.py           # entry point: python -m app.main
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── utils.py          # auth helpers (admin_required, ...)
│   ├── routers/
│   │   ├── admin.py
│   │   ├── cards.py
│   │   ├── cart_items.py
│   │   ├── inventory.py
│   │   ├── order_items.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   └── users.py
│   ├── templates/
│   │   └── index.html
│   └── test/
│       ├── conftest.py
│       ├── test_admin.py
│       ├── test_cards.py
│       ├── test_db.py
│       ├── test_integrity.py
│       ├── test_inventory.py
│       ├── test_orders.py
│       ├── test_payments.py
│       └── test_users.py
├── data/
│   ├── data.json
│   ├── loaddata.py
│   ├── gendata.py
│   └── fetchImageURL.py  # needs UNSPLASH_ACCESS_KEY set
├── Dockerfile
├── requirements.txt
└── README.md
```

## Running Tests

To run the test suite, use the following command from `backend/`:

```bash
pytest
```
