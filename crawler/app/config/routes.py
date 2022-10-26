from flask import Blueprint
from app.controllers.application_controller import ApplicationController

application_bp = Blueprint("api", "crawler")

application_bp.route("/", methods=["POST"])(ApplicationController.create)
application_bp.route("/", methods=["GET"])(ApplicationController.show)
application_bp.route("/api/file", methods=["POST"])(ApplicationController.save_file)
application_bp.route("/api/analyze", methods=["POST"])(ApplicationController.analyze)
