# Kpop Trading Card App

## Project Description
This application is designed for a P2P trading business of K-pop trading cards. It aims to streamline the process of listing products, tracking orders, and making deliveries. The application targets K-pop fans and includes features like sales forecasting and restock notifications. The main components are:
- Web application for listings.
- Database for trading details.
- Admin page for database management.

We will use trading data from the past 3 months to initialize the application and update it over time.

## Folder Structure
kpop-trading-card-app/
├── backend/
│ ├── app/
│ │ ├── __init__.py
│ │ ├── main.py
│ │ ├── crud.py
│ │ ├── database.py
│ │ └── routers/
│ │     ├── __init__.py
│ │     ├── admin.py
│ │     ├── cards.py
│ │     ├── cart_items.py
│ │     ├── inventory.py
│ │     ├── order_items.py
│ │     ├── orders.py
│ │     ├── payments.py
│ │     └── users.py
│ └── data/
│     └── loaddata.py
├── frontend/
│ ├── public/
│ └── src/
├── SQLquery/
│ └── Setup.sql
├── key-pair.pem
├── Procfile
├── README.md
├── requirements.txt
└── sample_data/


## Setting Up the Environment

### Prerequisites
- Python 3.8+
- MySQL

### Installation Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-repo-link/kpop-trading-card-app.git
    cd kpop-trading-card-app
    ```

2. **Create and Activate Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate 
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Flask application**
    - load the flask application:
        ```bash
        export FLASK_APP = app.py;
        ```
    - load the sample data:
        ```bash
        python backend/data/loaddata.py
        ```

5. **Run the Application**
    ```bash
        flask run
    ```
    The app should now be running on `http://127.0.0.1:5000`.

## Project Structure

### Backend
- **backend/app/__init__.py:** Initializes the backend module.
- **backend/data/loaddata.py:** Script to load sample data into the database.
- **backend/app/routers/:** Creating URL to call or update data when needed 
- **SQLquery/Setup.sql:** SQL script to set up the database schema.
- **backend/app/database.py:** Store RDS login credential and other settings.

### Frontend
- **frontend/public/:** Static files for styles and JavaScript.
- **frontend/src/:** Webpage file.

## Features
- User authentication
- View and search products
- Manage cart and checkout
- Admin functionalities
