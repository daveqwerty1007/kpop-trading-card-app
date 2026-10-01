# Kpop Trading Card App

## Project Description
This application is designed for a P2P trading business of K-pop trading cards. It aims to streamline the process of listing products, tracking orders, and making deliveries. The application targets K-pop fans and includes features like sales forecasting and restock notifications. The main components are:
- Web application for listings.
- Database for trading details.
- Admin page for database management.

We will use trading data from the past 3 months to initialize the application and update it over time.

## Folder Structure
```
kpop-trading-card-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # create_app(): config, auth, blueprints
│   │   ├── main.py           # entry point: python -m app.main
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # pydantic request/response schemas
│   │   ├── crud.py           # database operations
│   │   ├── utils.py          # auth helpers (admin_required, ...)
│   │   ├── routers/          # one Flask blueprint per resource
│   │   └── test/             # pytest suite
│   ├── data/
│   │   ├── data.json         # sample data
│   │   ├── loaddata.py       # loads data.json into the database
│   │   ├── gendata.py        # regenerates data.json
│   │   └── fetchImageURL.py  # fetches sample image URLs from Unsplash
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # React app (Create React App)
└── SQLquery/                 # MySQL scripts for the course report queries
```

## Setting Up the Environment

### Prerequisites
- Python 3.8+ (tested with 3.11)
- Node.js and npm (tested with Node 22)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python data/loaddata.py           # loads sample data into backend/app/kpop_trading.db
python -m app.main                # API on http://localhost:5001
```

Environment variables:
- `SECRET_KEY` signs login tokens. If it isn't set, the server picks a random
  key each time it starts, so everyone gets logged out on restart. Set it to a
  long random value anywhere other than local development, e.g.
  `export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")`.
- `DATABASE_URL` points at another database instead of the default SQLite
  file, e.g. `mysql+mysqlconnector://user:password@host/dbname`.

`loaddata.py` moves the sample orders' dates so the newest one is from today,
which keeps the dashboard and recommendations populated.

### Frontend
```bash
cd frontend
npm install
npm start                         # http://localhost:3000
```
The frontend calls the API at `REACT_APP_API_BASE_URL` in `frontend/.env`
(`http://localhost:5001` by default).

### Sample logins
- Admin (use the "Admin Login" tab): `adminone@example.com` / `adminpassword123`
- Customers: any user in `backend/data/data.json` (passwords are listed there)

### Tests
```bash
cd backend
pytest
```

## Project Structure

### Backend
- **backend/app/routers/:** API endpoints, one blueprint per resource.
- **backend/data/loaddata.py:** Script to load sample data into the database.
- **SQLquery/Setup.sql:** MySQL schema matching the app's tables, used for the course report queries.

### Frontend
- **frontend/public/:** Static files.
- **frontend/src/components/:** Pages and components.
- **frontend/src/services/api.js:** API client; attaches the login token to requests.

## Features
- User authentication
- View and search products
- Manage cart and checkout
- Admin functionalities
