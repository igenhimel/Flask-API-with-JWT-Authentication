from flask_restx import Namespace, Resource, reqparse, inputs
from flask_jwt_extended import create_access_token
import hashlib  
from datetime import timedelta
from models.db import db
import threading
import re

user_api = Namespace('user', description='User operations', path='/api')

def create_user_parser(*fields):
    parser = reqparse.RequestParser()
    for field in fields:
        parser.add_argument(field['name'],  location=field.get('location', 'json'),
                            help=field['help'], type=field.get('type', str), dest=field.get('dest'))
    return parser

signup_parser = create_user_parser(
    {'name': 'username', 'location': 'form', 'help': 'Username'},
    {'name': 'email', 'location': 'form', 'help': 'Email', 'type': inputs.email()},
    {'name': 'password', 'location': 'form',  'help': 'Password', 'dest': 'raw_password'}
)

login_parser = create_user_parser(
    {'name': 'username', 'location': 'form',  'help': 'Username'},
    {'name': 'password', 'location': 'form',  'help': 'Password', 'dest': 'raw_password'}
)


@user_api.route('/signup')
class UserController(Resource):
    @user_api.doc(parser=signup_parser, description='User Registration API')
    @user_api.response(201, 'Success')
    @user_api.response(400, 'Bad request')
    @user_api.response(500, 'Internal server error')
    def post(self):
        """
        User Registration API
        """
        args = signup_parser.parse_args()
    
        username = args['username'].lower() if args['username'] is not None else None
        email = args['email'].lower() if args['email'] is not None else None
        raw_password = args['raw_password']

        if not username or not email or not raw_password:
            return {'error': 'Username, email, and password are required'}, 400

        if len(username) < 4:
            return {'error': 'Username must be at least 4 characters long'}, 400

        if len(raw_password) < 6:
            return {'error': 'Password must be at least 6 characters long'}, 400

        # Additional validation for empty strings
        if username.strip() == '' or email.strip() == '' or raw_password.strip() == '':
            return {'error': 'Username, email, and password cannot be empty strings'}, 400

        # Validate username for whitespace
        if not re.match(r'^\S+$', username):
            return {'error': 'Username cannot contain whitespace characters'}, 400

        # Validate email address
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return {'error': 'Invalid email address'}, 400

        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()

        try:
            # Check if username or email already exists in the database
            db.cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = db.cursor.fetchone()

            if existing_user:
                return {'error': 'Username or email already exists'}, 400

            db.cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            db.connection.commit()
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            db.connection.rollback()
            return {'error': 'Failed to register user'}, 500


@user_api.route('/login')
class UserLogin(Resource):
    @user_api.doc(parser=login_parser, description='User Login API')
    @user_api.response(200, 'Success')
    @user_api.response(401, 'Unauthorized')
    @user_api.response(400, 'Bad request')
    @user_api.response(500, 'Internal server error')
    def post(self):
        """
        User Login API
        """
        args = login_parser.parse_args()
        username = args['username'].lower()
        raw_password = args['raw_password']

        if not username or not raw_password:
            return {'error': 'Username and password are required'}, 400

        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()

        try:
            db.cursor.execute("SELECT username FROM users WHERE username=%s AND password=%s", (username, hashed_password))
            user = db.cursor.fetchone()

            if user:

                # Create a JWT token
                expires = timedelta(minutes=10)
                access_token = create_access_token(identity=username, expires_delta=expires)
                return {"access_token": access_token ,'message': 'User logged in successfully'},200
            
            else:
                return {'error': 'Invalid credentials'}, 401
        except Exception as e:
          print("Error:", e)
          return {'error': 'Internal server error'}, 500
