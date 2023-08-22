from flask_restx import Namespace, Resource, reqparse, inputs
from flask_jwt_extended import create_access_token
import hashlib  
from datetime import timedelta
from models.db import db
import threading

user_api = Namespace('user', description='User operations')
user_token = {}  # In-memory dictionary to store user tokens


def check_user_token(username):
    # Check if the user has an active (token)
    return username in user_token

def save_user_token(username, token):
    # Save the user session with the JWT token
    user_token[username] = token

def clear_user_token(username):
    if username in user_token:
        user_token.pop(username)

def clear_token_after_delay(username, delay_minutes):
    threading.Timer(delay_minutes * 60, clear_user_token, args=[username]).start()


# Define a parser for the POST request

def create_user_parser(*fields):
    parser = reqparse.RequestParser()
    for field in fields:
        parser.add_argument(field['name'], required=True, location=field.get('location', 'json'),
                            help=field['help'], type=field.get('type', str), dest=field.get('dest'))
    return parser

signup_parser = create_user_parser(
    {'name': 'username', 'location': 'form', 'required': True, 'help': 'Username'},
    {'name': 'email', 'location': 'form', 'required': True, 'help': 'Email', 'type': inputs.email()},
    {'name': 'password', 'location': 'form', 'required': True, 'help': 'Password', 'dest': 'raw_password'}
)

login_parser = create_user_parser(
    {'name': 'username', 'location': 'form', 'required': True, 'help': 'Username'},
    {'name': 'password', 'location': 'form', 'required': True, 'help': 'Password', 'dest': 'raw_password'}
)


@user_api.route('/signup')
class UserController(Resource):
    @user_api.doc(parser=signup_parser, description='User Registration API')
    @user_api.response(200, 'Success')
    @user_api.response(400, 'Bad request')
    @user_api.response(500, 'Internal server error')
    def post(self):
        """
        User Registration API
        """
        args = signup_parser.parse_args()
        username = args['username']
        email = args['email']
        raw_password = args['raw_password']

        if not username or not email or not raw_password:
            return {'error': 'Username, email, and password are required'}, 400

        if len(raw_password) < 6:
            return {'error': 'Password must be at least 6 characters long'}, 400

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
        username = args['username']
        raw_password = args['raw_password']

        if not username or not raw_password:
            return {'error': 'Username and password are required'}, 400

        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()

        try:
            db.cursor.execute("SELECT username FROM users WHERE username=%s AND password=%s", (username, hashed_password))
            user = db.cursor.fetchone()

            if user:
                # Check if user already has an active session (logged in)
                if check_user_token(username):
                    return {'message': 'User already logged in', "Your available token":user_token[username]}, 200
                

                # Create a JWT token
                expires = timedelta(minutes=10)
                access_token = create_access_token(identity=username, expires_delta=expires)
                save_user_token(username, access_token)
                clear_token_after_delay(username, 10)
                return {"access_token": access_token ,'message': 'User logged in successfully'},200
            
                
            else:
                return {'error': 'Invalid credentials'}, 401
        except Exception as e:
          print("Error:", e)
          return {'error': 'Internal server error'}, 500
