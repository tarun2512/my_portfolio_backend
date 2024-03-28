from flask import Blueprint, request

from scripts.core.handlers.login_hanlder import LoginHandler
from scripts.constants.app_constants import Database, APIEndpoints
from scripts.schemas.response_model import DefaultResponse

login_blueprint = Blueprint("licence_configuration", __name__)

login = Database.login


@login_blueprint.route(APIEndpoints.login, methods=['POST'])
def get_table_data():
    # Get the JSON data from the request
    data = request.json
    login_handler = LoginHandler()
    response = login_handler.validate_login(data)
    if response.get('status') == 'success':
        return DefaultResponse(status="success", message=response.get("message"), data=True).dict()
    else:
        return DefaultResponse(message=response.get("message"), data=False).dict()


@login_blueprint.route(APIEndpoints.visitor_login, methods=['POST'])
def save_visitor_data():
    # Get the JSON data from the request
    data = request.json
    login_handler = LoginHandler()
    response = login_handler.save_visitor_data(data)
    if response.get('status') == 'success':
        return DefaultResponse(status="success", message=response.get("message"), data=True).dict()
    else:
        return DefaultResponse(message=response.get("message"), data=False).dict()


@login_blueprint.route(APIEndpoints.contact_me, methods=['POST'])
def contact_me():
    # Get the JSON data from the request
    data = request.json
    login_handler = LoginHandler()
    response = login_handler.contact_us_mail_sending(data.get("email"), data.get("message"))
    if response.get('status') == 'success':
        return DefaultResponse(status="success", message=response.get("message"), data=True).dict()
    else:
        return DefaultResponse(message=response.get("message"), data=False).dict()
