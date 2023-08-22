Absolutely, here's the README with improved formatting:

# Flask API with JWT Authentication

This repository contains a Flask-based RESTful API for property search and user management, along with JWT-based authentication.

## Introduction

Welcome to the Flask API with JWT Authentication project. This API provides endpoints for user registration, user login, and property search. It uses JWT authentication to secure user access.

## Table of Contents

- [API Endpoints](#api-endpoints)
- [Technologies Used](#Technologies-Used)
- [Flask Project Setup and Installation Guide](#Flask-Project-Setup-and-Installation-Guide)
- [Running PostgreSQL with Docker Compose & Import Data](#Running-PostgreSQL-with-Docker-Compose-&-Import-Data)
- [Running Elasticsearch with Docker Compose & Import Data](#Running-Elasticsearch-with-Docker-Compose-&-Import-Data)
- [OpenAPI Documentation](#openapi-documentation)

## API Endpoints

### User Registration

**Endpoint:** `/api/signup`

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

**Endpoint:** `/api/login`

- **Method:** POST
- **Description:** User login.
- **Request Body:**
  - `username`: User's username
  - `raw_password`: User's password
- **Response:**
  - Success: JWT token for authentication
  - Error: Appropriate error messages

### Property Search

**Endpoint:** `/api/search`

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


## Technologies Used

- Flask
- Flask-RESTx
- PostgreSQL
- Elasticsearch
- Flask-JWT-Extended



## Flask Project Setup and Installation Guide

This guide will walk you through the process of setting up and installing a Flask project.

### Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- Python (3.6 or higher)
- `venv` (Python's built-in virtual environment package)

### Getting Started

1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/YourUsername/YourFlaskProject.git
   cd YourFlaskProject
   ```

2. Create a virtual environment using `venv`:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install project dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Configure your PostgreSQL and Elasticsearch connections in the appropriate files (`models/db.py` for PostgreSQL and `elasticsearch.txt` for Elasticsearch).

2. Set your JWT secret key in the `app.config['JWT_SECRET_KEY']` field in `app.py`.

### Running the Flask App

1. Run the Flask app:
   ```bash
   python app.py
   ```


## Running PostgreSQL with Docker Compose & Import Data

1. Open a terminal.

2. Navigate to the directory where your `docker-compose.yaml` file for PostgreSQL is located.

3. Run the following command to start the PostgreSQL container:
   ```bash
   docker-compose up -d
   ```

### Creating a Server and Database in PostgreSQL

1. Open your web browser and access the PostgreSQL Admin Tool (usually accessed via `http://localhost:8080`).

2. Log in to the Admin Tool.

3. Click on "Add New Server."

4. Fill in the following details:
   - **Name**: Enter a name for the server.
   - **Host name/address**: Use the PostgreSQL container's name/image's name
   - **Port**: Default is `5432`.
   - **Maintenance database**: Default is `postgres`.
   - **Username**:  `your-user-name`.
   - **Password**: `your-password`.

5. Save the server configuration.

6. In the left sidebar, select the server you just created.

7. Click on the "Databases" tab and create a new database.

8. Give the database a name and choose the server where it will reside.

### Running Queries in PostgreSQL

1. In the PostgreSQL Admin Tool, go to the "Query Tool."

2. Open the `postgresql.txt` file and copy the SQL code you want to run.

3. Paste the SQL code into the Query Tool.

4. Click the "Execute" button to run the query.

## Running Elasticsearch with Docker Compose & Import Data

1. Open a terminal.

2. Navigate to the directory where your Elasticsearch `docker-compose.yaml` file is located.

3. Run the following command to start the Elasticsearch container:
   ```bash
   docker-compose up -d
   ```

### Running Elasticsearch Dev Tools

1. Open your web browser and access Kibana (usually accessed via `http://localhost:5601`).

2. Click on "Dev Tools" in the left sidebar under "Management."

3. Copy the Elasticsearch code from your `elasticsearch.txt` file and paste it into the Dev Tools console.

4. Press the "Play" button to run the code.

Remember to replace placeholders like IP addresses, usernames, passwords, and other configurations with the actual values from your setup.


Sure, here's the process to include in your GitHub README for setting up and installing a Flask project:


## OpenAPI Documentation

The API documentation is generated using Swagger UI. You can access it by visiting `http://localhost:5000`.

---
