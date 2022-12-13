from flask import Flask
from flask_cors import CORS
from application.app.config.routes import application_bp

flask = Flask("application")
CORS(flask, supports_credentials=True)

flask.register_blueprint(application_bp, url_prefix="/")
