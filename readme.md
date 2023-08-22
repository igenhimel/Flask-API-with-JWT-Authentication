# Flask API with JWT Authentication

This repository contains a Flask-based RESTful API for property search and user management, along with JWT-based authentication.

## API Endpoints


### User Registration

Endpoint: `/api/signup`

- **Method:** POST
- **Description:** Register a new user.
- **Request Body:**
  - `username`: User's username
  - `email`: User's email
  - `raw_password`: User's password
- **Response:**
  - Success: Message indicating successful registration
  - Error: Appropriate error messages

### User Login

Endpoint: `/api/login`

- **Method:** POST
- **Description:** User login.
- **Request Body:**
  - `username`: User's username
  - `raw_password`: User's password
- **Response:**
  - Success: JWT token for authentication
  - Error: Appropriate error messages

### Property Search

Endpoint: `/api/search`

- **Method:** GET
- **Description:** Search and sort property listings.
- **Authorization:** JWT token required.
- **Query Parameters:**
  - `title`: Property title
  - `amenities`: Property amenities
  - `price`: Property price
  - `location`: Property location
  - `sort_order`: Sorting order (ascending or descending) by price
- **Response:**
  - Success: List of property search results with optional sorting
  - Error: Appropriate error messages



## Setup
1. Clone the repository from GitHub:
git clone https://github.com/igenhimel/python-flask-W3.git

2. Navigate to the project directory:
cd python-flask-W3

3. Install the required packages using `pip install -r requirements.txt`.

2. Configure the PostgreSQL and Elasticsearch connections in `models/db.py`.
3. Set your JWT secret key in the `app.config['JWT_SECRET_KEY']` field in `app.py`.

## Usage

1. Run the Flask app using `python app.py`.
2. Access the Swagger UI documentation at `http://localhost:5000`.

