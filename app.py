from flask import Flask
from flask_restx import Api
from controllers.user_controller import user_api as user_api
from flask_swagger_ui import get_swaggerui_blueprint
from controllers.search_controller import search_api as search_api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_HEADER_TYPE'] = ''
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

# Create API with OpenAPI v3.0 support
api = Api(app, version='1.0', title='Flask Application - w3 Engineers', doc='/', ordered=True,security='jwt',  # Use the security name defined in authorizations
          authorizations={'jwt': 
          {'type': 'apiKey', 
          'in': 'header', 
          'name': 'Authorization',
          'description':'`please provide your JWT token in the input box below`'
          
          }})

# Add namespace (controllers) to API
api.add_namespace(user_api)
api.add_namespace(search_api)

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
