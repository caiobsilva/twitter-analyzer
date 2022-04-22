from flask import Blueprint
from app.controllers.application_controller import ApplicationController

application_bp = Blueprint("api", "crawler")

application_bp.route("/", methods=["GET"])(ApplicationController.index)
