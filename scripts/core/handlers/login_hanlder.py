from scripts.db.mongo.collections.my_resume import MyResume
from scripts.db.mongo.collections.user import User
from scripts.db.mongo.collections.visitors import Visitors, VisitorsSchema
from scripts.schemas.login_schema import LoginModel
from scripts.utils.mongo_utility import mongo_client
from bson.binary import Binary
import os
import time
import base64
import socket
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from smtplib import SMTPException, SMTPAuthenticationError


class LoginHandler:
    def __init__(self):
        self.user = User(mongo_client=mongo_client)
        self.visitors = Visitors(mongo_client=mongo_client)
        self.my_resume = MyResume(mongo_client=mongo_client)

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

    def contact_us_mail_sending(self, email, contact_message):
        try:
            subject = "Contacted through portfolio application"
            sender_address = 'chowdhary12345678@gmail.com'  # Replace with your sender email
            sender_password = 'lgbzmvyxcyxzihxw'  # Replace with your sender password
            receiver_address = 'tarunmadamanchi@gmail.com'  # Replace with your recipient email
            recipient_name = 'Tarun Madamanchi'

            message = MIMEMultipart()
            from_header = subject
            message['From'] = formataddr((str(Header(from_header, 'utf-8')), sender_address))
            message['To'] = formataddr((str(Header(recipient_name, 'utf-8')), receiver_address))

            html = f"""\
            <html>
              <body>
                <p>Hi {recipient_name},<br>
                <br>
                email: {email}<br>
                message: {contact_message}<br>
                </p>
              </body>
            </html>
            """
            body_html = MIMEText(html, 'html')
            message.attach(body_html)

            with smtplib.SMTP('smtp.gmail.com', 587) as session:
                session.starttls()
                session.login(sender_address, sender_password)
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)

            return {"status": "success"}
        except SMTPAuthenticationError:
            return {"status": "SMTP authentication failed"}
        except SMTPException as e:
            return {"status": str(e)}
        except Exception as e:
            return {"status": str(e)}

    def fetch_resume(self, request_data):
        record = self.my_resume.get_resume()
        path = os.path.join(os.getcwd(), "code", "data")
        if not os.path.exists(path):
            os.makedirs(os.path.join(path))
        pdf_data = base64.b64decode(record.get("pdf_data"))
        file_path = os.path.join(path, "my_resume.pdf")
        # Write binary data to a PDF file
        with open(file_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        record["last_fetched_date"] = int(time.time())
        record["last_fetched_by"] = request_data.get("user_name")
        self.my_resume.update_resume(record)
        return file_path

    def upload_resume(self, pdf_content, pdf_name):
        # Convert PDF content to Base64
        pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

        # Save PDF into MongoDB along with its name
        pdf_data = {
            'resume_name': pdf_name,
            'pdf_data': pdf_base64,
            'last_fetched_by': 'Admin',
            "last_updated_at": int(time.time()),
            "last_fetched_date": int(time.time()),
        }
        self.my_resume.insert_one(pdf_data)

        return {'message': 'PDF uploaded successfully'}
