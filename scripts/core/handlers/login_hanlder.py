from scripts.db.mongo.collections.user import User
from scripts.db.mongo.collections.visitors import Visitors, VisitorsSchema
from scripts.schemas.login_schema import LoginModel
from scripts.utils.mongo_utility import mongo_client
import socket
import datetime


class LoginHandler:
    def __init__(self):
        self.user = User(mongo_client=mongo_client)
        self.visitors = Visitors(mongo_client=mongo_client)

    def validate_login(self, data):
        final_json = {"status": "failed", "message": "User/Password invalid"}
        try:
            # Deserialize and validate the JSON data using the Pydantic model
            login_input = LoginModel(**data)
        except Exception as e:
            final_json["message"] = f"error 400 validation failed {str(e)}"
            return final_json

        saved_login_details = self.user.find_user(login_input.user_name)
        if not saved_login_details:
            return final_json
        elif (
            saved_login_details
            and login_input.password == saved_login_details.get("password")
        ):
            final_json['status'] = "success"
            final_json['message'] = "Successfully logged in"

        return final_json

    def save_visitor_data(self, data):
        hostname = socket.gethostname()
        visitor_ip = socket.gethostbyname(hostname)
        current_datetime = datetime.datetime.now()
        last_viewed_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        visitor_data = VisitorsSchema(visitor_name=data.get('user_name'),
                                      visitor_ip= visitor_ip,
                                      last_viewed_date=last_viewed_date).dict()
        self.visitors.save_user(data.get("user_name"), visitor_data)
        return {"status": "success", "message": "Successfully saved data"}

    def view_visitors_list(self):
        ...
