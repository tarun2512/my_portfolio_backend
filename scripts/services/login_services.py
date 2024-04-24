from flask import Blueprint, request, send_file, jsonify, send_from_directory
import os
from pathlib import Path
from scripts.constants.app_configurations import PathToStorage
from werkzeug.utils import secure_filename
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


@login_blueprint.route(APIEndpoints.download_resume, methods=['POST'])
def fetch_resume():
    data = request.json
    login_handler = LoginHandler()
    path = login_handler.fetch_resume(data)
    filename = 'my_custom_filename.pdf'
    # return send_file(path, as_attachment=True, mimetype='application/pdf', download_name=filename)
    response = send_file(path, as_attachment=True, mimetype='application/pdf')
    response.headers["Content-Disposition"] = f"attachment; filename={secure_filename(filename)}"
    return response

@login_blueprint.route(APIEndpoints.upload_resume, methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file is a PDF
    if file.filename.split('.')[-1].lower() != 'pdf':
        return jsonify({'error': 'File is not a PDF'}), 400

    # Read the file contents
    pdf_content = file.read()

    # Get the name of the PDF file
    pdf_name = file.filename
    login_handler = LoginHandler()
    response = login_handler.upload_resume(pdf_content, pdf_name)
    return response
