
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

1. **Build the Docker image:**

   ```bash
   pip install docker
   docker build -t kpop-trading-app ./backend
   ```

2. **Run the Docker container:**

   ```bash
   docker run -d -p 5000:5000 kpop-trading-card-app
   ```

3. Open your web browser and go to `http://localhost:5000` to access the application.


## Project Structure

\`\`\`
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── crud.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── cards.py
│   │   ├── cart_items.py
│   │   ├── inventory.py
│   │   ├── order_items.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   ├── users.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── admin_panel.html
│   │   ├── layout.html
│   │   ├── user_profile.html
│   │   ├── login.html
│   │   ├── card_list.html
│   │   ├── checkout.html
│   │   ├── cart.html
│   ├── static/
│       ├── css/
│       │   ├── styles.css
│       ├── js/
│       │   ├── main.js
│       ├── image/
│           ├── logo.png
│           ├── default_card.jpg
│
├── tests/
│   ├── __init__.py
│   ├── test_admin.py
│   ├── test_cards.py
│   ├── test_cart_items.py
│   ├── test_inventory.py
│   ├── test_order_items.py
│   ├── test_orders.py
│   ├── test_payments.py
│   ├── test_users.py
│
├── Dockerfile
├── requirements.txt
└── README.md
\`\`\`

## Running Tests

To run the basic tests for each model CURD operation, use the following command:

```bash
pytest
```