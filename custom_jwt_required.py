from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from jwt import ExpiredSignatureError

def custom_jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except ExpiredSignatureError:
            return {'message': 'Token has expired! Please Login Again'}, 401
        except Exception as e:
            return {'message': 'You are unauthorized to view these contents'}, 401
        
        return f(*args, **kwargs)
    return decorated
