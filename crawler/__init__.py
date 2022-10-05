from flask import Flask
from crawler.app.config.routes import application_bp

flask = Flask("crawler")
flask.register_blueprint(application_bp, url_prefix="/")
