from flask import Flask
from application.app.config.routes import application_bp

flask = Flask("application")
flask.register_blueprint(application_bp, url_prefix="/")
